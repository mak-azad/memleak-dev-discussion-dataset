# Memory grows without limit

- URL: https://github.com/facebook/rocksdb/issues/4112
- Repo: facebook/rocksdb (language: C++)
- State: closed; created 2018-07-11T15:13:14Z; status ok; passes offcwe

## Issue body

reporter (NONE) · toktarev · 2018-07-11T15:13:14Z · https://github.com/facebook/rocksdb/issues/4112

> Note: Please use Issues only for bug reports. For questions, discussions, feature requests, etc. post to dev group: https://www.facebook.com/groups/rocksdb.dev

### Expected behavior

Process consumes about 10 megabytes

### Actual behavior

Memory grows without limit

### Steps to reproduce the behavior

Run this code:

https://pastebin.com/Ch8RhsSB

Sorry RocksDB team, but it is huge problem.

This is trivial test and I expect it will work as finite state machine
Populate memory - flush - re-use memory.

I see like memory grows.




## Comment 404207092

reporter (NONE) · toktarev · 2018-07-11T15:16:03Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-404207092

BTW: Block cache is totally disabled

## Comment 404207235

reporter (NONE) · toktarev · 2018-07-11T15:16:24Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-404207235

> #include \<thread\>
> #include \<cstdio\>
> #include \<string\>
> #include \<iostream\>
> #include \<cinttypes\>
> #include "rocksdb/db.h"
> #include <db/memtable.h>
> #include "memtablefactory.h"
> #include <memtable/inlineskiplist.h>
>  
> using namespace std;
> using namespace rocksdb;
> using namespace std::chrono;
>  
> std::string kDBPath = \"\/repos\/rocksdata\";
>  
> template\<typename T\>
> T swap_endian(T u) \{
>     static_assert(CHAR_BIT == 8, \"CHAR_BIT != 8\");
>     union \{
>         T u;
>         unsigned char u8[sizeof(T)];
>     \} source, dest;
>  
>     source.u = u;
>  
>     for (size_t k = 0; k < sizeof(T); k++)
>         dest.u8[k] = source.u8[sizeof(T) - k - 1];
>  
>     return dest.u;
> \}
>  
> rocksdb::TableFactory *makeDictionaryTableFactory() {
>     auto block_opts = rocksdb::BlockBasedTableOptions{};
>     block_opts.checksum = ChecksumType::kCRC32c;
>     block_opts.no_block_cache = true;
>     return rocksdb::NewBlockBasedTableFactory(block_opts);
> }
>  
> int main() {
>     system("rm -rf /repos/rocksdata/*");
>  
>     DB *db;
>     Options options;
>     // Optimize RocksDB. This is the easiest way to get RocksDB to perform well
>     //options.IncreaseParallelism();
>     //options.OptimizeLevelStyleCompaction();
>     // create the DB if it's not already present
>  
>     options.create_if_missing = true;
>     options.db_write_buffer_size = 10 * 1024 * 1024;
>     options.compression = CompressionType::kNoCompression;
>     options.statistics = rocksdb::CreateDBStatistics();
>     options.write_buffer_size = 10 * 1024 * 1024;
>  
>     // open DB
>     Status s = DB::Open(options, kDBPath, &db);
>  
>     if (!s.ok()) {
>         std::cout << s.ToString();
>     }
>  
>     assert(s.ok());
>  
>     ColumnFamilyOptions cf_options{};
>     cf_options.table_factory.reset(makeDictionaryTableFactory());
>     cf_options.prefix_extractor.reset(rocksdb::NewNoopTransform());
>     cf_options.memtable_prefix_bloom_size_ratio = 0;
>     cf_options.write_buffer_size = 10 * 1024 * 1024;
>  
>     std::string name("Name");
>     ColumnFamilyHandle *cf;
>     Status status = db->CreateColumnFamily(cf_options, name, &cf);
>  
>     assert(s.ok());
>  
>     u_int64_t *buffer = new u_int64_t[4];
>     char *pointer = reinterpret_cast<char *>(buffer);
>     WriteBatch writeBatch{};
>     u_int64_t max = 10000000;
>  
>     Slice key(pointer, 32);
>     Slice value(reinterpret_cast<char *>(&max), 8);
>  
>     uint64_t begin = (uint64_t) std::chrono::duration_cast<std::chrono::nanoseconds>(
>             system_clock::now().time_since_epoch()).count();
>  
>     for (u_int64_t i = 0; i < 10000000000; i++) {
>         *(buffer) = swap_endian(i);
>         *(buffer + 1) = i + 1;
>         *(buffer + 2) = i + 2;
>         *(buffer + 3) = i + 3;
>  
>         writeBatch.Put(cf, key, value);
>  
>         if (i % 1000 == 0) {
>             Status s1 = db->Write(WriteOptions(), &writeBatch);
>             assert(s1.ok());
>             writeBatch.Clear();
>         }
>  
>         if (i % 1000000 == 0) {
>             uint64_t end = (uint64_t) std::chrono::duration_cast<std::chrono::nanoseconds>(
>                     system_clock::now().time_since_epoch()).count();
>             double time = (end - begin) / 1000000000;
>             double delta = i / time;
>             std::cout << "Speed=" << std::to_string(delta) << "\n\n";
>         }
>     }
>  
>     db->DestroyColumnFamilyHandle(cf);
>     delete db;
>     return 0;
> }

## Comment 404225221

reporter (NONE) · toktarev · 2018-07-11T16:07:41Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-404225221

Allocator tracker shows memory leak in:

rocksdb::BlockFetcher::ReadBlockContents

+0x00	pushq               %rbp
+0x01	movq                %rsp, %rbp
+0x04	pushq               %r15
+0x06	pushq               %r14
+0x08	pushq               %r13
+0x0a	pushq               %r12
+0x0c	pushq               %rbx
+0x0d	subq                $392, %rsp
+0x14	movq                %rsi, %rbx
+0x17	movq                %rdi, %r14
+0x1a	movq                160(%rbx), %rax
+0x21	movq                8(%rax), %rax
+0x25	movq                %rax, 248(%rbx)
+0x2c	movq                %rbx, %rdi
+0x2f	callq               "rocksdb::BlockFetcher::TryGetUncompressBlockFromPersistentCache()"
+0x34	testb               %al, %al
+0x36	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x46"
+0x38	vpxor               %xmm0, %xmm0, %xmm0
+0x3c	vmovdqu             %xmm0, (%r14)
+0x41	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x841"
+0x46	movq                8(%rbx), %rdi
+0x4a	testq               %rdi, %rdi
+0x4d	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0xaa"
+0x4f	movq                160(%rbx), %rax
+0x56	movq                (%rax), %rsi
+0x59	movq                8(%rax), %rdx
+0x5d	addq                $5, %rdx
+0x61	leaq                224(%rbx), %rcx
+0x68	callq               "rocksdb::FilePrefetchBuffer::TryReadFromCache(unsigned long long, unsigned long, rocksdb::Slice*) const"
+0x6d	testb               %al, %al
+0x6f	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0xaa"
+0x71	movq                160(%rbx), %rax
+0x78	movq                8(%rax), %rax
+0x7c	movq                %rax, 248(%rbx)
+0x83	movq                %rbx, %rdi
+0x86	callq               "rocksdb::BlockFetcher::CheckBlockChecksum()"
+0x8b	movl                208(%rbx), %eax
+0x91	testl               %eax, %eax
+0x93	jne                 "rocksdb::BlockFetcher::ReadBlockContents()+0xc1"
+0x95	movb                $1, 5264(%rbx)
+0x9c	movq                224(%rbx), %rax
+0xa3	movq                %rax, 240(%rbx)
+0xaa	cmpb                $0, 5264(%rbx)
+0xb1	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0xea"
+0xb3	movl                208(%rbx), %eax
+0xb9	testl               %eax, %eax
+0xbb	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x67f"
+0xc1	movl                %eax, (%r14)
+0xc4	movl                212(%rbx), %eax
+0xca	movl                %eax, 4(%r14)
+0xce	movq                216(%rbx), %rdi
+0xd5	xorl                %eax, %eax
+0xd7	testq               %rdi, %rdi
+0xda	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0xe1"
+0xdc	callq               "rocksdb::Status::CopyState(char const*)"
+0xe1	    movq                %rax, 8(%r14)
+0xe5	    jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x841"
+0xea	    movq                %rbx, %rdi
+0xed	    callq               "rocksdb::BlockFetcher::TryGetCompressedBlockFromPersistentCache()"
+0xf2	    testb               %al, %al
+0xf4	    jne                 "rocksdb::BlockFetcher::ReadBlockContents()+0x67f"
+0xfa	    movq                248(%rbx), %rdi
+0x101	    addq                $5, %rdi
+0x105	    cmpb                $0, 184(%rbx)
+0x10c	    je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x120"
+0x10e	    cmpq                $4999, %rdi
+0x115	    ja                  "rocksdb::BlockFetcher::ReadBlockContents()+0x120"
+0x117	    leaq                264(%rbx), %rax
+0x11e	    jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x144"
+0x120	    callq               "DYLD-STUB$$operator new[](unsigned long)"
+0x125	    movq                256(%rbx), %rdi
+0x12c	    movq                %rax, 256(%rbx)
+0x133	    testq               %rdi, %rdi
+0x136	    je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x144"
+0x138	    callq               "DYLD-STUB$$operator delete[](void*)"
+0x13d	    movq                256(%rbx), %rax
+0x144	    movq                %rax, 240(%rbx)
+0x14b	    leaq                1138286(%rip), %rdi
+0x152	    callq               *(%rdi)
+0x154	    movzbl              (%rax), %eax
+0x157	    movb                $1, %r12b
+0x15a	    cmpl                $3, %eax
+0x15d	    ja                  "rocksdb::BlockFetcher::ReadBlockContents()+0x171"
+0x15f	    movzbl              %al, %eax
+0x162	    cmpl                $2, %eax
+0x165	    seta                %r12b
+0x169	    xorl                %r15d, %r15d
+0x16c	    cmpl                $3, %eax
+0x16f	    jb                  "rocksdb::BlockFetcher::ReadBlockContents()+0x179"
+0x171	    callq               "rocksdb::Env::Default()"
+0x176	    movq                %rax, %r15
+0x179	    xorl                %eax, %eax
+0x17b	    testb               %r12b, %r12b
+0x17e	    je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x18f"
+0x180	    movq                (%r15), %rax
+0x183	    movq                248(%rax), %rax
+0x18a	    movq                %r15, %rdi
+0x18d	    callq               *%rax
+0x18f	    movq                %rax, -424(%rbp)
+0x196	    movq                (%rbx), %rsi
+0x199	    movq                160(%rbx), %rax
+0x1a0	    movq                (%rax), %rdx
+0x1a3	    movq                248(%rbx), %rcx
+0x1aa	    addq                $5, %rcx
+0x1ae	    leaq                224(%rbx), %r8
+0x1b5	    movq                240(%rbx), %r9
+0x1bc	    leaq                -56(%rbp), %r13
+0x1c0	    movq                %r13, %rdi
+0x1c3	    callq               "rocksdb::RandomAccessFileReader::Read(unsigned long long, unsigned long, rocksdb::Slice*, char*) const"
+0x1c8	    leaq                208(%rbx), %r12
+0x1cf	    cmpq                %r13, %r12
+0x1d2	    je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x223"
+0x1d4	    movq                -56(%rbp), %rax
+0x1d8	    movl                %eax, 208(%rbx)
+0x1de	    movl                $0, -56(%rbp)
+0x1e5	    shrq                $32, %rax
+0x1e9	    movl                %eax, 212(%rbx)
+0x1ef	    movl                $0, -52(%rbp)
+0x1f6	    movq                216(%rbx), %rdi
+0x1fd	    testq               %rdi, %rdi
+0x200	    movq                -424(%rbp), %r13
+0x207	    je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x20e"
+0x209	    callq               "DYLD-STUB$$operator delete[](void*)"
+0x20e	    movq                -48(%rbp), %rax
+0x212	    movq                %rax, 216(%rbx)
+0x219	    movq                $0, -48(%rbp)
+0x221	    jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x238"
+0x223	    movq                -48(%rbp), %rdi
+0x227	    testq               %rdi, %rdi
+0x22a	    movq                -424(%rbp), %r13
+0x231	    je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x238"
+0x233	    callq               "DYLD-STUB$$operator delete[](void*)"
+0x238	    testq               %r13, %r13
+0x23b	    je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x25f"
+0x23d	    movq                (%r15), %rax
+0x240	    movq                248(%rax), %rax
+0x247	    movq                %r15, %rdi
+0x24a	    callq               *%rax
+0x24c	    movq                %rax, %r15
+0x24f	    subq                %r13, %r15
+0x252	    leaq                1137999(%rip), %rdi
+0x259	    callq               *(%rdi)
+0x25b	    addq                %r15, 32(%rax)
+0x25f	    leaq                1138010(%rip), %rdi
+0x266	    callq               *(%rdi)
+0x268	    movzbl              (%rax), %eax
+0x26b	    cmpl                $1, %eax
+0x26e	    jbe                 "rocksdb::BlockFetcher::ReadBlockContents()+0x2a1"
+0x270	    movq                248(%rbx), %r15
+0x277	    addq                $5, %r15
+0x27b	    leaq                1137958(%rip), %rdi
+0x282	    callq               *(%rdi)
+0x284	    movl                $1, %ecx
+0x289	    vmovq               %rcx, %xmm0
+0x28e	    vmovq               %r15, %xmm1
+0x293	    vpunpcklqdq         %xmm1, %xmm0, %xmm0
+0x297	    vpaddq              16(%rax), %xmm0, %xmm0
+0x29c	    vmovdqu             %xmm0, 16(%rax)
+0x2a1	    movl                (%r12), %eax
+0x2a5	    testl               %eax, %eax
+0x2a7	    je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x2d2"
+0x2a9	    movl                %eax, (%r14)
+0x2ac	    movl                212(%rbx), %eax
+0x2b2	    movl                %eax, 4(%r14)
+0x2b6	    movq                216(%rbx), %rdi
+0x2bd	    xorl                %eax, %eax
+0x2bf	    testq               %rdi, %rdi
+0x2c2	    je                  "rocksdb::BlockFetcher::ReadBlockContents()+0xe1"
+0x2c8	callq               "rocksdb::Status::CopyState(char const*)"
+0x2cd	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0xe1"
+0x2d2	movq                248(%rbx), %rax
+0x2d9	addq                $5, %rax
+0x2dd	cmpq                %rax, 232(%rbx)
+0x2e4	jne                 "rocksdb::BlockFetcher::ReadBlockContents()+0x323"
+0x2e6	movq                %rbx, %rdi
+0x2e9	callq               "rocksdb::BlockFetcher::CheckBlockChecksum()"
+0x2ee	movl                (%r12), %eax
+0x2f2	testl               %eax, %eax
+0x2f4	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x637"
+0x2fa	movl                %eax, (%r14)
+0x2fd	movl                212(%rbx), %eax
+0x303	movl                %eax, 4(%r14)
+0x307	movq                216(%rbx), %rdi
+0x30e	xorl                %eax, %eax
+0x310	testq               %rdi, %rdi
+0x313	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0xe1"
+0x319	callq               "rocksdb::Status::CopyState(char const*)"
+0x31e	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0xe1"
+0x323	movq                (%rbx), %rsi
+0x326	addq                $8, %rsi
+0x32a	leaq                -312(%rbp), %rdi
+0x331	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::basic_string(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)"
+0x336	leaq                1004900(%rip), %rdx
+0x33d	leaq                -312(%rbp), %rdi
+0x344	xorl                %esi, %esi
+0x346	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::insert(unsigned long, char const*)"
+0x34b	movq                16(%rax), %rcx
+0x34f	movq                %rcx, -272(%rbp)
+0x356	vmovdqu             (%rax), %xmm0
+0x35a	vmovdqa             %xmm0, -288(%rbp)
+0x362	vpxor               %xmm0, %xmm0, %xmm0
+0x366	vmovdqu             %xmm0, (%rax)
+0x36a	movq                $0, 16(%rax)
+0x372	leaq                1004639(%rip), %rsi
+0x379	leaq                -288(%rbp), %rdi
+0x380	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::append(char const*)"
+0x385	movq                16(%rax), %rcx
+0x389	movq                %rcx, -240(%rbp)
+0x390	vmovdqu             (%rax), %xmm0
+0x394	vmovdqa             %xmm0, -256(%rbp)
+0x39c	vpxor               %xmm0, %xmm0, %xmm0
+0x3a0	vmovdqu             %xmm0, (%rax)
+0x3a4	movq                $0, 16(%rax)
+0x3ac	movq                160(%rbx), %rax
+0x3b3	movq                (%rax), %rsi
+0x3b6	leaq                -336(%rbp), %rdi
+0x3bd	callq               "DYLD-STUB$$std::__1::to_string(unsigned long long)"
+0x3c2	movzbl              -336(%rbp), %edx
+0x3c9	testb               $1, %dl
+0x3cc	jne                 "rocksdb::BlockFetcher::ReadBlockContents()+0x3da"
+0x3ce	leaq                -335(%rbp), %rsi
+0x3d5	shrq                %rdx
+0x3d8	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x3e8"
+0x3da	movq                -328(%rbp), %rdx
+0x3e1	movq                -320(%rbp), %rsi
+0x3e8	leaq                -256(%rbp), %rdi
+0x3ef	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::append(char const*, unsigned long)"
+0x3f4	movq                16(%rax), %rcx
+0x3f8	movq                %rcx, -208(%rbp)
+0x3ff	vmovdqu             (%rax), %xmm0
+0x403	vmovdqa             %xmm0, -224(%rbp)
+0x40b	vpxor               %xmm0, %xmm0, %xmm0
+0x40f	vmovdqu             %xmm0, (%rax)
+0x413	movq                $0, 16(%rax)
+0x41b	leaq                1004698(%rip), %rsi
+0x422	leaq                -224(%rbp), %rdi
+0x429	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::append(char const*)"
+0x42e	movq                16(%rax), %rcx
+0x432	movq                %rcx, -176(%rbp)
+0x439	vmovdqu             (%rax), %xmm0
+0x43d	vmovdqa             %xmm0, -192(%rbp)
+0x445	vpxor               %xmm0, %xmm0, %xmm0
+0x449	vmovdqu             %xmm0, (%rax)
+0x44d	movq                $0, 16(%rax)
+0x455	movq                248(%rbx), %rsi
+0x45c	addq                $5, %rsi
+0x460	leaq                -360(%rbp), %rdi
+0x467	callq               "DYLD-STUB$$std::__1::to_string(unsigned long)"
+0x46c	movzbl              -360(%rbp), %edx
+0x473	testb               $1, %dl
+0x476	jne                 "rocksdb::BlockFetcher::ReadBlockContents()+0x484"
+0x478	leaq                -359(%rbp), %rsi
+0x47f	shrq                %rdx
+0x482	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x492"
+0x484	movq                -352(%rbp), %rdx
+0x48b	movq                -344(%rbp), %rsi
+0x492	leaq                -192(%rbp), %rdi
+0x499	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::append(char const*, unsigned long)"
+0x49e	movq                16(%rax), %rcx
+0x4a2	movq                %rcx, -144(%rbp)
+0x4a9	vmovdqu             (%rax), %xmm0
+0x4ad	vmovdqa             %xmm0, -160(%rbp)
+0x4b5	vpxor               %xmm0, %xmm0, %xmm0
+0x4b9	vmovdqu             %xmm0, (%rax)
+0x4bd	movq                $0, 16(%rax)
+0x4c5	leaq                1004540(%rip), %rsi
+0x4cc	leaq                -160(%rbp), %rdi
+0x4d3	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::append(char const*)"
+0x4d8	movq                16(%rax), %rcx
+0x4dc	movq                %rcx, -112(%rbp)
+0x4e0	vmovdqu             (%rax), %xmm0
+0x4e4	vmovdqa             %xmm0, -128(%rbp)
+0x4e9	vpxor               %xmm0, %xmm0, %xmm0
+0x4ed	vmovdqu             %xmm0, (%rax)
+0x4f1	movq                $0, 16(%rax)
+0x4f9	movq                232(%rbx), %rsi
+0x500	leaq                -384(%rbp), %rdi
+0x507	callq               "DYLD-STUB$$std::__1::to_string(unsigned long)"
+0x50c	movzbl              -384(%rbp), %edx
+0x513	testb               $1, %dl
+0x516	jne                 "rocksdb::BlockFetcher::ReadBlockContents()+0x524"
+0x518	leaq                -383(%rbp), %rsi
+0x51f	shrq                %rdx
+0x522	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x532"
+0x524	movq                -376(%rbp), %rdx
+0x52b	movq                -368(%rbp), %rsi
+0x532	leaq                -128(%rbp), %rdi
+0x536	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::append(char const*, unsigned long)"
+0x53b	movq                16(%rax), %rcx
+0x53f	movq                %rcx, -80(%rbp)
+0x543	vmovdqu             (%rax), %xmm0
+0x547	vmovdqa             %xmm0, -96(%rbp)
+0x54c	vpxor               %xmm0, %xmm0, %xmm0
+0x550	vmovdqu             %xmm0, (%rax)
+0x554	movq                $0, 16(%rax)
+0x55c	movzbl              -96(%rbp), %eax
+0x560	testb               $1, %al
+0x562	jne                 "rocksdb::BlockFetcher::ReadBlockContents()+0x571"
+0x564	leaq                -95(%rbp), %rcx
+0x568	movq                %rcx, -72(%rbp)
+0x56c	shrq                %rax
+0x56f	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x57d"
+0x571	movq                -80(%rbp), %rax
+0x575	movq                %rax, -72(%rbp)
+0x579	movq                -88(%rbp), %rax
+0x57d	movq                %rax, -64(%rbp)
+0x581	leaq                977072(%rip), %rax
+0x588	movq                %rax, -400(%rbp)
+0x58f	movq                $0, -392(%rbp)
+0x59a	leaq                -72(%rbp), %rcx
+0x59e	leaq                -400(%rbp), %r8
+0x5a5	movl                $2, %esi
+0x5aa	xorl                %edx, %edx
+0x5ac	movq                %r14, %rdi
+0x5af	callq               "rocksdb::Status::Status(rocksdb::Status::Code, rocksdb::Status::SubCode, rocksdb::Slice const&, rocksdb::Slice const&)"
+0x5b4	leaq                -96(%rbp), %rdi
+0x5b8	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x5bd	leaq                -384(%rbp), %rdi
+0x5c4	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x5c9	leaq                -128(%rbp), %rdi
+0x5cd	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x5d2	leaq                -160(%rbp), %rdi
+0x5d9	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x5de	leaq                -360(%rbp), %rdi
+0x5e5	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x5ea	leaq                -192(%rbp), %rdi
+0x5f1	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x5f6	leaq                -224(%rbp), %rdi
+0x5fd	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x602	leaq                -336(%rbp), %rdi
+0x609	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x60e	leaq                -256(%rbp), %rdi
+0x615	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x61a	leaq                -288(%rbp), %rdi
+0x621	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x626	leaq                -312(%rbp), %rdi
+0x62d	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x632	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x841"
+0x637	cmpb                $0, 77(%rbx)
+0x63b	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x67f"
+0x63d	movq                200(%rbx), %rax
+0x644	movq                8(%rax), %rdi
+0x648	testq               %rdi, %rdi
+0x64b	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x67f"
+0x64d	movq                (%rdi), %rax
+0x650	movq                32(%rax), %rax
+0x654	callq               *%rax
+0x656	testb               %al, %al
+0x658	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x67f"
+0x65a	movq                160(%rbx), %rsi
+0x661	movq                200(%rbx), %rdi
+0x668	movq                240(%rbx), %rdx
+0x66f	movq                248(%rbx), %rcx
+0x676	addq                $5, %rcx
+0x67a	callq               "rocksdb::PersistentCacheHelper::InsertRawPage(rocksdb::PersistentCacheOptions const&, rocksdb::BlockHandle const&, char const*, unsigned long)"
+0x67f	leaq                1136954(%rip), %rdi
+0x686	callq               *(%rdi)
+0x688	movzbl              (%rax), %eax
+0x68b	movb                $1, %r13b
+0x68e	cmpl                $3, %eax
+0x691	ja                  "rocksdb::BlockFetcher::ReadBlockContents()+0x6a5"
+0x693	movzbl              %al, %eax
+0x696	cmpl                $2, %eax
+0x699	seta                %r13b
+0x69d	xorl                %r15d, %r15d
+0x6a0	cmpl                $3, %eax
+0x6a3	jb                  "rocksdb::BlockFetcher::ReadBlockContents()+0x6ad"
+0x6a5	callq               "rocksdb::Env::Default()"
+0x6aa	movq                %rax, %r15
+0x6ad	xorl                %r12d, %r12d
+0x6b0	testb               %r13b, %r13b
+0x6b3	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x6c7"
+0x6b5	movq                (%r15), %rax
+0x6b8	movq                248(%rax), %rax
+0x6bf	movq                %r15, %rdi
+0x6c2	callq               *%rax
+0x6c4	movq                %rax, %r12
+0x6c7	movq                224(%rbx), %rsi
+0x6ce	movq                248(%rbx), %rdx
+0x6d5	movb                (%rsi,%rdx), %al
+0x6d8	movb                %al, 5265(%rbx)
+0x6de	testb               %al, %al
+0x6e0	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x786"
+0x6e6	movb                184(%rbx), %al
+0x6ec	testb               %al, %al
+0x6ee	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x786"
+0x6f4	movq                16(%rbx), %rax
+0x6f8	movq                168(%rbx), %rcx
+0x6ff	movl                (%rax), %r8d
+0x702	movq                192(%rbx), %r9
+0x709	movq                176(%rbx), %rax
+0x710	movq                %rax, (%rsp)
+0x714	leaq                -416(%rbp), %r13
+0x71b	movq                %r13, %rdi
+0x71e	callq               "rocksdb::UncompressBlockContents(char const*, unsigned long, rocksdb::BlockContents*, unsigned int, rocksdb::Slice const&, rocksdb::ImmutableCFOptions const&)"
+0x723	leaq                208(%rbx), %rax
+0x72a	cmpq                %r13, %rax
+0x72d	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x790"
+0x72f	movq                -416(%rbp), %rax
+0x736	movl                %eax, 208(%rbx)
+0x73c	movl                $0, -416(%rbp)
+0x746	shrq                $32, %rax
+0x74a	movl                %eax, 212(%rbx)
+0x750	movl                $0, -412(%rbp)
+0x75a	movq                216(%rbx), %rdi
+0x761	testq               %rdi, %rdi
+0x764	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x76b"
+0x766	callq               "DYLD-STUB$$operator delete[](void*)"
+0x76b	movq                -408(%rbp), %rax
+0x772	movq                %rax, 216(%rbx)
+0x779	movq                $0, -408(%rbp)
+0x784	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x7a1"
+0x786	movq                %rbx, %rdi
+0x789	callq               "rocksdb::BlockFetcher::GetBlockContents()"
+0x78e	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x7a1"
+0x790	movq                -408(%rbp), %rdi
+0x797	testq               %rdi, %rdi
+0x79a	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x7a1"
+0x79c	callq               "DYLD-STUB$$operator delete[](void*)"
+0x7a1	cmpl                $0, 208(%rbx)
+0x7a8	jne                 "rocksdb::BlockFetcher::ReadBlockContents()+0x7f0"
+0x7aa	cmpb                $0, 5264(%rbx)
+0x7b1	jne                 "rocksdb::BlockFetcher::ReadBlockContents()+0x7f0"
+0x7b3	cmpb                $0, 77(%rbx)
+0x7b7	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x7f0"
+0x7b9	movq                200(%rbx), %rax
+0x7c0	movq                8(%rax), %rdi
+0x7c4	testq               %rdi, %rdi
+0x7c7	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x7f0"
+0x7c9	movq                (%rdi), %rax
+0x7cc	movq                32(%rax), %rax
+0x7d0	callq               *%rax
+0x7d2	testb               %al, %al
+0x7d4	jne                 "rocksdb::BlockFetcher::ReadBlockContents()+0x7f0"
+0x7d6	movq                200(%rbx), %rdi
+0x7dd	movq                160(%rbx), %rsi
+0x7e4	movq                168(%rbx), %rdx
+0x7eb	callq               "rocksdb::PersistentCacheHelper::InsertUncompressedPage(rocksdb::PersistentCacheOptions const&, rocksdb::BlockHandle const&, rocksdb::BlockContents const&)"
+0x7f0	movl                208(%rbx), %eax
+0x7f6	movl                %eax, (%r14)
+0x7f9	movl                212(%rbx), %eax
+0x7ff	movl                %eax, 4(%r14)
+0x803	movq                216(%rbx), %rdi
+0x80a	xorl                %eax, %eax
+0x80c	testq               %rdi, %rdi
+0x80f	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x816"
+0x811	callq               "rocksdb::Status::CopyState(char const*)"
+0x816	movq                %rax, 8(%r14)
+0x81a	testq               %r12, %r12
+0x81d	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x841"
+0x81f	movq                (%r15), %rax
+0x822	movq                248(%rax), %rax
+0x829	movq                %r15, %rdi
+0x82c	callq               *%rax
+0x82e	movq                %rax, %rbx
+0x831	subq                %r12, %rbx
+0x834	leaq                1136493(%rip), %rdi
+0x83b	callq               *(%rdi)
+0x83d	addq                %rbx, 48(%rax)
+0x841	movq                %r14, %rax
+0x844	addq                $392, %rsp
+0x84b	popq                %rbx
+0x84c	popq                %r12
+0x84e	popq                %r13
+0x850	popq                %r14
+0x852	popq                %r15
+0x854	popq                %rbp
+0x855	retq
+0x856	movq                %rax, %r13
+0x859	testq               %r12, %r12
+0x85c	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x8da"
+0x85e	movq                (%r15), %rax
+0x861	movq                248(%rax), %rax
+0x868	movq                %r15, %rdi
+0x86b	callq               *%rax
+0x86d	movq                %rax, %rbx
+0x870	subq                %r12, %rbx
+0x873	leaq                1136430(%rip), %rdi
+0x87a	callq               *(%rdi)
+0x87c	addq                %rbx, 48(%rax)
+0x880	movq                %r13, %rdi
+0x883	callq               "DYLD-STUB$$_Unwind_Resume"
+0x888	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x8d7"
+0x88a	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x8d7"
+0x88c	movq                %rax, %rdi
+0x88f	callq               "__clang_call_terminate"
+0x894	movq                %rax, %r13
+0x897	cmpq                $0, -424(%rbp)
+0x89f	je                  "rocksdb::BlockFetcher::ReadBlockContents()+0x8da"
+0x8a1	movq                (%r15), %rax
+0x8a4	movq                248(%rax), %rax
+0x8ab	movq                %r15, %rdi
+0x8ae	callq               *%rax
+0x8b0	movq                %rax, %r14
+0x8b3	subq                -424(%rbp), %r14
+0x8ba	leaq                1136359(%rip), %rdi
+0x8c1	callq               *(%rdi)
+0x8c3	addq                %r14, 32(%rax)
+0x8c7	movq                %r13, %rdi
+0x8ca	callq               "DYLD-STUB$$_Unwind_Resume"
+0x8cf	movq                %rax, %rdi
+0x8d2	callq               "__clang_call_terminate"
+0x8d7	movq                %rax, %r13
+0x8da	movq                %r13, %rdi
+0x8dd	callq               "DYLD-STUB$$_Unwind_Resume"
+0x8e2	movq                %rax, %rdi
+0x8e5	callq               "__clang_call_terminate"
+0x8ea	movq                %rax, %rdi
+0x8ed	callq               "__clang_call_terminate"
+0x8f2	movq                %rax, %r13
+0x8f5	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x9a2"
+0x8fa	movq                %rax, %r13
+0x8fd	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x996"
+0x902	movq                %rax, %r13
+0x905	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x98a"
+0x90a	movq                %rax, %r13
+0x90d	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x97e"
+0x90f	movq                %rax, %r13
+0x912	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x972"
+0x914	movq                %rax, %r13
+0x917	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x966"
+0x919	movq                %rax, %r13
+0x91c	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x95a"
+0x91e	movq                %rax, %r13
+0x921	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x94e"
+0x923	movq                %rax, %r13
+0x926	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x945"
+0x928	movq                %rax, %r13
+0x92b	jmp                 "rocksdb::BlockFetcher::ReadBlockContents()+0x939"
+0x92d	movq                %rax, %r13
+0x930	leaq                -96(%rbp), %rdi
+0x934	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x939	leaq                -384(%rbp), %rdi
+0x940	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x945	leaq                -128(%rbp), %rdi
+0x949	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x94e	leaq                -160(%rbp), %rdi
+0x955	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x95a	leaq                -360(%rbp), %rdi
+0x961	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x966	leaq                -192(%rbp), %rdi
+0x96d	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x972	leaq                -224(%rbp), %rdi
+0x979	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x97e	leaq                -336(%rbp), %rdi
+0x985	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x98a	leaq                -256(%rbp), %rdi
+0x991	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x996	leaq                -288(%rbp), %rdi
+0x99d	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x9a2	leaq                -312(%rbp), %rdi
+0x9a9	callq               "DYLD-STUB$$std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::~basic_string()"
+0x9ae	movq                %r13, %rdi
+0x9b1	callq               "DYLD-STUB$$_Unwind_Resume"

## Comment 404339714

other (CONTRIBUTOR) · siying · 2018-07-11T23:17:09Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-404339714

Can you paste the full call stack of the allocation?

## Comment 404401913

reporter (NONE) · toktarev · 2018-07-12T06:18:25Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-404401913

No, this is all information I have.

I am trying to find allocation in code as well.

## Comment 404824773

reporter (NONE) · toktarev · 2018-07-13T12:53:08Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-404824773

```
void BlockFetcher::GetBlockContents() {
  if (slice_.data() != used_buf_) {
    // the slice content is not the buffer provided
    *contents_ = BlockContents(Slice(slice_.data(), block_size_), false,
                               compression_type);
  } else {
    // page is uncompressed, the buffer either stack or heap provided
    if (got_from_prefetch_buffer_ || used_buf_ == &stack_buf_[0]) {
      heap_buf_ = std::unique_ptr<char[]>(new char[block_size_]);   <------- This is a leak
      memcpy(heap_buf_.get(), used_buf_, block_size_);
    }
    *contents_ = BlockContents(std::move(heap_buf_), block_size_, true,
                               compression_type);
  }
}

```

## Comment 404911498

reporter (NONE) · toktarev · 2018-07-13T18:11:57Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-404911498

I’ve found the reason of leak 

this is not exactly a leak
but a lot of memory is allocated
but not released
const int table_cache_size = (mutable_db_options_.max_open_files == -1)
                                 ? TableCache::kInfiniteCapacity
                                 : mutable_db_options_.max_open_files - 10;
table_cache_ = NewLRUCache(table_cache_size,
                           immutable_db_options_.table_cache_numshardbits);
all allocated records are stored in this cache
mutable_db_options_.max_open_files is equal 1
so table_cache_size= 4 mb

I set size of the cache to zero
no more memory grows
they store TableReader into this cache
TableReader keeps object Block
Block stores 350K of char *
due to all they are in cache Block is not released
and Rocks just writes new data to cache and allocate new blocks

## Comment 405277144

other (CONTRIBUTOR) · koldat · 2018-07-16T15:00:34Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-405277144

Hi @siying . I am having exactly same issue. It is serious one. Cache is simply growing. Callstack using jemalloc See attachment:

![out1250](https://user-images.githubusercontent.com/16866502/42765746-fc734be0-8918-11e8-9678-8b729f4a2e19.png)

![leak](https://user-images.githubusercontent.com/16866502/42766007-9ca7fc28-8919-11e8-8445-95a2cec91e1c.png)

My configuration is:
```
2018/07/16-08:57:30.518138 7fa622ed4700            table_factory options:   flush_block_policy_factory: FlushBlockBySizePolicyFactory (0x7fa61f618b58)
  cache_index_and_filter_blocks: 0
  cache_index_and_filter_blocks_with_high_priority: 0
  pin_l0_filter_and_index_blocks_in_cache: 0
  index_type: 0
  hash_index_allow_collision: 1
  checksum: 1
  no_block_cache: 0
  block_cache: 0x7fa5f9b21ce0
  block_cache_name: LRUCache
  block_cache_options:
    capacity : 268435456
    num_shard_bits : 4
    strict_capacity_limit : 0
    high_pri_pool_ratio: 0.000
  block_cache_compressed: (nil)
  persistent_cache: (nil)
  block_size: 4096
  block_size_deviation: 10
  block_restart_interval: 16
  index_block_restart_interval: 1
  metadata_block_size: 4096
  partition_filters: 0
  use_delta_encoding: 1
  filter_policy: nullptr
  whole_key_filtering: 1
  verify_compression: 0
  read_amp_bytes_per_bit: 0
  format_version: 2
  enable_index_compression: 1
```


Is there some workaround without need to disable cache?

## Comment 405282439

other (CONTRIBUTOR) · koldat · 2018-07-16T15:16:36Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-405282439

There is this bugfix message:
5.14.1 (6/20/2018)
Fix block-based table reader pinning blocks throughout its lifetime, causing memory usage increase.

Is it related to this issue? I was not able to find any change related to block table between 5.14.0 and 5.14.1. What changeset fixes this bug?

## Comment 405292663

reporter (NONE) · toktarev · 2018-07-16T15:46:50Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-405292663

Executed the same benchmark on the latest RocksDB version
git checkout tags/v5.14.2 -b b14.

Still see memory grows

Bytes Used	Count		Symbol Name
 188.32 MB      67.8%	36907	 	    rocksdb::ThreadPoolImpl::Impl::BGThreadWrapper(void*)
 188.32 MB      67.8%	36900	 	     rocksdb::ThreadPoolImpl::Impl::BGThread(unsigned long)
 188.15 MB      67.7%	34992	 	      rocksdb::DBImpl::BackgroundCallFlush()
 188.13 MB      67.7%	34876	 	       rocksdb::DBImpl::BackgroundFlush(bool*, rocksdb::JobContext*, rocksdb::LogBuffer*)
 188.13 MB      67.7%	34876	 	        rocksdb::DBImpl::FlushMemTableToOutputFile(rocksdb::ColumnFamilyData*, rocksdb::MutableCFOptions const&, bool*, rocksdb::JobContext*, rocksdb::LogBuffer*)
 188.11 MB      67.7%	34865	 	         rocksdb::FlushJob::Run(rocksdb::LogsWithPrepTracker*, rocksdb::FileMetaData*)
 187.99 MB      67.7%	34818	 	          rocksdb::FlushJob::WriteLevel0Table()
 187.99 MB      67.7%	34815	 	           rocksdb::BuildTable(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, rocksdb::Env*, rocksdb::ImmutableCFOptions const&, rocksdb::MutableCFOptions const&, rocksdb::EnvOptions const&, rocksdb::TableCache*, rocksdb::InternalIterator*, std::__1::unique_ptr<rocksdb::InternalIterator, std::__1::default_delete<rocksdb::InternalIterator> >, rocksdb::FileMetaData*, rocksdb::InternalKeyComparator const&, std::__1::vector<std::__1::unique_ptr<rocksdb::IntTblPropCollectorFactory, std::__1::default_delete<rocksdb::IntTblPropCollectorFactory> >, std::__1::allocator<std::__1::unique_ptr<rocksdb::IntTblPropCollectorFactory, std::__1::default_delete<rocksdb::IntTblPropCollectorFactory> > > > const*, unsigned int, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::vector<unsigned long long, std::__1::allocator<unsigned long long> >, unsigned long long, rocksdb::SnapshotChecker*, rocksdb::CompressionType, rocksdb::CompressionOptions const&, bool, rocksdb::InternalStats*, rocksdb::TableFileCreationReason, rocksdb::EventLogger*, int, rocksdb::Env::IOPriority, rocksdb::TableProperties*, int, unsigned long long, unsigned long long, rocksdb::Env::WriteLifeTimeHint)
 187.99 MB      67.7%	34815	 	            rocksdb::TableCache::NewIterator(rocksdb::ReadOptions const&, rocksdb::EnvOptions const&, rocksdb::InternalKeyComparator const&, rocksdb::FileDescriptor const&, rocksdb::RangeDelAggregator*, rocksdb::TableReader**, rocksdb::HistogramImpl*, bool, rocksdb::Arena*, bool, int)
 187.99 MB      67.7%	34815	 	             rocksdb::TableCache::FindTable(rocksdb::EnvOptions const&, rocksdb::InternalKeyComparator const&, rocksdb::FileDescriptor const&, rocksdb::Cache::Handle**, bool, bool, rocksdb::HistogramImpl*, bool, int, bool)
 187.94 MB      67.6%	34182	 	              rocksdb::TableCache::GetTableReader(rocksdb::EnvOptions const&, rocksdb::InternalKeyComparator const&, rocksdb::FileDescriptor const&, bool, unsigned long, bool, rocksdb::HistogramImpl*, std::__1::unique_ptr<rocksdb::TableReader, std::__1::default_delete<rocksdb::TableReader> >*, bool, int, bool, bool)
 187.82 MB      67.6%	31650	 	               rocksdb::BlockBasedTableFactory::NewTableReader(rocksdb::TableReaderOptions const&, std::__1::unique_ptr<rocksdb::RandomAccessFileReader, std::__1::default_delete<rocksdb::RandomAccessFileReader> >&&, unsigned long long, std::__1::unique_ptr<rocksdb::TableReader, std::__1::default_delete<rocksdb::TableReader> >*, bool) const
 187.82 MB      67.6%	31650	 	                rocksdb::BlockBasedTable::Open(rocksdb::ImmutableCFOptions const&, rocksdb::EnvOptions const&, rocksdb::BlockBasedTableOptions const&, rocksdb::InternalKeyComparator const&, std::__1::unique_ptr<rocksdb::RandomAccessFileReader, std::__1::default_delete<rocksdb::RandomAccessFileReader> >&&, unsigned long long, std::__1::unique_ptr<rocksdb::TableReader, std::__1::default_delete<rocksdb::TableReader> >*, bool, bool, int)
 185.75 MB      66.8%	1899	 	                 rocksdb::BlockBasedTable::CreateIndexReader(rocksdb::FilePrefetchBuffer*, rocksdb::BlockBasedTable::IndexReader**, rocksdb::InternalIterator*, int)
 185.75 MB      66.8%	1899	 	                  rocksdb::BinarySearchIndexReader::Create(rocksdb::RandomAccessFileReader*, rocksdb::FilePrefetchBuffer*, rocksdb::Footer const&, rocksdb::BlockHandle const&, rocksdb::ImmutableCFOptions const&, rocksdb::InternalKeyComparator const*, rocksdb::BlockBasedTable::IndexReader**, rocksdb::PersistentCacheOptions const&)
 185.73 MB      66.8%	1266	 	                   rocksdb::(anonymous namespace)::ReadBlockFromFile(rocksdb::RandomAccessFileReader*, rocksdb::FilePrefetchBuffer*, rocksdb::Footer const&, rocksdb::ReadOptions const&, rocksdb::BlockHandle const&, std::__1::unique_ptr<rocksdb::Block, std::__1::default_delete<rocksdb::Block> >*, rocksdb::ImmutableCFOptions const&, bool, rocksdb::Slice const&, rocksdb::PersistentCacheOptions const&, unsigned long long, unsigned long)
 185.68 MB      66.8%	633	 	                    rocksdb::BlockFetcher::ReadBlockContents()
 185.68 MB      66.8%	633	 	                     operator new(unsigned long)


## Comment 405838249

other (CONTRIBUTOR) · koldat · 2018-07-18T07:34:07Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-405838249

My solution was to use recommendation here: https://github.com/facebook/rocksdb/wiki/Partitioned-Index-Filters (I have huge database and I require small memory footprint)

Table files are using cache driven by capacity of max_open_files. When I used big value it was growing in time a lot, because my index is around 5MB per file (and I had 5k files - 200MB each). When I used smaller value then query performance went down. Using two level index helps here, because direct impact in table cache is small and indices are cached in block cache that can be controlled. I have also increased block size which made my index even smaller.

@toktarev your test is not setting max_open_files thus it is infinite size (4M files). That is why it probably just grows. Try to set that max_open_files=50 (just for test). I guess it will stop growing after some time.

 


## Comment 405847024

reporter (NONE) · toktarev · 2018-07-18T08:08:54Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-405847024

@koldat it is clear that max_open_files reduces corresponding cache capacity.

But if I set it small and add `Get` operation to the benchmark I see considerable performance degradation after some time

## Comment 405852117

other (CONTRIBUTOR) · koldat · 2018-07-18T08:27:00Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-405852117

@toktarev sure you will see performance degradation. You have to choose how you want to achieve your result. In ideal case everything fits in memory for other cases you have to tune. What I am doing:

1. I try to keep my table files big, but not huge (not multiplying file size between levels).
2. I am always trying to time partition my data (prefix with time partition like day number)
3. I am deleting old data using delete files in range (because of 1 and 2 it works perfectly). Delete operation kills seek performance due to tomb stones.
4. Queries to partitioned data is hitting caches better (data are collocated).
5. I have started to use second level index. In case you have big number of files you will after some time end up in situation it will not fit in memory. Two level index helps here. And you can control index cache size.

Can you please do the test (max_open_file=50) and confirm that it is not memory leak? (Original issue)


## Comment 405853971

reporter (NONE) · toktarev · 2018-07-18T08:33:28Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-405853971

@koldat  sure I'll test it a bit latter (a bit busy right now).

I don't understand why RocksDB keeps file blocks in cache.
There is no big needs for this.

I'd like to ask them revise their memory management and free allocated memory in Blocks after each Flush or Read operation.

This is 360K cache blocks which just consumes memory for nothing.






## Comment 405859006

other (CONTRIBUTOR) · koldat · 2018-07-18T08:50:52Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-405859006

@toktarev It makes a lot of sense to keep it in memory. Let me describe it on example:

You are calling GET operation
1. It checks memtable. If it is there return.
2. It checks all L0 files in range for GET (see table get steps down). If it is there return.
3. It checks L1 files in range. If it is there return.
4. It checks L2 files in range. If it is there return.
5. etc.

Every table check for GET has to do this. Let me describe worst scenario (nothing opened and cached).
1. Open file and read index. Index describes (binary tree) of all blocks in file. If you will not have it in memory it will slow down every operation. That is the consumed memory. Sometimes index is big (5M), because more blocks make it bigger. If you will need to load it for every operation it will impact the performance.
2. It finds correct block. This block is cached and deserialized. Then it does local search in block for requested key.
3. Value is returned.

Now imagine you have to do this for all table files that are possibly hitting that key. It is a lot of operation you need to do.

Solution I used (two level index) seems brilliant (for my use case!). The difference is that it loads first level index into memory. But this guy is much smaller thus you can have much higher number of files opened. Second level (index partitions) are than using block cache using standard caching and eviction algorithms. That means if you have enough memory for caching it is used and fast. When you start to starve on memory, performance will go down.

RocksDB is mostly about tuning. There is not an ideal way how to use it. But if you are using that correctly, there cannot be anything faster. On the other hand, incorrect usage can make it really bad. Personally I do not see anything wrong in memory management after I started to understand what it does. In case the test will prove there is not a leak.

Anyway kudos to authors!


## Comment 405866543

reporter (NONE) · toktarev · 2018-07-18T09:16:35Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-405866543

There is no leak.
There is just memory consumption.
@koldat 
Thanks for explanation

But I still see at least 1 problem:

I can't use https://github.com/facebook/rocksdb/wiki/Partitioned-Index-Filters
for Hash-optimized MemTables (optimized for lookUp) at least I didn't find how to do it




## Comment 405970583

reporter (NONE) · toktarev · 2018-07-18T15:23:23Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-405970583

My custom application load huge number of data into RocksDB (about 70G)

After some time I see:

-rw-r--r-- 1 ubuntu ubuntu 118410341 Jul 18 15:19 000121.sst
-rw-r--r-- 1 ubuntu ubuntu 118412305 Jul 18 15:19 000122.sst
-rw-r--r-- 1 ubuntu ubuntu 118412022 Jul 18 15:19 000123.sst
-rw-r--r-- 1 ubuntu ubuntu 118410456 Jul 18 15:19 000124.sst
-rw-r--r-- 1 ubuntu ubuntu 118411486 Jul 18 15:19 000125.sst
-rw-r--r-- 1 ubuntu ubuntu 118413017 Jul 18 15:19 000126.sst
-rw-r--r-- 1 ubuntu ubuntu 118408698 Jul 18 15:19 000127.sst
-rw-r--r-- 1 ubuntu ubuntu 118413935 Jul 18 15:19 000128.sst
-rw-r--r-- 1 ubuntu ubuntu 118414146 Jul 18 15:20 000129.sst
-rw-r--r-- 1 ubuntu ubuntu 118412573 Jul 18 15:20 000130.sst
-rw-r--r-- 1 ubuntu ubuntu 118415362 Jul 18 15:20 000131.sst
-rw-r--r-- 1 ubuntu ubuntu 118410121 Jul 18 15:20 000132.sst
-rw-r--r-- 1 ubuntu ubuntu 118410383 Jul 18 15:20 000133.sst
-rw-r--r-- 1 ubuntu ubuntu 118414743 Jul 18 15:20 000134.sst
-rw-r--r-- 1 ubuntu ubuntu 118410111 Jul 18 15:20 000135.sst
-rw-r--r-- 1 ubuntu ubuntu  31155716 Jul 18 15:20 000136.sst
-rw-r--r-- 1 ubuntu ubuntu 133695647 Jul 18 15:20 000137.sst

And process consumes more that 70G of RAM.

Corresponding column family is optimized for lookUp and Partitioned Filters and Index doesn't work there.




## Comment 405971165

reporter (NONE) · toktarev · 2018-07-18T15:25:03Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-405971165

I see only 17 files and 70G of RAM consumed.

## Comment 405976966

other (CONTRIBUTOR) · koldat · 2018-07-18T15:41:35Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-405976966

It is hard to say. Anyway it looks strange, because listed files are around 2GB size in total. That means compression generates files 35 times smaller (strange). It also strangely correlates with your data size. Are you sure that you do not have issue (memory leak) in your application?

## Comment 406766749

other (CONTRIBUTOR) · yuslepukhin · 2018-07-21T03:14:58Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-406766749

Our profiling indicates there is a huge leak accumulating within a couple of days with a process growing up to 60 GB a day. The process usually recycles. I am seeing multiple stacks that has a common theme of a BlockFetcher and trying to insert the block into cache etc. The below happens during Get()/MultiGet(), at the end of compaction etc. The first below stack is the most prolific raking many Gbs.My suspicion it may have something to do with the recent LRU cache changes though not sure. Does not happen in 5.6.1

	ntdll!RtlpAllocateHeap+1DE9 (d:\rs1\minkernel\ntos\rtl\heap.c, 6734)
	ntdll!RtlpAllocateHeapInternal+727 (d:\rs1\minkernel\ntos\rtl\heap.c, 2021)
	ucrtbase!_malloc_base+36 (d:\rs1\minkernel\crts\ucrt\src\appcrt\heap\malloc_base.cpp, 34)
	RocksDBStore!operator new+31 (f:\dd\vctools\crt\vcstartup\src\heap\new_scalar.cpp, 19)
	RocksDBStore!rocksdb::ZSTD_Uncompress+65 (d:\vsts\agent_1\_work\1\s\util\compression.h, 1044)
	RocksDBStore!rocksdb::UncompressBlockContentsForCompressionType+27D (d:\vsts\agent_1\_work\1\s\table\format.cc, 354)
	RocksDBStore!rocksdb::UncompressBlockContents+3B (d:\vsts\agent_1\_work\1\s\table\format.cc, 390)
	RocksDBStore!rocksdb::BlockFetcher::ReadBlockContents+552 (d:\vsts\agent_1\_work\1\s\table\block_fetcher.cc, 230)
	RocksDBStore!rocksdb::`anonymous namespace'::ReadBlockFromFile+12D (d:\vsts\agent_1\_work\1\s\table\block_based_table_reader.cc, 87)
	RocksDBStore!rocksdb::BlockBasedTable::MaybeLoadDataBlockToCache+3A9 (d:\vsts\agent_1\_work\1\s\table\block_based_table_reader.cc, 1748)
	RocksDBStore!rocksdb::BlockBasedTable::NewDataBlockIterator<rocksdb::DataBlockIter>+19D (d:\vsts\agent_1\_work\1\s\table\block_based_table_reader.cc, 1624)
	RocksDBStore!rocksdb::BlockBasedTableIterator<rocksdb::DataBlockIter>::InitDataBlock+2DE (d:\vsts\agent_1\_work\1\s\table\block_based_table_reader.cc, 2103)
	RocksDBStore!rocksdb::BlockBasedTableIterator<rocksdb::DataBlockIter>::FindKeyForward+D8 (d:\vsts\agent_1\_work\1\s\table\block_based_table_reader.cc, 2125)

	ntdll!RtlpAllocateHeap+1DE9 (d:\rs1\minkernel\ntos\rtl\heap.c, 6734)
	ntdll!RtlpAllocateHeapInternal+727 (d:\rs1\minkernel\ntos\rtl\heap.c, 2021)
	ucrtbase!_malloc_base+36 (d:\rs1\minkernel\crts\ucrt\src\appcrt\heap\malloc_base.cpp, 34)
	RocksDBStore!operator new+31 (f:\dd\vctools\crt\vcstartup\src\heap\new_scalar.cpp, 19)
	RocksDBStore!rocksdb::BlockFetcher::GetBlockContents+A4 (d:\vsts\agent_1\_work\1\s\table\block_fetcher.cc, 172)
	RocksDBStore!rocksdb::BlockFetcher::ReadBlockContents+5CA (d:\vsts\agent_1\_work\1\s\table\block_fetcher.cc, 237)
	RocksDBStore!rocksdb::`anonymous namespace'::ReadBlockFromFile+12D (d:\vsts\agent_1\_work\1\s\table\block_based_table_reader.cc, 87)
	RocksDBStore!rocksdb::BlockBasedTable::MaybeLoadDataBlockToCache+3A9 (d:\vsts\agent_1\_work\1\s\table\block_based_table_reader.cc, 1748)
	RocksDBStore!rocksdb::BlockBasedTable::NewDataBlockIterator<rocksdb::DataBlockIter>+19D (d:\vsts\agent_1\_work\1\s\table\block_based_table_reader.cc, 1624)
	RocksDBStore!rocksdb::BlockBasedTableIterator<rocksdb::DataBlockIter>::InitDataBlock+2DE (d:\vsts\agent_1\_work\1\s\table\block_based_table_reader.cc, 2103)
	RocksDBStore!rocksdb::BlockBasedTableIterator<rocksdb::DataBlockIter>::FindKeyForward+D8 (d:\vsts\agent_1\_work\1\s\table\block_based_table_reader.cc, 2125)

## Comment 407142689

other (CONTRIBUTOR) · yuslepukhin · 2018-07-23T17:45:57Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407142689

@siying @ajkr This is real. There is something going on with cached blocks.

## Comment 407146068

other (CONTRIBUTOR) · siying · 2018-07-23T17:56:14Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407146068

@koldat which release or commit are you running on while seeing the leak?
@yuslepukhin same question 

CC @maysamyabandeh . One the the previous heap profile shows the partitioned index took most of the memory.

## Comment 407147881

other (CONTRIBUTOR) · siying · 2018-07-23T18:01:53Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407147881

@yuslepukhin Get()/MultiGet() is not supposed to go this path. Maybe it's the compaction path? Can you paste the whole stack so that we can figure out where it is from?

## Comment 407149501

other (CONTRIBUTOR) · yuslepukhin · 2018-07-23T18:07:09Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407149501

@siying Thanks for responding. 
The commit I am using is de98fd88e3b9e4ac5c8114aada07635256d9e3ae, however, the leak shows up in earlier commits such as 1f32dc7d2b6721a1fe13eb515d52e5cd6f110f59

There are multiple stacks that show in my profiling. Let me gather the top and I will post it here.

@maysamyabandeh Partitioned index also caught my attention.

## Comment 407159529

other (CONTRIBUTOR) · yuslepukhin · 2018-07-23T18:40:01Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407159529

This covers practically all of it.

[TopStacksPosted.txt](https://github.com/facebook/rocksdb/files/2220613/TopStacksPosted.txt)


## Comment 407160251

reporter (NONE) · toktarev · 2018-07-23T18:42:29Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407160251

I confirm

	RocksDBStore!rocksdb::UncompressBlockContentsForCompressionType+27D (d:\vsts\agent_1\_work\1\s\table\format.cc, 354)
	RocksDBStore!rocksdb::UncompressBlockContents+3B (d:\vsts\agent_1\_work\1\s\table\format.cc, 390)
	RocksDBStore!rocksdb::BlockFetcher::ReadBlockContents+552 (d:\vsts\agent_1\_work\1\s\table\block_fetcher.cc, 230)

This causes a lot of allocations and problems

## Comment 407161636

other (CONTRIBUTOR) · koldat · 2018-07-23T18:47:04Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407161636

I am using 5.12. branch with our JNI modifications. I can say that two level index maybe "hide" the leak, because grow of memory is not noticeable (so I thought it was incorrect usage). Most of memory was taken from compaction and seek and seekPrev (see picture). Seek is hitting that ReadBlockContents as well as compaction.

I guess that maybe index cache does not evict indices for files that are deleted.

## Comment 407162094

reporter (NONE) · toktarev · 2018-07-23T18:48:32Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407162094

We switched all column families on two level index.

We still observe memory grows on intensive read operations.

## Comment 407209746

other (CONTRIBUTOR) · siying · 2018-07-23T21:38:51Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407209746

@koldat what's your block cache size? Data blocks from a deleted file are not necessarily being deleted immediately. Eventually they will be evicted based on LRU. If your actual block cache usage is larger than capacity, then it's a problem. Otherwise, it is still expected.

## Comment 407211199

other (CONTRIBUTOR) · siying · 2018-07-23T21:44:52Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407211199

For those who run on C++ or you can get block cache size using another way, what's your reading of Cache::GetCapacity(), Cache::GetUsage() and Cache::GetPinnedUsage() reading?

## Comment 407239941

other (CONTRIBUTOR) · yuslepukhin · 2018-07-24T00:19:10Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407239941

@siying We only use uncompressed cache and graph GetUsage() on it which is fairly flat and it shows as configured value times the partitions on a box. I do not have immediate access to GetPinnedUsage().

## Comment 407240175

other (CONTRIBUTOR) · yuslepukhin · 2018-07-24T00:20:56Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407240175

@siying There are indications that leak existed in 5.6.1

## Comment 407708388

other (CONTRIBUTOR) · koldat · 2018-07-25T10:24:12Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407708388

I was trying to simulate issue using @toktarev source code. When I set properly max_open_files then it works fine. Even if I use block cache. Pinned/Usage/Capacity of block cache and of table_cache is moving in configured limits only.

@yuslepukhin can you please send us your options? I am wondering if you have unlimited max_open files or something like that.

## Comment 407708902

reporter (NONE) · toktarev · 2018-07-25T10:26:17Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407708902

@koldat it works fine because my test doesn't use `Get`.

Using `Get` I see performance slowdown.

## Comment 407709565

other (CONTRIBUTOR) · koldat · 2018-07-25T10:29:05Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407709565

@toktarev I have tried even random Gets, DeleteFilesInRange, compactions, etc. and everything work as expected. Please let's not discuss "performance" in this issue. This issue is only about memory.

## Comment 407710184

reporter (NONE) · toktarev · 2018-07-25T10:31:51Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407710184

Which max_open_files  value did you set ?

I set the same in my custom application.

Everything just hunged, so I had to return max_open_files back.

## Comment 407710507

other (CONTRIBUTOR) · koldat · 2018-07-25T10:33:13Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407710507

  options.max_open_files = 500;


## Comment 407711097

reporter (NONE) · toktarev · 2018-07-25T10:35:53Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407711097

I set it to 10 in my application, probably it would work better for 500.

Anyway we have some limit after our application just hungs.
It is not a problem of performance (faster slower) it is a problem of application's work.

If it hungs - it is huge problem if memory allocation is normal.



## Comment 407712712

other (CONTRIBUTOR) · koldat · 2018-07-25T10:42:51Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407712712

If you set 10 then it is a problem. My tuning options (I do not know your app so it does not need to work perfectly):
target_file_size_base=128M
target_file_size_multiplier=1
compression=LZ4
write_buffer_size=128M
max_open_files=1024
index_type=twoLevel
blockSize=16k
If you need use one level index then I would go for:
max_open_files=128
blockSize=16k or 32k

Anyway, let's finish memory leak here, please. It is much more important problem.

## Comment 407713854

reporter (NONE) · toktarev · 2018-07-25T10:48:23Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407713854

Both problems are important.

Configuration for benchmark or business case is not a problem's resolution.

I suspect that in some conditions you will see the same "application hungs" even with your configuration settings. Probably it happens when number of sst files become greater than max_open_files and `Get` operations should read directly from file omiting  block cache.

I don't have any objections agains finish with memory leak, I am not an obstacle for this.

But this is my ticket and I created it for my problem.






## Comment 407844584

other (CONTRIBUTOR) · yuslepukhin · 2018-07-25T18:05:31Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407844584

@koldat We currently do not limit the number of files opened as it worked well in all cases. In all, except may be the most recent one. I will quickly try limiting it.

## Comment 407845168

other (CONTRIBUTOR) · siying · 2018-07-25T18:07:32Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407845168

Based on the discussion, the leakage only happens if options.max_open_files=-1?

## Comment 407845599

reporter (NONE) · toktarev · 2018-07-25T18:09:01Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407845599

if options.max_open_files=-1 a lot of memory is allocated but it is not a memory leak

At least in my test

## Comment 407847569

other (CONTRIBUTOR) · yuslepukhin · 2018-07-25T18:15:43Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407847569

@siying It is not certain for now. I am gathering more details as to what kind of compaction style is being used in that bed and how many files are in partitions.

## Comment 407848013

other (CONTRIBUTOR) · koldat · 2018-07-25T18:17:13Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407848013

@toktarev it is documented feature. -1 instructs Rocksdb to cache all table indices up to 4 milion files. If you do not want that you should set a limit.

@siying yes. At least I did not reproduced after configuration change. Let’s wait for @yuslepukhin test. For me it happened when my data set started to grow much faster thus higher effect that I did not noticed before.


## Comment 407848611

reporter (NONE) · toktarev · 2018-07-25T18:19:23Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407848611

@koldat I set limit.

The question is - what should I configure also to prevent RocksDB working directly with disk during lookups ?

If it is impossible it is quite dangerous option and I understand why it is -1 by default


## Comment 407852335

other (CONTRIBUTOR) · yuslepukhin · 2018-07-25T18:31:43Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407852335

@siying @koldat the stacks indicate a potential issue with block cache and the size of it is limited by options which is shared by all tables. The max open file setting affects the table cache size. How is the two related?

## Comment 407854844

other (CONTRIBUTOR) · koldat · 2018-07-25T18:40:27Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407854844

@yuslepukhin table cache is counting open files (1 size per file) up to max open file and is for whole database. If you have big sst then index can be 10mb per file thus 100 files is 1gb. That is the problem. Block cache is size limited, but table cache count limited. Take a look in log file to see what is size of your indexes (index_size=xxxx).

When you use two level index then table cache is much smaller (one can use high max open files) and real index blocks are in block cache thus counts to size limit. I have found this as best for me, because I have exact control of my heap (I am docker constrained) which is must have. You can probably use much higher numbers.


## Comment 407855955

other (CONTRIBUTOR) · yuslepukhin · 2018-07-25T18:44:09Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407855955

@siying @koldat  kEstimateTableReadersMem property which we monitor is not big and relatively flat, I would assume that this includes the index.

## Comment 407870922

reporter (NONE) · toktarev · 2018-07-25T19:38:56Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407870922

@siying 

Could you please explain if max_open_files limit is a safe option ?

I am scared to set it less then port::GeMaxFiles().

May be other options can help to prevent system from very slow lookUps ?

I didn't find this explanation in RocksDB documentation.






## Comment 407902264

other (CONTRIBUTOR) · yuslepukhin · 2018-07-25T21:30:09Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407902264

@koldat here is a sample of table creation log entry. Not our typical load, experimental bed where the leak is acute:

EVENT_LOG_v1 {"time_micros": 1532203080080358, "cf_name": "ContentDataCG", "job": 140, "event": "table_file_creation", "file_number": 5127, "file_size": 268690599, "table_properties": {"data_size": 268643118, "index_size": 83051, "filter_size": 10565, "raw_key_size": 319656, "raw_average_key_size": 38, "raw_value_size": 1255453845, "raw_average_value_size": 149245, "num_data_blocks": 2677, "num_entries": 8412, "filter_policy_name": "rocksdb.BuiltinBloomFilter", "kDeletedKeys": "0", "kMergeOperands": "0"}}"


## Comment 407908156

other (CONTRIBUTOR) · koldat · 2018-07-25T21:50:57Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407908156

@yuslepukhin yours numbers are much smaller than mine (I have smaller entries thus much more entries -> bigger index).

I was looking in source and metric you are using should be reflecting table cache size. I am quite lost. I was going through all of stacks in this thread and I do not see any obvious leak. I am just user and do not know internals, but there is pointer/reference puzzle game in this area :) We can help community with divide and conquer. I would stick with initial plan and try to configure max_open_files even if counters are looking good. Until we will have better plan.... What is your size DB and file count?

## Comment 407908928

other (CONTRIBUTOR) · yuslepukhin · 2018-07-25T21:54:19Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407908928

Here is the results of the experiement.
We have limited the number of open files on the bed to 100 and we can see the immediate impact on the  kEstimateTableReadersMem value. So the TableReaders now take less memory. The issue is that neither the original value of  kEstimateTableReadersMem nor the reduced value really affect the overall picture. The reduction of 20MB (over the past 3 hours) does not make a dent on the multi-GB overall process memory increase.

## Comment 407909536

other (CONTRIBUTOR) · yuslepukhin · 2018-07-25T21:56:47Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407909536

@koldat Yes, the pointer/reference game is there

## Comment 407912477

other (CONTRIBUTOR) · koldat · 2018-07-25T22:08:10Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-407912477

Maybe this max open file is secondary issue (unlimited default configuration). And we were seeing different one under heavy load. I am for example using mostly iterators.
And maybe that two level index helped me, because it is using different block reader thus does not hit leak condition. Maybe....
My increase was quite slow (1gb a day) and I am ingesting like 1Tb of raw data per hour, reevaluating, recompressing with resuling dB increase of 20gb a day. Still with only 500mb block cache. After two days 1or 2 gb increase. After I started with two level increase is gone (do not know why now honestly). 


## Comment 408252524

other (CONTRIBUTOR) · yuslepukhin · 2018-07-26T22:18:54Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-408252524

Looks like we continue leaking with block_cache disabled.

## Comment 408314896

other (CONTRIBUTOR) · koldat · 2018-07-27T05:24:02Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-408314896

@yuslepukhin 
- Can you share your config section (first part of log file)? 
- Are you using jemalloc (conservative settings) so we do not need to consider fragmentation? 
- What is the speed of leak?
- Have you tried to dump heap after you close db? So we will know that it is leak or caches.

## Comment 409326620

reporter (NONE) · toktarev · 2018-07-31T18:43:43Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-409326620

any news ?

## Comment 409331149

other (CONTRIBUTOR) · yuslepukhin · 2018-07-31T18:59:02Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-409331149

I have disabled the cache and and the tracing picture is entirely different. At this point the issue that we are experiencing is evidently not related to what either of you have seen. For that reason I have not replied to @koldat as the findings is out of rocksdb library land.

## Comment 411918441

other (CONTRIBUTOR) · yuslepukhin · 2018-08-09T22:29:46Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-411918441

@toktarev I am still looking at it. 

## Comment 413636395

other (CONTRIBUTOR) · yuslepukhin · 2018-08-16T18:11:56Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-413636395

Here is the result of the investigation on my side. 
The scenario is using Tx databse which keeps a number of Memtables around in memory.
The number of the memtables kept around defaults to the max_write_buffer_number.
The scenario deals with big records and with the number of partitions on the machine the number of memtables memory usage grows beyond the physical memory installed.
I am done with with this issue.


## Comment 418892916

other (CONTRIBUTOR) · ajkr · 2018-09-05T21:49:39Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-418892916

@toktarev - you are correct that `OptimizeForPointLookup` sets hash index which is not compatible with partitioned index. Further, since you are not using `cache_index_and_filter_blocks`, we pin the whole indexes in-memory for open table readers. The hash table part of the index will be particularly huge -- since you're using `NoopTransform`, the hash table is going to have a separate entry for every single key-value pair in the SST. While this setup probably is optimal for point lookups, it sacrifices everything to achieve it, like memory consumption as you found. 

Additionally, I have found hash index only marginally improves read perf in a subset of use cases, despite its huge memory cost. I'd suggest first try setting `index_type = kBinarySearch` so there's no hash index that needs to be pinned in-memory. If that's not enough try setting `kTwoLevelIndexSearch`, which causes only the index root partition to be pinned in-memory.

## Comment 442484017

reporter (NONE) · toktarev · 2018-11-28T15:19:00Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-442484017

This stack allocates huge number of memory without limit and max_open_files = 20.

```rocksdb::BlockFetcher::GetBlockContents().  /src/rocksdb/table/block_fetcher.cc:164
rocksdb::BlockFetcher::ReadBlockContents() /src/rocksdb/table/block_fetcher.cc:225
ocksdb::BlockBasedTable::ReadFilter(rocksdb::FilePrefetchBuffer*, rocksdb::BlockHandle const&, bool) const /src/rocksdb/table/block_based_table_reader.cc:1228
rocksdb::BlockBasedTable::GetFilter(rocksdb::FilePrefetchBuffer*, rocksdb::BlockHandle const&, bool, bool, rocksdb::GetContext*) const /src/rocksdb/table/block_based_table_reader.cc:1328
rocksdb::PartitionedFilterBlockReader::CacheDependencies(bool) /src/rocksdb/table/partitioned_filter_block.cc:306
rocksdb::BlockBasedTable::Open(rocksdb::ImmutableCFOptions const&, rocksdb::EnvOptions const&, rocksdb::BlockBasedTableOptions const&, rocksdb::InternalKeyComparator const&, std::__1::unique_ptr<rocksdb::RandomAccessFileReader, std::__1::default_delete<rocksdb::RandomAccessFileReader> >&&, unsigned long long, std::__1::unique_ptr<rocksdb::TableReader, std::__1::default_delete<rocksdb::TableReader> >*, bool, bool, int) /src/rocksdb/table/block_based_table_reader.cc:879
rocksdb::BlockBasedTableFactory::NewTableReader(rocksdb::TableReaderOptions const&, std::__1::unique_ptr<rocksdb::RandomAccessFileReader, std::__1::default_delete<rocksdb::RandomAccessFileReader> >&&, unsigned long long, std::__1::unique_ptr<rocksdb::TableReader, std::__1::default_delete<rocksdb::TableReader> >*, bool) const /src/rocksdb/table/block_based_table_factory.cc:69
rocksdb::TableCache::GetTableReader(rocksdb::EnvOptions const&, rocksdb::InternalKeyComparator const&, rocksdb::FileDescriptor const&, bool, unsigned long, bool, rocksdb::HistogramImpl*, std::__1::unique_ptr<rocksdb::TableReader, std::__1::default_delete<rocksdb::TableReader> >*, bool, int, bool, bool) /src/rocksdb/db/table_cache.cc:113
rocksdb::TableCache::FindTable(rocksdb::EnvOptions const&, rocksdb::InternalKeyComparator const&, rocksdb::FileDescriptor const&, rocksdb::Cache::Handle**, bool, bool, rocksdb::HistogramImpl*, bool, int, bool) /src/rocksdb/db/table_cache.cc:150
rocksdb::TableCache::NewIterator(rocksdb::ReadOptions const&, rocksdb::EnvOptions const&, rocksdb::InternalKeyComparator const&, rocksdb::FileDescriptor const&, rocksdb::RangeDelAggregator*, rocksdb::TableReader**, rocksdb::HistogramImpl*, bool, rocksdb::Arena*, bool, int) /src/rocksdb/db/table_cache.cc:217
rocksdb::BuildTable(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, rocksdb::Env*, rocksdb::ImmutableCFOptions const&, rocksdb::MutableCFOptions const&, rocksdb::EnvOptions const&, rocksdb::TableCache*, rocksdb::InternalIterator*, std::__1::unique_ptr<rocksdb::InternalIterator, std::__1::default_delete<rocksdb::InternalIterator> >, rocksdb::FileMetaData*, rocksdb::InternalKeyComparator const&, std::__1::vector<std::__1::unique_ptr<rocksdb::IntTblPropCollectorFactory, std::__1::default_delete<rocksdb::IntTblPropCollectorFactory> >, std::__1::allocator<std::__1::unique_ptr<rocksdb::IntTblPropCollectorFactory, std::__1::default_delete<rocksdb::IntTblPropCollectorFactory> > > > const*, unsigned int, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, std::__1::vector<unsigned long long, std::__1::allocator<unsigned long long> >, unsigned long long, rocksdb::SnapshotChecker*, rocksdb::CompressionType, rocksdb::CompressionOptions const&, bool, rocksdb::InternalStats*, rocksdb::TableFileCreationReason, rocksdb::EventLogger*, int, rocksdb::Env::IOPriority, rocksdb::TableProperties*, int, unsigned long long, unsigned long long, rocksdb::Env::WriteLifeTimeHint) /src/rocksdb/db/builder.cc:196
rocksdb::FlushJob::WriteLevel0Table() /src/rocksdb/db/flush_job.cc:345
rocksdb::FlushJob::Run(rocksdb::FileMetaData*) /src/rocksdb/db/flush_job.cc:211
rocksdb::DBImpl::FlushMemTableToOutputFile(rocksdb::ColumnFamilyData*, rocksdb::MutableCFOptions const&, bool*, rocksdb::JobContext*, rocksdb::LogBuffer*) /src/rocksdb/db/db_impl_compaction_flush.cc:132
rocksdb::DBImpl::BackgroundFlush(bool*, rocksdb::JobContext*, rocksdb::LogBuffer*) /src/rocksdb/db/db_impl_compaction_flush.cc:1350
rocksdb::DBImpl::BackgroundCallFlush() /src/rocksdb/db/db_impl_compaction_flush.cc:1375
rocksdb::ThreadPoolImpl::Impl::BGThread(unsigned long) /src/rocksdb/util/threadpool_imp.cc:1913
rocksdb::ThreadPoolImpl::Impl::BGThreadWrapper(void*) /src/rocksdb/util/threadpool_imp.cc:302
```

## Comment 442484663

reporter (NONE) · toktarev · 2018-11-28T15:20:37Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-442484663

cache_index_blocks=false
cache_index_and_filter_blocks_with_high_priority=true
partition_filters = true
index_type = rocksdb::BlockBasedTableOptions::IndexType::kTwoLevelIndexSearch

## Comment 446706162

reporter (NONE) · toktarev · 2018-12-12T19:07:39Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-446706162

[w.pdf](https://github.com/facebook/rocksdb/files/2673181/w.pdf)

it is possible to see here last profilng result

## Comment 446992739

reporter (NONE) · toktarev · 2018-12-13T14:44:10Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-446992739

partition_filters = false
no_block_cache = true
cache_index_and_filter_blocks = false
cache_index_and_filter_blocks_with_high_priority = false
filter_policy = nullptr
max_open_files=2

After switching to these parameters I see stable memory RSS during 16 minutes and further ....


The key problem here is:

There is no explicit memory leak but during long running write process - the number of sst files grows, as a result all structures which will be allocated and created for new sst files consume more memory, like:

TableCache of fileReaders (max_open_files).
Bloom filters (new for each sst).
Block cache partition filters.
Blocks of files in block cache.

Only after disabling of all these structures I see stable memory consumption.

There is strict_capacity param in block cache, but if I set it to true - I see exception "Cache is full".







## Comment 447194186

other (CONTRIBUTOR) · ajkr · 2018-12-14T02:42:46Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-447194186

Thanks for the update. Is there anything remaining for us to answer or investigate?

FWIW, when I ran the initial provided code and set `max_open_files=20`, it stabilized at 30MB RSS. If there's any other concern, could you please provide updated code for us to use?

## Comment 447276776

reporter (NONE) · toktarev · 2018-12-14T10:03:49Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-447276776

```
#include <db/memtable.h>
#include <dirent.h>
#include <memtable/inlineskiplist.h>
#include <cinttypes>
#include <cstdio>
#include <iostream>
#include <string>
#include <thread>
#include "rocksdb/db.h"

using namespace std;
using namespace rocksdb;
using namespace std::chrono;

std::string kDBPath = "/repos/rocksdata";

#include <ostream>

#if defined(OS_MACOSX)
#include <mach/mach.h>
#else
#include <string.h>
#include <unistd.h>
#endif

struct MemorySnapshot {
  uint64_t vm_total;

  uint64_t vm_available;

  uint64_t virtual_size;

  uint64_t resident_size;

  uint64_t resident_size_peak;

  uint64_t page_size;

  int64_t pinned_size;

  uint32_t region_count;

  int32_t return_code;
};

#if defined(OS_MACOSX)

MemorySnapshot TakeSnapshot() {
  struct task_vm_info t_info {};

  mach_msg_type_number_t t_info_count = TASK_VM_INFO_COUNT;

  MemorySnapshot ms{};
  ms.return_code = task_info(mach_task_self(), TASK_VM_INFO,
                             (task_info_t)&t_info, &t_info_count);
  if (KERN_SUCCESS == ms.return_code) {
    ms.virtual_size = t_info.virtual_size;
    ms.resident_size = t_info.resident_size;
    ms.resident_size_peak = t_info.resident_size_peak;
    ms.region_count = static_cast<uint32_t>(t_info.region_count);
    ms.page_size = static_cast<uint64_t>(t_info.page_size);
    ms.pinned_size = -1;

    mach_msg_type_number_t count = HOST_VM_INFO_COUNT;
    vm_statistics_data_t vmstat;
    ms.return_code = host_statistics(mach_host_self(), HOST_VM_INFO,
                                     (host_info_t)&vmstat, &count);
    if (KERN_SUCCESS == ms.return_code) {
      ms.vm_total = ms.page_size * (vmstat.wire_count + vmstat.active_count +
                                    vmstat.inactive_count + vmstat.free_count +
                                    vmstat.purgeable_count);
      ms.vm_available =
          ms.page_size *
          (vmstat.inactive_count + vmstat.free_count + vmstat.purgeable_count);
    }
  }

  return ms;
}

#else

namespace {
const uint64_t KB_MULTIPLIER = 1u << 10u;

uint64_t parseUnsigned(char *line) {
  // This assumes that a digit will be found and the line ends in " kB".
  uint64_t len = strlen(line);

  const char *p = line;
  while (*p < '0' || *p > '9') p++;
  line[len - 3] = '\0';

  return atol(p) * KB_MULTIPLIER;
}
}  // namespace

MemorySnapshot TakeSnapshot() {
  MemorySnapshot ms{};

  FILE *file = fopen("/proc/self/status", "r");
  if (file == NULL) {
    ms.return_code = 1;
    return ms;
  }
  /*
   * Example output for this file:

  VmPeak:     6164 kB
  VmSize:     6164 kB
  VmLck:         0 kB
  VmPin:         0 kB
  VmHWM:       720 kB
  VmRSS:       720 kB
  VmData:      320 kB
  VmStk:       132 kB
  VmExe:        48 kB
  VmLib:      1944 kB
  VmPTE:        32 kB
  VmPMD:        12 kB
  VmSwap:        0 kB
  */

  ms.region_count = 1;  // linux doesn't do region memory management
  ms.page_size = sysconf(_SC_PAGESIZE);
  char line[128];
  while (fgets(line, 128, file) != NULL) {
    if (strncmp(line, "VmSize:", 7) == 0) {
      ms.virtual_size = parseUnsigned(line);
    } else if (strncmp(line, "VmRSS:", 6) == 0) {
      ms.resident_size = parseUnsigned(line);
    } else if (strncmp(line, "VmLck:", 6) == 0) {
      // TODO -sf- I'm not sure if it's this field, of `VMPin`
      ms.pinned_size = parseUnsigned(line);
    } else if (strncmp(line, "VmHWM:", 6) == 0) {
      ms.resident_size_peak = parseUnsigned(line);
    }
  }

  fclose(file);

  file = fopen("/proc/meminfo", "r");
  if (file == NULL) {
    ms.return_code = 2;
    return ms;
  }

  /*
   * Example output for this file:
   * MemTotal:        2046652 kB
     MemFree:          557292 kB
     MemAvailable:    1678188 kB
     Cached:          1228440 kB
     SReclaimable:      42744 kB

     We are looking for MemTotal and MemAvailable, but some older versions of
   linux don't supply MemAvailable; in those situations, we are looking for
   MemFree, Cached, and SReclaimable. For more infomation, see

     https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=34e431b0ae398fc54ea69ff85ec700722c9da773

     Our version doesn't account for the low-water mark, so it's probably more
   conservative than we want, but that's a good thing.
   */
  int64_t mem_available = -1;
  uint64_t cached, free, reclaimable;
  while (fgets(line, 128, file) != NULL) {
    if (strncmp(line, "MemTotal:", 9) == 0) {
      ms.vm_total = parseUnsigned(line);
    } else if (strncmp(line, "MemAvailable:", 13) == 0) {
      mem_available = parseUnsigned(line);
    } else if (strncmp(line, "MemFree:", 8) == 0) {
      free = parseUnsigned(line);
    } else if (strncmp(line, "Cached:", 7) == 0) {
      cached = parseUnsigned(line);
    } else if (strncmp(line, "SReclaimable:", 13) == 0) {
      reclaimable = parseUnsigned(line);
    }
  }

  if (mem_available < 0) {
    ms.vm_available = cached + free + reclaimable;
  } else {
    // if it's not -1, then it's been set to a positive number
    ms.vm_available = static_cast<uint64_t>(mem_available);
  }

  fclose(file);

  return ms;
}

#endif

template <typename T>
T swap_endian(T u) {
  static_assert(CHAR_BIT == 8, "CHAR_BIT != 8");

  union {
    T u;
    unsigned char u8[sizeof(T)];
  } source, dest;

  source.u = u;

  for (size_t k = 0; k < sizeof(T); k++)
    dest.u8[k] = source.u8[sizeof(T) - k - 1];

  return dest.u;
}

const char PATH_SEPARATOR =
#ifdef _WIN32
    '\\';
#else
    '/';
#endif

using path = std::string;

path concat_path(const path &dir, const path &file) {
  path result(dir);
  const bool result_has_separator = (result.back() == PATH_SEPARATOR);
  const bool file_has_separator = (file.front() == PATH_SEPARATOR);
  if (result_has_separator && file_has_separator) {
    // Too many separators, remove one.
    result.pop_back();
  } else if (!result_has_separator && !file_has_separator) {
    // No separator, add one.
    result.push_back(PATH_SEPARATOR);
  }
  result.append(file);
  return result;
}

std::vector<path> read_directory(const path &directory) {
  static const std::string CURRENT_DIRECTORY(".");
  static const std::string PARENT_DIRECTORY("..");
  std::vector<path> files;
  DIR *dir = opendir(directory.c_str());
  if (dir != NULL) {
    struct dirent *ent;
    while ((ent = readdir(dir)) != NULL) {
      if (CURRENT_DIRECTORY == ent->d_name || PARENT_DIRECTORY == ent->d_name) {
        continue;
      }
      path file(concat_path(directory, ent->d_name));
      files.push_back(file);
    }
    closedir(dir);
  }
  return files;
}

size_t count_sst_files(const std::string &dir) {
  std::vector<std::string> files = read_directory(dir);
  size_t sst_count = 0;
  std::string sst_ending = ".sst";
  for (auto &file : files) {
    if (file.length() >= sst_ending.length() &&
        file.compare(file.length() - sst_ending.length(), sst_ending.length(),
                     sst_ending) == 0) {
      ++sst_count;
    }
  }
  return sst_count;
}

rocksdb::TableFactory *makeDictionaryTableFactory() {
  auto blockOpts = rocksdb::BlockBasedTableOptions{};
  blockOpts.index_type =
      rocksdb::BlockBasedTableOptions::IndexType::kTwoLevelIndexSearch;
  blockOpts.partition_filters = true;
  blockOpts.metadata_block_size = 4096;
  blockOpts.block_size = 4096;
  blockOpts.block_cache = rocksdb::NewLRUCache(1ul << 30u, 16, false);
  blockOpts.cache_index_and_filter_blocks = true;
  blockOpts.cache_index_and_filter_blocks_with_high_priority = true;
  auto *pPolicy = rocksdb::NewBloomFilterPolicy(10, false);
  auto filter_ptr = std::shared_ptr<const rocksdb::FilterPolicy>(pPolicy);
  blockOpts.filter_policy = filter_ptr;
  return rocksdb::NewBlockBasedTableFactory(blockOpts);
}

int main() {
  std::system("exec rm -rf /repos/rocksdata/");
  std::system("exec mkdir /repos/rocksdata");

  DB *db;
  Options options;
  size_t aSize = 1024 * 1024;

  options.write_buffer_size = static_cast<size_t>(1024 * 1024 / 4);
  options.min_write_buffer_number_to_merge = 2;
  options.max_write_buffer_number = 6;
  options.level0_file_num_compaction_trigger = 2;
  options.target_file_size_base = aSize / 8;
  options.max_bytes_for_level_base = 1024 * 1024;
  options.compaction_style = rocksdb::kCompactionStyleLevel;
  options.compression_per_level.resize(2);
  options.num_levels = 2;

  for (int i = 0; i < 2; ++i) {
    options.compression_per_level[i] = rocksdb::CompressionType::kNoCompression;
  }

  options.create_if_missing = true;
  options.compression = rocksdb::CompressionType::kNoCompression;
  options.statistics = rocksdb::CreateDBStatistics();
  options.write_buffer_size = aSize;
  options.max_open_files = 2;

  // open DB
  Status s = DB::Open(options, kDBPath, &db);

  if (!s.ok()) {
    std::cout << s.ToString();
  }

  assert(s.ok());

  ColumnFamilyOptions cf_options{};
  cf_options.table_factory.reset(makeDictionaryTableFactory());
  cf_options.prefix_extractor.reset(rocksdb::NewNoopTransform());
  cf_options.write_buffer_size = 1024 * 1024;
  cf_options.num_levels = 2;

  std::string name("Name");
  ColumnFamilyHandle *cf;
  Status status = db->CreateColumnFamily(cf_options, name, &cf);

  assert(s.ok());

  u_int64_t *buffer = new u_int64_t[4];
  char *pointer = reinterpret_cast<char *>(buffer);
  WriteBatch writeBatch{};
  u_int64_t max = 10000000;

  Slice key(pointer, 32);
  Slice value(reinterpret_cast<char *>(&max), 8);

  uint64_t begin =
      (uint64_t)std::chrono::duration_cast<std::chrono::nanoseconds>(
          system_clock::now().time_since_epoch())
          .count();

  for (u_int64_t i = 0; i < 10000000000; i++) {
    *(buffer) = swap_endian(i);
    *(buffer + 1) = i + 1;
    *(buffer + 2) = i + 2;
    *(buffer + 3) = i + 3;

    writeBatch.Put(cf, key, value);

    if (i % 1000 == 0) {
      Status s1 = db->Write(WriteOptions(), &writeBatch);
      if (!s1.ok()) {
        std::cout << s1.ToString();
      }
      assert(s1.ok());
      writeBatch.Clear();
    }

    *(buffer) = swap_endian(i - 1024);
    *(buffer + 1) = i + 1;
    *(buffer + 2) = i + 2;
    *(buffer + 3) = i + 3;

    ReadOptions read_options{};
    std::string value1;
    db->Get(read_options, key, &value1);

    if (i % 1000000 == 0) {
      uint64_t end =
          (uint64_t)std::chrono::duration_cast<std::chrono::nanoseconds>(
              system_clock::now().time_since_epoch())
              .count();
      double time = (end - begin) / 1000000000;
      double delta = i / time;
      MemorySnapshot mem_snapshot = TakeSnapshot();
      auto rss_mb = mem_snapshot.resident_size / (1000.0 * 1000);
      double prss_mb = mem_snapshot.resident_size_peak / (1000.0 * 1000);
      size_t file_count = count_sst_files("/repos/rocksdata");

      std::cout << "Speed=" << std::to_string(delta) << ", RSS: " << rss_mb
                << " MB"
                << " (Peak RSS: " << prss_mb << " MB)"
                << " File Count  " << file_count << "\n\n";

      rocksdb::CompactRangeOptions opts{};
      opts.change_level = true;
      db->CompactRange(opts, cf, nullptr, nullptr);
    }
  }

  db->DestroyColumnFamilyHandle(cf);
  delete db;
  return 0;
}
```

This code shows infinite memory consumption.

If we comment line:
cf_options.table_factory.reset(makeDictionaryTableFactory());

Rss become stable.

Block cache + TableCache (max_open_file_size) are culprits of infinite memory growth.



## Comment 447289997

reporter (NONE) · toktarev · 2018-12-14T10:54:18Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-447289997

```
    if (usage_ - lru_usage_ + charge > capacity_ &&
        (strict_capacity_limit_ || handle == nullptr)) {
      if (handle == nullptr) {
        // Don't insert the entry but still return ok, as if the entry inserted
        // into cache and get evicted immediately.
        last_reference_list.push_back(e);
      } else {
        delete[] reinterpret_cast<char*>(e);
        *handle = nullptr;
        s = Status::Incomplete("Insert failed due to LRU cache being full.");
      }
```

one more question:

It is very strange logic for LRU cache 
"Insert failed due to LRU cache being full"

of Cache is full - we should just skip addition or remove last element from cache and replace but we definetelly shouldn't stop out application with such error.





## Comment 447312293

reporter (NONE) · toktarev · 2018-12-14T12:34:42Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-447312293

lru_cache.cc:

```
void LRUCacheShard::EvictFromLRU(size_t charge,
                                 autovector<LRUHandle*>* deleted) {
  while (usage_ + charge > 0 && lru_.next != &lru_) {
    LRUHandle* old = lru_.next;
    assert(old->InCache());
    assert(old->refs == 1);  // LRU list contains elements which may be evicted
    LRU_Remove(old);
    table_.Remove(old->key(), old->hash);
    old->SetInCache(false);
    Unref(old);
    usage_ -= old->charge;
    deleted->push_back(old);
  }

  if (usage_>0)
  std::cout << usage_ << std::endl;
}

```

As I understand I shouldn't see usage_t printing at all because I trasformed capacity=0.
In real execution I see non-zero usage's printing.






## Comment 447345454

reporter (NONE) · toktarev · 2018-12-14T14:43:25Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-447345454

```
table_ = {rocksdb::LRUHandleTable} 
 list_ = {rocksdb::LRUHandle ** | 0x7fa7706a9fa0} 0x00007fa7706a9fa0
  *list_ = {rocksdb::LRUHandle * | 0x0} NULL
  [1] = {rocksdb::LRUHandle * | 0x0} NULL
  [2] = {rocksdb::LRUHandle * | 0x0} NULL
  [3] = {rocksdb::LRUHandle * | 0x7fa770485c20} 0x00007fa770485c20
   value = {void * | 0x0} NULL
   deleter = {void (*)(const rocksdb::Slice &, void *) | 0x0} NULL
   next_hash = {rocksdb::LRUHandle * | 0x0} NULL
   next = {rocksdb::LRUHandle * | 0x0} NULL
   prev = {rocksdb::LRUHandle * | 0x0} NULL
   charge = {size_t} 4074
   key_length = {size_t} 43
   refs = {uint32_t} 2
   flags = {char} 1 '\x01'
   hash = {uint32_t} 601469731
   key_data = {char [1]} "\x84\x80\x80\b\x88\x97\x96\n"
  [4] = {rocksdb::LRUHandle * | 0x0} NULL
  [5] = {rocksdb::LRUHandle * | 0x0} NULL
  [6] = {rocksdb::LRUHandle * | 0x0} NULL
  [7] = {rocksdb::LRUHandle * | 0x0} NULL
  [8] = {rocksdb::LRUHandle * | 0x0} NULL
  [9] = {rocksdb::LRUHandle * | 0x0} NULL
  [10] = {rocksdb::LRUHandle * | 0x0} NULL
 length_ = {uint32_t} 16
 elems_ = {uint32_t} 1
usage_ = {size_t} 4074
lru_usage_ = {size_t} 0
```

## Comment 447354879

reporter (NONE) · toktarev · 2018-12-14T15:15:15Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-447354879

Seems this is not a bug, because it is possible that record is added in cache but is not added to the lru_list, however it looks suspicious.

## Comment 465362035

other (NONE) · veerav123 · 2019-02-20T00:00:00Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-465362035

Is it resolved?

## Comment 465907283

other (NONE) · Bingo403 · 2019-02-21T08:28:27Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-465907283

the same problem.

## Comment 469017777

other (NONE) · lpl6338236 · 2019-03-03T12:23:12Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-469017777

Same problem with 5.14.2. 
It seems all data of open sst files are cached in memory, instead of just the file descriptor.

## Comment 469445745

other (NONE) · sam-guo · 2019-03-04T22:21:52Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-469445745

We are seeing the same issue that memory keeps increasing until oom-killer kills it. We've set the cache_index_and_filter_blocks = True, but it does not seem to help, same behavior (which I am very surprised). This only happens when we use Iterator to do seek etc. Waiting for a solution - either permanent or a workaround. Thanks.

## Comment 469820534

other (NONE) · veerav123 · 2019-03-05T19:15:34Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-469820534

I am still seeing the same issue with cache_index_and_filter_blocks = true. My
process is not doing any writes. It is doing only reads.

On Mon, Mar 4, 2019 at 2:22 PM sam-guo <notifications@github.com> wrote:

> We are seeing the same issue that memory keeps increasing until oom-killer
> kills it. We've set the cache_index_and_filter_blocks = True, but it does
> not seem to help, same behavior (which I am very surprised). This only
> happens when we use Iterator to do seek etc. Waiting for a solution -
> either permanent or a workaround. Thanks.
>
> —
> You are receiving this because you commented.
> Reply to this email directly, view it on GitHub
> <https://github.com/facebook/rocksdb/issues/4112#issuecomment-469445745>,
> or mute the thread
> <https://github.com/notifications/unsubscribe-auth/AVncCgC_miOgNzUNrw0KN-rYvY-HjPp_ks5vTZyhgaJpZM4VLVar>
> .
>


## Comment 469825174

reporter (NONE) · toktarev · 2019-03-05T19:29:01Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-469825174

I really like this issue :)

+1 new complaint every day )

## Comment 469837771

other (NONE) · vitalyisaev2 · 2019-03-05T20:05:52Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-469837771

I had a kind of similar problem with [gorocksdb](https://github.com/tecbot/gorocksdb), a Go RocksDB wrapper. Every iteration over whole database caused the increase of `RSS`. My research on this topic is [here](https://github.com/vitalyisaev2/gorocksdb_merge_operator_issue). I thought I have fixed this problem by rewriting `MergeOperator` implementation from `Go` to `C++`, so the leak is highly likely on the side of Golang wrapper. I don't observe monotonic `RSS` growth anymore.

But all the recent updates to the current issue make me suspicious again.

## Comment 469916689

other (CONTRIBUTOR) · anand1976 · 2019-03-06T00:34:11Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-469916689

@veerav123 I'm not sure what exact problem you are seeing, but responding to the most recent report by @toktarev. The following combination of options can cause unbounded memory consumption growth -
```
BlockBasedTableOptions::partition_filters = true
BlockBasedTableOptions::pin_top_level_index_and_filter = true (default)
LRUCacheOptions::strict_capacity_limit = false (default) 
DBOptions::max_open_files = -1 (default)
```
This is due to the fact that the top level filter partition is pinned in memory for each open file, and if strict_capacity_limit is false, will not be bounded by the block cache size. If ```max_open_files``` is -1, there is no limit on number of open files. In order to limit memory usage, either set ```max_open_files``` to some sane value, or set ```pin_top_level_index_and_filter``` to false.

## Comment 470110388

reporter (NONE) · toktarev · 2019-03-06T13:39:45Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-470110388

Setting `pin_top_level_index_and_filter` to false causes performance degradation.

## Comment 470201438

other (NONE) · sam-guo · 2019-03-06T17:34:11Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-470201438

@anand1976 thanks for the info. I am using RocksJava, how can I set strict_capacity_limit = true (to avoid the memory problem)? I don't see the call available on either "Options" or "BlockBasedTableConfig" classes.

## Comment 470205585

other (CONTRIBUTOR) · koldat · 2019-03-06T17:45:44Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-470205585

It is on Cache object. Create it using LRUCache.


st 6. 3. 2019 18:35 odesílatel sam-guo <notifications@github.com> napsal:

> @anand1976 <https://github.com/anand1976> thanks for the info. I am using
> RocksJava, how can I set strict_capacity_limit = true (to avoid the memory
> problem)? I don't see the call available on either "Options" or
> "BlockBasedTableConfig" classes.
>
> —
> You are receiving this because you were mentioned.
> Reply to this email directly, view it on GitHub
> <https://github.com/facebook/rocksdb/issues/4112#issuecomment-470201438>,
> or mute the thread
> <https://github.com/notifications/unsubscribe-auth/AQFcxl6c3uMz3bx8rjv2ZLN3H_4YOddRks5vT_xYgaJpZM4VLVar>
> .
>


## Comment 470211080

other (NONE) · veerav123 · 2019-03-06T18:00:39Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-470211080

@anand1976 ,   I have the following code and I still see the memory growing unbounded:
```
    rocksdb::Options dbOptions;
    dbOptions.create_if_missing = true;
    dbOptions.manual_wal_flush = true;
    dbOptions.allow_mmap_reads = true;
    dbOptions.compression = rocksdb::CompressionType::kNoCompression;

    rocksdb::BlockBasedTableOptions table_options;
    table_options.block_cache = rocksdb::NewLRUCache(1 * 1024 * 1024 * 1024LL, -1, true);
    table_options.cache_index_and_filter_blocks = true;
    table_options.filter_policy.reset(rocksdb::NewBloomFilterPolicy(10, true));
    table_options.block_restart_interval = 4;
    dbOptions.table_factory.reset(rocksdb::NewBlockBasedTableFactory(table_options));
    dbOptions.max_open_files = -1;
```
The third param here:
```
table_options.block_cache = rocksdb::NewLRUCache(1 * 1024 * 1024 * 1024LL, -1, true);
```
sets ```strict_capacity_limit = true```

## Comment 470243140

reporter (NONE) · toktarev · 2019-03-06T19:29:14Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-470243140

The problem of memory growth is not actually because of RocksDB's memory leak

I suspect that it is just Arena's leak

http://codearcana.com/posts/2016/07/11/arena-leak-in-glibc.html

RocksDB introduced MemoryAllocator in last versions and now it is possible to organise kind of pooling for block caches's blocks.

However Arena still allocates a lot of new memory and it causes unbounded RSS growth.




## Comment 470243539

reporter (NONE) · toktarev · 2019-03-06T19:30:22Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-470243539

everybody can try MALLOC_ARENA_MAX=1 and check if it helped

However it will affect performance.

## Comment 470250265

other (NONE) · veerav123 · 2019-03-06T19:49:42Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-470250265

@toktarev why not use WITH_JEMALLOC parameter when RocksDB is built? I'll try that and update it here

## Comment 470250766

reporter (NONE) · toktarev · 2019-03-06T19:51:07Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-470250766

@veerav123

MALLOC_ARENA_MAX is environment parameter  and should be set before execution of corresponding binary file

## Comment 470251056

reporter (NONE) · toktarev · 2019-03-06T19:51:53Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-470251056

JEMALLOC is a good point to check

## Comment 470251651

other (NONE) · veerav123 · 2019-03-06T19:53:19Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-470251651

@toktarev yes I meant to check using RocksDB built with jemalloc which might handle these memory arena and fragmentation issues better than glibc

## Comment 470261455

reporter (NONE) · toktarev · 2019-03-06T20:21:39Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-470261455

iirc @koldat  uses jemalloc in his tests and has the same complaining with the corresponding diagram

## Comment 470269235

other (CONTRIBUTOR) · koldat · 2019-03-06T20:44:49Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-470269235

We are not having any problems after I use rocksdb the way I described many times in this thread. Our read write load is very high and dB size is around terabytes. Still we are able to handle that with limited docker instance with 5gb ram limit including our Java app which is itself quite hungry. My guess is that rocksdb is taking max 2gb. All is running perfectly stable for months.

What I took as best for us:
1. Set Max open files! Yes it is a must. 
2. Two level index. 
3. Shared and strictly limited caches.
4. Jemalloc. It helps to keep memory stable. We have quite aggressive setup, but still no noticeable performance impact. 
5. Directio for sequence scans. 
6. Custom patches (Java specific) 

All of these basically helps system and library. And it works perfectly. I use modified 5.12.5. Unfortunately patches that also helps a lot for high loads (Java direct buffers) were not merged. Otherwise jvm suffers from memory hot spots. 

Anyway, rocksdb team, this is great work. I love this library. 


## Comment 470357786

reporter (NONE) · toktarev · 2019-03-07T02:24:21Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-470357786

4.Jemalloc. It helps to keep memory stable. We have quite aggressive setup, but still no noticeable performance impact.

Seems that it was a key point.

## Comment 470469686

other (CONTRIBUTOR) · koldat · 2019-03-07T10:22:31Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-470469686

BTW here is JEMALLOC setting I use:
export LD_PRELOAD=/usr/lib/libjemalloc.so.2
export MALLOC_CONF=abort_conf:true,narenas:16,lg_tcache_max:13

We use latest jemalloc (5.x)


## Comment 470559989

reporter (NONE) · toktarev · 2019-03-07T15:02:25Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-470559989

@koldat 
Where you able to have stable memory consumption running my benchmark which I specified here:
https://github.com/facebook/rocksdb/issues/4112#issuecomment-447276776 ?

I made the following steps:

Install Jemalloc using Macos using 

```
brew install jemalloc
```

1) Downloaded master branch of RocksDB

2) make static_lib

3) strict_capacity_limit = true

