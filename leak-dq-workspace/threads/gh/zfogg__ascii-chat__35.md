# 🧠 Implement Memory Pool Allocators for High-Performance Memory Management

- URL: https://github.com/zfogg/ascii-chat/issues/35
- Repo: zfogg/ascii-chat (language: C)
- State: open; created 2025-08-12T09:34:37Z; status ok; passes offcwe

## Issue body

reporter (OWNER) · zfogg · 2025-08-12T09:34:37Z · https://github.com/zfogg/ascii-chat/issues/35

## Problem
Current memory management relies on individual `malloc()`/`free()` calls through `SAFE_MALLOC()` macros, causing significant performance overhead:
- **Frequent allocations**: Packet data, frame buffers, audio samples allocated/freed continuously
- **Memory fragmentation**: Heap fragmentation after extended runtime reduces performance
- **Allocation overhead**: `malloc()` syscalls dominate CPU usage in high-throughput scenarios  
- **Cache misses**: Scattered allocations lead to poor memory locality
- **Lock contention**: System allocator locks serialize memory operations across threads

## Current Memory Usage Patterns

### High-Frequency Allocations:
```c
// From packet_queue.c - constant allocation churn
SAFE_MALLOC(node->data, len, char *);  // Every packet enqueue
// ... later ...
SAFE_FREE(node->data);                 // Every packet dequeue
```

### Frame Buffer Allocations:
```c
// From compression.c - temporary compression buffers  
SAFE_MALLOC(compressed_data, compressed_size, char *);
// Process frame...
free(compressed_data);  // Freed immediately after use
```

### Audio Sample Buffers:
```c
// From mixer.c - continuous audio buffer allocation
float *mix_buffer = malloc(AUDIO_FRAMES_PER_BUFFER * sizeof(float));
// Mix audio...
free(mix_buffer);  // Could be reused instead\!
```

## Proposed Solution: Custom Memory Pool Allocators

### 1. Fixed-Size Block Pools (Most Common Case)
**Use case**: Packet data, audio buffers, small temporary allocations

```c
typedef struct memory_pool {
    void *memory_start;          // Start of pre-allocated memory region
    size_t block_size;           // Fixed size per block
    size_t block_count;          // Total number of blocks
    _Atomic uint64_t free_mask;  // Bitset: 1=free, 0=allocated (lock-free\!)
    _Atomic size_t alloc_hint;   // Hint for next allocation (reduces scanning)
    pthread_mutex_t fallback_mutex; // Only for resize operations
    char padding[64];            // Cache line alignment
} memory_pool_t;

// Fast allocation (usually O(1), worst case O(64))
void* pool_alloc(memory_pool_t *pool) {
    uint64_t free_mask = atomic_load_acquire(&pool->free_mask);
    
    if (free_mask == 0) {
        return NULL; // Pool exhausted
    }
    
    // Find first free bit (often just 1-2 instructions with __builtin_ctzl)
    size_t block_idx = __builtin_ctzll(free_mask);
    uint64_t expected = free_mask;
    uint64_t desired = expected & ~(1ULL << block_idx);
    
    // Atomic compare-and-swap to claim the block
    if (atomic_compare_exchange_weak(&pool->free_mask, &expected, desired)) {
        return (char*)pool->memory_start + (block_idx * pool->block_size);
    }
    
    // Retry if another thread claimed this block first
    return pool_alloc(pool); // Tail recursion optimized to loop
}

// Fast deallocation (always O(1))
void pool_free(memory_pool_t *pool, void *ptr) {
    if (\!ptr) return;
    
    size_t offset = (char*)ptr - (char*)pool->memory_start;
    size_t block_idx = offset / pool->block_size;
    
    // Atomic bitwise OR to mark block as free
    atomic_fetch_or_release(&pool->free_mask, 1ULL << block_idx);
}
```

### 2. Size-Segregated Pools
**Use case**: Multiple allocation sizes with optimal memory usage

