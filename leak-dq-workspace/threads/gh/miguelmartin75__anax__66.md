# attempting free on address which was not malloc()-ed

- URL: https://github.com/miguelmartin75/anax/issues/66
- Repo: miguelmartin75/anax (language: C++)
- State: open; created 2016-03-08T13:22:05Z; status ok; passes main

## Issue body

reporter (NONE) · jvikstrom · 2016-03-08T13:22:05Z · https://github.com/miguelmartin75/anax/issues/66

I'm getting this error:
# 

==13005==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x62e00000a040 in thread T0
    #0 0x7f1f5077d517 in operator delete(void_) (/usr/lib/x86_64-linux-gnu/libasan.so.1+0x55517)
    #1 0x418b13 in __gnu_cxx::new_allocatoranax::World::EntityAttributes::Attribute::deallocate(anax::World::EntityAttributes::Attribute_, unsigned long) /usr/include/c++/4.9/ext/new_allocator.h:110
    #2 0x418560 in std::allocator_traitsstd::allocator<anax::World::EntityAttributes::Attribute >::deallocate(std::allocatoranax::World::EntityAttributes::Attribute&, anax::World::EntityAttributes::Attribute_, unsigned long) /usr/include/c++/4.9/bits/alloc_traits.h:383
    #3 0x418169 in std::_Vector_base<anax::World::EntityAttributes::Attribute, std::allocator<anax::World::EntityAttributes::Attribute> >::_M_deallocate(anax::World::EntityAttributes::Attribute_, unsigned long) /usr/include/c++/4.9/bits/stl_vector.h:178
    #4 0x417923 in std::_Vector_base<anax::World::EntityAttributes::Attribute, std::allocator<anax::World::EntityAttributes::Attribute> >::~_Vector_base() /usr/include/c++/4.9/bits/stl_vector.h:160
    #5 0x417359 in std::vector<anax::World::EntityAttributes::Attribute, std::allocator<anax::World::EntityAttributes::Attribute> >::~vector() /usr/include/c++/4.9/bits/stl_vector.h:425
    #6 0x417097 in anax::World::EntityAttributes::~EntityAttributes() /usr/local/include/anax/World.hpp:176
    #7 0x41711d in anax::World::~World() /usr/local/include/anax/World.hpp:45
    #8 0x416f52 in main /PATH2/main.cpp:6
    #9 0x7f1f4f38bec4 in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x21ec4)
    #10 0x416de8 (/BUILDDIR/PROJECTNAME+0x416de8)

0x62e00000a040 is located 0 bytes to the right of 40000-byte region [0x62e000000400,0x62e00000a040)
allocated by thread T0 here:
    #0 0x7f1f5077d09f in operator new(unsigned long) (/usr/lib/x86_64-linux-gnu/libasan.so.1+0x5509f)
    #1 0x7f1f4fcf6561 in __gnu_cxx::new_allocatoranax::World::EntityAttributes::Attribute::allocate(unsigned long, void const*) /usr/include/c++/4.8/ext/new_allocator.h:104
    #2 0x7f1f4fcf57fc in std::_Vector_base<anax::World::EntityAttributes::Attribute, std::allocator<anax::World::EntityAttributes::Attribute> >::_M_allocate(unsigned long) /usr/include/c++/4.8/bits/stl_vector.h:168
    #3 0x7f1f4fcf5644 in std::_Vector_base<anax::World::EntityAttributes::Attribute, std::allocator<anax::World::EntityAttributes::Attribute> >::_M_create_storage(unsigned long) /usr/include/c++/4.8/bits/stl_vector.h:181
    #4 0x7f1f4fcf4478 in std::_Vector_base<anax::World::EntityAttributes::Attribute, std::allocator<anax::World::EntityAttributes::Attribute> >::_Vector_base(unsigned long, std::allocatoranax::World::EntityAttributes::Attribute const&) /usr/include/c++/4.8/bits/stl_vector.h:136
    #5 0x7f1f4fcf3989 in std::vector<anax::World::EntityAttributes::Attribute, std::allocator<anax::World::EntityAttributes::Attribute> >::vector(unsigned long, std::allocatoranax::World::EntityAttributes::Attribute const&) /usr/include/c++/4.8/bits/stl_vector.h:270
    #6 0x7f1f4fcf36d8 in anax::World::EntityAttributes::EntityAttributes(unsigned long) /PATH1/anax/include/anax/World.hpp:194
    #7 0x7f1f4fcf2830 in anax::World::World(unsigned long) /PATH1/anax/src/anax/World.cpp:46
    #8 0x7f1f4fcf27b6 in anax::World::World() /PATH1/anax/src/anax/World.cpp:40
    #9 0x416f43 in main /PATH2/main.cpp:6
    #10 0x7f1f4f38bec4 in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x21ec4)

