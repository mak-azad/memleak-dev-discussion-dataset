# Memory allocation and excessive memory usage in some functions

- URL: https://github.com/burakyueksel/physics/issues/17
- Repo: burakyueksel/physics (language: C)
- State: open; created 2023-02-06T18:44:32Z; status ok; passes main

## Issue body

reporter (OWNER) · burakyueksel · 2023-02-06T18:44:32Z · https://github.com/burakyueksel/physics/issues/17

Example, see returnX functions in matrix library.
Example to that:

https://github.com/burakyueksel/physics/blob/main/src/matrix.c#L368

where a new matrix is created, but its memory is never freed.

I have implemented the returnX function, for better coding style. This became very apparent in se3 ctrl implementation. Example
https://github.com/burakyueksel/physics/blob/main/src/controls.c#L292

But it comes with the curse: every time that function is called, the matrix used for that purpose is never deleted.

Find a more elegant solution to that.

And in general to keep the memory usage in control, use stacks.




