# Leaking GPU memory

- URL: https://github.com/shader-slang/slangpy/issues/115
- Repo: shader-slang/slangpy (language: C++)
- State: open; created 2025-03-13T14:36:39Z; status ok; passes offcwe

## Issue body

reporter (NONE) · ranftlr · 2025-03-13T14:36:39Z · https://github.com/shader-slang/slangpy/issues/115

Thanks for this cool project!

I'm seeing a steadily increasing memory footprint when applying a function multiple times. Minimal example adapted from the slangpy examples:  

```slang
// example.slang
import "slangpy";

[Differentiable]
float polynomial(float a, float b, float c, float x) {
    return a * x * x + b * x + c;
}
```

```python
import slangpy as spy
import pathlib
import numpy as np

device = spy.create_device(include_paths=[
    pathlib.Path(__file__).parent.absolute(),
])

module = spy.Module.load_from_file(device, "example.slang")

while True:
    x = spy.Tensor.numpy(device, np.ones(1000*1000, dtype=np.float32)).with_grads(zero=True) 
    result: spy.Tensor = module.polynomial(a=2, b=8, c=-1, x=x, _result='tensor')
```

`nvidia-smi` shows increasing memory usage when running this, up until eventually hitting an OOM error.


I'm on Ubuntu 22.04, python 3.10, CUDA 12.6 and Nvidia Driver version 560.35.05. Not sure if relevant, but the system has multiple GPUs.