```c
typedef enum {
    POOL_TINY    = 0,  // 1-64 bytes (packet headers)
    POOL_SMALL   = 1,  // 65-512 bytes (small packets)  
    POOL_MEDIUM  = 2,  // 513-4096 bytes (audio buffers)
    POOL_LARGE   = 3,  // 4097-65536 bytes (video frames)
    POOL_HUGE    = 4,  // 65537+ bytes (compressed frames)
    POOL_COUNT   = 5
} pool_size_class_t;

typedef struct {
    memory_pool_t pools[POOL_COUNT];
    size_t size_thresholds[POOL_COUNT];
    _Atomic uint64_t stats[POOL_COUNT]; // Allocation counts per pool
} segregated_allocator_t;

// Smart allocation: pick optimal pool for size
void* smart_alloc(segregated_allocator_t *alloc, size_t size) {
    // Binary search or lookup table to find size class
    pool_size_class_t class = find_size_class(size);
    
    void *ptr = pool_alloc(&alloc->pools[class]);
    if (ptr) {
        atomic_fetch_add_relaxed(&alloc->stats[class], 1);
        return ptr;
    }
    
    // Pool exhausted - try next size class or fallback to malloc
    return fallback_alloc(alloc, size, class);
}
```

### 3. Thread-Local Storage Pools  
**Use case**: Eliminate inter-thread contention entirely

```c
typedef struct {
    memory_pool_t local_pool;    // Thread-private pool
    segregated_allocator_t *global; // Fallback to shared pools
    _Atomic size_t allocated_bytes;  // For memory usage tracking
} thread_local_allocator_t;

// Thread-local allocation (zero contention)
__thread thread_local_allocator_t *tls_allocator = NULL;

void* tls_alloc(size_t size) {
    if (\!tls_allocator) {
        tls_allocator = init_thread_allocator();
    }
    
    // Try thread-local pool first (common case - very fast)
    void *ptr = pool_alloc(&tls_allocator->local_pool);
    if (ptr) {
        return ptr;
    }
    
    // Fallback to global pools if local pool exhausted  
    return smart_alloc(tls_allocator->global, size);
}
```

## Integration with Existing Code

### 1. Replace SAFE_MALLOC Macros
```c
// Current macro in common.h:
#define SAFE_MALLOC(ptr, size, type) \
    do { \
        (ptr) = malloc(size); \
        if (\!(ptr)) { \
            log_error("malloc failed"); \
            return; \
        } \
    } while (0)

// New pool-aware macro:
#define POOL_MALLOC(ptr, size, type, pool_hint) \
    do { \
        (ptr) = pool_malloc(size, pool_hint); \
        if (\!(ptr)) { \
            log_error("pool allocation failed"); \
            return; \
        } \
    } while (0)

#define POOL_FREE(ptr, pool_hint) pool_free_smart(ptr, pool_hint)
```

### 2. Smart Pool Selection
```c
typedef enum {
    POOL_HINT_PACKET,     // Short-lived packet data
    POOL_HINT_FRAME,      // Video/audio frame buffers  
    POOL_HINT_TEMP,       // Temporary compression buffers
    POOL_HINT_PERSISTENT  // Long-lived data (client info, etc.)
} pool_hint_t;

// Automatic pool selection based on usage pattern
void* pool_malloc(size_t size, pool_hint_t hint) {
    switch (hint) {
        case POOL_HINT_PACKET:
            return packet_pool_alloc(size);    // High-frequency, small sizes
        case POOL_HINT_FRAME: 
            return frame_pool_alloc(size);     // Medium-frequency, large sizes
        case POOL_HINT_TEMP:
            return temp_pool_alloc(size);      // Very high-frequency, reusable
        case POOL_HINT_PERSISTENT:
            return malloc(size);               // Rare allocations, use system malloc
    }
}
```

## Expected Performance Improvements

### Allocation Speed:
- **Pool allocation**: ~10-50 CPU cycles (bitset + pointer arithmetic)
- **System malloc**: ~200-1000 CPU cycles (kernel syscalls, lock contention)
- **Speedup**: 5-20x faster allocation/deallocation

### Memory Locality:
- **Current**: Random heap addresses, poor cache utilization
- **With pools**: Contiguous memory blocks, excellent cache locality
- **Cache miss reduction**: 50-80% fewer L2/L3 cache misses

### Fragmentation Elimination:
- **Current**: Heap fragmentation reduces available memory over time
- **With pools**: Zero fragmentation (fixed-size blocks)
- **Memory efficiency**: 90-95% utilization vs 60-80% with fragmented heap

