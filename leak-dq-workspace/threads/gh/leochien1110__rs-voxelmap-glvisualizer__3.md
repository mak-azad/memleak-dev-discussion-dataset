# readvoxel GPU memory leak

- URL: https://github.com/leochien1110/rs-voxelmap-glvisualizer/issues/3
- Repo: leochien1110/rs-voxelmap-glvisualizer (language: C++)
- State: open; created 2021-10-24T16:56:26Z; status ok; passes offcwe

## Issue body

reporter (OWNER) · leochien1110 · 2021-10-24T16:56:26Z · https://github.com/leochien1110/rs-voxelmap-glvisualizer/issues/3

GPU memory leak in legacy branch-> `readvoxel`
Output of `nvidia-smi`:

```bash
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 470.42.01    Driver Version: 470.42.01    CUDA Version: 11.4     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ...  Off  | 00000000:3C:00.0  On |                  N/A |
| 33%   61C    P0    45W / 151W |    884MiB /  8119MiB |     23%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|    0   N/A  N/A      1590      G   /usr/lib/xorg/Xorg                160MiB |
|    0   N/A  N/A      2457      G   /usr/lib/xorg/Xorg                390MiB |
|    0   N/A  N/A      2580      G   /usr/bin/gnome-shell              134MiB |
|    0   N/A  N/A      3225      G   ...AAAAAAAAA= --shared-files       97MiB |
|    0   N/A  N/A     18800      G   ./read_voxel                       22MiB |
+-----------------------------------------------------------------------------+
```