4) export MALLOC_CONF=abort_conf:true,narenas:16,lg_tcache_max:13

It is running now like this:

Speed=1000000.000000, RSS: 11.4319 MB (Peak RSS: 11.4319 MB) File Count  66
...
Speed=909090.909091, RSS: 14.6227 MB (Peak RSS: 15.3969 MB) File Count  1999
...
Speed=984615.384615, RSS: 17.3548 MB (Peak RSS: 18.092 MB) File Count  4266
...
Speed=1017094.017094, RSS: 24.8873 MB (Peak RSS: 25.1044 MB) File Count  7933
...
Speed=744245.524297, RSS: 37.3678 MB (Peak RSS: 40.9805 MB) File Count  19399
...
Speed=730864.197531, RSS: 39.4363 MB (Peak RSS: 40.9805 MB) File Count  19733
..

Memory goes up and up and up.

I don't know if it will have some limit in the future but my Block cache config is following:

```
  std::shared_ptr<MemoryAllocator> al = std::make_shared<CustomAllocator>();
  JemallocAllocatorOptions opts{};
  opts.limit_tcache_size = true;
  opts.tcache_size_lower_bound = 16 * 1024 * 1024;
  opts.tcache_size_upper_bound = 32 * 1024 * 1024;
  Status s = NewJemallocNodumpAllocator(opts, &al);
  blockOpts.block_cache = rocksdb::NewLRUCache(1024 * 1024, 0, true, 0, al);
  return rocksdb::NewBlockBasedTableFactory(blockOpts);

```



