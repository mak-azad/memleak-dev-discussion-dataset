"""Codebook, retrieval signatures and text-processing rules.

Single source of truth for:
  * DQ_LABELS   - the diagnostic-question codebook (32 original + 4 added in the off-CWE pass)
  * NON_DIAGNOSTIC - codes excluded from diagnostic frequency tables
  * THEMES      - theme codes used in the off-CWE pass
  * DQ_PATTERNS - regex prefilter used to select GitHub *statements* in the main pass
                  (NOT the coding itself: final codes are hand-assigned, see codes/*.csv)
  * CWE_SIGNATURES - regexes assigning multi-label CWE signatures to threads
  * text cleaning / sentence splitting rules for each source and pass

Changing anything here changes which units are extracted, and therefore which
hand codes join (see scripts/04_join_codes.py). Bump CODEBOOK_VERSION when you do.
"""
from __future__ import annotations
import html
import re

CODEBOOK_VERSION = "2026-10-05"

DQ_LABELS: dict[str, tuple[str, str]] = {
    'V1': ('Report interpretation', 'Is the suspected leak/invalid free real, or a false positive / benign report?'),
    'R2': ('Report interpretation', "What does the tool's report category or runtime error mean (definitely/indirectly/possibly lost, still reachable, suppressed, invalid pointer)?"),
    'R3': ('Report interpretation', 'Is the report caused by my code, or by a library, runtime, or the tool itself?'),
    'R4': ('Report interpretation', 'Where was the block allocated / where does the leak or bad free originate?'),
    'R5': ('Report interpretation', 'How do I detect, configure, or suppress this with the tool?'),
    'A1': ('Allocation', 'Is this memory on the heap at all (vs. stack, static, string literal)?'),
    'A2': ('Allocation', 'Does this function/API allocate what it returns (must the caller free it)?'),
    'A3': ('Allocation', 'Which allocator family produced this pointer (malloc/new/new[]/custom/library)?'),
    'A4': ('Allocation', 'Is the allocation size bounded and validated (untrusted input, overflow, huge/negative size, failure)?'),
    'O1': ('Ownership', 'Who is responsible for releasing this memory (caller vs. callee contract)?'),
    'O2': ('Ownership', 'Was ownership transferred (to a container, smart pointer, library, or object), so someone else releases it?'),
    'D1': ('Deallocation', 'Is there a matching release for this allocation, and where should it go?'),
    'D2': ('Deallocation', 'Is the pointer passed to free exactly the one the allocator returned (not offset/advanced)?'),
    'D3': ('Deallocation', 'Is the deallocator the right one for the allocator (free vs delete vs delete[] vs library free)?'),
    'D4': ('Deallocation', 'Is the pointer valid to free right now (initialized, not already freed, not dangling)?'),
    'C1': ('Control flow', 'Is the memory released on every path: error handling, early return, exceptions, longjmp?'),
    'C2': ('Control flow', 'Is the old block released on each loop iteration / reallocation (realloc failure, reassignment in a loop)?'),
    'L1': ('Lifetime', 'Must the memory be freed before program exit, or is exit-time retention acceptable?'),
    'L2': ('Lifetime', 'Is the object destroyed when its lifetime ends (scope exit, destructor called, virtual destructor)?'),
    'L3': ('Lifetime', 'Does memory keep growing with repetitions (retained longer than needed, unbounded growth)?'),
    'L4': ('Lifetime', 'Are threads joined/detached so that their resources are released?'),
    'E1': ('Escape / aliasing', 'Was the last reference overwritten or lost before release?'),
    'E2': ('Escape / aliasing', 'Does the pointer escape (global, struct field, return value) so it must be released elsewhere?'),
    'E3': ('Escape / aliasing', 'Do other aliases or copies refer to the same block (shallow copy, copy ctor, two owners)?'),
    'N1': ('Composite cleanup', 'Are nested sub-allocations released (struct members, list nodes, 2-D arrays) before/with the parent?'),
    'N2': ('Composite cleanup', 'Is a reference cycle or refcount imbalance preventing release?'),
    'N3': ('Composite cleanup', 'Does the cleanup routine / destructor release every resource the object owns?'),
    'X1': ('Cross-module', 'Are allocation and release done by the same module/runtime heap (DLL, CRT, FFI boundary)?'),
    'G': ('Non-diagnostic', 'Generic: why does this leak/crash? (no specific evidence asked)'),
    'T1': ('Non-diagnostic', 'Triage: reproducer, full trace, version, build flags'),
    'P': ('Non-diagnostic', 'Prevention / best-practice advice'),
    'K': ('Non-diagnostic', 'Allocator internals (how free knows the size, etc.)'),
    'RK': ('Resource kind', 'What kind of resource is held (memory, fd, socket, handle, JNI ref, GPU object, thread), and which call releases it?'),
    'R6': ('Report interpretation', 'Is the growth in RSS / task-manager memory leaked memory, or freed memory the allocator has not returned (fragmentation, arenas, caches)?'),
    'D5': ('Deallocation', 'Is the block accessed after it was released (use after free, dangling reference)?'),
    'H1': ('Deallocation', 'Was the heap already corrupted before the failing free/malloc (earlier overflow)?'),
}