SUMMARY: AddressSanitizer: bad-free ??:0 operator delete(void*)
==13005==ABORTING

When using this code:
`#include <anax/anax.hpp>
int main()
{

   // anax::World *world = new anax::World;
    anax::World world;
}`

So I don't know what to do.


## Comment 194037137

maintainer (OWNER) · miguelmartin75 · 2016-03-09T00:32:27Z · https://github.com/miguelmartin75/anax/issues/66#issuecomment-194037137

Interesting, I'm going to have to see if I can reproduce on Linux. I wouldn't have expected that this would occur. 

What compiler are you using? GCC 4.9? 


## Comment 194244495

reporter (NONE) · jvikstrom · 2016-03-09T11:11:29Z · https://github.com/miguelmartin75/anax/issues/66#issuecomment-194244495

gcc (Ubuntu 4.9.2-0ubuntu1~14.04) 4.9.2
I'm also using linux. VERSION="14.04.3 LTS, Trusty Tahr"
(It's Mint 17)


## Comment 194246733

reporter (NONE) · jvikstrom · 2016-03-09T11:17:36Z · https://github.com/miguelmartin75/anax/issues/66#issuecomment-194246733

/usr/include/c++/4.9/bits/unique_ptr.h:236: error: undefined reference to `anax::World::SystemDeleter::operator()(anax::detail::BaseSystem*) const'

That is the error I get when doing this.

`
    #include <anax/anax.hpp>
    int main()
    {

```
    anax::World *world = new anax::World;
    delete world;
    //anax::World world;
}
```

`

I must have done something wrong when I installed anax, right?


## Comment 195341844

maintainer (OWNER) · miguelmartin75 · 2016-03-11T12:06:45Z · https://github.com/miguelmartin75/anax/issues/66#issuecomment-195341844

Hm before you could compile your program and now you can't? Try this:

```
c++ main.cpp -lanax -std=c++11
```


## Comment 195480016

reporter (NONE) · jvikstrom · 2016-03-11T18:02:06Z · https://github.com/miguelmartin75/anax/issues/66#issuecomment-195480016

./bin: error while loading shared libraries: libanax.so.2: cannot open shared object file: No such file or directory

I have like zero experience linking libraries using the terminal as I usually only use cmake.

But I suppose that error message means I didn't install it correctly.


## Comment 195661664

maintainer (OWNER) · miguelmartin75 · 2016-03-12T05:12:43Z · https://github.com/miguelmartin75/anax/issues/66#issuecomment-195661664

That message means it can't find libanax.so.2. You have to give the compiler the path to where libanax is located, if installed by cmake this will likely be in /usr/local/lib. e.g.

```
c++ main.cpp -L/usr/local/lib -lanax -std=c++11
```


## Comment 195980041

reporter (NONE) · jvikstrom · 2016-03-13T15:37:30Z · https://github.com/miguelmartin75/anax/issues/66#issuecomment-195980041

I had to add the path to anax to my LD_LIBRARY_PATH, then it worked.
It compiled successfully and ran without segmentation faults. (This is when I compiled through the terminal)


## Comment 196838388

maintainer (OWNER) · miguelmartin75 · 2016-03-15T14:10:56Z · https://github.com/miguelmartin75/anax/issues/66#issuecomment-196838388

If you compile with `-fsanitize=address` does it produce the same error you were describing?


## Comment 197401469

reporter (NONE) · jvikstrom · 2016-03-16T16:08:42Z · https://github.com/miguelmartin75/anax/issues/66#issuecomment-197401469

Unless doing these two commands:
LD_LIBRARY_PATH=/usr/local/lib
export LD_LIBRARY_PATH

it gives me this error when running it: ./bin: error while loading shared libraries: libanax.so.2: cannot open shared object file: No such file or directory

Otherwise it runs and compiles fine when I compile through the terminal.


## Comment 202910154

reporter (NONE) · jvikstrom · 2016-03-29T14:08:30Z · https://github.com/miguelmartin75/anax/issues/66#issuecomment-202910154

The problem seemed to be was that I linked ${ANAX_LIBRARY_DEBUG} instead of ${ANAX_LIBRARY_RELEASE} in cmake. When I linked the release one it works.

