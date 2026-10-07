# Memory issues - Indirect leak

- URL: https://github.com/SialkLang/Sialk/issues/4
- Repo: SialkLang/Sialk (language: C)
- State: open; created 2024-08-09T10:58:29Z; status ok; passes main

## Issue body

reporter (MEMBER) · BaseMax · 2024-08-09T10:58:29Z · https://github.com/SialkLang/Sialk/issues/4

input source `input.sialk`:
```


عملکرد سلام {

    لیست = 999 + 12

    نمایش لیست
}
```

--------

Memory issues:

```
max@Workstation:/mnt/c/Users/MAX/salam$ ./s
Welcome to Salam Programming Language!
Salam is the first Persian/Iranian computer scripting language.

Usage:
  salam <filename>                      # Execute a Salam script

Example:
  salam my_script.salam         # Run the Salam script 'my_script.salam'

Feel free to explore and create using Salam!
For more information, visit: https://salamlang.ir

max@Workstation:/mnt/c/Users/MAX/salam$ ./s input.salam
[0]: 3 FUNCTION - عملکرد
[1]: 0 IDENTIFIER - سلام
[2]: 16 SECTION_OPEN - {
[3]: 0 IDENTIFIER - لیست
[4]: 27 EQUAL - =
[5]: 1 NUMBER - 999
[6]: 22 PLUS - +
[7]: 1 NUMBER - 12
[8]: 7 PRINT - نمایش
[9]: 0 IDENTIFIER - لیست
[10]: 17 SECTION_CLOSE - }
[11]: 35 EOF -
Parsing function
Parsing block
Parsing statement
Parsing expression
Parsing pratt
Parsing identifier
Parsing operator assignment
Parsing pratt
Parsing number
Parsing operator binary
Parsing pratt
Parsing number
Parsing statement
Parsing statement print
Parsing expression
Parsing pratt
Parsing identifier
<?xml version="1.0" encoding="UTF-8"?>
<AST>
  <Functions>
    <FunctionDeclaration>
      <Name>سلام</Name>
      <Arguments />
      <Block>
        <Expression>
          <Assignment>
            <Left>
              <Expression>
                <Identifier>
                  <Name>لیست</Name>
                </Identifier>
              </Expression>
            </Left>
            <Right>
              <Expression>
                <BinaryOperator>
                  <Operator>+</Operator>
                  <Left>
                    <Expression>
                      <Literal>
                        <Type>INT</Type>
                        <Value>999</Value>
                      </Literal>
                    </Expression>
                  </Left>
                  <Right>
                    <Expression>
                      <Literal>
                        <Type>INT</Type>
                        <Value>12</Value>
                      </Literal>
                    </Expression>
                  </Right>
                </BinaryOperator>
              </Expression>
            </Right>
          </Assignment>
        </Expression>
        <StatementPrint>
          <Expression>
            <Identifier>
              <Name>لیست</Name>
            </Identifier>
          </Expression>
        </StatementPrint>
      </Block>
    </FunctionDeclaration>
  </Functions>
  <Expressions>
  </Expressions>
</AST>
====================================
1011
No return value from main function, so default!
====================================
RUN DONE
free lexer
end lexer free
free parser
Free function سلام
ast_node_free
node type: 0
free ast function
free function name
free function arguments
free function body
ast_node_free
node type: 8
free ast block
ast_node_free
node type: 9
free ast expr AST_EXPRESSION
ast_expression_free
---- expr type: 4
ast_expression_free_assignment
ast_node_free
node type: 4
free ast print
free print expr
ast_expression_free
---- expr type: 2
ast_expression_free_identifier
free print expr value
check expr value of print
ast_expression_free_data
start checking type on ast_expression_free_data
free expression data
free expression data main
let's free it's at all
*parser is null 1
parser is null 0
end parser free
free interpreter
end interpreter free
DONE

=================================================================
==815==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 48 byte(s) in 1 object(s) allocated from:
    #0 0x7f86f2939887 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x55d004a9e49f in interpreter_expression_binary /mnt/c/Users/MAX/salam/salam.c:3110
    #2 0x55d004aaaf23 in interpreter_expression /mnt/c/Users/MAX/salam/salam.c:3538
    #3 0x55d004aaa405 in interpreter_expression_assignment /mnt/c/Users/MAX/salam/salam.c:3464
    #4 0x55d004aaaf5b in interpreter_expression /mnt/c/Users/MAX/salam/salam.c:3546
    #5 0x55d004aaae15 in interpreter_statement_expression /mnt/c/Users/MAX/salam/salam.c:3510
    #6 0x55d004a9a77b in interpreter_interpret_once /mnt/c/Users/MAX/salam/salam.c:2855
    #7 0x55d004a9d11c in interpreter_block /mnt/c/Users/MAX/salam/salam.c:3039
    #8 0x55d004a9bb19 in interpreter_function_declaration /mnt/c/Users/MAX/salam/salam.c:2922
    #9 0x55d004a9b54c in interpreter_interpret /mnt/c/Users/MAX/salam/salam.c:2897
    #10 0x55d004aabcce in main /mnt/c/Users/MAX/salam/salam.c:3656
    #11 0x7f86f2050d8f  (/lib/x86_64-linux-gnu/libc.so.6+0x29d8f)

Direct leak of 16 byte(s) in 1 object(s) allocated from:
    #0 0x7f86f2939887 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x55d004a8aab8 in led_equal /mnt/c/Users/MAX/salam/salam.c:2112
    #2 0x55d004a8a254 in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2099
    #3 0x55d004a897db in parser_expression /mnt/c/Users/MAX/salam/salam.c:2077
    #4 0x55d004a8918e in parser_statement /mnt/c/Users/MAX/salam/salam.c:2056
    #5 0x55d004a90078 in parser_block /mnt/c/Users/MAX/salam/salam.c:2347
    #6 0x55d004a847fb in parser_function /mnt/c/Users/MAX/salam/salam.c:1839
    #7 0x55d004a914d5 in parser_parse /mnt/c/Users/MAX/salam/salam.c:2394
    #8 0x55d004aabba4 in main /mnt/c/Users/MAX/salam/salam.c:3649
    #9 0x7f86f2050d8f  (/lib/x86_64-linux-gnu/libc.so.6+0x29d8f)

Direct leak of 8 byte(s) in 1 object(s) allocated from:
    #0 0x7f86f2939887 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x55d004a8f6d9 in nud_identifier /mnt/c/Users/MAX/salam/salam.c:2309
    #2 0x55d004a89d7d in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2093
    #3 0x55d004a897db in parser_expression /mnt/c/Users/MAX/salam/salam.c:2077
    #4 0x55d004a85692 in parser_statement_print /mnt/c/Users/MAX/salam/salam.c:1875
    #5 0x55d004a89066 in parser_statement /mnt/c/Users/MAX/salam/salam.c:2045
    #6 0x55d004a90078 in parser_block /mnt/c/Users/MAX/salam/salam.c:2347
    #7 0x55d004a847fb in parser_function /mnt/c/Users/MAX/salam/salam.c:1839
    #8 0x55d004a914d5 in parser_parse /mnt/c/Users/MAX/salam/salam.c:2394
    #9 0x55d004aabba4 in main /mnt/c/Users/MAX/salam/salam.c:3649
    #10 0x7f86f2050d8f  (/lib/x86_64-linux-gnu/libc.so.6+0x29d8f)

Indirect leak of 48 byte(s) in 1 object(s) allocated from:
    #0 0x7f86f2939887 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x55d004a8d630 in nud_number /mnt/c/Users/MAX/salam/salam.c:2214
    #2 0x55d004a89d7d in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2093
    #3 0x55d004a8aeb3 in led_equal /mnt/c/Users/MAX/salam/salam.c:2114
    #4 0x55d004a8a254 in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2099
    #5 0x55d004a897db in parser_expression /mnt/c/Users/MAX/salam/salam.c:2077
    #6 0x55d004a8918e in parser_statement /mnt/c/Users/MAX/salam/salam.c:2056
    #7 0x55d004a90078 in parser_block /mnt/c/Users/MAX/salam/salam.c:2347
    #8 0x55d004a847fb in parser_function /mnt/c/Users/MAX/salam/salam.c:1839
    #9 0x55d004a914d5 in parser_parse /mnt/c/Users/MAX/salam/salam.c:2394
    #10 0x55d004aabba4 in main /mnt/c/Users/MAX/salam/salam.c:3649
    #11 0x7f86f2050d8f  (/lib/x86_64-linux-gnu/libc.so.6+0x29d8f)

Indirect leak of 48 byte(s) in 1 object(s) allocated from:
    #0 0x7f86f2939887 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x55d004a8d630 in nud_number /mnt/c/Users/MAX/salam/salam.c:2214
    #2 0x55d004a89d7d in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2093
    #3 0x55d004a8c8c6 in led_plus_minus /mnt/c/Users/MAX/salam/salam.c:2176
    #4 0x55d004a8a254 in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2099
    #5 0x55d004a8aeb3 in led_equal /mnt/c/Users/MAX/salam/salam.c:2114
    #6 0x55d004a8a254 in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2099
    #7 0x55d004a897db in parser_expression /mnt/c/Users/MAX/salam/salam.c:2077
    #8 0x55d004a8918e in parser_statement /mnt/c/Users/MAX/salam/salam.c:2056
    #9 0x55d004a90078 in parser_block /mnt/c/Users/MAX/salam/salam.c:2347
    #10 0x55d004a847fb in parser_function /mnt/c/Users/MAX/salam/salam.c:1839
    #11 0x55d004a914d5 in parser_parse /mnt/c/Users/MAX/salam/salam.c:2394
    #12 0x55d004aabba4 in main /mnt/c/Users/MAX/salam/salam.c:3649
    #13 0x7f86f2050d8f  (/lib/x86_64-linux-gnu/libc.so.6+0x29d8f)

Indirect leak of 24 byte(s) in 1 object(s) allocated from:
    #0 0x7f86f2939887 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x55d004a8c9be in led_plus_minus /mnt/c/Users/MAX/salam/salam.c:2182
    #2 0x55d004a8a254 in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2099
    #3 0x55d004a8aeb3 in led_equal /mnt/c/Users/MAX/salam/salam.c:2114
    #4 0x55d004a8a254 in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2099
    #5 0x55d004a897db in parser_expression /mnt/c/Users/MAX/salam/salam.c:2077
    #6 0x55d004a8918e in parser_statement /mnt/c/Users/MAX/salam/salam.c:2056
    #7 0x55d004a90078 in parser_block /mnt/c/Users/MAX/salam/salam.c:2347
    #8 0x55d004a847fb in parser_function /mnt/c/Users/MAX/salam/salam.c:1839
    #9 0x55d004a914d5 in parser_parse /mnt/c/Users/MAX/salam/salam.c:2394
    #10 0x55d004aabba4 in main /mnt/c/Users/MAX/salam/salam.c:3649
    #11 0x7f86f2050d8f  (/lib/x86_64-linux-gnu/libc.so.6+0x29d8f)

Indirect leak of 16 byte(s) in 1 object(s) allocated from:
    #0 0x7f86f2939887 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x55d004a8c8d4 in led_plus_minus /mnt/c/Users/MAX/salam/salam.c:2179
    #2 0x55d004a8a254 in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2099
    #3 0x55d004a8aeb3 in led_equal /mnt/c/Users/MAX/salam/salam.c:2114
    #4 0x55d004a8a254 in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2099
    #5 0x55d004a897db in parser_expression /mnt/c/Users/MAX/salam/salam.c:2077
    #6 0x55d004a8918e in parser_statement /mnt/c/Users/MAX/salam/salam.c:2056
    #7 0x55d004a90078 in parser_block /mnt/c/Users/MAX/salam/salam.c:2347
    #8 0x55d004a847fb in parser_function /mnt/c/Users/MAX/salam/salam.c:1839
    #9 0x55d004a914d5 in parser_parse /mnt/c/Users/MAX/salam/salam.c:2394
    #10 0x55d004aabba4 in main /mnt/c/Users/MAX/salam/salam.c:3649
    #11 0x7f86f2050d8f  (/lib/x86_64-linux-gnu/libc.so.6+0x29d8f)

Indirect leak of 16 byte(s) in 1 object(s) allocated from:
    #0 0x7f86f2939887 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x55d004a8d546 in nud_number /mnt/c/Users/MAX/salam/salam.c:2211
    #2 0x55d004a89d7d in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2093
    #3 0x55d004a8c8c6 in led_plus_minus /mnt/c/Users/MAX/salam/salam.c:2176
    #4 0x55d004a8a254 in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2099
    #5 0x55d004a8aeb3 in led_equal /mnt/c/Users/MAX/salam/salam.c:2114
    #6 0x55d004a8a254 in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2099
    #7 0x55d004a897db in parser_expression /mnt/c/Users/MAX/salam/salam.c:2077
    #8 0x55d004a8918e in parser_statement /mnt/c/Users/MAX/salam/salam.c:2056
    #9 0x55d004a90078 in parser_block /mnt/c/Users/MAX/salam/salam.c:2347
    #10 0x55d004a847fb in parser_function /mnt/c/Users/MAX/salam/salam.c:1839
    #11 0x55d004a914d5 in parser_parse /mnt/c/Users/MAX/salam/salam.c:2394
    #12 0x55d004aabba4 in main /mnt/c/Users/MAX/salam/salam.c:3649
    #13 0x7f86f2050d8f  (/lib/x86_64-linux-gnu/libc.so.6+0x29d8f)

Indirect leak of 16 byte(s) in 1 object(s) allocated from:
    #0 0x7f86f2939887 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x55d004a8d546 in nud_number /mnt/c/Users/MAX/salam/salam.c:2211
    #2 0x55d004a89d7d in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2093
    #3 0x55d004a8aeb3 in led_equal /mnt/c/Users/MAX/salam/salam.c:2114
    #4 0x55d004a8a254 in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2099
    #5 0x55d004a897db in parser_expression /mnt/c/Users/MAX/salam/salam.c:2077
    #6 0x55d004a8918e in parser_statement /mnt/c/Users/MAX/salam/salam.c:2056
    #7 0x55d004a90078 in parser_block /mnt/c/Users/MAX/salam/salam.c:2347
    #8 0x55d004a847fb in parser_function /mnt/c/Users/MAX/salam/salam.c:1839
    #9 0x55d004a914d5 in parser_parse /mnt/c/Users/MAX/salam/salam.c:2394
    #10 0x55d004aabba4 in main /mnt/c/Users/MAX/salam/salam.c:3649
    #11 0x7f86f2050d8f  (/lib/x86_64-linux-gnu/libc.so.6+0x29d8f)

Indirect leak of 16 byte(s) in 1 object(s) allocated from:
    #0 0x7f86f2939887 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x55d004a8ed70 in nud_identifier /mnt/c/Users/MAX/salam/salam.c:2281
    #2 0x55d004a89d7d in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2093
    #3 0x55d004a897db in parser_expression /mnt/c/Users/MAX/salam/salam.c:2077
    #4 0x55d004a8918e in parser_statement /mnt/c/Users/MAX/salam/salam.c:2056
    #5 0x55d004a90078 in parser_block /mnt/c/Users/MAX/salam/salam.c:2347
    #6 0x55d004a847fb in parser_function /mnt/c/Users/MAX/salam/salam.c:1839
    #7 0x55d004a914d5 in parser_parse /mnt/c/Users/MAX/salam/salam.c:2394
    #8 0x55d004aabba4 in main /mnt/c/Users/MAX/salam/salam.c:3649
    #9 0x7f86f2050d8f  (/lib/x86_64-linux-gnu/libc.so.6+0x29d8f)

Indirect leak of 9 byte(s) in 1 object(s) allocated from:
    #0 0x7f86f28e09a7 in __interceptor_strdup ../../../../src/libsanitizer/asan/asan_interceptors.cpp:454
    #1 0x55d004a8f930 in nud_identifier /mnt/c/Users/MAX/salam/salam.c:2311
    #2 0x55d004a89d7d in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2093
    #3 0x55d004a897db in parser_expression /mnt/c/Users/MAX/salam/salam.c:2077
    #4 0x55d004a8918e in parser_statement /mnt/c/Users/MAX/salam/salam.c:2056
    #5 0x55d004a90078 in parser_block /mnt/c/Users/MAX/salam/salam.c:2347
    #6 0x55d004a847fb in parser_function /mnt/c/Users/MAX/salam/salam.c:1839
    #7 0x55d004a914d5 in parser_parse /mnt/c/Users/MAX/salam/salam.c:2394
    #8 0x55d004aabba4 in main /mnt/c/Users/MAX/salam/salam.c:3649
    #9 0x7f86f2050d8f  (/lib/x86_64-linux-gnu/libc.so.6+0x29d8f)

Indirect leak of 9 byte(s) in 1 object(s) allocated from:
    #0 0x7f86f28e09a7 in __interceptor_strdup ../../../../src/libsanitizer/asan/asan_interceptors.cpp:454
    #1 0x55d004a8f930 in nud_identifier /mnt/c/Users/MAX/salam/salam.c:2311
    #2 0x55d004a89d7d in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2093
    #3 0x55d004a897db in parser_expression /mnt/c/Users/MAX/salam/salam.c:2077
    #4 0x55d004a85692 in parser_statement_print /mnt/c/Users/MAX/salam/salam.c:1875
    #5 0x55d004a89066 in parser_statement /mnt/c/Users/MAX/salam/salam.c:2045
    #6 0x55d004a90078 in parser_block /mnt/c/Users/MAX/salam/salam.c:2347
    #7 0x55d004a847fb in parser_function /mnt/c/Users/MAX/salam/salam.c:1839
    #8 0x55d004a914d5 in parser_parse /mnt/c/Users/MAX/salam/salam.c:2394
    #9 0x55d004aabba4 in main /mnt/c/Users/MAX/salam/salam.c:3649
    #10 0x7f86f2050d8f  (/lib/x86_64-linux-gnu/libc.so.6+0x29d8f)

Indirect leak of 8 byte(s) in 1 object(s) allocated from:
    #0 0x7f86f2939887 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x55d004a8f6d9 in nud_identifier /mnt/c/Users/MAX/salam/salam.c:2309
    #2 0x55d004a89d7d in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2093
    #3 0x55d004a897db in parser_expression /mnt/c/Users/MAX/salam/salam.c:2077
    #4 0x55d004a8918e in parser_statement /mnt/c/Users/MAX/salam/salam.c:2056
    #5 0x55d004a90078 in parser_block /mnt/c/Users/MAX/salam/salam.c:2347
    #6 0x55d004a847fb in parser_function /mnt/c/Users/MAX/salam/salam.c:1839
    #7 0x55d004a914d5 in parser_parse /mnt/c/Users/MAX/salam/salam.c:2394
    #8 0x55d004aabba4 in main /mnt/c/Users/MAX/salam/salam.c:3649
    #9 0x7f86f2050d8f  (/lib/x86_64-linux-gnu/libc.so.6+0x29d8f)

Indirect leak of 2 byte(s) in 1 object(s) allocated from:
    #0 0x7f86f28e09a7 in __interceptor_strdup ../../../../src/libsanitizer/asan/asan_interceptors.cpp:454
    #1 0x55d004a8cc15 in led_plus_minus /mnt/c/Users/MAX/salam/salam.c:2183
    #2 0x55d004a8a254 in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2099
    #3 0x55d004a8aeb3 in led_equal /mnt/c/Users/MAX/salam/salam.c:2114
    #4 0x55d004a8a254 in parser_expression_pratt /mnt/c/Users/MAX/salam/salam.c:2099
    #5 0x55d004a897db in parser_expression /mnt/c/Users/MAX/salam/salam.c:2077
    #6 0x55d004a8918e in parser_statement /mnt/c/Users/MAX/salam/salam.c:2056
    #7 0x55d004a90078 in parser_block /mnt/c/Users/MAX/salam/salam.c:2347
    #8 0x55d004a847fb in parser_function /mnt/c/Users/MAX/salam/salam.c:1839
    #9 0x55d004a914d5 in parser_parse /mnt/c/Users/MAX/salam/salam.c:2394
    #10 0x55d004aabba4 in main /mnt/c/Users/MAX/salam/salam.c:3649
    #11 0x7f86f2050d8f  (/lib/x86_64-linux-gnu/libc.so.6+0x29d8f)

SUMMARY: AddressSanitizer: 284 byte(s) leaked in 14 allocation(s).
```

