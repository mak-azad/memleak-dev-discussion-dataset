# LeakSanitizer: detected memory leaks

- URL: https://github.com/semitrivial/csv_parser/issues/7
- Repo: semitrivial/csv_parser (language: C)
- State: open; created 2024-03-30T00:28:46Z; status ok; passes main

## Issue body

reporter (NONE) · dennisrazumovsky · 2024-03-30T00:28:46Z · https://github.com/semitrivial/csv_parser/issues/7

Thank you for you hard work guys. That is nice and useful library but seems there are memory leaks detected.

How to repeat:

1. Install LLVM for sanitizer

```sh
sudo apt -y install llvm
```


2. Build with sanitizer

```sh
git clone https://github.com/semitrivial/csv_parser.git
cd csv_parser
clang -fsanitize=address -g -O0 -DDEBUG -Wall csv.c split.c fread_csv_line.c tests/test.c -o test
```

3, Run with sanitizer
```sh
ASAN_OPTIONS=symbolize=1 ASAN_SYMBOLIZER_PATH=/usr/bin/llvm-symbolizer ./test
```

```sh
unning test_parse_csv...Success.
Running test_split_on_unescaped_newlines...Success.
Running test_fread_csv_line...Success.

=================================================================
==115538==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 26 byte(s) in 1 object(s) allocated from:
    #0 0x562f0af00b53 in strdup (/home/user/examples/csv_parser/test+0x8cb53) (BuildId: 6dbba5a4b3656ad04924963f1dc4003f03e58507)
    #1 0x562f0af524be in fread_csv_line /home/user/examples/csv_parser/fread_csv_line.c:106:12
    #2 0x562f0af52ec2 in test_fread_csv_line /home/user/examples/csv_parser/tests/test.c:99:16
    #3 0x562f0af52554 in run_test /home/user/examples/csv_parser/tests/test.c:12:12
    #4 0x562f0af525cc in main /home/user/examples/csv_parser/tests/test.c:25:3
    #5 0x7f4e037c1d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

Direct leak of 18 byte(s) in 1 object(s) allocated from:
    #0 0x562f0af00b53 in strdup (/home/user/examples/csv_parser/test+0x8cb53) (BuildId: 6dbba5a4b3656ad04924963f1dc4003f03e58507)
    #1 0x562f0af524be in fread_csv_line /home/user/examples/csv_parser/fread_csv_line.c:106:12
    #2 0x562f0af53060 in test_fread_csv_line /home/user/examples/csv_parser/tests/test.c:108:16
    #3 0x562f0af52554 in run_test /home/user/examples/csv_parser/tests/test.c:12:12
    #4 0x562f0af525cc in main /home/user/examples/csv_parser/tests/test.c:25:3
    #5 0x7f4e037c1d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

Direct leak of 16 byte(s) in 1 object(s) allocated from:
    #0 0x562f0af00b53 in strdup (/home/user/examples/csv_parser/test+0x8cb53) (BuildId: 6dbba5a4b3656ad04924963f1dc4003f03e58507)
    #1 0x562f0af524be in fread_csv_line /home/user/examples/csv_parser/fread_csv_line.c:106:12
    #2 0x562f0af52fd6 in test_fread_csv_line /home/user/examples/csv_parser/tests/test.c:105:16
    #3 0x562f0af52554 in run_test /home/user/examples/csv_parser/tests/test.c:12:12
    #4 0x562f0af525cc in main /home/user/examples/csv_parser/tests/test.c:25:3
    #5 0x7f4e037c1d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

Direct leak of 16 byte(s) in 1 object(s) allocated from:
    #0 0x562f0af00b53 in strdup (/home/user/examples/csv_parser/test+0x8cb53) (BuildId: 6dbba5a4b3656ad04924963f1dc4003f03e58507)
    #1 0x562f0af524be in fread_csv_line /home/user/examples/csv_parser/fread_csv_line.c:106:12
    #2 0x562f0af52e38 in test_fread_csv_line /home/user/examples/csv_parser/tests/test.c:96:16
    #3 0x562f0af52554 in run_test /home/user/examples/csv_parser/tests/test.c:12:12
    #4 0x562f0af525cc in main /home/user/examples/csv_parser/tests/test.c:25:3
    #5 0x7f4e037c1d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

Direct leak of 16 byte(s) in 1 object(s) allocated from:
    #0 0x562f0af00b53 in strdup (/home/user/examples/csv_parser/test+0x8cb53) (BuildId: 6dbba5a4b3656ad04924963f1dc4003f03e58507)
    #1 0x562f0af524be in fread_csv_line /home/user/examples/csv_parser/fread_csv_line.c:106:12
    #2 0x562f0af52dae in test_fread_csv_line /home/user/examples/csv_parser/tests/test.c:93:16
    #3 0x562f0af52554 in run_test /home/user/examples/csv_parser/tests/test.c:12:12
    #4 0x562f0af525cc in main /home/user/examples/csv_parser/tests/test.c:25:3
    #5 0x7f4e037c1d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

Direct leak of 14 byte(s) in 1 object(s) allocated from:
    #0 0x562f0af00b53 in strdup (/home/user/examples/csv_parser/test+0x8cb53) (BuildId: 6dbba5a4b3656ad04924963f1dc4003f03e58507)
    #1 0x562f0af524be in fread_csv_line /home/user/examples/csv_parser/fread_csv_line.c:106:12
    #2 0x562f0af52f4c in test_fread_csv_line /home/user/examples/csv_parser/tests/test.c:102:16
    #3 0x562f0af52554 in run_test /home/user/examples/csv_parser/tests/test.c:12:12
    #4 0x562f0af525cc in main /home/user/examples/csv_parser/tests/test.c:25:3
    #5 0x7f4e037c1d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

Direct leak of 14 byte(s) in 1 object(s) allocated from:
    #0 0x562f0af00b53 in strdup (/home/user/examples/csv_parser/test+0x8cb53) (BuildId: 6dbba5a4b3656ad04924963f1dc4003f03e58507)
    #1 0x562f0af524be in fread_csv_line /home/user/examples/csv_parser/fread_csv_line.c:106:12
    #2 0x562f0af52d24 in test_fread_csv_line /home/user/examples/csv_parser/tests/test.c:90:16
    #3 0x562f0af52554 in run_test /home/user/examples/csv_parser/tests/test.c:12:12
    #4 0x562f0af525cc in main /home/user/examples/csv_parser/tests/test.c:25:3
    #5 0x7f4e037c1d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

Direct leak of 12 byte(s) in 1 object(s) allocated from:
    #0 0x562f0af00b53 in strdup (/home/user/examples/csv_parser/test+0x8cb53) (BuildId: 6dbba5a4b3656ad04924963f1dc4003f03e58507)
    #1 0x562f0af524be in fread_csv_line /home/user/examples/csv_parser/fread_csv_line.c:106:12
    #2 0x562f0af530ea in test_fread_csv_line /home/user/examples/csv_parser/tests/test.c:111:16
    #3 0x562f0af52554 in run_test /home/user/examples/csv_parser/tests/test.c:12:12
    #4 0x562f0af525cc in main /home/user/examples/csv_parser/tests/test.c:25:3
    #5 0x7f4e037c1d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

Direct leak of 12 byte(s) in 1 object(s) allocated from:
    #0 0x562f0af00b53 in strdup (/home/user/examples/csv_parser/test+0x8cb53) (BuildId: 6dbba5a4b3656ad04924963f1dc4003f03e58507)
    #1 0x562f0af524be in fread_csv_line /home/user/examples/csv_parser/fread_csv_line.c:106:12
    #2 0x562f0af52c9a in test_fread_csv_line /home/user/examples/csv_parser/tests/test.c:87:16
    #3 0x562f0af52554 in run_test /home/user/examples/csv_parser/tests/test.c:12:12
    #4 0x562f0af525cc in main /home/user/examples/csv_parser/tests/test.c:25:3
    #5 0x7f4e037c1d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

Direct leak of 1 byte(s) in 1 object(s) allocated from:
    #0 0x562f0af00b53 in strdup (/home/user/examples/csv_parser/test+0x8cb53) (BuildId: 6dbba5a4b3656ad04924963f1dc4003f03e58507)
    #1 0x562f0af524be in fread_csv_line /home/user/examples/csv_parser/fread_csv_line.c:106:12
    #2 0x562f0af53174 in test_fread_csv_line /home/user/examples/csv_parser/tests/test.c:114:16
    #3 0x562f0af52554 in run_test /home/user/examples/csv_parser/tests/test.c:12:12
    #4 0x562f0af525cc in main /home/user/examples/csv_parser/tests/test.c:25:3
    #5 0x7f4e037c1d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

SUMMARY: AddressSanitizer: 145 byte(s) leaked in 10 allocation(s).
```
