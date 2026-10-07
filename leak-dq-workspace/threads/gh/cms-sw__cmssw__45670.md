# [ASAN_X] RelVal 537.0: attempting free on address which was not malloc()-ed

- URL: https://github.com/cms-sw/cmssw/issues/45670
- Repo: cms-sw/cmssw (language: C++)
- State: open; created 2024-08-08T13:21:42Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · iarspider · 2024-08-08T13:21:42Z · https://github.com/cms-sw/cmssw/issues/45670

In [CMSSW_14_1_ASAN_X_2024-08-07-2300](https://cmssdt.cern.ch/SDT/cgi-bin/logreader/el8_amd64_gcc12/CMSSW_14_1_ASAN_X_2024-08-07-2300/pyRelValMatrixLogs/run/537.0_DYToLL012Jets_5FS_TuneCH3_13TeV_amcatnloFxFx_herwig7/step1_DYToLL012Jets_5FS_TuneCH3_13TeV_amcatnloFxFx_herwig7.log#/1631-1631), RelVal 537.0 failed:

```
=================================================================
==1457289==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x602000ee22f0 in thread T0
    #0 0x15049a038248 in operator delete[](void*) ../../../../libsanitizer/asan/asan_new_delete.cpp:155
    #1 0x150497a0676d in TNamed::~TNamed() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/external/el8_amd64_gcc12/lib/libCore.so+0x23d76d)
    #2 0x15048e942af8 in TH1F::~TH1F() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/external/el8_amd64_gcc12/lib/libHist.so+0x2bfaf8)
    #3 0x15044930d829 in LheWeightValidation::~LheWeightValidation() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/lib/el8_amd64_gcc12/pluginValidationEventGenerator_plugins.so+0x1ac829)
    #4 0x15044930e61c in virtual thunk to LheWeightValidation::~LheWeightValidation() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/lib/el8_amd64_gcc12/pluginValidationEventGenerator_plugins.so+0x1ad61c)
    #5 0x15045e78209a in std::_Sp_counted_deleter<edm::one::EDProducerBase*, std::default_delete<edm::one::EDProducerBase>, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_dispose() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/lib/el8_amd64_gcc12/pluginFWCoreModules.so+0xfd09a)
    #6 0x15045e7871c9 in std::_Sp_counted_ptr_inplace<edm::maker::ModuleHolderT<edm::one::EDProducerBase>, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_dispose() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/lib/el8_amd64_gcc12/pluginFWCoreModules.so+0x1021c9)
    #7 0x15049953ab25 in std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_release() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/lib/el8_amd64_gcc12/libFWCoreFramework.so+0x233b25)
    #8 0x150499b536fa in std::_Rb_tree<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::pair<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const, edm::propagate_const<std::shared_ptr<edm::maker::ModuleHolder> > >, std::_Select1st<std::pair<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const, edm::propagate_const<std::shared_ptr<edm::maker::ModuleHolder> > > >, std::less<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >, std::allocator<std::pair<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const, edm::propagate_const<std::shared_ptr<edm::maker::ModuleHolder> > > > >::_M_erase(std::_Rb_tree_node<std::pair<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const, edm::propagate_const<std::shared_ptr<edm::maker::ModuleHolder> > > >*) [clone .isra.0] (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/lib/el8_amd64_gcc12/libFWCoreFramework.so+0x84c6fa)
    #9 0x150499b539cc in std::_Sp_counted_ptr_inplace<edm::ModuleRegistry, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_dispose() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/lib/el8_amd64_gcc12/libFWCoreFramework.so+0x84c9cc)
    #10 0x15049953ab25 in std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_release() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/lib/el8_amd64_gcc12/libFWCoreFramework.so+0x233b25)
    #11 0x1504996b6883 in edm::Schedule::~Schedule() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/lib/el8_amd64_gcc12/libFWCoreFramework.so+0x3af883)
    #12 0x150499628466 in edm::EventProcessor::~EventProcessor() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/lib/el8_amd64_gcc12/libFWCoreFramework.so+0x321466)
    #13 0x408c87 in (anonymous namespace)::EventProcessorWithSentry::~EventProcessorWithSentry() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/bin/el8_amd64_gcc12/cmsRun+0x408c87)
    #14 0x40870e in main (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/bin/el8_amd64_gcc12/cmsRun+0x40870e)
    #15 0x150495e957e4 in __libc_start_main (/lib64/libc.so.6+0x3a7e4)
    #16 0x408a5d in _start (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/bin/el8_amd64_gcc12/cmsRun+0x408a5d)

0x602000ee22f0 is located 48 bytes to the right of 16-byte region [0x602000ee22b0,0x602000ee22c0)
freed by thread T0 here:
    #0 0x15049a038248 in operator delete[](void*) ../../../../libsanitizer/asan/asan_new_delete.cpp:155
    #1 0x150497a0676d in TNamed::~TNamed() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/external/el8_amd64_gcc12/lib/libCore.so+0x23d76d)
    #2 0x15044930e61c in virtual thunk to LheWeightValidation::~LheWeightValidation() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/lib/el8_amd64_gcc12/pluginValidationEventGenerator_plugins.so+0x1ad61c)
    #3 0x15045e78209a in std::_Sp_counted_deleter<edm::one::EDProducerBase*, std::default_delete<edm::one::EDProducerBase>, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_dispose() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/lib/el8_amd64_gcc12/pluginFWCoreModules.so+0xfd09a)
    #4 0x15045e7871c9 in std::_Sp_counted_ptr_inplace<edm::maker::ModuleHolderT<edm::one::EDProducerBase>, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_dispose() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/lib/el8_amd64_gcc12/pluginFWCoreModules.so+0x1021c9)
    #5 0x15049953ab25 in std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_release() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/lib/el8_amd64_gcc12/libFWCoreFramework.so+0x233b25)
    #6 0x150499b536fa in std::_Rb_tree<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::pair<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const, edm::propagate_const<std::shared_ptr<edm::maker::ModuleHolder> > >, std::_Select1st<std::pair<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const, edm::propagate_const<std::shared_ptr<edm::maker::ModuleHolder> > > >, std::less<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >, std::allocator<std::pair<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const, edm::propagate_const<std::shared_ptr<edm::maker::ModuleHolder> > > > >::_M_erase(std::_Rb_tree_node<std::pair<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const, edm::propagate_const<std::shared_ptr<edm::maker::ModuleHolder> > > >*) [clone .isra.0] (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/lib/el8_amd64_gcc12/libFWCoreFramework.so+0x84c6fa)
    #7 0x150499b539cc in std::_Sp_counted_ptr_inplace<edm::ModuleRegistry, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>::_M_dispose() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/lib/el8_amd64_gcc12/libFWCoreFramework.so+0x84c9cc)
    #8 0x15049953ab25 in std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_release() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/lib/el8_amd64_gcc12/libFWCoreFramework.so+0x233b25)
    #9 0x1504996b6883 in edm::Schedule::~Schedule() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/lib/el8_amd64_gcc12/libFWCoreFramework.so+0x3af883)
    #10 0x150499628466 in edm::EventProcessor::~EventProcessor() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/lib/el8_amd64_gcc12/libFWCoreFramework.so+0x321466)
    #11 0x408c87 in (anonymous namespace)::EventProcessorWithSentry::~EventProcessorWithSentry() (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/bin/el8_amd64_gcc12/cmsRun+0x408c87)
    #12 0x40870e in main (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/bin/el8_amd64_gcc12/cmsRun+0x40870e)
    #13 0x150495e957e4 in __libc_start_main (/lib64/libc.so.6+0x3a7e4)

previously allocated by thread T0 here:
    #0 0x15049a037838 in operator new[](unsigned long) ../../../../libsanitizer/asan/asan_new_delete.cpp:98
    #1 0x150497a2c237 in TString::Init(int, int) (/cvmfs/cms-ib.cern.ch/sw/x86_64/nweek-02849/el8_amd64_gcc12/cms/cmssw/CMSSW_14_1_ASAN_X_2024-08-07-2300/external/el8_amd64_gcc12/lib/libCore.so+0x263237)

SUMMARY: AddressSanitizer: bad-free ../../../../libsanitizer/asan/asan_new_delete.cpp:155 in operator delete[](void*)
==1457289==ABORTING
```

## Comment 2275813005

reporter (CONTRIBUTOR) · iarspider · 2024-08-08T13:21:49Z · https://github.com/cms-sw/cmssw/issues/45670#issuecomment-2275813005

assign core

## Comment 2275813402

other (CONTRIBUTOR) · cmsbuild · 2024-08-08T13:21:59Z · https://github.com/cms-sw/cmssw/issues/45670#issuecomment-2275813402

New categories assigned: core

@Dr15Jones,@makortel,@smuzaffar you have been requested to review this Pull request/Issue and eventually sign? Thanks

## Comment 2275813445

other (CONTRIBUTOR) · cmsbuild · 2024-08-08T13:22:00Z · https://github.com/cms-sw/cmssw/issues/45670#issuecomment-2275813445

cms-bot internal usage<!-- bot cache: {"commits":{},"emoji":{"2275813005":"+1","2276383783":"+1"},"signatures":{}} -->

## Comment 2275813468

other (CONTRIBUTOR) · cmsbuild · 2024-08-08T13:22:01Z · https://github.com/cms-sw/cmssw/issues/45670#issuecomment-2275813468

A new Issue was created by  @iarspider.

@Dr15Jones, @antoniovilela, @makortel, @mandrenguyen, @rappoccio, @sextonkennedy, @smuzaffar can you please review it and eventually sign/assign? Thanks.

cms-bot commands are listed <a href="http://cms-sw.github.io/cms-bot-cmssw-issues.html">here</a>


## Comment 2276383651

other (CONTRIBUTOR) · makortel · 2024-08-08T18:05:37Z · https://github.com/cms-sw/cmssw/issues/45670#issuecomment-2276383651

@pcanal, would this be a symptom for two `TH1F` being created with the same name? (I have a vague recollection of similar issue before, but I wasn't able to find it)

## Comment 2276383783

other (CONTRIBUTOR) · makortel · 2024-08-08T18:05:41Z · https://github.com/cms-sw/cmssw/issues/45670#issuecomment-2276383783

type root

## Comment 2276392203

other (CONTRIBUTOR) · makortel · 2024-08-08T18:10:46Z · https://github.com/cms-sw/cmssw/issues/45670#issuecomment-2276392203

The error was not reported in the earlier ASAN IB CMSSW_14_1_ASAN_X_2024-08-05-2300, and the list of CMSSW or cmsdist PRs don't show anything clearly related.