NON_DIAGNOSTIC: frozenset[str] = frozenset({"G", "T1", "P", "K", "NA"})

THEMES: dict[str, str] = {
    'RES': 'Non-memory resource leak (fd, socket, handle, cgo/JNI handle) ~ CWE-772/775',
    'THR': 'Thread / process lifetime ~ CWE-404',
    'GRW': 'Growth without a classic leak (allocator retention, fragmentation, caches) ~ CWE-400/770',
    'REF': 'Reference counting in bindings / COM / kernel ~ CWE-911',
    'GPU': 'GPU / graphics memory',
    'KER': 'Kernel memory (kmemleak)',
    'POOL': 'Memory pools, arenas, custom allocators',
    'DF': 'Double free ~ CWE-415',
    'UAF': 'Use after free / dangling ~ CWE-416',
    'HC': 'Heap corruption surfacing at free/malloc ~ CWE-122/787',
    'UNI': 'Uninitialised memory in leak reports ~ CWE-457/908',
    'LIB': 'Library / runtime global cleanup',
    'INFO': "'Leak' meaning information disclosure ~ CWE-200",
    'IN': 'Inside the seven target CWEs',
    'NA': 'Not relevant',
}

DQ_PATTERNS: dict[str, list[str]] = {
    'R1': ['false positive', '\\bis (this|it|that) (really |actually )?(a )?(memory )?leak', '(really|actually|real|genuine) (memory )?leak', '\\bbenign\\b', '\\bsafe to ignore\\b', '\\bcan (i|we) (safely )?ignore\\b', '\\bshould (i|we) (be )?worr', '\\bis (this|that|it) (bad|a problem|harmful)\\b'],
    'R2': ['still reachable', 'possibly lost', 'indirectly lost', 'definitely lost', 'indirect leak', 'suppressed'],
    'R3': ['\\b(library|libc|glibc|runtime|pthread|iostream|openmp|libstdc\\+\\+|driver|SDL|Qt|GTK)\\b.{0,60}\\b(leak|allocat|own memory|internal|cache|pool)', '\\b(leak|report|error)s?\\b.{0,60}\\b(in|from|inside) (the )?(library|libc|glibc|runtime|system librar|third[- ]party)', 'suppression', '\\bnot (in )?my code\\b', "does(n't| not) (point|reference) (to )?my"],
    'R4': ['where (was|is) (it|this|the memory|that memory|the block)? ?allocated', 'allocation (stack|site|trace|point)', 'track-origins', 'allocated (by|at|in) (thread|function|line)', 'which (allocation|malloc|new)\\b', '\\bwhere does (the|this) (leak|memory) come from'],
    'A1': ['\\b(on|in) the (stack|heap)\\b', '\\bstring literal', '\\bstatic (array|storage|variable|buffer|memory)', '\\b(local|automatic) (array|variable|storage|object)', 'not (been )?(dynamically )?allocated (with|by|using) (malloc|new|calloc)', "wasn'?t (malloc|allocated)", 'not malloc', '\\bread-?only memory\\b', '\\bheap[- ]allocated\\b', '\\bstack[- ]allocated\\b'],
    'A2': ['\\b(does|do) (\\w+\\(?\\)? ?)?(allocate|malloc)', '\\bshould (i|we|you) (free|delete|release)\\b.{0,40}\\b(return|from|by)\\b', '\\breturn(s|ed)? (a )?(pointer|buffer|string).{0,40}(static|internal|allocated|must be freed|need to be freed)', '\\bstatic (buffer|storage)\\b', '\\b(do|does|must|should) (i|we|you|the caller) (need to )?free\\b.{0,60}\\b(getenv|strdup|asprintf|getline|basename|dirname|setlocale|getpwuid|readdir|strtok|ctime|localtime|gmtime|strerror)', '\\b(getenv|setlocale|getpwuid|getpwnam|readdir|ctime|localtime|gmtime|strerror|inet_ntoa|basename|dirname)\\b.{0,60}\\b(free|static|owned)'],
    'A3': ['allocated (with|by|using|via) (malloc|new|calloc|realloc|strdup|new\\[\\]|operator new|a custom|the library)', '\\b(malloc|new\\[\\]|new)\\b.{0,30}\\b(paired|match|matching|corresponding)\\b', 'which (allocator|deallocator)', '\\bcustom allocator\\b', '\\boperator new\\b'],
    'A4': ['\\b(huge|too large|too big|excessive|enormous|very large|large) (allocation|size|malloc|amount of memory|request)', 'allocation-size-too-big', 'exceeds maximum supported size', '\\bnegative (size|value|number)\\b.{0,40}\\b(malloc|alloc|size)', '\\b(size|length|count)\\b.{0,40}\\b(from|read from|controlled by|supplied by) (the )?(user|input|file|network|header|attacker)', '\\binteger overflow\\b', '\\bsize_t\\b.{0,40}\\b(wrap|overflow|negative)', '\\bbad_alloc\\b', '\\bmalloc\\b.{0,40}\\breturn(s|ed)? NULL\\b', '\\bcheck (the )?(size|length)\\b'],
    'O1': ["\\bwho (is|'s) (responsible|in charge)", '\\bwho (should|must|will|has to) (free|delete|release|own|deallocate|clean)', '\\bresponsib\\w+ (for|to) (free|delet|releas|clean)', '\\bcaller (must|should|is expected to|has to|needs to) (free|delete|release)', '\\b(callee|caller)\\b.{0,40}\\b(free|own)', '\\bownership\\b', '\\bwho owns\\b', '\\bowner\\b'],
    'O2': ['\\b(takes|take|taking|transfer\\w*|pass\\w*|hand\\w*) (over )?ownership', '\\bstd::move\\b', '\\b(unique_ptr|shared_ptr|smart pointer)s?\\b.{0,40}\\b(own|delete|free|manage)', "\\b(container|vector|list|map)\\b.{0,40}\\b(own|delete the pointers|free the elements|doesn'?t delete)", '\\brelease\\(\\)'],
    'D1': ["\\b(never|not|don'?t|didn'?t|doesn'?t|forgot to|forget to|missing) (call )?(free|delete|deallocat|releas)\\w*", '\\bno (corresponding|matching) (free|delete)', '\\bevery (malloc|new|allocation|calloc)\\b.{0,40}\\b(free|delete)', '\\b(need|have) to (call )?(free|delete)\\b', '\\bwhere (do|should) (i|we|you) (call )?(free|delete)'],
    'D2': ['\\b(incremented|advanced|moved|modified|changed|offset)\\b.{0,40}\\bpointer\\b.{0,40}\\bfree', '\\bfree\\b.{0,40}\\b(incremented|advanced|offset|middle|original pointer|start of)', '\\bpointer arithmetic\\b.{0,40}\\bfree', '\\b(keep|save|store) (a copy of )?the original pointer', '\\bsame (pointer|address|value) (that|as|returned)', '\\bbytes inside of\\b', 'not at (the )?(start|beginning)'],
    'D3': ['\\bdelete\\s*\\[\\s*\\]', '\\bdelete\\b.{0,30}\\b(instead of|vs\\.?|versus|or) (free|delete)', '\\bfree\\b.{0,30}\\b(instead of|vs\\.?|versus) delete', '\\bmismatch', '\\bmix(ing|ed)? (malloc|new|free|delete)', '\\b(malloc|calloc|strdup)\\b.{0,40}\\b(with|by) delete\\b', '\\bnew\\b.{0,40}\\b(with|by) free\\b', '\\b(matching|corresponding|appropriate|correct|right) (deallocat|free|release|delete)'],
    'D4': ['\\bdouble[- ]free', '\\b(already|twice|previously) freed', '\\bfreed (it )?twice', '\\buninitiali[sz]ed pointer', '\\bfree\\(\\s*NULL\\s*\\)', '\\bdangling\\b', '\\bset (it|the pointer|ptr) to NULL\\b', '\\bnot initiali[sz]ed\\b', '\\bgarbage (value|address)\\b', '\\buse[- ]after[- ]free\\b'],
    'C1': ['\\berror (path|handling|case|branch)', '\\bearly return', '\\breturn(s|ing)? (early|before)', '\\b(if|when) .{0,30}\\bfails?\\b.{0,40}\\b(free|leak)', '\\bexception\\w*\\b.{0,60}\\b(leak|free|delete|cleanup|destructor)', '\\b(leak|free|delete)\\w*\\b.{0,60}\\bexception', '\\b(goto|cleanup label|longjmp|exit\\(\\))', '\\ball (code )?paths', '\\bthrow(s|n)?\\b.{0,40}\\b(leak|delete)'],
    'C2': ['\\b(in|inside) (a|the|each|every) (loop|iteration)', '\\beach (iteration|time)\\b.{0,40}\\b(malloc|alloc|new|free)', '\\brealloc\\b.{0,60}\\b(fail|NULL|original|leak|same pointer|temp)', '\\bp\\s*=\\s*realloc\\s*\\(\\s*p', '\\b(repeatedly|every call|each call)\\b.{0,40}\\b(allocat|malloc|new)'],
    'L1': ['\\bbefore (the )?(program|process|application)? ?(exit|termination|ends|terminates|quits)', '\\b(at|on) (program |process )?exit\\b', '\\bOS (will )?(reclaim|free|clean)', '\\bwhen the (program|process) (exits|ends|terminates)', '\\bfree\\w* (memory )?(at|before) exit'],
    'L2': ["\\bdestructor\\w*\\b.{0,40}\\b(not |never |isn'?t |wasn'?t |called|invoked|run)", '\\bvirtual destructor', '\\bout of scope\\b', '\\bgoes out of scope', '\\blifetime\\b', '\\bRAII\\b', '\\bdelete this\\b'],
    'L3': ['\\b(memory|usage|RSS|heap)\\b.{0,30}\\b(keeps|keep|continues to|constantly|steadily) (grow|increas|rising)', '\\bgrow(s|ing)? (without bound|unbounded|indefinitely)', '\\bunbounded\\b', '\\b(cache|global|static) (map|vector|list|container|variable)s?\\b.{0,40}\\b(grow|retain|hold)', '\\bnever (shrinks|released back|returned to the OS)'],
    'E1': ['\\boverwr(ite|ote|itten|iting)\\b.{0,40}\\b(pointer|address|reference)', '\\b(pointer|address|reference)\\b.{0,40}\\boverwr', '\\blos(e|t|ing) (the |your |all )?(only |last )?(pointer|reference|address|handle)', '\\breassign\\w*\\b.{0,30}\\bpointer', '\\bno (longer )?(have|has) (a |any )?(pointer|reference)', '\\bno way to free', '\\bpoints? to (something|somewhere) else'],
    'E2': ['\\b(stored|store|saved|kept) (it |the pointer |the address )?(in|into) (a |the )?(global|struct|member|field|list|container|array|map|static)', '\\breturn(s|ed|ing)? (a |the )?pointer\\b.{0,40}\\b(caller|outside|function)', '\\bescape', '\\b(global|static) (pointer|variable)\\b.{0,40}\\b(free|leak|reachable)'],
    'E3': ['\\balias', '\\bshallow copy', '\\bcopy constructor', '\\bassignment operator', '\\brule of (three|five|zero)', '\\b(two|both|multiple) (pointers|objects|owners)\\b.{0,40}\\b(same|point)', '\\bcopies? (of )?the pointer'],
    'N1': ['\\b(each|every|all) (node|element|row|member|field|sub-?array|string)s?\\b.{0,40}\\b(free|delete)', '\\bfree\\w*\\b.{0,40}\\b(each|every|all) (node|element|row|member|field|string)', '\\b(nested|inner|member|child) (pointer|allocation|struct|array)s?\\b', '\\bfree\\w* the (struct|outer|parent|array of pointers)\\b.{0,40}\\b(first|before|after|members)', '\\b(linked list|2d array|array of pointers|double pointer|\\*\\*)\\b'],
    'N2': ['\\b(circular|cyclic) (reference|dependenc)', '\\breference cycle', '\\bweak_ptr\\b', '\\bref(erence)? ?count\\w*\\b', '\\bretain cycle'],
    'N3': ["\\b(destructor|cleanup|teardown|dispose|close|deinit|free_\\w+|_free|_destroy)\\b.{0,50}\\b(doesn'?t|does not|never|forgot|missing|should|must|also) (free|delete|release|clean)", '\\bincomplete cleanup', '\\bclean ?up (function|routine|code)\\b', '\\bdeinit'],
    'X1': ['\\b(dll|shared library|\\.so|module|crt|runtime)s?\\b.{0,40}\\b(heap|boundar|allocat|free)', '\\bdifferent (heap|crt|runtime|allocator)', '\\bacross (the )?(dll|module|library|ffi|language)', '\\b(ctypes|jni|ffi|cython|swig|p/invoke)\\b'],
    'T1': ['\\breproduc', '\\b(full|complete) (stack ?trace|backtrace|output|log)', '\\bbacktrace\\b', '\\bwhich version\\b', '\\bwhat version\\b', '\\bcompil(ed|e) (it )?with\\b', '\\b(minimal|complete|verifiable) (reproducible )?example\\b', '\\bmcve\\b', '\\bminimal reproducible\\b', '\\bcan you (post|share|provide|attach|try)\\b', '\\bbuild (flags|options)\\b'],
}