## Comment 470562693

reporter (NONE) · toktarev · 2019-03-07T15:08:30Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-470562693

```
#include <db/memtable.h>
#include <dirent.h>
#include <memtable/inlineskiplist.h>
#include <cinttypes>
#include <cstdio>
#include <iostream>
#include <string>
#include <thread>
#include "rocksdb/db.h"
#include "util/jemalloc_nodump_allocator.h"

using namespace std;
using namespace rocksdb;
using namespace std::chrono;

std::string kDBPath = "/repos/rocksdata";

#include <ostream>

#if defined(OS_MACOSX)
#include <mach/mach.h>
#else
#include <string.h>
#include <unistd.h>
#endif

struct MemorySnapshot {
  uint64_t vm_total;

  uint64_t vm_available;

  uint64_t virtual_size;

  uint64_t resident_size;

  uint64_t resident_size_peak;

  uint64_t page_size;

  int64_t pinned_size;

  uint32_t region_count;

  int32_t return_code;
};

#if defined(OS_MACOSX)

MemorySnapshot TakeSnapshot() {
  struct task_vm_info t_info {};

  mach_msg_type_number_t t_info_count = TASK_VM_INFO_COUNT;

  MemorySnapshot ms{};
  ms.return_code = task_info(mach_task_self(), TASK_VM_INFO,
                             (task_info_t)&t_info, &t_info_count);
  if (KERN_SUCCESS == ms.return_code) {
    ms.virtual_size = t_info.virtual_size;
    ms.resident_size = t_info.resident_size;
    ms.resident_size_peak = t_info.resident_size_peak;
    ms.region_count = static_cast<uint32_t>(t_info.region_count);
    ms.page_size = static_cast<uint64_t>(t_info.page_size);
    ms.pinned_size = -1;

    mach_msg_type_number_t count = HOST_VM_INFO_COUNT;
    vm_statistics_data_t vmstat;
    ms.return_code = host_statistics(mach_host_self(), HOST_VM_INFO,
                                     (host_info_t)&vmstat, &count);
    if (KERN_SUCCESS == ms.return_code) {
      ms.vm_total = ms.page_size * (vmstat.wire_count + vmstat.active_count +
                                    vmstat.inactive_count + vmstat.free_count +
                                    vmstat.purgeable_count);
      ms.vm_available =
          ms.page_size *
          (vmstat.inactive_count + vmstat.free_count + vmstat.purgeable_count);
    }
  }

  return ms;
}

#else

namespace {
const uint64_t KB_MULTIPLIER = 1u << 10u;

uint64_t parseUnsigned(char *line) {
  // This assumes that a digit will be found and the line ends in " kB".
  uint64_t len = strlen(line);

  const char *p = line;
  while (*p < '0' || *p > '9') p++;
  line[len - 3] = '\0';

  return atol(p) * KB_MULTIPLIER;
}
}  // namespace

MemorySnapshot TakeSnapshot() {
  MemorySnapshot ms{};

  FILE *file = fopen("/proc/self/status", "r");
  if (file == NULL) {
    ms.return_code = 1;
    return ms;
  }
  /*
   * Example output for this file:

  VmPeak:     6164 kB
  VmSize:     6164 kB
  VmLck:         0 kB
  VmPin:         0 kB
  VmHWM:       720 kB
  VmRSS:       720 kB
  VmData:      320 kB
  VmStk:       132 kB
  VmExe:        48 kB
  VmLib:      1944 kB
  VmPTE:        32 kB
  VmPMD:        12 kB
  VmSwap:        0 kB
  */

  ms.region_count = 1;  // linux doesn't do region memory management
  ms.page_size = sysconf(_SC_PAGESIZE);
  char line[128];
  while (fgets(line, 128, file) != NULL) {
    if (strncmp(line, "VmSize:", 7) == 0) {
      ms.virtual_size = parseUnsigned(line);
    } else if (strncmp(line, "VmRSS:", 6) == 0) {
      ms.resident_size = parseUnsigned(line);
    } else if (strncmp(line, "VmLck:", 6) == 0) {
      // TODO -sf- I'm not sure if it's this field, of `VMPin`
      ms.pinned_size = parseUnsigned(line);
    } else if (strncmp(line, "VmHWM:", 6) == 0) {
      ms.resident_size_peak = parseUnsigned(line);
    }
  }

  fclose(file);

  file = fopen("/proc/meminfo", "r");
  if (file == NULL) {
    ms.return_code = 2;
    return ms;
  }

  /*
   * Example output for this file:
   * MemTotal:        2046652 kB
     MemFree:          557292 kB
     MemAvailable:    1678188 kB
     Cached:          1228440 kB
     SReclaimable:      42744 kB

     We are looking for MemTotal and MemAvailable, but some older versions of
   linux don't supply MemAvailable; in those situations, we are looking for
   MemFree, Cached, and SReclaimable. For more infomation, see

     https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=34e431b0ae398fc54ea69ff85ec700722c9da773

     Our version doesn't account for the low-water mark, so it's probably more
   conservative than we want, but that's a good thing.
   */
  int64_t mem_available = -1;
  uint64_t cached, free, reclaimable;
  while (fgets(line, 128, file) != NULL) {
    if (strncmp(line, "MemTotal:", 9) == 0) {
      ms.vm_total = parseUnsigned(line);
    } else if (strncmp(line, "MemAvailable:", 13) == 0) {
      mem_available = parseUnsigned(line);
    } else if (strncmp(line, "MemFree:", 8) == 0) {
      free = parseUnsigned(line);
    } else if (strncmp(line, "Cached:", 7) == 0) {
      cached = parseUnsigned(line);
    } else if (strncmp(line, "SReclaimable:", 13) == 0) {
      reclaimable = parseUnsigned(line);
    }
  }

  if (mem_available < 0) {
    ms.vm_available = cached + free + reclaimable;
  } else {
    // if it's not -1, then it's been set to a positive number
    ms.vm_available = static_cast<uint64_t>(mem_available);
  }

  fclose(file);

  return ms;
}

#endif

template <typename T>
T swap_endian(T u) {
  static_assert(CHAR_BIT == 8, "CHAR_BIT != 8");

  union {
    T u;
    unsigned char u8[sizeof(T)];
  } source, dest;

  source.u = u;

  for (size_t k = 0; k < sizeof(T); k++)
    dest.u8[k] = source.u8[sizeof(T) - k - 1];

  return dest.u;
}

const char PATH_SEPARATOR =
#ifdef _WIN32
    '\\';
#else
    '/';
#endif

using path = std::string;

path concat_path(const path &dir, const path &file) {
  path result(dir);
  const bool result_has_separator = (result.back() == PATH_SEPARATOR);
  const bool file_has_separator = (file.front() == PATH_SEPARATOR);
  if (result_has_separator && file_has_separator) {
    // Too many separators, remove one.
    result.pop_back();
  } else if (!result_has_separator && !file_has_separator) {
    // No separator, add one.
    result.push_back(PATH_SEPARATOR);
  }
  result.append(file);
  return result;
}

std::vector<path> read_directory(const path &directory) {
  static const std::string CURRENT_DIRECTORY(".");
  static const std::string PARENT_DIRECTORY("..");
  std::vector<path> files;
  DIR *dir = opendir(directory.c_str());
  if (dir != NULL) {
    struct dirent *ent;
    while ((ent = readdir(dir)) != NULL) {
      if (CURRENT_DIRECTORY == ent->d_name || PARENT_DIRECTORY == ent->d_name) {
        continue;
      }
      path file(concat_path(directory, ent->d_name));
      files.push_back(file);
    }
    closedir(dir);
  }
  return files;
}

size_t count_sst_files(const std::string &dir) {
  std::vector<std::string> files = read_directory(dir);
  size_t sst_count = 0;
  std::string sst_ending = ".sst";
  for (auto &file : files) {
    if (file.length() >= sst_ending.length() &&
        file.compare(file.length() - sst_ending.length(), sst_ending.length(),
                     sst_ending) == 0) {
      ++sst_count;
    }
  }
  return sst_count;
}

class CustomAllocator : public rocksdb::MemoryAllocator {
 public:
  CustomAllocator() {}

  ~CustomAllocator() {}

  const char *Name() const { return "Custom"; }

  void *Allocate(size_t size) { return malloc(size); }

  void Deallocate(void *p) { free(p); }

  size_t UsableSize(void * /*p*/, size_t allocation_size) const {
    return allocation_size;
  }
};

rocksdb::TableFactory *makeDictionaryTableFactory() {
  auto blockOpts = rocksdb::BlockBasedTableOptions{};
  blockOpts.index_type =
      rocksdb::BlockBasedTableOptions::IndexType::kTwoLevelIndexSearch;
  blockOpts.block_size = 4096;
  blockOpts.partition_filters = true;
  blockOpts.metadata_block_size = 4096;
  blockOpts.cache_index_and_filter_blocks = true;
  blockOpts.pin_top_level_index_and_filter = false;
  blockOpts.pin_l0_filter_and_index_blocks_in_cache = false;
  blockOpts.cache_index_and_filter_blocks_with_high_priority = true;
  auto *pPolicy = rocksdb::NewBloomFilterPolicy(10, false);
  auto filter_ptr = std::shared_ptr<const rocksdb::FilterPolicy>(pPolicy);
  blockOpts.filter_policy = filter_ptr;
  std::shared_ptr<MemoryAllocator> al = std::make_shared<CustomAllocator>();
  JemallocAllocatorOptions opts{};
  opts.limit_tcache_size = true;
  opts.tcache_size_lower_bound = 16 * 1024 * 1024;
  opts.tcache_size_upper_bound = 32 * 1024 * 1024;
  Status s = NewJemallocNodumpAllocator(opts, &al);
  blockOpts.block_cache = rocksdb::NewLRUCache(1024 * 1024, 0, true, 0, al);
  return rocksdb::NewBlockBasedTableFactory(blockOpts);
}

int main() {
  std::system("exec rm -rf /repos/rocksdata/");
  std::system("exec mkdir /repos/rocksdata");

  DB *db;
  Options options;
  size_t aSize = 1024 * 1024;

  options.num_levels = 7;
  options.write_buffer_size = static_cast<size_t>(aSize / 4);
  options.min_write_buffer_number_to_merge = 2;
  options.max_write_buffer_number = 6;
  options.level0_file_num_compaction_trigger = 2;
  options.target_file_size_base = aSize / 8;
  options.max_background_compactions = 1;
  options.compression_per_level.resize(2);

  for (int i = 0; i < options.num_levels; ++i) {
    options.compression_per_level[i] = rocksdb::CompressionType::kNoCompression;
  }

  options.create_if_missing = true;
  options.compression = rocksdb::CompressionType::kNoCompression;
  options.statistics = rocksdb::CreateDBStatistics();
  options.write_buffer_size = aSize;
  options.max_open_files = 2;

  // open DB
  Status s = DB::Open(options, kDBPath, &db);

  if (!s.ok()) {
    std::cout << s.ToString();
  }

  assert(s.ok());

  ColumnFamilyOptions cf_options{};
  cf_options.table_factory.reset(makeDictionaryTableFactory());
  cf_options.prefix_extractor.reset(rocksdb::NewNoopTransform());
  cf_options.write_buffer_size = aSize;
  cf_options.num_levels = options.num_levels;

  std::string name("Name");
  ColumnFamilyHandle *cf;
  Status status = db->CreateColumnFamily(cf_options, name, &cf);

  assert(s.ok());

  u_int64_t *buffer = new u_int64_t[4];
  char *pointer = reinterpret_cast<char *>(buffer);
  WriteBatch writeBatch{};
  u_int64_t max = 10000000;

  Slice key(pointer, 32);
  Slice value(reinterpret_cast<char *>(&max), 8);

  uint64_t begin =
      (uint64_t)std::chrono::duration_cast<std::chrono::nanoseconds>(
          system_clock::now().time_since_epoch())
          .count();

  for (u_int64_t i = 0; i < 10000000000; i++) {
    *(buffer) = swap_endian(i);
    *(buffer + 1) = i + 1;
    *(buffer + 2) = i + 2;
    *(buffer + 3) = i + 3;

    writeBatch.Put(cf, key, value);

    if (i % 1000 == 0) {
      Status s1 = db->Write(WriteOptions(), &writeBatch);
      if (!s1.ok()) {
        std::cout << s1.ToString();
      }
      assert(s1.ok());
      writeBatch.Clear();
    }

    *(buffer) = swap_endian(i - 1024);
    *(buffer + 1) = i + 1;
    *(buffer + 2) = i + 2;
    *(buffer + 3) = i + 3;

    ReadOptions read_options{};
    std::string value1;
    db->Get(read_options, key, &value1);

    if (i % 1000000 == 0) {
      uint64_t end =
          (uint64_t)std::chrono::duration_cast<std::chrono::nanoseconds>(
              system_clock::now().time_since_epoch())
              .count();
      double time = (end - begin) / 1000000000;
      double delta = i / time;
      MemorySnapshot mem_snapshot = TakeSnapshot();
      auto rss_mb = mem_snapshot.resident_size / (1000.0 * 1000);
      double prss_mb = mem_snapshot.resident_size_peak / (1000.0 * 1000);
      size_t file_count = count_sst_files("/repos/rocksdata");

      std::cout << "Speed=" << std::to_string(delta) << ", RSS: " << rss_mb
                << " MB"
                << " (Peak RSS: " << prss_mb << " MB)"
                << " File Count  " << file_count << "\n\n";
    }
  }

  db->DestroyColumnFamilyHandle(cf);
  delete db;
  return 0;
}

```

