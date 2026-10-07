# [Bug] Memory Leak in Training Loop (CPU)

- URL: https://github.com/ANSHAM1/LSTMiniNet/issues/1
- Repo: ANSHAM1/LSTMiniNet (language: C++)
- State: open; created 2025-08-31T17:41:14Z; status ok; passes main

## Issue body

reporter (OWNER) · ANSHAM1 · 2025-08-31T17:41:14Z · https://github.com/ANSHAM1/LSTMiniNet/issues/1

While training LSTMiniNet, memory usage increases continuously with every epoch and is never released. On longer training runs, this eventually leads to a system crash due to memory exhaustion.

This occurs on CPU build (C++20, no external ML/DL libraries) and seems related to how computational graphs or intermediate states are handled inside each epoch.

✅ Expected Behavior
Memory usage should remain stable across epochs (aside from temporary batch allocations).
After an epoch completes, no leftover graph nodes, gradients, or matrices should persist.

📊 Actual Behavior
Memory usage grows linearly with the number of epochs.
On long runs, this causes memory overflow and program termination.

🔍 Possible Causes
Reverse AutoDiff Engine: shared_ptr<Node> objects from previous epochs may not be released due to lingering references.
Gradient accumulation: Gradients may be stacking without reset between epochs.
Matrix allocations: Intermediate matrices might not be destroyed after use.

📌 Additional Context
This issue makes it difficult to run training for more than a few epochs.

Fixing it likely requires ensuring that:
    1. Graph nodes from one epoch don’t persist into the next.
    2. Gradients and states are reset after each step/epoch.
    3. Matrices are properly destructed when out of scope.

⚠️ Request: Could contributors suggest best practices for cleaning up autodiff graphs in C++ (shared_ptr cycle breaking, epoch cleanup, etc.)?
