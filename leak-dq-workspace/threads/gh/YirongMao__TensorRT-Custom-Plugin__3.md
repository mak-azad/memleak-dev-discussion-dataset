# free(): invalid pointer

- URL: https://github.com/YirongMao/TensorRT-Custom-Plugin/issues/3
- Repo: YirongMao/TensorRT-Custom-Plugin (language: C++)
- State: open; created 2022-06-07T10:10:32Z; status ok; passes main

## Issue body

reporter (NONE) · GeneralJing · 2022-06-07T10:10:32Z · https://github.com/YirongMao/TensorRT-Custom-Plugin/issues/3

free(): invalid pointer
Aborted (core dumped)
大佬，编译完，使用builder.py加载生成的.so后，注销后面的代码，或者不注销也行，执行完的时候会报错。这个是什么原因呢？我把官方代码拷贝进来，编译完，加载.so后，也会报错，这个是不是最外层在tensorRT plugin里面还有什么操作没有包含进来呢