### Thread Scalability:
- **Current**: All threads contend for system allocator locks
- **With pools**: Thread-local pools eliminate contention
- **Scalability**: Linear performance with thread count

## Implementation Plan

### Phase 1: Core Pool Infrastructure
- [ ] Implement basic fixed-size memory pool with bitset free tracking
- [ ] Add atomic operations for lock-free allocation/deallocation
- [ ] Create size-segregated allocator with multiple pools
- [ ] Implement pool initialization and cleanup functions

### Phase 2: Integration Layer  
- [ ] Create pool-aware versions of SAFE_MALLOC/SAFE_FREE macros
- [ ] Add pool hint system for automatic pool selection
- [ ] Implement smart allocation with fallback to malloc
- [ ] Add memory usage tracking and statistics

### Phase 3: Thread-Local Optimization
- [ ] Implement thread-local storage pools  
- [ ] Add pool replenishment from global pools when local pools empty
- [ ] Optimize for common allocation patterns in audio/video threads
- [ ] Add pool rebalancing based on usage patterns

### Phase 4: Advanced Features
- [ ] Implement pool resizing for dynamic workloads
- [ ] Add memory pressure detection and pool shrinking
- [ ] Implement cross-platform memory alignment (SIMD, cache lines)
- [ ] Add debugging/profiling hooks for memory usage analysis

## Memory Layout Optimization

### Cache-Aligned Pools:
```c
// Align allocations to cache lines for SIMD and performance
#define CACHE_LINE_SIZE 64
#define SIMD_ALIGNMENT 32

void* pool_alloc_aligned(memory_pool_t *pool, size_t alignment) {
    void *ptr = pool_alloc(pool);
    
    // Check if already aligned
    if (((uintptr_t)ptr & (alignment - 1)) == 0) {
        return ptr;
    }
    
    // Return aligned pointer within the block
    uintptr_t aligned = (((uintptr_t)ptr + alignment - 1) & ~(alignment - 1));
    return (void*)aligned;
}
```

### NUMA-Aware Allocation:
```c
// On NUMA systems, allocate pools local to CPU cores
void init_numa_pools() {
    int numa_nodes = numa_num_configured_nodes();
    
    for (int node = 0; node < numa_nodes; node++) {
        void *memory = numa_alloc_onnode(POOL_SIZE, node);
        init_pool_on_memory(&numa_pools[node], memory, POOL_SIZE);
    }
}
```

## Testing and Validation

### Correctness Testing:
- [ ] Single-threaded allocation/deallocation verification
- [ ] Multi-threaded stress testing with Thread Sanitizer
- [ ] Double-free detection (should be impossible with bitset)
- [ ] Use-after-free detection with pool boundary checking

### Performance Benchmarking:
- [ ] Allocation speed comparison: pools vs malloc
- [ ] Memory usage efficiency measurements  
- [ ] Cache performance analysis (perf/Instruments)
- [ ] Real-world workload performance (audio/video streaming)

### Memory Usage Analysis:
- [ ] Pool utilization monitoring (detect over/under-provisioning)
- [ ] Fragmentation measurement and elimination verification
- [ ] Peak memory usage tracking during heavy load
- [ ] Memory leak detection (pools should never leak)

## Files to Modify
- `common.h` - Replace SAFE_MALLOC with pool-aware macros
- `lib/memory_pool.c/h` - New memory pool implementation
- `lib/packet_queue.c` - Use packet pools for node allocation
- `lib/compression.c` - Use temporary pools for compression buffers
- `lib/mixer.c` - Use audio pools for mixing buffers
- `src/server.c` - Initialize global pools at startup
- `Makefile` - Add memory pool compilation

## References
- [jemalloc](https://github.com/jemalloc/jemalloc) - Production memory allocator
- [TCMalloc](https://google.github.io/tcmalloc/) - Google's thread-caching malloc
- [Hoard Allocator](https://github.com/emeryberger/Hoard) - Scalable memory allocator
- [Intel TBB Memory Allocator](https://software.intel.com/content/www/us/en/develop/documentation/tbb-documentation/)

This improvement would eliminate one of the most significant performance bottlenecks in high-throughput applications: memory allocation overhead. Combined with lock-free data structures, it would provide the foundation for massive scalability improvements.