## Comment 470668434

other (NONE) · veerav123 · 2019-03-07T19:49:33Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-470668434

@anand1976 @koldat 
Is ```max_open_files``` a data build time change? 

If I built the data with ```max_open_files=-1```, can I use ```max_open_files=500``` during run time?

## Comment 470686430

other (CONTRIBUTOR) · koldat · 2019-03-07T20:43:05Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-470686430

Yes you can set this to any value any time without any breakage. Like most of database settings. 

## Comment 471508781

reporter (NONE) · toktarev · 2019-03-11T11:51:16Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-471508781

@veerav123 

did jemalloc help ?

## Comment 471765188

other (NONE) · veerav123 · 2019-03-11T22:28:59Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-471765188

No, it didn't help.

On Mon, Mar 11, 2019 at 4:51 AM toktarev <notifications@github.com> wrote:

> @veerav123 <https://github.com/veerav123>
>
> did jemalloc help ?
>
> —
> You are receiving this because you were mentioned.
> Reply to this email directly, view it on GitHub
> <https://github.com/facebook/rocksdb/issues/4112#issuecomment-471508781>,
> or mute the thread
> <https://github.com/notifications/unsubscribe-auth/AVncCiShOUFyXTP6APVd-JExgCTDNaZLks5vVkNZgaJpZM4VLVar>
> .
>


