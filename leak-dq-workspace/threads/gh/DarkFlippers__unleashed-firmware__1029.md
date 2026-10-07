# [NFC]: Memory leaks & double-frees in NFC app (supported-card parsers, app lifecycle, DESFire)

- URL: https://github.com/DarkFlippers/unleashed-firmware/issues/1029
- Repo: DarkFlippers/unleashed-firmware (language: C)
- State: closed; created 2026-07-05T14:22:19Z; status ok; passes main

## Issue body

reporter (MEMBER) · mishamyte · 2026-07-05T14:22:19Z · https://github.com/DarkFlippers/unleashed-firmware/issues/1029

## Summary

A comprehensive memory audit of the NFC app (`applications/main/nfc`) and NFC stack (`lib/nfc`) — ~61k LOC, ~285 files — surfaced **7 memory bugs + 1 RAM over-allocation**. Four are **double-frees (heap corruption)**, three are **leaks**, one is an over-allocation. The protocol/worker core, CLI, scene lifecycle, and render layer are otherwise clean.

## Findings

| # | Location | Type | Triggers |
|---|----------|------|----------|
| 1 | `plugins/supported_cards/plantain.c:457` + `:710` | **double-free** of `card_number_str` | every Plantain card with a card number |
| 2 | `plugins/supported_cards/szppk_so.c:420-423` | **double-free** of 4 primary strings + **leak** of 4 secondary | two-trip SZPPK ticket (`second_ticket_marker != 0`) |
| 3 | `plugins/supported_cards/sevppk_tk.c:371-374` | same copy-paste bug | two-trip SEV ticket |
| 4 | `plugins/supported_cards/sk_tk.c:378-381` | same copy-paste bug | two-trip SK ticket |
| 5 | `plugins/supported_cards/saflok.c:347` | **leak** — `restricted_weekday_string` never freed (0 frees in file) | every Saflok card parse |
| 6 | `nfc_app.c:54` | **leak** — `api_resolver` (+2 list nodes) never freed | every NFC-app open→close |
| 7 | `scenes/nfc_scene_mf_classic_dict_attack.c:257` | **leak** — `Stream` + `RECORD_STORAGE` ref on error path | CUID dict present but `buffered_file_stream_open` fails |
| 8 | `lib/nfc/protocols/mf_desfire/mf_desfire_i.c:903` | **over-allocation** ~15× RAM per file | every DESFire read (`sizeof(MfDesfireData)` used where element is `MfDesfireFileData`) |

### Details

- **1 plantain** — `printf_plantain_data` frees `purse->card_number_str` (`:457`), then the caller frees the same dangling, non-NULL pointer again (`:710`). Fix: drop the free inside the print function; ownership stays with the caller.
- **2–4 PPK family** — identical copy-paste error: inside the `second_ticket_marker != 0` branch, `secondary_ticket.*` is allocated but cleanup re-frees the already-freed `primary_ticket.*` → double-free + the 4 secondary strings leak. Fix: free the `secondary_ticket.*` members.
- **5 saflok** — `restricted_weekday_string` is allocated, only read via `furi_string_get_cstr`, and never freed (the file contains zero `furi_string_free`). Fix: free before `} while(false)`.
- **6 nfc_app** — `composite_api_resolver_alloc()` + 2× `composite_api_resolver_add`, never freed in `nfc_app_free`; `nfc_supported_cards` only borrows the pointer. Fix: `composite_api_resolver_free(instance->api_resolver)` in `nfc_app_free`.
- **7 CUID dict** — the `buffered_file_stream_open`-fail branch does only `buffered_file_stream_close` + `free(dict)`, leaking the `Stream` object and the `RECORD_STORAGE` reference; the sibling `total_keys == 0` path already handles it correctly. Fix: `keys_dict_free(dict)`.
- **8 DESFire** — `mf_desfire_file_data_array_config.type_size = sizeof(MfDesfireData)` (~60+ B) but the element type is `MfDesfireFileData` (`{ SimpleArray* data; }` = 4 B). Not corruption (consistent stride, freed correctly), just wasted heap scaled by (#files × #apps). Fix: `sizeof(MfDesfireFileData)`.

## Excluded (verified not bugs)

Three "uninitialized pointer field after `malloc`" candidates were ruled out — Flipper's `malloc` → `pvPortMalloc` zero-fills every allocation (`furi/core/memmgr_heap.c:467`, `xToWipe = xWantedSize`): `nfc_supported_cards.c` `app`, `nfc_protocol_support.c` `base`, `nfc_scanner_alloc` `state`/`scan_worker` (and `NfcScannerStateIdle == 0`).

## Also noted (minor / hardening — not in this fix set)

- `felica_listener.c:34` — `mbedtls_des3_init` in alloc with no `mbedtls_des3_free` in `felica_listener_free` (not a heap leak; session-key material not zeroized on teardown).
- `mf_classic_poller.c:261` — `memset` over live dict-attack pointers (safe today, fragile).
- `detect_reader.c:81` — listener freed in event handlers, not `on_exit` (latent leak if torn down while active).
- `nfc_device.c:313` — `nfc_device_load_legacy` leaves the device dirty on the verify-ok/load-fail path (state hygiene, not a leak).

## Fix plan

Branch `bug/nfc-memory-leaks`, one commit per finding (#1–#8).

Found in version: dev