CWE_SIGNATURES: dict[str, list[str]] = {
    'CWE-762': ['mismatched free', 'alloc-dealloc-mismatch', 'mismatched-new-delete', '\\bdelete\\s*\\[\\s*\\]', '\\bmalloc\\b.{0,80}\\bdelete\\b', '\\bnew\\b.{0,60}\\bfree\\(', '\\bdifferent heap', '\\bacross (the )?dll'],
    'CWE-590': ['not malloc\\(\\)-ed', 'bad-free', '\\bfree\\w*\\b.{0,60}\\b(stack|local array|static array|string literal|global array|automatic)', '\\b(stack|string literal|static)\\b.{0,60}\\bfree\\(', '\\bdelete\\b.{0,40}\\bstack'],
    'CWE-761': ['bytes inside of', '\\b(increment|advanc|offset|pointer arithmetic)\\w*\\b.{0,80}\\bfree', '\\bfree\\w*\\b.{0,60}\\b(incremented|advanced|middle of|offset)'],
    'CWE-763': ['free\\(\\): invalid (pointer|size)', 'munmap_chunk', 'pointer being freed was not allocated', 'double free', '\\binvalid free\\b', '\\bfree\\w*\\b.{0,40}\\buninitiali', '\\bshould i free\\b', 'must not be freed', '\\bfree\\b.{0,40}\\b(getenv|setlocale|getpwuid|readdir|ctime|localtime|gmtime|strerror|basename)'],
    'CWE-789': ['allocation-size-too-big', 'exceeds maximum supported size', '\\bbad_alloc\\b', '\\b(huge|very large|too large|excessive) (allocation|malloc|memory)', '\\bmalloc\\b.{0,40}\\bnegative', '\\b(memory|usage)\\b.{0,30}\\bkeeps? (grow|increas)', '\\bout[- ]of[- ]memory\\b', '\\bmemory exhaustion'],
    'CWE-459': ['\\bindirect(ly)? (leak|lost)', '\\b(free|delete)\\w*\\b.{0,60}\\b(struct members|each node|linked list|2d array|members|nodes|array of pointers)', '\\bdestructor\\b', '\\bcircular reference|reference cycle|weak_ptr', '\\bcleanup\\b.{0,40}\\b(incomplete|missing|leak)'],
    'CWE-401': ['\\bmemory leak', '\\bleak(s|ed|ing)?\\b', 'definitely lost', 'LeakSanitizer', 'still reachable', 'possibly lost', '\\bnever freed\\b'],
}

