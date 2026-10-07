# Fuzzing pocketpy findings (WIP)

- URL: https://github.com/pocketpy/pocketpy/issues/541
- Repo: pocketpy/pocketpy (language: C)
- State: open; created 2026-08-25T16:01:02Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · szdytom · 2026-08-25T16:01:02Z · https://github.com/pocketpy/pocketpy/issues/541

I'm fuzzing pocketpy a bit and I'll keep my finding in this single issue to avoid creating too many issues. Please expect false positives.

## Runtime string subscript crashes on an invalid-UTF-8 byte

```py
s = 'a\xffb'
print(s[1])       # -> SIGABRT: "invalid utf8 char"
```

A string that contains a raw invalid UTF-8 byte (e.g. a source file/string literal holding a literal `0xFF` byte) is accepted by the lexer and stored; the moment it is **indexed or sliced**, the UTF-8 walk `c11__unicode_index_to_byte` (str.c:301) / `c11_sv__u8_getitem` calls `c11__u8_header(byte, false)`, which aborts on the invalid lead byte instead of treating the string as bytes or raising a clean error. The fuzzer surface for this is a *runtime* value whose bytes are invalid UTF-8 — reachable by feeding a raw non-UTF-8 byte into a string literal (which the byte-level fuzzer mutator can do), then subscripting it.

## `str * int` bitmask/`size*n` integer overflow can cause a memory-safety crash

Input:

```py
print('abcdefgh' * 1152921504606846976)   # ASan global-buffer-overflow
print('ab' * 5000000000000000000)         # ASan SEGV / write
```

`str__mul__` computes

```c
char* p = py_newstrn(py_retval(), self->size * n);   // py_str.c:178  (int64 product)
for(int i = 0; i < n; i++) {                          // py_str.c:179
    memcpy(p + i * self->size, self->data, self->size);   // py_str.c:180
}
```

The byte count `self->size * n` is a 64-bit multiply with **no overflow check**, and the loop counter/`i * self->size` arithmetic is done in `int`. For `'abcdefgh' * 1152921504606846976` the product is
`8 * 1152921504606846976 = 2^63`, which overflows `int64` leaving a wrongly-sized buffer; the loop then `memcpy`s `n` (1.15e18) copies, overflowing the (tiny) destination and reading past the heap/global object → **global-buffer-overflow** (read size 1,751,606,885, past `pk_default_vm`). For `'ab' * 5000000000000000000` the same overflow instead produces a **deadly `SEGV` write** in `c11_string__ctor3` (str.c:43). `str.__rmul__` and the `str * n` path share the code.

## `pickle.loads` crashes on malformed input (header / opcode not bounded)

Input:

```py
import pickle
pickle.loads(b'PK')        # 2a: Assertion `p_end != NULL' in pkl__header_read_sv
pickle.loads(b'PK\n0\n')   # 2b: pkl__read_int(): invalid op: 0
```

the pickled byte stream is parsed with **no length/bounds checks**. Two distinct crash sites were confirmed:
  - **2a. Header parse (assert):** `b'PK'` or `b'PK\n'`. After consuming the `PK` magic, `pkl__header_read_sv` (`strchr` from a pointer one-past the buffer) finds no `'('`/`')'` separator and hits `assert(p_end != NULL)` (pickle.c:485) → SIGABRT. The read itself is already past the input buffer.
  - **2b. Body opcode (abort):** `b'PK\n0\n'`. The first body byte read after the (mis)parsed header produces an opcode `pkl__read_int` does not handle ("invalid op: 0"), reaching `c11__abort` (pickle.c:147) → SIGABRT.

 **CPython control:** `pickle.loads(b'PK')` → `_pickle.UnpicklingError: pickle data was truncated`; `pickle.loads(b'PK\n0\n')` → `UnpicklingError` (clean).

## `int()` does not strip surrounding whitespace

Input:

```py
int(" 42 ")
```

CPython gives 42, pocketpy `ValueError: invalid literal for int() with base 10`.

## `round()`'s behavior differs from CPython

Ties are rounded differently: pocketpy rounds half *away from zero*; CPython uses *banker's (half-to-even)*.

  | value         | CPython | pocketpy |
  | ------------- | ------- | -------- |
  | `round(0.5)`  | 0       | 1        |
  | `round(1.5)`  | 2       | 2        |
  | `round(2.5)`  | 2       | **3**    |
  | `round(3.5)`  | 4       | 4        |
  | `round(4.5)`  | 4       | **5**    |
  | `round(-0.5)` | 0       | -1       |
  | `round(-2.5)` | -2      | -3       |

`round(float, 0)` overflows for |float| > int64 max. pocketpy returns INT64_MIN instead of the (rounded) float.
  
```py
print(round(1.7976931348623157e+308, 0))
# CPython  -> 1.7976931348623157e+308
# pocketpy -> -9.223372036854776e+18   (== INT64_MIN)
```
  
Also `round(1e19,0)`, `round(9.3e18,0)`, `round(1e100,0)` → pocketpy returns `-9.223372036854776e+18`; CPython returns the value.

`round(x, negative_ndigits)` rejected: `round(3.14159, -1)` → CPython `0.0`, pocketpy `ValueError: ndigits should be non-negative`.

## No cycle detection in recursive container operations

Input:

```py
x = []
x.append(x)
print(repr(x))     # -> ASan stack-overflow in pocketpy
```

`list.__repr__` recursively calls py_repr for every element without detecting recursive containers. For a self-referential list, `repr(x)` repeatedly invokes `list__repr__ ` on the same list until the C call stack is exhausted, aborting with a stack overflow instead of returning a cycle-safe representation such as `[[...]]`. Path: `src/public/PyList.c:list__repr__` → `py_repr` → `list__repr__`.

There are many variants of the bug, such as:

```py
x = []
x.append(x)
y = []
y.append(y)
print(x == y)
```

## Malformed \x escape followed by newline triggers lexer assertion failure

Input:

```py
x = "\x
x"
```

Running the debug build aborts with:

```
src/compiler/lexer.c:42: char eatchar(Lexer *):
Assertion `c != '\n'' failed.
```

