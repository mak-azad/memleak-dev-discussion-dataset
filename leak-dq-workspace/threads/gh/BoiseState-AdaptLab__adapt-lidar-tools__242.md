# csv-driver: Mismatched free() / delete / delete [ ]

- URL: https://github.com/BoiseState-AdaptLab/adapt-lidar-tools/issues/242
- Repo: BoiseState-AdaptLab/adapt-lidar-tools (language: C++)
- State: open; created 2019-07-22T00:01:49Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · SpencerFleming · 2019-07-22T00:01:49Z · https://github.com/BoiseState-AdaptLab/adapt-lidar-tools/issues/242

So, I was working on this as a part of #136, but it's causing me enough trouble that I want to document it as its own issue and get some help with it if I can.

Essentially, despite me getting a csv file with data in it, csv-driver is exiting with code 1. Valgrind tells me the following:

> 4535 ==36357== Mismatched free() / delete / delete []
> 4536 ==36357==    at 0x4C2AFF8: free (vg_replace_malloc.c:540)
> 4537 ==36357==    by 0x40ABCF: FlightLineData::calc_xyz_activation(std::vector<Peak*, std::allocato     r<Peak*> >*) (FlightLineData.cpp:379)
> 4538 ==36357==    by 0x40DD53: LidarDriver::fit_data_csv(FlightLineData&, std::vector<std::string*,      std::allocator<std::string*> >&, csv_CmdLine&) (LidarDriver.cpp:175)
> 4539 ==36357==    by 0x4059DA: main (pls_to_csv.cpp:46)
> 4540 ==36357==  Address 0xf0d8360 is 0 bytes inside a block of size 128 alloc'd
> 4541 ==36357==    at 0x4C2A4AA: operator new(unsigned long) (vg_replace_malloc.c:344)
> 4542 ==36357==    by 0x414ECD: GaussianFitter::guess_peaks(std::vector<Peak*, std::allocator<Peak*>      >*, std::vector<int, std::allocator<int> >, std::vector<int, std::allocator<int> >) (Gaussian     Fitter.cpp:751)
> 4543 ==36357==    by 0x413EAF: GaussianFitter::find_peaks(std::vector<Peak*, std::allocator<Peak*>      >*, std::vector<int, std::allocator<int> >, std::vector<int, std::allocator<int> >, unsigned l     ong) (GaussianFitter.cpp:365)
> 4544 ==36357==    by 0x40DCB0: LidarDriver::fit_data_csv(FlightLineData&, std::vector<std::string*,      std::allocator<std::string*> >&, csv_CmdLine&) (LidarDriver.cpp:167)
> 4545 ==36357==    by 0x4059DA: main (pls_to_csv.cpp:46)

fit_data_csv is similar to fit_data, except that instead of putting peaks into a LidarVolume object, it just runs to_string on them and then deletes them. That said, this distinction only occurs once calc_xyz_activation has already been called, so I'm not sure why that would even affect calc_xyz except that perhaps some artifact is being left in the peak vector between iterations, despite my deleting of every peak followed by a clear statement.

## Comment 513599117

reporter (CONTRIBUTOR) · SpencerFleming · 2019-07-22T00:02:37Z · https://github.com/BoiseState-AdaptLab/adapt-lidar-tools/issues/242#issuecomment-513599117

~half an hour on this.

## Comment 514855685

reporter (CONTRIBUTOR) · SpencerFleming · 2019-07-25T01:14:02Z · https://github.com/BoiseState-AdaptLab/adapt-lidar-tools/issues/242#issuecomment-514855685

~ 1 hr on this

## Comment 518811748

reporter (CONTRIBUTOR) · SpencerFleming · 2019-08-06T19:33:04Z · https://github.com/BoiseState-AdaptLab/adapt-lidar-tools/issues/242#issuecomment-518811748

Interesting news: I have found that the error in my first comment (mismatched free) is actually a nonfatal error for geotiff-driver. I'll have to do more research with this in mind when I get around do it!