_DQ_RX = {k: [re.compile(p, re.I) for p in v] for k, v in DQ_PATTERNS.items()}
_SIG_RX = {k: [re.compile(p, re.I) for p in v] for k, v in CWE_SIGNATURES.items()}


def dq_prefilter(sentence: str) -> list[str]:
    """Regex DQ candidates for a sentence (used only to select GitHub statements in the main pass)."""
    return [k for k, rx in _DQ_RX.items() if any(r.search(sentence) for r in rx)]


def cwe_signatures(text: str) -> list[str]:
    """Multi-label CWE signatures over title + body (sanitizer output included)."""
    return [k for k, rx in _SIG_RX.items() if any(r.search(text) for r in rx)]


# ---------------------------------------------------------------- Stack Overflow
SO_LANG_TAGS = {"c", "c++", "valgrind", "memory-leaks", "malloc", "free", "address-sanitizer",
                "dynamic-memory-allocation", "delete-operator", "new-operator", "c++11", "c++17", "c++14",
                "pointers", "memory-management", "leak-sanitizer", "heap-memory", "realloc", "smart-pointers",
                "destructor", "glibc"}
SO_ALLOC_HINT = re.compile(r"malloc|calloc|realloc|free|delete|\bnew\b|leak|valgrind|sanitizer|alloc", re.I)
SO_SPLIT = re.compile(r"(?<=[.?!])\s+(?=[A-Z(\"'`@])")
# memory-relatedness filter for interrogatives (main pass)
SO_MEM_MAIN = re.compile(r"free|malloc|alloc|delete|new\b|leak|pointer|memory|heap|stack|destructor|own|valgrind|"
                         r"sanitizer|asan|lsan|reachable|lost|release|realloc|smart|shared_ptr|unique_ptr|scope|"
                         r"lifetime|null|exit|size", re.I)
