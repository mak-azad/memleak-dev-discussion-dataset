# wasm: heap use-after-free when export wrapper outlives Module

- URL: https://github.com/saghul/txiki.js/issues/1078
- Repo: saghul/txiki.js (language: C)
- State: open; created 2026-08-31T02:09:43Z; status ok; passes offcwe

## Issue body

reporter (NONE) · xmzyshypnc · 2026-08-31T02:09:43Z · https://github.com/saghul/txiki.js/issues/1078

The Wasm export wrapper returned by `Instance.exports` binds to the C-level native instance object (from `buildInstance`), not to the JS `Instance`. If only the export function is retained, the JS `Instance` becomes garbage, its `#moduleRef` is released, and the `Module` finalizer runs `wasm_runtime_unload` — but the C-level `TJSWasmInstance` is still alive (pinned by `.bind()`). The next call to the export reaches `wasm_runtime_lookup_function`, which `strcmp`s over the freed module's export table. Same class of bug as #1051 (FFI dlopen UAF).

### Reproducer

```js
const bytes = new Uint8Array([
  0,97,115,109,1,0,0,0,
  1,6,1,96,1,127,1,127,
  2,10,1,3,101,110,118,2,99,98,0,0,
  3,2,1,0,
  7,7,1,3,114,117,110,0,1,
  10,8,1,6,0,32,0,16,0,11
]);

function getExport() {
  const mod = new WebAssembly.Module(bytes);
  const inst = new WebAssembly.Instance(mod, { env: { cb: x => x } });
  return inst.exports.run;
}

const run = getExport();
for (let i = 0; i < 100; i++) new ArrayBuffer(1024 * 1024);
run();
```

```
$ ./build/tjs run repro.js
Segmentation fault: 11
```

Probabilistic (~30%), depends on whether the GC collects the Module before `run()` is called. ASan reports a heap-use-after-free read in `strcmp` → `cmp_export_func_inst` → `wasm_lookup_function` → `tjs_wasm_callfunction`.

### Cause

`src/js/polyfills/wasm.js:343` creates export wrappers as:

```js
fn = callWasmFunction.bind(instance, item.name);
```

`instance` is the C-level native object returned by `buildInstance()`. The JS `Instance` class (line 374) stores `this.#moduleRef = module` to keep the Module alive, but the export wrapper does not reference the JS `Instance` — only the C native object. So:

1. User keeps only the export: `const run = new Instance(mod, imports).exports.run`
2. JS `Instance` is unreachable → GC'd → `#moduleRef` released
3. `Module` is unreachable → GC'd → `tjs_wasm_module_finalizer` → `wasm_runtime_unload` (frees WAMR module)
4. C `TJSWasmInstance` is still alive (held by `.bind()`) with a dangling `module_inst`
5. `run()` → `wasm_runtime_lookup_function` → `strcmp` on freed export name → **heap UAF**

The C struct `TJSWasmInstance` (`src/wasm.c`) does not store a `JSValue` reference to the Module, so WAMR's requirement that the module outlive its instances is not enforced.

### Suggested fix

Add a `JSValue module_ref` to `TJSWasmInstance`. `JS_DupValue` it in `tjs_wasm_buildinstance`, `JS_FreeValueRT` it in `tjs_wasm_instance_finalizer`.

**Reported by**: [@xmzyshypnc](https://github.com/xmzyshypnc), [@carol233](https://github.com/carol233), [@lyyffee](https://github.com/lyyffee)