## Comment 472962334

other (NONE) · veerav123 · 2019-03-14T16:56:58Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-472962334

@toktarev , try 5.15.10 and all the tuning/config suggestions from @koldat, that seems to work

## Comment 472964448

reporter (NONE) · toktarev · 2019-03-14T17:01:32Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-472964448

@veerav123 only for 5.15 or later as well ?

## Comment 472976395

other (NONE) · veerav123 · 2019-03-14T17:26:54Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-472976395

I tried 5.15.10. I believe the later ones should also work 

## Comment 472978505

reporter (NONE) · toktarev · 2019-03-14T17:31:57Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-472978505

@veerav123 how many levels do you use ?

## Comment 472981599

reporter (NONE) · toktarev · 2019-03-14T17:39:22Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-472981599

you wrote before

-No, it didn't help.


I just try to understand what did you change 

## Comment 472985652

other (NONE) · veerav123 · 2019-03-14T17:48:11Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-472985652

@toktarev , My response "-No, it didn't help." was for using jemalloc alone.
But I all these suggestion from @koldat here:
https://github.com/facebook/rocksdb/wiki/Partitioned-Index-Filters ->[I did all that is suggested under "How to Use it"]

## Comment 472988009

reporter (NONE) · toktarev · 2019-03-14T17:53:25Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-472988009