# off-CWE pass: broader memory filter, then a stricter leak-relevance filter
SO_MEM_OFF = re.compile(SO_MEM_MAIN.pattern + r"|close|handle|descriptor|thread|refcount|reference|DECREF|INCREF|GPU|cuda|texture", re.I)
SO_LEAK_OFF = re.compile(r"leak|free|delete|release|clos|lost|reachable|valgrind|sanitizer|asan|double|dangling|corrupt|"
                         r"own|destructor|exit|handle|descriptor|refcount|reference count|DECREF|INCREF|garbage|grow|"
                         r"fragment|RSS|pool|arena|deallocat|dispose|cleanup|clean up|join|detach", re.I)


def so_clean(body_html: str) -> str:
    """Strip code blocks and quoted tool output; keep inline code text."""
    h = re.sub(r"<pre.*?</pre>", " ", body_html or "", flags=re.S)
    h = re.sub(r"<blockquote.*?</blockquote>", " ", h, flags=re.S)
    h = re.sub(r"</(p|li|h\d)>", ". ", h)
    h = html.unescape(re.sub(r"<[^>]+>", " ", h))
    return re.sub(r"\s+", " ", h).strip()


def so_interrogatives(text: str, mem: re.Pattern[str]) -> list[str]:
    out = []
    for s in SO_SPLIT.split(text):
        s = s.strip(" .")
        if s.endswith("?") and mem.search(s) and 10 <= len(s) <= 450:
            out.append(s)
    return out


