# Calc reference solution: Bad free() practice?

- URL: https://github.com/diku-compSys/compSys-e2023-pub/issues/2
- Repo: diku-compSys/compSys-e2023-pub (language: C)
- State: open; created 2023-10-19T10:47:28Z; status ok; passes main

## Issue body

reporter (NONE) · CausesHavok · 2023-10-19T10:47:28Z · https://github.com/diku-compSys/compSys-e2023-pub/issues/2

I was working on an old exercise "calc" (from "c dynamic memory"). 
The reference solution has a single line to free the stack. However, we could end up with orphaned stack nodes and no reference to them. Causing memory leaks, right? I can understand that the actual implementation of calc might never get into this situation, but is it not better to (like in list.c) run through your stack and making sure that everything is freed? From the point of view of the stack implementer we dont know that the stack WILL be empty before we are asked to "drop" it.

https://github.com/diku-compSys/compSys-e2023-pub/blob/989d28437ee62c823baf64801e1b830f16df1dab/lectures/23-09-20_c_dynamic_memory/calc_solution/stack.c#L21C1-L23C2