could you please send little benchmark which shows stable RSS during long time of heavy writes and reads ?

I used the  same configuration
max_open_files=2

```
  auto blockOpts = rocksdb::BlockBasedTableOptions{};
  blockOpts.index_type =
      rocksdb::BlockBasedTableOptions::IndexType::kTwoLevelIndexSearch;
  blockOpts.block_size = 4096;
  blockOpts.partition_filters = true;
  blockOpts.metadata_block_size = 4096;
  blockOpts.cache_index_and_filter_blocks = true;
  blockOpts.pin_top_level_index_and_filter = false;
  blockOpts.pin_l0_filter_and_index_blocks_in_cache = false;
  blockOpts.cache_index_and_filter_blocks_with_high_priority = true;
  auto *pPolicy = rocksdb::NewBloomFilterPolicy(10, false);
  auto filter_ptr = std::shared_ptr<const rocksdb::FilterPolicy>(pPolicy);
  blockOpts.filter_policy = filter_ptr;
  std::shared_ptr<MemoryAllocator> al = std::make_shared<CustomAllocator>();
  JemallocAllocatorOptions opts{};
  opts.limit_tcache_size = true;
  opts.tcache_size_lower_bound = 16 * 1024 * 1024;
  opts.tcache_size_upper_bound = 32 * 1024 * 1024;
  Status s = NewJemallocNodumpAllocator(opts, &al);
  blockOpts.block_cache = rocksdb::NewLRUCache(1024 * 1024, 0, true, 0, al);
  return rocksdb::NewBlockBasedTableFactory(blockOpts);

```