# ---------------------------------------------------------------- GitHub
GH_MEM_Q_MAIN = re.compile(SO_MEM_MAIN.pattern, re.I)
GH_MEM_Q_OFF = re.compile(r"free|alloc|leak|memory|close|handle|thread|ref|pointer|delete|release|own", re.I)
GH_KEY_OFF = re.compile(r"leak|never (freed|closed|released)|not (freed|closed|released)|double free|freed twice|"
                        r"use[- ]after[- ]free|dangling|refcount|reference count|DECREF|INCREF|grow|fragment|RSS|"
                        r"ownership|responsible|error path|destructor|cleanup|close\(|fclose|descriptor|handle|join|"
                        r"detach|corrupt|overflow|uninitiali|pool|arena|release", re.I)
_GH_SPLIT = re.compile(r"(?<=[.?!])\s+(?=[A-Z(\"'`])")


def gh_clean(md: str) -> str:
    """Markdown body -> prose: drop fenced/indented code, quotes, sanitizer frames, HTML comments."""
    t = md or ""
    t = re.sub(r"```[\s\S]*?```", " ", t)
    t = re.sub(r"(?m)^(\s{4}|\t).*$", " ", t)
    t = re.sub(r"(?m)^>.*$", " ", t)
    t = re.sub(r"(?m)^\s*(==\d+==|#\d+\s+0x|\s*at 0x|\s*by 0x).*$", " ", t)
    t = re.sub(r"<!--[\s\S]*?-->", " ", t)
    t = t.replace("\r", "")
    t = re.sub(r"\n{2,}", ". ", t)
    return re.sub(r"\s+", " ", t).strip()


def gh_sentences(md: str, lo: int, hi: int) -> list[str]:
    out = []
    for s in _GH_SPLIT.split(gh_clean(md)):
        s = re.sub(r"^[. ]+|[. ]+$", "", s.strip())
        if lo <= len(s) <= hi:
            out.append(s)
    return out
