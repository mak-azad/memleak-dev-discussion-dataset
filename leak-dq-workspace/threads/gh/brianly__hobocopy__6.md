# Bug: mismatched new[]/delete in Utilities::Free and CComException::get_File

- URL: https://github.com/brianly/hobocopy/issues/6
- Repo: brianly/hobocopy (language: C++)
- State: open; created 2026-07-27T20:10:05Z; status ok; passes main

## Issue body

reporter (OWNER) · brianly · 2026-07-27T20:10:05Z · https://github.com/brianly/hobocopy/issues/6

Two spots free an array allocation with scalar `delete` instead of `delete[]`, which is undefined behavior:

- `Utilities.h:303-306` — `Free(LPCSTR x) { delete x; }` deletes a `new CHAR[]` buffer allocated in `ConvertToMultibyteString` (`Utilities.h:66`).
- `CComException.h:57-63` — `get_File` has the identical `new[]`/`delete` mismatch.

Additionally, `ConvertToMultibyteString` (`Utilities.h:66`) may leave its buffer unterminated — it converts exactly `GetLength()` bytes into a `GetLength()+1` buffer but never writes the NUL terminator.

**Fix:** change `delete` to `delete[]` at both sites, ensure the multibyte buffer is NUL-terminated, or better, replace the raw-array pattern with `std::vector<char>`/`std::string` to remove manual lifetime management entirely.