but still see that memory grows and . grows and grows






## Comment 472990918

reporter (NONE) · toktarev · 2019-03-14T17:59:56Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-472990918

I suspect that @koldat 's setting give us considerably  better  memory consumption than without it.

But I still don't believe that there is some limit where RocksDb stops consumes memory

RSS peak always grows on the far distance (+ some kiolobytes in minute or so on)

We can just considerably reduce the speed of this growth.

Probably it is fine for some projects.




## Comment 472994861

reporter (NONE) · toktarev · 2019-03-14T18:09:34Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-472994861

I used custom MemoryAllocator (pool of char *) + JeMalloc and see that there is one place which allocated and allocated - it is Arena's buffer for the list of files which should be compacted.


The more we write the more sst files we have and that buffer directly depends on the number of sst files.

this is why it allocates and allocates buffer of bigger size on each compaction.

On some projects it can be very slow growth.



## Comment 473185950

other (CONTRIBUTOR) · koldat · 2019-03-15T07:30:15Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-473185950

@toktarev I have quickly tried your sample (rewritten to Java) and RSS really slowly growing. But not that much it produces thousands of files and I was still under 100MB. It is hard to say if it is fragmentation or not with these small numbers. 

You are having very small buffers and file sizes. It is not normal setup for your expectations. I would also recommend these as good starting point: 
writeBufferSize: 128MB
maxWriteBufferNumber: 4
targetFileSizeBase: 128MB
blockSize: 8, 16 kB (I have small records so I use even 32kB) - yes it sounds stupid to use big block for small records, but I target the tradeoff of read deserialization speed versus size of index and size of block (compression efficiency). More blocks, bigger index... Of course if you target the speed use 4K. 

Then your test will not produce millions of files and will become more valid. It will also target better that magic max_files, because there will not be that many files -> Faster query with less memory.

What we use a lot is SSTFileWriter. In parallel to random writes we are ingesting huge amount of preprocessed (sorted) data. It is much faster and if you do it right you will not impact compaction at all. So be careful how you define your keys. But with this I can ingest 8GB of data every 30 minutes with just using one core and couple of megabytes (use 1GB file sizes, because index of generating SST is in memory).

Sorry I did not have time to track all allocations for your test so just throwing more recommendations.


## Comment 473210640

reporter (NONE) · toktarev · 2019-03-15T09:08:34Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-473210640

@koldat thanks for this detailed help and explanations

## Comment 473212673

reporter (NONE) · toktarev · 2019-03-15T09:15:35Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-473212673

--What we use a lot is SSTFileWriter

Not it is clear why you don't experience a problems with memory growth.
Our system doesn't allow such architecture.

## Comment 473219190

other (CONTRIBUTOR) · koldat · 2019-03-15T09:36:52Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-473219190

Here is my last analysis. I used your test rewritten to Java. Jemalloc is dumping profiles every 1GB allocated with precision of 64B.
export LD_PRELOAD=/usr/lib/libjemalloc.so.2
export MALLOC_CONF=prof:true,lg_prof_interval:30,lg_prof_sample:6,prof_final:true

I have run test till 2400 files were created. It created almost same profiles (**no leak**):
-rw-r--r-- 1 1010 1010    3822 Mar 15 08:50 jeprof.62.0.f.heap
-rw-r--r-- 1 1010 1010 7875102 Mar 15 08:51 jeprof.63.0.i0.heap
-rw-r--r-- 1 1010 1010 7876326 Mar 15 08:51 jeprof.63.1.i1.heap
-rw-r--r-- 1 1010 1010 7884022 Mar 15 08:59 jeprof.63.10.i10.heap
-rw-r--r-- 1 1010 1010 7878004 Mar 15 09:00 jeprof.63.11.i11.heap
-rw-r--r-- 1 1010 1010 7880946 Mar 15 09:01 jeprof.63.12.i12.heap
-rw-r--r-- 1 1010 1010 7881767 Mar 15 09:02 jeprof.63.13.i13.heap
-rw-r--r-- 1 1010 1010 7891183 Mar 15 09:02 jeprof.63.14.i14.heap
-rw-r--r-- 1 1010 1010 7883031 Mar 15 09:03 jeprof.63.15.i15.heap
-rw-r--r-- 1 1010 1010 7877386 Mar 15 09:04 jeprof.63.16.i16.heap
-rw-r--r-- 1 1010 1010 7879674 Mar 15 09:05 jeprof.63.17.i17.heap
-rw-r--r-- 1 1010 1010 7887372 Mar 15 09:05 jeprof.63.18.i18.heap
-rw-r--r-- 1 1010 1010 7886440 Mar 15 09:06 jeprof.63.19.i19.heap
-rw-r--r-- 1 1010 1010 7875580 Mar 15 08:52 jeprof.63.2.i2.heap
-rw-r--r-- 1 1010 1010 7884272 Mar 15 09:06 jeprof.63.20.i20.heap
-rw-r--r-- 1 1010 1010 7879833 Mar 15 09:07 jeprof.63.21.i21.heap
-rw-r--r-- 1 1010 1010 7886892 Mar 15 09:08 jeprof.63.22.i22.heap
-rw-r--r-- 1 1010 1010 7881281 Mar 15 08:53 jeprof.63.3.i3.heap
-rw-r--r-- 1 1010 1010 7875448 Mar 15 08:53 jeprof.63.4.i4.heap
-rw-r--r-- 1 1010 1010 7895426 Mar 15 08:54 jeprof.63.5.i5.heap
-rw-r--r-- 1 1010 1010 7877721 Mar 15 08:55 jeprof.63.6.i6.heap
-rw-r--r-- 1 1010 1010 7881744 Mar 15 08:56 jeprof.63.7.i7.heap
-rw-r--r-- 1 1010 1010 7877553 Mar 15 08:57 jeprof.63.8.i8.heap
-rw-r--r-- 1 1010 1010 7877491 Mar 15 08:58 jeprof.63.9.i9.heap

jeprof --show_bytes --base jeprof.63.1.i1.heap --text /opt/jdk/bin/java jeprof.63.21.i21.heap > /tmp/app-profiling2.txt

This difference report is oscillating around 1.5MB. Thus no increase. Thus **no leak**.
 My source code:
```
public class RockTest {

    static {
        RocksDB.loadLibrary();
    }
    
    private static long count_sst_files(String dir) {
        File[] files = new File(dir).listFiles(new FileFilter() {
            @Override
            public boolean accept(File pathname) {
                return pathname.isFile() && pathname.getName().endsWith(".sst");
            }
        });
        return files == null ? 0 : files.length;
    }

    private static BlockBasedTableConfig makeDictionaryTableFactory() {
        BlockBasedTableConfig blockOpts = new BlockBasedTableConfig();
        blockOpts.setIndexType(IndexType.kTwoLevelIndexSearch);
        blockOpts.setBlockSize(4096);
        // blockOpts.partition_filters = true;
        // blockOpts.metadata_block_size = 4096;
        // blockOpts.setCcache_index_and_filter_blocks = true;
        // blockOpts.pin_top_level_index_and_filter = false;
        // blockOpts.pin_l0_filter_and_index_blocks_in_cache = false;
        // blockOpts.cache_index_and_filter_blocks_with_high_priority = true;
        // auto *pPolicy = rocksdb::NewBloomFilterPolicy(10, false);
        // auto filter_ptr = std::shared_ptr<const rocksdb::FilterPolicy>(pPolicy);
        // blockOpts.filter_policy = filter_ptr;
        blockOpts.setBlockCache(new LRUCache(1024 * 1024, 0, true));
        return blockOpts;
    }

    public static void main(String[] args) throws RocksDBException, IOException {
        String dir = "rocksdata";
        DBUtils.deleteDirectory(dir);

        long aSize = 1024 * 1024;

        Options options = new Options();

        options.setNumLevels(7);
        options.setWriteBufferSize(aSize);
        options.setMinWriteBufferNumberToMerge(2);
        options.setMaxWriteBufferNumber(6);
        options.setLevel0FileNumCompactionTrigger(2);
        options.setTargetFileSizeBase(aSize / 8);
        options.setMaxBackgroundCompactions(1);
        options.setCreateIfMissing(true);
        options.setCompressionType(CompressionType.NO_COMPRESSION);
        options.setStatistics(new Statistics());
        options.setMaxOpenFiles(2);
        options.setTableFormatConfig(makeDictionaryTableFactory());

        // open DB
        RocksDB db = RocksDB.open(options, dir);

        ByteBuffer key = ByteBuffer.allocateDirect(8 * 4);
        ByteBuffer value = ByteBuffer.allocateDirect(8);

        long max = 1000000000L;

        long begin = System.nanoTime();

        try (WriteBatch writeBatch = new WriteBatch();
            WriteOptions writeOptions = new WriteOptions();
            ReadOptions readOptions = new ReadOptions()) {
            for (long i = 0; i < max; i++) {
                key.clear();
                key.order(ByteOrder.BIG_ENDIAN);
                key.putLong(i);
                key.order(ByteOrder.LITTLE_ENDIAN);
                key.putLong(i + 1);
                key.putLong(i + 2);
                key.putLong(i + 3);
                key.flip();

                value.clear();
                value.putLong(max);
                value.flip();
                
                writeBatch.put(key, value);

                if (i % 1000 == 0) {
                    db.write(writeOptions, writeBatch);
                    writeBatch.clear();
                }

                key.clear();
                key.order(ByteOrder.BIG_ENDIAN);
                key.putLong(i - 1024);
                key.order(ByteOrder.LITTLE_ENDIAN);
                key.putLong(i + 1);
                key.putLong(i + 2);
                key.putLong(i + 3);
                key.flip();

                value.clear();
                db.get(readOptions, key, value);


                if (i % 1000000 == 0) {
                    long end = System.nanoTime();
                    double time = (end - begin) / 1000000000.0;
                    double delta = i / time;
                    long file_count = count_sst_files(dir);

                    System.out.println("Speed=" + delta + " File Count  " + file_count);
                }
            }
        }

        db.close();
        options.close();
    }
}
```


## Comment 473220348

reporter (NONE) · toktarev · 2019-03-15T09:40:30Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-473220348

--This difference report is oscillating around 1.5MB - Thus no leak

Actually no.

My test prints RSS peak.

RSS peak grows in my test.



## Comment 473220875

reporter (NONE) · toktarev · 2019-03-15T09:42:20Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-473220875

I don't use some additional stuff (Java, JeMalloc reports and so on).

1) Download last RocksDB (from master)
2) make static_lib with pre-installed JEMalloc
3) Running of C++ test which prints RSS and RSS peak.

## Comment 473240915

other (CONTRIBUTOR) · koldat · 2019-03-15T10:48:23Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-473240915

@toktarev RSS memory is memory that kernel allocated to process. Thus it is good indicator, but not precise. Use Total memory from jemalloc. It is sum of all malloc calls substracted by free calls. Everything else is fragmentation. 

## Comment 473252848

reporter (NONE) · toktarev · 2019-03-15T11:33:22Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-473252848

Wrong fragmentation makes OOM killer to kill process on many machines.
So ...

## Comment 473258084

other (CONTRIBUTOR) · koldat · 2019-03-15T11:54:54Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-473258084

@toktarev we should not blame Rocksdb for memory fragmentation. It is issue of memory allocation in general (glibc, jemalloc). Anyway, if you want to solve problem then you should help software with cooperative setup. I can damage any application out there including Linux/Windows itself if I want. I am not sure what this issue is about then. Leak is not there (you can clearly see that from jemalloc report.

## Comment 473259941

reporter (NONE) · toktarev · 2019-03-15T12:02:19Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-473259941

---@toktarev we should not blame Rocksdb for memory fragmentation

We should.

If process allocated char buffers of different sizes in many places it should take care about fragmentation problems.

Last RocksDB version even includes MemoryAllocator to resolve partly this issue.

I understand that you are contributor and that you loves RocksDB too much, but I don't experience here some cultural sentiments and just try to write high-quality software.










## Comment 473266470

other (CONTRIBUTOR) · koldat · 2019-03-15T12:26:21Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-473266470

> I understand that you are contributor and that you loves RocksDB too much, but I don't experience here some cultural sentiments and just try to write high-quality software.

I am not part of Rocksdb team. I was trying to be constructive to solve your issue where you are not, but OK I am giving up. Thanks

## Comment 473268339

reporter (NONE) · toktarev · 2019-03-15T12:32:19Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-473268339

--I am not part of Rocksdb team

i know, but I see label Contributor on your message.

--I was trying to be constructive to solve your issue where you are not

The only one constructive thing here is to detect which buffer do we allocate, what for 
and can we just pool them to get rid of fragmentation problems.









## Comment 517458025

other (NONE) · edtbl76 · 2019-08-01T21:05:37Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-517458025

[@koldat](https://github.com/facebook/rocksdb/issues/4112#issuecomment-473219190)

I'm actually seeing similar behavior. I'm also using the JNI. Can you provide the versions you tested with? 

Thanks in advance!



## Comment 517564358

other (CONTRIBUTOR) · koldat · 2019-08-02T06:03:17Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-517564358

There is not much difference, because it is not a leak. For Java I recommend you to use jemalloc and set fixed heap (same xmx and xms). Then play with configuration like I described. 

In Java you have to be careful to close all objects properly. These are tiny in Java so gc does not care about these much, but can hold a lot of native. So leaking several iterators can generate a lot of memory. You can modify base class of all objects and log in finalize method. That's how we unit test. We have logger and then call twice System.gc after everything is expected to be closed. That finalize should not find anything live. 



## Comment 517727864

other (NONE) · edtbl76 · 2019-08-02T14:45:27Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-517727864

Thanks, thats great info! There are quite a few scenarios where Rocks can suffer from weakly constrained memory growth based on configuration alone.  I completely agree that this more than likely isn't a leak. Do you know if anyone is using jemalloc as the default memory allocator in production? 

## Comment 517729650

other (CONTRIBUTOR) · koldat · 2019-08-02T14:50:10Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-517729650

Yes we are using that in production in all our services. It lowers process memory consumption and stabilize it, because it has smaller fragmentation than standard allocator especially when it runs together with JVM. 

## Comment 517730704

other (NONE) · edtbl76 · 2019-08-02T14:52:54Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-517730704

The fragmentation avoidance is exactly what I was considering. I imagine that works very well w/ partitioned indexes. Thanks again!

## Comment 567476616

other (NONE) · hcguersoy · 2019-12-19T12:49:55Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-567476616

> ...call twice System.gc after everything is expected to be closed. 

That sounds like vodoo. Measured the overhead you produce by calling `System.gc()` manually? You trigger two times a major gc. Things which I try to avoid.


## Comment 567524227

other (CONTRIBUTOR) · koldat · 2019-12-19T15:01:02Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-567524227

@hcguersoy This was suggestion **ONLY** for unit testing. There is no other way how to force GC to start cleanup to identify leaks. Then the class will log you everything that was not closed properly. You shouldn't get any output there if your application does not have leak. 

Of course it is not for production or normal runtime code...

## Comment 586540321

other (CONTRIBUTOR) · ajkr · 2020-02-15T01:39:12Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-586540321

> I used custom MemoryAllocator (pool of char *) + JeMalloc and see that there is one place which allocated and allocated - it is Arena's buffer for the list of files which should be compacted.
> 
> The more we write the more sst files we have and that buffer directly depends on the number of sst files.
> 
> this is why it allocates and allocates buffer of bigger size on each compaction.
> 
> On some projects it can be very slow growth.

Right now it is expected that RSS grows proportional to file count. There is currently no mechanism for spilling excess per-file metadata (e.g., `FileMetaData` objects) to disk and then later fetching them as needed for reads. This hasn't been problematic before since not a lot of users have reported such high file count together with such tight memory constraints.

A first step could be charge per-file metadata memory usage to block cache so that can be used as a global memory limit. A second step could be file metadata spilling/fetching. But I'd rather not implement the second step if the metadata size can be reduced sufficiently by making files larger. Is there a fundamental reason why they have to be so small/numerous? I can see why `write_buffer_size` is small, but why also `target_file_size_base`?

edit: also by running your example code I am seeing most memory growth coming from `rocksdb::VersionBuilder::Rep::Apply` and `std::__cxx11::basic_string::_M_construct` (there is high memory consumption for `rocksdb::Arena::AllocateNewBlock` but it tends to fluctuate up/down as memtables are filled/freed). To me this seems like growth comes from `FileMetaData`s and their smallest/largest keys, which are installed to the `VersionStorageInfo` during the apply phase at the end of each flush/compaction.

## Comment 586614339

reporter (NONE) · toktarev · 2020-02-15T16:12:36Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-586614339

----I can see why write_buffer_size is small, but why also target_file_size_base

Sorry but I don't understand such questions.

My point is: if we are widely-used application we should work as high-quality finite state machine.

It means that whatever setting user has - everything will work (+/- performance level).

If you have some parameters which lead to memory leak or memory leak caused by fragmentation - this is bad architecture.

I understand that many programmers don't agree with me because they are constructive and resolve such problems setting corresponding good parameters.

This is my strict point.

So if you have some ways to make RocksDB work as finite state machine with limited memory usage I am very glad and will cherry-pick corresponding commit once it will be implemented.





## Comment 586634950

other (CONTRIBUTOR) · ajkr · 2020-02-15T19:47:23Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-586634950

> If you have some parameters which lead to memory leak or memory leak caused by fragmentation - this is bad architecture.

I did not find leak or fragmentation to be the root cause. The root cause appears to be RocksDB holds per-file metadata in-memory while having a growing number of files. For most use cases, the per-file metadata component of RSS is negligible compared to memtable and block cache. But not for all use cases - thanks for pointing that out.

I agree it is an architectural limitation and will think about fixes. I do not think pursuing fragmentation avoidance will fundamentally improve things. Even if there were no fragmentation at all, in the current architecture there would still be a limit on a DB's file count given a memory budget - it'd be a higher limit, but I'm sure you could still find a way to tune the parameters to hit the limit.

## Comment 586635272

reporter (NONE) · toktarev · 2020-02-15T19:50:43Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-586635272

----I agree it is an architectural limitation

today - my day.

Thanks.

## Comment 586635643

reporter (NONE) · toktarev · 2020-02-15T19:54:32Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-586635643

--I did not find leak or fragmentation to be the root cause

actually it is and we had to tune gclib's ARENA properties to get rid of memory growth problem.

## Comment 586636473

other (CONTRIBUTOR) · ajkr · 2020-02-15T20:03:48Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-586636473

It fixed the problem in a DB that is growing in size? Or one that is a stable size?

## Comment 586636549

reporter (NONE) · toktarev · 2020-02-15T20:05:05Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-586636549

Yes, playing the game with ARENA properties and RocksDB's parameters (like a magic) we made it work.

## Comment 586636848

other (NONE) · vitalyisaev2 · 2020-02-15T20:08:21Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-586636848

@toktarev I think that you have such a lot of experience in debugging `RocksDB`, that many `RocksDB` users would be grateful if you could put it all together in a blog post or an article: what is your `RocksDB` use case, how did you tune the performance, discovered memory leak and finally fixed it. Personally for me this information is really important.

## Comment 586637106

reporter (NONE) · toktarev · 2020-02-15T20:10:48Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-586637106

I think that RocksDB team MUST make it work with any parameters without memory leaks.

It is REALLY possible.

Very very big memtable and little multiplier - is not a justification to say "Leak is good in this case".

But of course we don't pay money for RocksDB's usage - so we can only complain.



## Comment 596835344

other (NONE) · gaojieliu · 2020-03-10T00:01:14Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-596835344

> Yes, playing the game with ARENA properties and RocksDB's parameters (like a magic) we made it work.

@toktarev 
Could you share what you have done to make it work?

Thanks a lot

## Comment 623099973

other (NONE) · negbie · 2020-05-03T12:07:37Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-623099973

@gaojieliu I think he justed played the trial and error game around this https://github.com/prestodb/presto/issues/8993

## Comment 623100646

reporter (NONE) · toktarev · 2020-05-03T12:12:41Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-623100646

@negbie MALLOC_ARENA_MAX  tunning was one of our steps

The global RocksDB tunning helped mostly

Why do you think this is error game ?

## Comment 623101589

other (NONE) · negbie · 2020-05-03T12:20:27Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-623101589

Because it's not obvious at least it wasn't for me ;)

## Comment 623101966

reporter (NONE) · toktarev · 2020-05-03T12:23:22Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-623101966

Live and learn (век живи век учись)

## Comment 623147028

other (NONE) · gaojieliu · 2020-05-03T17:17:27Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-623147028

@negbie Thanks,  and we have tried to tune MALLOC_ARENA_MAX, and still see the growth, maybe the number we put is too large: 32, and we will continue to tune it.

@toktarev 
Do you mind to share the additional tuning of RocksDB configs?

Thanks

## Comment 623147508

reporter (NONE) · toktarev · 2020-05-03T17:20:10Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-623147508

@gaojieliu  
you should set MALLOC_ARENA_MAX=2 and check

--Do you mind to share the additional tuning of RocksDB configs?

I can't


## Comment 623147934

reporter (NONE) · toktarev · 2020-05-03T17:23:06Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-623147934

There is also malloc_trim command which also might help in same cases

## Comment 662029150

other (NONE) · patkivikram · 2020-07-21T18:23:20Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-662029150

We are still struggling with memory growth with the following settings 
`"write_buffer_size": 8388608,
    "max_write_buffer_number": 2,
    "block_cache_size": 8388608,
    "bloom_filter_size": 3,
    "max_open_files": 500,
    "block_cache_compressed_size": 8388608,
    "compression": rocksdb.CompressionType.lz4_compression`

Not sure what else are we missing. Using rocksdb 6.10.2 on centos 75

## Comment 709816850

other (NONE) · helyho · 2020-10-16T06:04:09Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-709816850

use jemalloc and config like this: 
cache_index_blocks=true
cache_index_and_filter_blocks_with_high_priority=true
pin_l0_filter_and_index_blocks_in_cache=false
partition_filters = true
index_type = rocksdb::BlockBasedTableOptions::IndexType::kTwoLevelIndexSearch

my process's rss almost hold on a stale size (centos8 kernel 4.18.0)

but on centos7(kernel 3.10.0) memory still grows

## Comment 710120725

reporter (NONE) · toktarev · 2020-10-16T15:37:20Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-710120725

@helyho I created PR which fixed problems with RAII in the RocksDB code

Nobody cares.

## Comment 743720302

other (CONTRIBUTOR) · cculianu · 2020-12-12T07:55:10Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-743720302

I also am seeing memory usage explode over time in my db.  Any ways to fix?

## Comment 743730955

reporter (NONE) · toktarev · 2020-12-12T09:41:58Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-743730955

It's time to call this ticket "THE WALL OF CRYING"

## Comment 777257804

other (NONE) · olegloktev · 2021-02-11T07:49:15Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-777257804

Hi, I am being struggled with growing memory issue for some time in my c++ project on linux. I found that using seek by iterators may cause more memory consuming but I'm pretty sure that I dispose it when it's not needed. I've tried to use jemalloc (set in LD_PRELOAD) and set rocks options mentioned in this thread but still see how memory usage increases. I will appreciate if someone can give some piece of advice how to tune rocks the right way

## Comment 777263311

other (NONE) · vitalyisaev2 · 2021-02-11T08:04:27Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-777263311

@toktarev 

> @helyho I created PR which fixed problems with RAII in the RocksDB code
> 
> Nobody cares.

Has it been already merged?

## Comment 777271272

reporter (NONE) · toktarev · 2021-02-11T08:20:18Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-777271272

@vitalyisaev2, no I closed my PR.

Review process is very long here.

## Comment 777272382

reporter (NONE) · toktarev · 2021-02-11T08:22:46Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-777272382

> Hi, I am being struggled with growing memory issue for some time in my c++ project on linux. I found that using seek by iterators may cause more memory consuming but I'm pretty sure that I dispose it when it's not needed. I've tried to use jemalloc (set in LD_PRELOAD) and set rocks options mentioned in this thread but still see how memory usage increases. I will appreciate if someone can give some piece of advice how to tune rocks the right way

Welcome to the club !

## Comment 777274478

other (CONTRIBUTOR) · koldat · 2021-02-11T08:26:54Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-777274478

@olegloktev go through this thread and my recommendations. I am not sure why @toktarev is so negative about this. I had never a problem with rocksdb guys, they always accepted my PRs. I have also found that memory grows was never a problem of rocksdb, but my setup. It is basically doing what it is asked for. No reason to cry about it. Please take a look on configuration examples of people here or show your I will try to help you.

## Comment 777277540

reporter (NONE) · toktarev · 2021-02-11T08:32:31Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-777277540

Sure, everything is fine, everybody should be positive, we should close this issue.

People don't have problem with RocksDB, they are just negative - this is their problem.

## Comment 777278039

reporter (NONE) · toktarev · 2021-02-11T08:33:46Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-777278039

---. I had never a problem with rocksdb guys, they always accepted my PRs

Sure, because you are positive :)

