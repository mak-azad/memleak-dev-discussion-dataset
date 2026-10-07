# [llvm 12.0.1] g++ 11 warns of mismatched-new-delete

- URL: https://github.com/llvm/llvm-project/issues/52997
- Repo: llvm/llvm-project (language: LLVM)
- State: open; created 2022-01-04T22:33:15Z; status ok; passes main

## Issue body

reporter (NONE) · cktan · 2022-01-04T22:33:15Z · https://github.com/llvm/llvm-project/issues/52997

Hi, 

Compiler: g++-11 (Ubuntu 11-20210417-1ubuntu1) 11.0.1 20210417 (experimental) [master revision c1c86ab96c2:b6fb0ccbb48:8ae884c09fbba91e9cec391290ee4a2859e7ff41]

LLVM: 12.0.1 built locally with g++-11.


I have a repro case below that caused g++ 11 to emit mismatched-new-delete warning. This may be more of a gcc-11 problem than llvm.

```
$ cat test.cpp
#include "llvm/IR/IRBuilder.h"

void foo(llvm::IRBuilder<>& builder, llvm::BasicBlock* block)
{
  builder.SetInsertPoint(block);
  builder.CreateICmpEQ(0, 0);
}
```

Compiling it with -O0:
```
$  g++-11 -Wall -Wextra -Wno-unused-parameter -I../llvm-12-release+assert/include -std=c++17 -fno-rtti -D_GNU_SOURCE -D_DEBUG -D__STDC_CONSTANT_MACROS -D__STDC_FORMAT_MACROS -D__STDC_LIMIT_MACROS -c -o test.o test.cpp
In file included from test.cpp:1:
../llvm-12-release+assert/include/llvm/IR/IRBuilder.h: In member function ‘llvm::Value* llvm::IRBuilderBase::CreateICmp(llvm::CmpInst::Predicate, llvm::Value*, llvm::Value*, const llvm::Twine&)’:
../llvm-12-release+assert/include/llvm/IR/IRBuilder.h:2385:43: warning: ‘static void llvm::User::operator delete(void*)’ called on pointer returned from a mismatched allocation function [-Wmismatched-new-delete]
 2385 |     return Insert(new ICmpInst(P, LHS, RHS), Name);
      |                                           ^
```

Compiling with -O1 will not result in warnings. 





## Comment 1139864415

other (NONE) · msebor · 2022-05-27T17:36:43Z · https://github.com/llvm/llvm-project/issues/52997#issuecomment-1139864415

The GCC warning issues false positives when one of the allocation and deallocation functions is inlined into its caller but not the other.  There's some detail in GCC bugs [103993](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=103993) and [100861](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=100861).

## Comment 1139888674

other (CONTRIBUTOR) · EugeneZelenko · 2022-05-27T17:45:11Z · https://github.com/llvm/llvm-project/issues/52997#issuecomment-1139888674

Could you please try version 14 or `main`?
