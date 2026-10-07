# munmap_chunk(): invalid pointer

- URL: https://github.com/Electrostatics/apbs/issues/247
- Repo: Electrostatics/apbs (language: C)
- State: open; created 2022-10-04T20:06:13Z; status ok; passes main

## Issue body

reporter (NONE) · yuntaoyang · 2022-10-04T20:06:13Z · https://github.com/Electrostatics/apbs/issues/247

Hi APBS developers,

**Describe the bug**
I ran APBS using a PDB file for a protein complex. But APBS was aborted and got the following error message. How to fix this issue?

**log file**
This executable compiled on May 30 2019 at 19:36:46
Parsing input file Myo1_Myo1.in...
rank 0 size 1...
read
Parsed input file.
Got paths for 1 molecules
Reading PQR-format atom data from Myo1_Myo1.pqr.
  63126 atoms
  Centered at (5.216e+01, 5.426e+01, -7.410e+00)
  Net charge -4.00e+01 e
Preparing to run 2 PBE calculations.
CALCULATION #1: MULTIGRID
  Setting up problem...
  Vpbe_ctor:  Using max ion radius (0 A) for exclusion function
  Debye length:  0 A
  Current memory usage:  93259.980 MB total, 93259.980 MB high water
  Using cubic spline charge discretization.
  Grid dimensions: 545 x 801 x 929
  Grid spacings: 0.777 x 0.807 x 0.811
  Grid lengths: 422.617 x 645.682 x 752.906
  Grid center: (52.160, 54.262, -7.410)
  Multigrid levels: 4
  Molecule ID: 1
  Linearized traditional PBE
  Single Debye-Huckel sphere boundary conditions
  0 ion species (0.000 M ionic strength):
  Solute dielectric: 2.000
  Solvent dielectric: 78.540
  Using "molecular" surface definition;harmonic average smoothing
  Solvent probe radius: 1.400 A
  Temperature:  298.150 K
  Electrostatic energies will be calculated
Vbuildband: dpbfa problem: 1
Vbuildband: leading principle minor not PD...
Vbuildops: Changing your mgsolv to iterative
  Total electrostatic energy = -NAN kJ/mol
  Calculating forces...
CALCULATION #2: MULTIGRID
  Setting up problem...
  Vpbe_ctor:  Using max ion radius (0 A) for exclusion function
munmap_chunk(): invalid pointer
Aborted (core dumped)

**To Reproduce**
Steps to reproduce the behavior:
1. pdb2pqr30 --apbs-input Myo1_Myo1.in --whitespace Myo1_Myo1.pdb Myo1_Myo1.pqr
2. apbs Myo1_Myo1.in

**Server: CentOS**

Thank you so much for your help!

Best,
Yuntao Yang


## Comment 1268482367

maintainer (MEMBER) · sobolevnrm · 2022-10-05T14:04:45Z · https://github.com/Electrostatics/apbs/issues/247#issuecomment-1268482367

Hello --

How much memory does the server have?

Thank you

## Comment 1268486184

reporter (NONE) · yuntaoyang · 2022-10-05T14:07:46Z · https://github.com/Electrostatics/apbs/issues/247#issuecomment-1268486184

> Hello --
> 
> How much memory does the server have?
> 
> Thank you

Hi Nathan,

The total memory is about 6000 GB. The available memory was about 3000 GB when I ran the program.

Best,
Yuntao
