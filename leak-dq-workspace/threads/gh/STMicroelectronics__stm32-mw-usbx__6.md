# [Bug]: UX_MEMORY_CORRUPTED return from error callback when using H5 interrupt IN transaction

- URL: https://github.com/STMicroelectronics/stm32-mw-usbx/issues/6
- Repo: STMicroelectronics/stm32-mw-usbx (language: C)
- State: open; created 2026-08-19T09:04:40Z; status ok; passes main

## Issue body

reporter (NONE) · leejugy · 2026-08-19T09:04:40Z · https://github.com/STMicroelectronics/stm32-mw-usbx/issues/6

### Bug Summary

Double free and use-after-free of ux_transfer_request_data_pointer

### Detailed Description

## 1. Describe the bug

UX_MEMORY_CORRUPTED occurs when a USB hub is connected and then a single MSC device is plugged into the hub.
Code is attempting to free memory areas that should not be freed and is attempting to free memory twice.
As a result, the device is not recognized through the hub.
Also it has use-after-free bug.

## 2. Expected Behavior

After usb hub detected, usb msc class is detected with no error.

## 3. Actual Behavior

After usb hub detected, usb msc class is not detected with UX_MEMORY_CORRUPTED.

## 4. Environment
> Board: stm32h563zit6
USBX Version: 6.4.0
CubemX H5 Package Info: 1.7.0
USBX Version: usbx-6.4.0.260508
USB bus connection: Stm32 Root Hub <-> GL850 Expansion Hub <-> 1 USB MSC Device

There is still code remaining in the current master branch that could be problematic.

## 5. Detailed Description

The bug occurs when an Interrupt IN transaction occurs.

The usb hub class allocates ux_transfer_request_data_pointer through the call stack below.
**Execution flow**
```txt
_ux_host_stack_rh_change_process()
    ↓
_ux_host_stack_rh_device_insertion()
    ↓
_ux_host_stack_new_device_create()
    ↓
_ux_host_stack_class_device_scan()
    ↓
ux_host_class_hub_entry()
      command_request = UX_HOST_CLASS_COMMAND_ACTIVATE
    ↓
_ux_host_class_hub_activate()
    ↓
_ux_host_class_hub_interrupt_endpoint_start()
```

**ux_host_class_hub_intterupt_endpoint_start.c:121**
```c
        /* Obtain a buffer for this transaction. The buffer will always be reused.  */
        transfer_request -> ux_transfer_request_data_pointer =  _ux_utility_memory_allocate(UX_SAFE_ALIGN, UX_CACHE_SAFE_MEMORY, 
                                                                transfer_request -> ux_transfer_request_requested_length);
```

The comment states that the buffer can be reused. Under normal operation, the buffer's lifecycle is until `ux_host_class_hub_deactivate` is called.

**ux_host_class_hub_deactivate.c:144**
```c
    _ux_utility_memory_free(transfer_request -> ux_transfer_request_data_pointer);
```

Now, here is the problematic code section.

The call stack for the code section that must not be freed or deallocated is as follows:
**Execution flow**
```txt
HAL_HCD_SOF_Callback()
    ↓
_ux_host_semaphore_put(&_ux_system_host -> ux_system_host_hcd_semaphore);
    ↓
_ux_host_stack_hcd_thread_entry()
      _ux_host_semaphore_get_norc(&_ux_system_host -> ux_system_host_hcd_semaphore, UX_WAIT_FOREVER);
    ↓
 hcd -> ux_hcd_entry_function()
      UX_HCD_PROCESS_DONE_QUEUE
    ↓
 _ux_hcd_stm32_entry()
    ↓
 _ux_hcd_stm32_periodic_schedule()
 if ((frame_index & ed -> ux_stm32_ed_interval_mask) == ed -> ux_stm32_ed_interval_position) 
    ↓
 _ux_hcd_stm32_request_trans_prepare()
```

In my case, an interrupt-IN transaction occurs every 128ms (every 128 SOF intervals).

