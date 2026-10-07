# Code bug(memory leaks)

- URL: https://github.com/yandex/faster-rnnlm/issues/49
- Repo: yandex/faster-rnnlm (language: C++)
- State: open; created 2018-09-13T09:38:34Z; status ok; passes main

## Issue body

reporter (NONE) · fabulousfeng · 2018-09-13T09:38:34Z · https://github.com/yandex/faster-rnnlm/issues/49

**~MaybeStaticArray() (hierarchical_softmax.cc:316)**
**Mismatched free() / delete / delete []** is detected by **Valgrind**. 
`delete dynamic_array; ` 
should be replaced by 
`delete [] dynamic_array;` 
since you defined `new T[dynamic_size]` in the constructor.
This may cause undefined behavior.

## Comment 420947073

reporter (NONE) · fabulousfeng · 2018-09-13T09:40:07Z · https://github.com/yandex/faster-rnnlm/issues/49#issuecomment-420947073

@akhti 