Location: `src/compiler/lexer.c:42` — `eatchar` (`assert(c != '\n')`), reached from `_eat_string` (`lexer.c:302`) during `\x` hex-escape handling.

Inside a string literal, `\x` requires two hex digits. The guard only checks that 2 bytes exist before the *source end*, not that they are not newlines. If a literal newline immediately follows `\x`, `eatchar` is called on `'\n'` and its `assert` fires, crashing the lexer instead of reporting a clean `SyntaxError`.

## UTF-8 over-read causing heap-buffer-overflow in `c11__u8_value`

Input can be generated with:

```sh
python3 -c 'import sys; sys.stdout.buffer.write(b"a"*127 + b"\xfc\n")' > test.py
# or alternatively, a truncated 0xf0 also reproduces it with 129 a bytes
python3 -c 'import sys; sys.stdout.buffer.write(b"a"*129 + b"\xf0\n")' > test.py
```

A multi-byte UTF-8 lead byte (e.g. `0xfc`, `0xf0`) makes `c11__u8_header` return 4–6; `c11__u8_value` then reads that many bytes from the source buffer without checking there are that many bytes *left*, so a character placed near the end of the allocated source buffer over-reads it. Path: `lex_one_token` → `eat_name` (`src/compiler/lexer.c:215`); also reachable via `SourceData__ctor`.

The uninstrumented build may report a syntax error instead of visibly crashing because the over-read is undefined behavior. ASan reports:

```
heap-buffer-overflow
c11__u8_value (src/common/str.c:366)
eat_name (src/compiler/lexer.c:215)
lex_one_token (src/compiler/lexer.c:599)
```

## Out-of-bounds read in the `CodeObject` (`.pyc`) deserializer

`CodeObject__deserialize` reads a sequence of **count/length fields** from the byte stream and immediately uses them to allocate and `memcpy` that many bytes out of the input buffer, **without ever checking that the length fits within the remaining input**. The trailing 4-byte checksum in the `.pyc` format only guards against *accidental* corruption — it is a salted-free 31x rolling hash and is not a keyed MAC, so it does not stop a deliberate/crafted payload. A tiny crafted `.pyc` (23 bytes) is enough to make the deserializer read 4,000,000 bytes from a 23-byte heap buffer.

A malicious `.pyc` file can be generated with this simple script:

```py
#!/usr/bin/env python3
"""Builds a tiny .pyc that makes pocketpy's deserializer read past the buffer."""
import struct
import sys


def pocketpy_checksum(data: bytes) -> int:
    """c11__checksum_32bit: res = res*31 + byte."""
    res = 0
    for b in data:
        res = res * 31 + b
    return res & 0xFFFFFFFF


def build_malicious_pyc(codes_len: int = 1_000_000) -> bytes:
    payload = bytearray()
    payload += struct.pack("<H", 0x434F)        # magic "CO" (little-endian)
    payload += struct.pack("<bb", 1, 1)         # major_ver, minor_ver
    payload += b"x\x00"                          # name cstr
    payload += struct.pack("<i", codes_len)      # codes_len  <- attacker controlled
    payload += b"["                              # '[' mark
    payload += b"A" * 8                          # filler
    payload += struct.pack("<I", pocketpy_checksum(payload))  # trailing checksum
    return bytes(payload)


def main() -> int:
    out = sys.argv[1] if len(sys.argv) > 1 else "oob.pyc"
    data = build_malicious_pyc()
    with open(out, "wb") as f:
        f.write(data)
    print(f"[*] wrote {out} ({len(data)} bytes); codes_len={1000000}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

In `CodeObject__deserialize` (`src/objects/codeobject_ser.c`), the length field for each array is read from the input and then passed straight to a `c11_vector__extend(..., read_bytes(d, len * sizeof(T)), len)` without any validation. `read_bytes` does not validate either — it just returns `self->data + self->index` and advances `self->index += size`. Because `codes_len` (an `int32`) is fully attacker-controlled and is never compared against the remaining bytes of the deserializer input, the `memcpy` source pointer runs far past the end of the buffer causing a **heap-buffer-overflow read**.

`src/objects/codeobject_ser.c`:

| Field            | length read | read_bytes / extend        |
| ---------------- | ----------- | -------------------------- |
| `codes_len`      | line 207    | lines 209–210              |
| `codes_ex_len`   | line 214    | lines 216–217              |
| `blocks_len`     | line 256    | lines 258–259              |
| `consts_len`     | line 222    | loop over `consts_len`     |
| `varnames_len`   | line 231    | loop over `varnames_len`   |
| `names_len`      | line 242    | loop over `names_len`      |
| `func_decls_len` | line 264    | loop over `func_decls_len` |

…and, inside `FuncDecl__deserialize`:

| Field        | read     | extend                 |
| ------------ | -------- | ---------------------- |
| `args_len`   | line 338 | lines 340–341          |
| `kwargs_len` | line 346 | loop over `kwargs_len` |

The first three (`codes_len`, `codes_ex_len`, `blocks_len`) are the most obviously exploitable because they feed a raw `memcpy` of `len * sizeof(T)` bytes; the loop-based ones can also be used to cause a large/invalid count that allocates or indexes erroneously, and `varnames_len`/`names_len` can force `py_name()` on oversized strings.

This table is just a quick review around the reported part, there might be more.

<details>
<summary>Resolved Findings</summary>

## Interpreter crash on `%` in error message

Input:

```
x = %
```

`pk_vsprintf` (in `src/common/sstream.c:242`) parses the error message as a format string; when the message contains an unsupported character after `%` or ends with `%`, it hits the `default` branch and executes `assert(false)`. This crash only occurs when `NDEBUG` is not defined (debug builds)—release builds (with `-DNDEBUG`) do not crash; instead, they output the illegal character literally. Combined with other issues, this could further lead to security attacks related to string formatting.

Resolved by: b89ebd4cca075f4cb30030016ec9b9af375e6cda

## Lexer Buffer Leak when having boundary quotes in raw strings.

Input:

```py
x = r"a"b"
```

Per #55, it is by design that raw string cannot have boundary quotes in it. However, there is a memory leak on the error path:

```
ERROR: LeakSanitizer: detected memory leaks / Direct leak of 68 byte(s) ... c11_sbuf__ctor ... eat_string /lexer.c:384
```

Inside `eat_string`, after `c11_sbuf__ctor` allocates a buffer, if the lexical error branch is taken and the function returns early, `c11_sbuf__dtor` is not called to free the buffer.

Resolved by: 8f703fdd783baab081c03444bd2cef8f5f227d38

## Mismatched Destructor Function Pointer in CodeObject destructor

Input:

```python
eval("1+1")
```

Any code path that destroys a reference‑counted object can trigger this issue—for example, `eval`/`exec`, cleanup after compilation or execution errors, and `gc.collect()` when it reclaims function objects that contain nested `def` statements. The following input also reproduces the problem:

```python
exec("x=1")
def make():
    def inner():
        pass
    return inner
for i in range(50):
    make()
import gc
gc.collect()
```

Calling a destructor through a mismatched function pointer, which constitutes C‑level undefined behavior. Specifically, when releasing a `CodeObject`, the destructor is invoked with an incorrect function pointer type at `src/objects/codeobject.c:137` (via `PK_DECREF(decl)`). The root cause is that `FuncDecl_` is actually a `FuncDecl*`, but it is cast to `void (*)(void*)` during registration (`codeobject.c:31`: `self->rc.dtor = (void(*)(void*))FuncDecl__dtor;`) and subsequently called through that mismatched type, violating C’s function‑pointer type‑matching rules. This triggers an UBSan function error: 

```
call to function FuncDecl__dtor through pointer to incorrect function type 'void (*)(void *)'”*, which is a genuine 
```

Resolved by: f38f3656d0b2145130e9ec1638a0be44bf8ba687

</details>


## Comment 5705852653

other (NONE) · Shubham-Padkonde · 2026-09-16T23:12:22Z · https://github.com/pocketpy/pocketpy/issues/541#issuecomment-5705852653

I reproduced the string-repetition finding on current main with AddressSanitizer: `'ab' * 2147483648` reaches an invalid write in `str__mul__` after the byte length narrows to `int`.

I am preparing a focused fix for this part of #541: check the repeat count by division before multiplying, include the string/object header overhead in the representable allocation bound, and return immediately for empty strings. The regression covers both operand orders, the reported 64-bit overflow counts, 32-bit narrowing, and huge repeats of an empty string. I am using `ValueError` for an oversized result because this runtime does not currently define `OverflowError`.

This leaves the other findings in this issue open. Prepared with Codex assistance; sanitizer and full-suite validation are in progress.