1. In the case of the first interrupt IN transaction
`ed->ux_stm32_ed_data` is NULL at first. so this line is ignored
**ux_hcd_stm32_periodic_schedule.c:220**
```c
            if (ed -> ux_stm32_ed_data != NULL)
            {
              ed -> ux_stm32_ed_data_free = UX_HCD_STM32_ED_STATUS_ALIGNED_BUFFER_PENDING_FREE;
            }
```

2. `_ux_hcd_stm32_request_trans_prepare` is invoked. Because `ed->ux_stm32_ed_data` is NULL, this line is also ignored.
**ux_hcd_stm32_request_trans_prepare.c:78**
```c
    if ((ed -> ux_stm32_ed_data != UX_NULL) && (ed -> ux_stm32_ed_type != EP_TYPE_ISOC) &&
        (ed ->ux_stm32_ed_data_free == UX_HCD_STM32_ED_STATUS_ALIGNED_BUFFER_PENDING_FREE))
    {
      _ux_utility_memory_free(ed -> ux_stm32_ed_data);
      ed -> ux_stm32_ed_data = UX_NULL;
      ed ->ux_stm32_ed_data_free = UX_HCD_STM32_ED_STATUS_ALIGNED_BUFFER_FREE_DONE;
    }
```

3. Code sets `ed->ux_stm32_ed_data` to reusable buffer `transfer -> ux_transfer_request_data_pointer`
**ux_hcd_stm32_request_trans_prepare.c:87**
```c
ed -> ux_stm32_ed_data = transfer -> ux_transfer_request_data_pointer;
```

4. stmh5 is not using dma so, return function with UX_SUCCESS.
**ux_hcd_stm32_request_trans_prepare.c:90**
```c
    /* If DMA not enabled, nothing to do.  */
    if (!hcd_stm32 -> hcd_handle -> Init.dma_enable)
        return(UX_SUCCESS);
```

5. After 128ms, second interrupt IN transaction is started. `ed -> ux_stm32_ed_data` still has same address with `transfer -> ux_transfer_request_data_pointer`.
Because `ed -> ux_stm32_ed_data` is not NULL. Below code line is executed.
**ux_hcd_stm32_periodic_schedule.c:220**
```c
            if (ed -> ux_stm32_ed_data != NULL)
            {
              ed -> ux_stm32_ed_data_free = UX_HCD_STM32_ED_STATUS_ALIGNED_BUFFER_PENDING_FREE;
            }
```
The reusable buffer address that has a lifetime until `ux_host_class_hub_deactivate` is called is treated as pending-free region at interrupt IN transaction.

6. Free `ed -> ux_stm32_ed_data` and use deallocated address `transfer -> ux_transfer_request_data_pointer` for transfer.
**ux_hcd_stm32_request_trans_prepare.c:78**
```c
    if ((ed -> ux_stm32_ed_data != UX_NULL) && (ed -> ux_stm32_ed_type != EP_TYPE_ISOC) &&
        (ed ->ux_stm32_ed_data_free == UX_HCD_STM32_ED_STATUS_ALIGNED_BUFFER_PENDING_FREE))
    {
      _ux_utility_memory_free(ed -> ux_stm32_ed_data);
      ed -> ux_stm32_ed_data = UX_NULL;
      ed ->ux_stm32_ed_data_free = UX_HCD_STM32_ED_STATUS_ALIGNED_BUFFER_FREE_DONE;
    }

    /* Save transfer data pointer.  */
    ed -> ux_stm32_ed_data = transfer -> ux_transfer_request_data_pointer;
```

7. After 128ms, third interrupt IN transaction is started. Also, deallocated address `transfer -> ux_transfer_request_data_pointer` is handled as pending-free region.
In `ux_hcd_stm32_request_trans_prepare` function, `ed -> ux_stm32_ed_data` region is deallocated again.
As a result UX_MEMORY_CORRUPTED error code is passed to error handler
**_ux_utility_memory_free.c:172**
```
            _ux_system_error_handler(UX_SYSTEM_LEVEL_THREAD,
                                     UX_SYSTEM_CONTEXT_UTILITY, UX_MEMORY_CORRUPTED);
```

