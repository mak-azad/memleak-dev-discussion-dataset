# Self-referential types cause memory leaks

- URL: https://github.com/edwardwawrzynek/ovid/issues/24
- Repo: edwardwawrzynek/ovid (language: C++)
- State: open; created 2020-08-25T05:43:23Z; status ok; passes main

## Issue body

reporter (OWNER) · edwardwawrzynek · 2020-08-25T05:43:23Z · https://github.com/edwardwawrzynek/ovid/issues/24

Self-referential types (ie `struct Test { t *Test }`) cause std::shared_ptr cycles.

Type's don't have clear ownership, which is why shared_ptr is used. However, nearly all types survive until the llvm ir has been generated. 

It may make more sense to just allocate all types with a custom function that keeps track of allocations in a linked list, use raw pointers, and just free all types right before llvm codegen.