## Comment 777285535

other (CONTRIBUTOR) · koldat · 2021-02-11T08:49:34Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-777285535

@toktarev I am not positive guy in general. But just saying everything is bad and no one helps does not fix the issue. I was just saying to @olegloktev, please read what was written, learn from it and share your problem. Then I can try to help.

## Comment 777287450

reporter (NONE) · toktarev · 2021-02-11T08:52:56Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-777287450

Ok. let's be more clear.

I've already described some ways how to help with memory growth, but it looks like special hacks and workarounds.

From my point of view good quality means that memory will not grow if anyone will run original test without special configuration settings.

If no, and person needs to "dance around the tree" to make memory consumption stable - this is problem.

Of course this is just my opinion and RocksDB guys can have another one.




## Comment 777291935

other (CONTRIBUTOR) · koldat · 2021-02-11T09:00:45Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-777291935

We have like 40 instances running in a cluster where each is having roughly 1-2TB of data (each around 10k SST files). Here is example of memory stability over 30 days. It is a huge one (IO throughput like 1TB IO writes per day).

It is definitely not a "dance around". Just following recomendations.

![image](https://user-images.githubusercontent.com/16866502/107617244-d499d680-6c4f-11eb-92bd-68aee7e9afc0.png)


## Comment 777308421

other (CONTRIBUTOR) · cculianu · 2021-02-11T09:27:49Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-777308421

> Ok. let's be more clear.
> 
> I've already described some ways how to help with memory growth, but it looks like special hacks and workarounds.
> 
> From my point of view good quality means that memory will not grow if anyone will run original test without special configuration settings.
> 
> If no, and person needs to "dance around the tree" to make memory consumption stable - this is problem.
> 
> Of course this is just my opinion and RocksDB guys can have another one.

I agree with this. Quality software doesn't eat gigs of memory "by default" unless you do a special voodoo ritual to prevent it from doing so.  RocksDB is generally very fast and of high quality in some ways -- but not in the area of memory consumption.  There it could use improvement.  The fact that it's so difficult to constrain its memory use -- is a huge red flag.



## Comment 777312163

other (CONTRIBUTOR) · koldat · 2021-02-11T09:34:07Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-777312163

Sure, here is example of instance that is configured to not eat that much cache over the last 60 days. Again pretty stable. I am just saying it is all about configuration. Question is if defaults are good. But there is never configuration that works for all so authors of software needs to instruct library what they need.

![image](https://user-images.githubusercontent.com/16866502/107620120-80ddbc00-6c54-11eb-8ee0-730457e14a6d.png)


## Comment 777316384

reporter (NONE) · toktarev · 2021-02-11T09:41:19Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-777316384

@koldat 

Of course, I (together with team-mates) spent many time and made our RocksDB stable as well.

We are talking about quality.

## Comment 777321629

other (CONTRIBUTOR) · cculianu · 2021-02-11T09:49:52Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-777321629

> We are talking about quality.

This.  Quality in software.  Relevant talk by a game industry legend: https://youtu.be/pW-SOdj4Kkk

## Comment 777333983

reporter (NONE) · toktarev · 2021-02-11T10:09:58Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-777333983

Actually this is very big surprise for me that C++ application has such problems with memory.

I understand when Java application dies due to frequent GCs and so  on ..

But C++ application written in Silicon Valley, hmmm ....

## Comment 777579727

reporter (NONE) · toktarev · 2021-02-11T15:31:57Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-777579727

> > @gaojieliu
> > you should set MALLOC_ARENA_MAX=2 and check
> > --Do you mind to share the additional tuning of RocksDB configs?
> > I can't
> 
> Is it a commercial secret or you don't know for sure?
> If it is a secret (why?) or anybody knows how to fix it please don't hesitate to contact me by mail
> 
> ## [loktevoleg123@gmail.com](mailto:loktevoleg123@gmail.com)

Hello Oleg.

I can't share all steps we did (commercial secret).
But all necessary pieces of required steps where described in this issue.



## Comment 777666056

reporter (NONE) · toktarev · 2021-02-11T17:36:41Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-777666056

@koldat 
https://github.com/facebook/rocksdb/pull/7148/files

please, take a look at this change.
It is really possible that RocksDB will just hung on `lock`.

Of course no a big deal, but quality of the software = set of well written "not big deal" pieces.



## Comment 777676193

other (CONTRIBUTOR) · koldat · 2021-02-11T17:53:06Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-777676193

I am sorry, but I do not know anything about your "lock" issue and it is not related to this one so I would not mix it. I was commenting on memory usage that I was also fighting with on my start (due to lack of my knowledge). As you have your own view on that I am not able to help more here as I am just a happy user of this library. If someone will want to help with memory configuration please create new issue with fresh data. I am unsubscribing from this one.

## Comment 777688287

reporter (NONE) · toktarev · 2021-02-11T18:12:44Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-777688287

@koldat, ok up to you.
---As you have your own view on that
I don't need some help more, I just receive new and new complains being author of this issue.

Good luck !


## Comment 778027314

other (NONE) · olegloktev · 2021-02-12T07:24:17Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-778027314

Thank you guys for trying to help.
I've tried this config and as I see memory keeps growing slowly as it did
> use jemalloc and config like this:
> cache_index_blocks=true
> cache_index_and_filter_blocks_with_high_priority=true
> pin_l0_filter_and_index_blocks_in_cache=false
> partition_filters = true
> index_type = rocksdb::BlockBasedTableOptions::IndexType::kTwoLevelIndexSearch
> 
> my process's rss almost hold on a stale size (centos8 kernel 4.18.0)
> 
> but on centos7(kernel 3.10.0) memory still grows

Also I've tried to play with these settings: https://github.com/facebook/rocksdb/wiki/Partitioned-Index-Filters#how-to-use-it
with such configuration and aslo with cache settings set to false, not sure if it helps, looks like it doesn't.
Unfortunately it takes a long time to see if my changes have any impact on memory consuming and it is not so easy in my case to measure data streams to compare memory usage. 
Keeping searching, any further information is appreciated

## Comment 778040173

reporter (NONE) · toktarev · 2021-02-12T07:57:06Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-778040173

Oleg, did you try glibc + MALLOC_ARENA_MAX=2 ?

## Comment 800877412

other (NONE) · olegloktev · 2021-03-17T07:56:46Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-800877412

> Oleg, did you try glibc + MALLOC_ARENA_MAX=2 ?

Yes, I saw some decrease of memory consuming but it didn't help generally.
After some experience I may conclude that in my case the "issue" was caused by relatively small db size and rocks thought that it may grow significant and didn't want to free memory. So what helped me to see stable memory size consuming is using OptimizeForSmallDb which is recommended for DBs less than 1Gb which is my case. But I still keep MALLOC_ARENA_MAX=2 too because it helps to keep memory consuming level in lower bounds

## Comment 818858045

other (NONE) · linas · 2021-04-13T16:08:49Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-818858045

FYI, this appears to be a duplicate of  #3216  (I posted some notes there) I can add that the memory leak appears to be linearly associated with a file descriptor leak. I can count file descriptors by saying `lsof -p pid |grep sst |wc` and watch that number go up. I can force compaction to occur by closing the DB and reopening, and reclosing. After this, `lsof` shows that most of these files have been deleted: that is, `lsof -p pid |grep sst |grep deleted |wc` is now large.  

***Resolved:*** See my own comment https://github.com/facebook/rocksdb/issues/4112#issuecomment-818964308 immediately below.

(In my case, the compacted size of my db is 500 MBytes. Continuous editing of this DB will blow up RAM use to 200GBytes in an hour or two. There appears to be about 50MBytes RAM use per `sst` file, which is the same as the average `sst` file size ... Running with the default `ulimit -n 1024` will cause rdb to get an error on max open files at around 50GBytes ram usage. Increasing `ulimit -n 4096` allows processing to continue, and RAM usage to grow. My best guess is that each `sst` file is memory mapped, and that, even upon compaction/deletion, this memory mapping remains and eats RAM.  That is, this is *NOT* a malloc bug! This appears to be memory-mapping, file-handle management bug. At least, to me. ... and it turned out to be my bug. This is associated with my failure to delete the iterator returned by `NewIteratior()`)

## Comment 818964308

other (NONE) · linas · 2021-04-13T18:33:05Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-818964308

Update: after this comment: https://github.com/facebook/rocksdb/issues/3216#issuecomment-818893768 I came to realize that I have made a complete newbie mistake in my c++ code: rocks iterators are *NOT* smart pointers that self-delete when they go out of scope. They must be explicitly deleted! Upon fixing this complete-newbie mistake, all my disk and RAM usage problems go away! Wow!

I suggest that anyone else reading this take a good close look at their iterators, and review `<rocksdb/db.h>` for anything else that needs an explicit `delete`.

## Comment 938480737

other (NONE) · czs007 · 2021-10-08T09:11:25Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-938480737

hi guys, any update on this?

## Comment 973164594

other (CONTRIBUTOR) · ajkr · 2021-11-18T18:58:04Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-973164594

> hi guys, any update on this?

I am not sure what you are referring to specifically. We are working on limiting memory usage and updates on that will be in the release notes ("HISTORY.md").

## Comment 973207611

reporter (NONE) · toktarev · 2021-11-18T19:52:14Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-973207611

Thank you FaceBook team.

My complaints were not useless.

## Comment 973275019

other (CONTRIBUTOR) · cculianu · 2021-11-18T21:11:57Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-973275019

Just FYI -- My application https://github.com/cculianu/fulcrum , which makes heavy use of rocksdb runs great on Linux.  But on macOS and on Windows it leaks memory.  On Linux memory usage is rock solid at 800- 900MB even if the process is up for a month.  On Windows or macOS it grows and grows and grows so much that after a few days it's like 7-9 GB consumption and growing.  I'm pretty sure the leak is inside rocksdb.  Rest of app is tight.  Sadly, I lack the tools on macOS or Windows to actually run things like valgrind, etc.  

So yes -- kindly do search for leaks on macOS and/or Windows.  I suspect you have plenty.


## Comment 973276284

reporter (NONE) · toktarev · 2021-11-18T21:13:46Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-973276284

We had problems with runs on Linux as well, but after 1-2 weeks of stress testing.

## Comment 973278180

reporter (NONE) · toktarev · 2021-11-18T21:16:37Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-973278180

I suspect that the root cause is a bad collaboration with the internals of libc allocator, and that
caused problems with fragmentation.

At least fix using MALLOC_ARENA points on this.

Please, correct me if I am wrong.

## Comment 973279616

other (CONTRIBUTOR) · cculianu · 2021-11-18T21:18:46Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-973279616

Well I tried also with and without using jemalloc on both Windows and macOS.  Note that macOS I believe has a superior allocator to the standard glibc one..  I *rarely* see fragmentation issues on macOS.

I have no idea if it's fragmentation or if it's something else... really I do not.  Curious that on Linux it's fine..


## Comment 1774012354

other (NONE) · areyohrahul · 2023-10-22T06:50:30Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-1774012354

Hi @toktarev, were you able to find any solution for this?

I'm using RocksJni (8.5.4) and I'm seeing a constant growth in memory. All the things mentioned here were checked. 

My DB size on disk is 5 GB. Block cache size is 10 GB with strict limits. Memtables should take note more than 1GB.
Max open files are 100. Total files of my DB are 70-80 though.

I tried changing MAX_ARENA config. Then, I tried using jemalloc / tcmalloc as well. But nothing worked.

I'm closing all RocksObject from code also. From my observations, the issue is in the read flow only.


Been stuck on this for weeks now. Can someone please help?


## Comment 1774042534

other (CONTRIBUTOR) · cculianu · 2023-10-22T09:21:22Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-1774042534

For what it’s worth I’ve had great success by using jemalloc along with the following ENV var to get jemalloc to not use thread-local caches for allocated RAM (which wastes memory since each thread has effectively its own heap)

```MALLOC_CONF=tcache:false```

## Comment 1774082420

reporter (NONE) · toktarev · 2023-10-22T12:32:13Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-1774082420

> My DB size on disk is 5 GB. Block cache size is 10 GB with strict limits. Memtables should take note more than 1GB.

Hi @areyohrahul 

I understand your pain and remember my pain when I worked on this problem.
We closed this problem using MAX_ARENA config.

But i don't know why it is not a solution for you.

I can give you 2 advices here:

1) If you are a programmer - increase you deep expertise (what happens during memory allocation, when it happens (from OS point of view))
2) If you are a manager - hire smart programmer with deep system expertices.

Otherwise you will just experience pain and "guess on the coffee's heap".






## Comment 1776515059

other (NONE) · areyohrahul · 2023-10-24T04:18:08Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-1776515059

Hi @cculianu, how did you end up using jemalloc? Did you have to compile RocksDB again with some special flag? Or did you just change some setting for Java?

## Comment 1776558491

other (CONTRIBUTOR) · cculianu · 2023-10-24T05:26:22Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-1776558491

Oh I'm a C++ guy.. I don't use Java. There is a way to "force" the java runtime process to use jemalloc though without its knowledge..  via some LD_PRELOAD magic. If you install jemalloc, you can use LD_PRELOAD to force it.  See this guide:

https://github.com/jemalloc/jemalloc/wiki/Getting-Started

You can try that -- this assumes the java runtime uses `malloc()` though internally and doesnt' do some crazy stuff like calling the OS's `sbrk()` system call itself..


## Comment 1776587807

other (NONE) · areyohrahul · 2023-10-24T06:07:36Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-1776587807

Thanks @cculianu, this helps a lot. Will try this out. 

## Comment 1784876483

other (NONE) · areyohrahul · 2023-10-30T10:15:56Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-1784876483

Hey @toktarev, I tried changing the MAX_ARENA config but it didn't work. Can you share how did you analyse the source of the problem and how exactly did you change it?

Also, do you use JNI or CPP?

## Comment 1787807234

reporter (NONE) · toktarev · 2023-10-31T18:49:39Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-1787807234

@areyohrahul 

JNI (Java + CPP).

I remember that MAX_ARENA fixed memory growth in long runs.



## Comment 4250322813

other (NONE) · zmrgo · 2026-04-15T08:10:29Z · https://github.com/facebook/rocksdb/issues/4112#issuecomment-4250322813

@areyohrahul  you may use java 1.8, and the rocksdb version may lagger than 7.9, cause the upgrade of rocksdb since 7.9/jdk, rocksdb has changed its logical of release memory, you may try "try with resource" mode to use the object of rocksdb.