## 6. Solution of this problem

I edit the code below.
**ux_hcd_stm32_periodic_schedule.c:173**
```c
            if (ed -> ux_stm32_ed_data != NULL && ed -> ux_stm32_ed_data != transfer_request -> ux_transfer_request_data_pointer)
            {
              ed -> ux_stm32_ed_data_free = UX_HCD_STM32_ED_STATUS_ALIGNED_BUFFER_PENDING_FREE;
            }
```

**ux_hcd_stm32_periodic_schedule.c:220**
```c
            if (ed -> ux_stm32_ed_data != NULL && ed -> ux_stm32_ed_data != transfer_request -> ux_transfer_request_data_pointer)
            {
              ed -> ux_stm32_ed_data_free = UX_HCD_STM32_ED_STATUS_ALIGNED_BUFFER_PENDING_FREE;
            }
```

Code is now ignored to free reusable region of `transfer -> ux_transfer_request_data_pointer`.

No double free occurs, also after first interrupt IN transaction, allocated region is used.

This bug also occurs when the transfer buffer is 4-byte aligned.

## Comment 5396497646

other (NONE) · MKISTM · 2026-08-24T14:16:47Z · https://github.com/STMicroelectronics/stm32-mw-usbx/issues/6#issuecomment-5396497646

Hello @leejugy,

Thank you for this report, this point will be tracked internally.
I'll keep you informed about last update.

Best Regards,
KIWA Mohamed Chaker.


## Comment 5396501983

other (NONE) · MKISTM · 2026-08-24T14:17:06Z · https://github.com/STMicroelectronics/stm32-mw-usbx/issues/6#issuecomment-5396501983

ST Internal Reference: 42c389938372c714c09687402fda1ed4

## Comment 5518150893

other (NONE) · halytech-dm · 2026-09-02T23:53:14Z · https://github.com/STMicroelectronics/stm32-mw-usbx/issues/6#issuecomment-5518150893

Independent reproduction of the same bug on a different controller and device
class, for the internal ticket's record:

- **STM32U575** (OTG_FS host, `Init.dma_enable = DISABLE`), STM32CubeU5 **1.9.0**
  (USBX 6.4.0 / `v6.4.0_260508` host-controller glue). Not present on CubeU5 1.8.0,
  whose glue predates the `ux_stm32_ed_data_free` deferred-free scheme.
- Device: Telit LE910C1 / ME910G1 cellular modem (CDC-ECM composition); the
  vendor AT interface has a 64-byte **interrupt IN** endpoint polled by our host
  class. No hub, no isochronous endpoints.
- Symptom: `UX_MEMORY_CORRUPTED` (0x19) from the error callback on **every**
  periodic submission — about 340 per second (15,022 in a 45 s session).

Same mechanism as described above: in a non-DMA build
`_ux_hcd_stm32_request_trans_prepare()` always leaves `ed->ux_stm32_ed_data` set
to `transfer->ux_transfer_request_data_pointer` (it returns before any bounce
allocation), so both `PENDING_FREE` sites in `_ux_hcd_stm32_periodic_schedule()`
mark the class's own buffer and the next `trans_prepare` frees it.
`_ux_hcd_stm32_request_trans_finish()` already has the correct guards (early
return on `!dma_enable` and on `ed_data == transfer->data_pointer`); the two
periodic-schedule sites are the only markers without them.

The fix in PR #8 (`ed_data != transfer_request->ux_transfer_request_data_pointer`)
is the right shape — it also covers DMA-enabled builds whose class buffer is
already 4-byte aligned, where `trans_prepare` likewise skips the bounce allocation.
We are shipping an equivalent local patch (gated on `Init.dma_enable`, which is
sufficient for OTG_FS) until a CubeU5 pack carries the fix. Happy to test a
candidate pack/tag on the U575 if useful.

