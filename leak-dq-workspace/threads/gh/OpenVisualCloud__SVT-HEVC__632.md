# memory exhaustion when encodig 4K UHD 4:4:4 10-bit video

- URL: https://github.com/OpenVisualCloud/SVT-HEVC/issues/632
- Repo: OpenVisualCloud/SVT-HEVC (language: C)
- State: open; created 2023-02-06T10:34:59Z; status ok; passes main

## Issue body

reporter (NONE) · MartinPulec · 2023-02-06T10:34:59Z · https://github.com/OpenVisualCloud/SVT-HEVC/issues/632

Hi, this report can alternatively be considered also as a question - what is the memory requirement for 10-bit 4K UHD video?

On some Linux machine (Ubuntu 22.04) with i7-1260P and 32 GB of RAM, encoding starts but exhausts memory very quickly until the process gets killed by OOM-killer. Steps to reproduce:

    ffmpeg -f lavfi -i smptebars=size=3840x2160 -pix_fmt yuv444p10le -t 1 -strict -1 in.y4m
    SvtHevcEncApp -i in.y4m -b out.mp4

Replacing _yuv444p10le_ with _yuv420p_ works correctly. [SVT-HEVC README](https://github.com/OpenVisualCloud/SVT-HEVC/blob/master/README.md#hardware) tells that 16 GB should be sufficient for 4K, but I understand that it may be meant for 8-bit 4:2:0. Another interesting observation is that I've tried this on a different machine, with 128 GB RAM, but it consumed during the encode just around 8 GB. Also it seems that the library actually scales its memory requirements differently for different HW, I've tested with another 32 GB ram, this time with AMD 2950X, and it worked and took just something like one third of RAM during the encode (~ 10 GB). The one non-working setup required significantly more memory than those 2 working, therefore it doesn't seem to inherently require excessive amount of RAM (at least for some setups).
    

## Comment 1419660581

other (CONTRIBUTOR) · 1480c1 · 2023-02-06T19:53:33Z · https://github.com/OpenVisualCloud/SVT-HEVC/issues/632#issuecomment-1419660581

> it seems that the library actually scales its memory requirements differently for different HW

Fortunately, or unfortunately, all svt libraries scale their memory usage based on the detected core count as well, so it is not linearly tied to the input. Unfortunately, I cannot find if we had any concrete numbers regarding how much ram is needed for 4k 10-bit 444 input for 1 core. I, too, can reproduce this even with `-lp 1` requesting more than 40 GiBs of ram, along with 100+ virtual (requested, but not actually allocated for it)

## Comment 1420577004

reporter (NONE) · MartinPulec · 2023-02-07T10:54:26Z · https://github.com/OpenVisualCloud/SVT-HEVC/issues/632#issuecomment-1420577004

Well, but even so – it doesn't seem any reasonable upper bound (of course our definitions may differ) for the above command, I've re-tried with `-lp 1` and additional 64 GB swap. The allocation exhausted 32 GB of physical ram, then the 64 GB swap and after that it got killed by OOM killer. Unfortunately I don't have much more disk space on that machine.

Anyways, the above-described behavior occurs also for 8-bit yuv 4:4:4, so we can abstract from 10-bit. I've tested and it takes some 5.5 GB RAM to encode 4K UHD 4:2:2 sample video but 96 GB is not sufficient for 4:4:4. I think that these values don't correspond well.

## Comment 1422712577

other (NONE) · alatteri · 2023-02-08T14:47:02Z · https://github.com/OpenVisualCloud/SVT-HEVC/issues/632#issuecomment-1422712577

I have 2 Intel machines with 32GB of RAM (i7-1260P & E-2288G), and OOM happens on both.
I also have 2 AMD Ryzen machines with 16GB of RAM (3950X & 5950X) which work wonderfully with SVT-HEVC.
