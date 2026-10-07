# memory leak in particles MPI communication?

- URL: https://github.com/IAS-Astrophysics/athenak/issues/716
- Repo: IAS-Astrophysics/athenak (language: C++)
- State: open; created 2026-03-13T15:32:45Z; status ok; passes main

## Issue body

reporter (COLLABORATOR) · gnwong · 2026-03-13T15:32:45Z · https://github.com/IAS-Astrophysics/athenak/issues/716

### Summary

In `particles::ParticlesBoundaryValues::CountSendsAndRecvs` at https://github.com/IAS-Astrophysics/athenak/blob/main/src/bvals/bvals_part.cpp#L237C1-L239C32, a derived MPI datatype is created and committed but never freed.

```
MPI_Datatype mpi_ituple;
MPI_Type_contiguous(3, MPI_INT, &mpi_ituple);
MPI_Type_commit(&mpi_ituple);
```

I believe that, according to the MPI standard, derived datatypes should be freed with `MPI_Type_free` when they're no longer needed. Since this creation happens in the particle communication loop, it likely leads to a buildup of MPI datatype objects inside of MPI.

### Suggested fixes

1. Simply add `MPI_Type_free(&mpi_ituple);` after the `MPI_Allgatherv` call, which should be safe since the latter is blocking.
2. Instantiate the mpi datatype earlier in the lifecycle so that it's created and committed once. Then reuse on this call.

I think option (2) is better, but it'd require a larger (but not quite substantial) change to the setup.

Thoughts?

## Comment 4061330627

maintainer (COLLABORATOR) · jmstone · 2026-03-14T20:32:24Z · https://github.com/IAS-Astrophysics/athenak/issues/716#issuecomment-4061330627

You could add this datatype to the particle class and then create/free it in the particle constructor/destructor.  I guess this is to avoid allocating and deallocating memory every timestep?  Seems like a good thing to avoid.
