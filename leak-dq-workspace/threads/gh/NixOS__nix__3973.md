# free(): invalid pointer

- URL: https://github.com/NixOS/nix/issues/3973
- Repo: NixOS/nix (language: C++)
- State: open; created 2020-08-31T12:54:31Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · nmattia · 2020-08-31T12:54:31Z · https://github.com/NixOS/nix/issues/3973

**Describe the bug**

I'm getting a core dump when running `nix-instantiate`:

``` shell
$ nix-instantiate foo.nix -A some.attribute
free(): invalid pointer
Aborted (core dumped)
```

Unfortunately I can't share the code, but it seems to be happening when running a derivation that's then imported (IFD) but I'm not sure if that actually matters. `-vv` doesn't show anything suspicious. `nix-store --realize`ing the `.drv` works fine so I guess the problem is not in the drv's build.

After tweaking the Nix code a bit, I get a few more errors:

``` shell
$ nix-instantiate foo.nix -A some-attribute
munmap_chunk(): invalid pointer
Aborted (core dumped)
```

and sometimes

``` shell
Segmentation fault (core dumped)
```

(got that one in the repl)

Happy to share as much info as I can, I'll try to boil it down to a snippet I can share.

``` shell
$ nix --version
nix (Nix) 2.4pre20200721_ff314f1
```

I'll try to reproduce.

## Comment 791500555

other (NONE) · stale[bot] · 2021-03-05T15:43:22Z · https://github.com/NixOS/nix/issues/3973#issuecomment-791500555

I marked this as stale due to inactivity. &rarr; [More info](https://github.com/NixOS/nix/blob/master/.github/STALE-BOT.md)


## Comment 1104706494

other (NONE) · stale[bot] · 2022-04-21T04:52:35Z · https://github.com/NixOS/nix/issues/3973#issuecomment-1104706494

I closed this issue due to inactivity. &rarr; [More info](https://github.com/NixOS/nix/blob/master/.github/STALE-BOT.md)


## Comment 2125629902

other (NONE) · I-Al-Istannen · 2024-05-22T19:49:26Z · https://github.com/NixOS/nix/issues/3973#issuecomment-2125629902

I have the same error when running `nix build`. GDB gives me the following backtrace

<details>
<summary>Backtrace</summary>


```
#0  __pthread_kill_implementation (threadid=<optimized out>, signo=signo@entry=6, no_tid=no_tid@entry=0) at pthread_kill.c:44
#1  0x00007ffff72a8eb3 in __pthread_kill_internal (threadid=<optimized out>, signo=6) at pthread_kill.c:78
#2  0x00007ffff7250a30 in __GI_raise (sig=sig@entry=6) at ../sysdeps/posix/raise.c:26
#3  0x00007ffff72384c3 in __GI_abort () at abort.c:79
#4  0x00007ffff7239354 in __libc_message_impl (fmt=fmt@entry=0x7ffff73c22ea "%s\n") at ../sysdeps/posix/libc_fatal.c:132
#5  0x00007ffff72b3085 in malloc_printerr (str=str@entry=0x7ffff73c006b "free(): invalid pointer") at malloc.c:5772
#6  0x00007ffff72b549c in _int_free (av=<optimized out>, p=p@entry=0x55555c964a60, have_lock=have_lock@entry=0) at malloc.c:4507
#7  0x00007ffff72b7dae in __GI___libc_free (mem=0x55555c964a70) at malloc.c:3398
#8  0x00007ffff74ac78a in operator delete (ptr=<optimized out>) at /usr/src/debug/gcc/gcc/libstdc++-v3/libsupc++/del_op.cc:49
#9  0x00007ffff74ac79a in operator delete (ptr=<optimized out>) at /usr/src/debug/gcc/gcc/libstdc++-v3/libsupc++/del_ops.cc:33
#10 0x00007ffff77945f0 in std::__new_allocator<char>::deallocate (this=0x55555c983c80, __p=<optimized out>, __n=<optimized out>) at /usr/include/c++/14.1.1/bits/new_allocator.h:172
#11 std::allocator<char>::deallocate (this=0x55555c983c80, __p=<optimized out>, __n=<optimized out>) at /usr/include/c++/14.1.1/bits/allocator.h:208
#12 std::allocator_traits<std::allocator<char> >::deallocate (__a=..., __p=<optimized out>, __n=<optimized out>) at /usr/include/c++/14.1.1/bits/alloc_traits.h:513
#13 std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::_M_destroy (this=0x55555c983c80, __size=<optimized out>)
    at /usr/include/c++/14.1.1/bits/basic_string.h:294
#14 std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::_M_dispose (this=0x55555c983c80) at /usr/include/c++/14.1.1/bits/basic_string.h:288
#15 std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::~basic_string (this=<optimized out>, this=<optimized out>)
    at /usr/include/c++/14.1.1/bits/basic_string.h:809
#16 nix::PosixSourceAccessor::cachedLstat (this=this@entry=0x555555816850, path=...) at src/libutil/posix-source-accessor.cc:111
#17 0x00007ffff7794d63 in nix::PosixSourceAccessor::maybeLstat (this=0x555555816850, path=...) at src/libutil/posix-source-accessor.cc:116
#18 0x00007ffff7f05e08 in nix::FilteringInputAccessor::maybeLstat (this=0x5555558168f0, path=...) at src/libfetchers/filtering-input-accessor.cc:19
#19 0x00007ffff779995b in nix::SourceAccessor::lstat (this=0x5555558169b0, path=...) at src/libutil/source-accessor.cc:53
#20 0x00007ffff7799c49 in nix::SourcePath::lstat (this=<optimized out>) at /usr/include/c++/14.1.1/bits/shared_ptr_base.h:1350
#21 0x00007ffff7d08f1c in nix::EvalState::callPathFilter (this=0x555555810c10, filterFun=0x55555c952ef0, path=...,
    pathArg="/nix/store/57rsy3z79kvxah2l4j13bjwpsgxkbhby-source/pkgs/development/tools/yarn2nix-moretea/yarn2nix/lib/fixPkgAddMissingSha1.js", pos=...)
    at src/libexpr/primops.cc:2244
#22 0x00007ffff7d24cf9 in operator() (p=..., __closure=0x55555c9569b0) at /usr/include/c++/14.1.1/bits/char_traits.h:350
#23 std::__invoke_impl<bool, nix::addPath(EvalState&, PosIdx, std::string_view, SourcePath, Value*, FileIngestionMethod, std::optional<Hash>, Value&, const NixStringContext&)::<lambda(const nix::Path&)>&, const std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&> (__f=...) at /usr/include/c++/14.1.1/bits/invoke.h:61
#24 std::__invoke_r<bool, nix::addPath(EvalState&, PosIdx, std::string_view, SourcePath, Value*, FileIngestionMethod, std::optional<Hash>, Value&, const NixStringContext&)::<lambda(const nix::Path&)>&, const std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&> (__fn=...) at /usr/include/c++/14.1.1/bits/invoke.h:114
#25 std::_Function_handler<bool(const std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&), nix::addPath(EvalState&, PosIdx, std::string_view, SourcePath, Value*, FileIngestionMethod, std::optional<Hash>, Value&, const NixStringContext&)::<lambda(const nix::Path&)> >::_M_invoke(const std::_Any_data &, const std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > &) (__functor=..., __args#0=...) at /usr/include/c++/14.1.1/bits/std_function.h:290
#26 0x00007ffff7736587 in std::function<bool (std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)>::operator()(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) const (this=0x7ffffffed560,
    __args#0="/nix/store/57rsy3z79kvxah2l4j13bjwpsgxkbhby-source/pkgs/development/tools/yarn2nix-moretea/yarn2nix/lib/fixPkgAddMissingSha1.js")
    at /usr/include/c++/14.1.1/bits/std_function.h:591
#27 operator() (__closure=<optimized out>, path=...) at src/libutil/archive.cc:91
#28 0x00007ffff773668f in std::function<void (nix::CanonPath const&)>::operator()(nix::CanonPath const&) const (this=0x55555c984860, __args#0=...)
    at /usr/include/c++/14.1.1/bits/std_function.h:591
#29 operator() (__closure=<optimized out>, path=...) at src/libutil/archive.cc:93
#30 0x00007ffff7735764 in std::function<void (nix::CanonPath const&)>::operator()(nix::CanonPath const&) const (this=0x55555c984860, __args#0=...)
    at /usr/include/c++/14.1.1/bits/std_function.h:591
#31 nix::SourceAccessor::dumpPath(nix::CanonPath const&, nix::Sink&, std::function<bool (std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)>&) (
    this=<optimized out>, path=..., sink=..., filter=...) at src/libutil/archive.cc:107
#32 0x00007ffff778fe2b in std::function<void (nix::CanonPath const&)>::operator()(nix::CanonPath const&) const (this=0x55555c94b558, __args#0=...)
    at /usr/include/c++/14.1.1/bits/std_function.h:591
#33 operator() (__closure=<synthetic pointer>, yield=...) at src/libutil/serialise.cc:315
#34 operator() (__closure=<optimized out>, c=...) at /usr/include/boost/coroutine2/detail/pull_control_block_cc.ipp:88
#35 std::__invoke_impl<boost::context::fiber, boost::coroutines2::detail::pull_coroutine<std::__cxx11::basic_string<char> >::control_block::control_block<nix::VirtualStackAllocator, nix::sinkToSource(std::function<void(Sink&)>, std::function<void()>)::SinkToSource::read(char*, size_t)::<lambda(boost::coroutines2::coroutine<std::__cxx11::basic_string<char> >::push_type&)> >(boost::context::preallocated, nix::VirtualStackAllocator&&, nix::sinkToSource(std::function<void(Sink&)>, std::function<void()>)::SinkToSource::read(char*, size_t)::<lambda(boost::coroutines2::coroutine<std::__cxx11::basic_string<char> >::push_type&)>&&)::<lambda(boost::context::fiber&&)>&, boost::context::fiber> (__f=...)
    at /usr/include/c++/14.1.1/bits/invoke.h:61
#36 std::__invoke<boost::coroutines2::detail::pull_coroutine<std::__cxx11::basic_string<char> >::control_block::control_block<nix::VirtualStackAllocator, nix::sinkToSource(std::function<void(Sink&)>, std::function<void()>)::SinkToSource::read(char*, size_t)::<lambda(boost::coroutines2::coroutine<std::__cxx11::basic_string<char> >::push_type&)> >(boost::context::preallocated, nix::VirtualStackAllocator&&, nix::sinkToSource(std::function<void(Sink&)>, std::function<void()>)::SinkToSource::read(char*, size_t)::<lambda(boost::coroutines2::coroutine<std::__cxx11::basic_string<char> >::push_type&)>&&)::<lambda(boost::context::fiber&&)>&, boost::context::fiber> (__fn=...) at /usr/include/c++/14.1.1/bits/invoke.h:97
#37 std::invoke<boost::coroutines2::detail::pull_coroutine<std::__cxx11::basic_string<char> >::control_block::control_block<nix::VirtualStackAllocator, nix::sinkToSource(std::function<void(Sink&)>, std::function<void()>)::SinkToSource::read(char*, size_t)::<lambda(boost::coroutines2::coroutine<std::__cxx11::basic_string<char> >::push_type&)> >(boost::context::preallocated, nix::VirtualStackAllocator&&, nix::sinkToSource(std::function<void(Sink&)>, std::function<void()>)::SinkToSource::read(char*, size_t)::<lambda(boost::coroutines2::coroutine<std::__cxx11::basic_string<char> >::push_type&)>&&)::<lambda(boost::context::fiber&&)>&, boost::context::fiber> (__fn=...) at /usr/include/c++/14.1.1/functional:121
#38 boost::context::detail::fiber_record<boost::context::fiber, nix::VirtualStackAllocator, boost::coroutines2::detail::pull_coroutine<std::__cxx11::basic_string<char> >::control_block::control_block<nix::VirtualStackAllocator, nix::sinkToSource(std::function<void(Sink&)>, std::function<void()>)::SinkToSource::read(char*, size_t)::<lambda(boost::coroutines2::coroutine<std::__cxx11::basic_string<char> >::push_type&)> >(boost::context::preallocated, nix::VirtualStackAllocator&&, nix::sinkToSource(std::function<void(Sink&)>, std::function<void()>)::SinkToSource::read(char*, size_t)::<lambda(boost::coroutines2::coroutine<std::__cxx11::basic_string<char> >::push_type&)>&&)::<lambda(boost::context::fiber&&)> >::run (
    this=<optimized out>, fctx=<optimized out>) at /usr/include/boost/context/fiber_fcontext.hpp:157
#39 boost::context::detail::fiber_entry<boost::context::detail::fiber_record<boost::context::fiber, nix::VirtualStackAllocator, boost::coroutines2::detail::pull_coroutine<std::__cxx11::basic_string<char> >::control_block::control_block<nix::VirtualStackAllocator, nix::sinkToSource(std::function<void(Sink&)>, std::function<void()>)::SinkToSource::read(char*, size_t)::<lambda(boost::coroutines2::coroutine<std::__cxx11::basic_string<char> >::push_type&)> >(boost::context::preallocated, nix::VirtualStackAllocator&&, nix::sinkToSource(std::function<void(Sink&)>, std::function<void()>)::SinkToSource::read(char*, size_t)::<lambda(boost::coroutines2::coroutine<std::__cxx11::basic_string<char> >::push_type&)>&&)::<lambda(boost::context::fiber&&)> > >(boost::context::detail::transfer_t) (t=...) at /usr/include/boost/context/fiber_fcontext.hpp:97
#40 0x00007ffff7e1f157 in make_fcontext () from /usr/lib/libboost_context.so.1.83.0
#41 0x0000000000000000 in ?? ()
```


</details>

My setup is the following:

```nix
// flake.nix
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      forAllSystems = nixpkgs.lib.genAttrs nixpkgs.lib.systems.flakeExposed;
    in
    rec {
      packages = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        rec {
          default = frontend;
          frontend = pkgs.mkYarnPackage rec {
            pname = "screeny";
            version = "0.0.1";

            src = ./hey;

            buildPhase = ''
              export HOME=$(mktemp -d)
              yarn --offline build
              mkdir "$out"
              cp -r dist/* "$out/"
            '';
            outputHash = "";
            outputHashMode = "recursive";
            outputHashAlgo = "sha256";
          };
        }
      );
    };
}
```

And then a folder `hey` with the following two files.
`hey/yarn.lock`
```
# yarn.lock
# THIS IS AN AUTOGENERATED FILE. DO NOT EDIT THIS FILE DIRECTLY.
# yarn lockfile v1


```
and the `hey/package.json`
```
{
  "name": "frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "devDependencies": {
  }
}
```

## Comment 2126010025

maintainer (MEMBER) · cole-h · 2024-05-23T01:03:20Z · https://github.com/NixOS/nix/issues/3973#issuecomment-2126010025

Could you also paste the `flake.lock`, the version of Nix you're using, and what kind of machine you're on?

Using `nix (Nix) 2.22.0pre20240320_7d2ead5` I can't reproduce; I just see a build failure:

```
$ wl-paste | tail -n +2 > flake.nix
$ mkdir hey
$ wl-paste > hey/yarn.lock
$ wl-paste > hey/package.json
$ nix build
warning: creating lock file '/tmp/tmp.Tsw24SqnJa/flake.lock':
• Added input 'nixpkgs':
    'github:NixOS/nixpkgs/5710852ba686cc1fd0d3b8e22b3117d43ba374c2?narHash=sha256-8BO3B7e3BiyIDsaKA0tY8O88rClYRTjvAp66y%2BVBUeU%3D' (2024-05-21)
warning: found empty hash, assuming 'sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='
error: builder for '/nix/store/r22ka31mwsph8pinf24bfy09x437j711-frontend-0.0.1.drv' failed with exit code 127;
       last 12 log lines:
       > Running phase: unpackPhase
       > unpacking source archive /nix/store/nzl6cwllxwgzkfipdpjym4ipfjv8ybp8-hey
       > source root is hey
       > Running phase: patchPhase
       > Running phase: updateAutotoolsGnuConfigScriptsPhase
       > Running phase: configurePhase
       > Running phase: buildPhase
yarn run v1.22.22
$ tsc && vite build
       > /bin/sh: tsc: not found
error Command failed with exit code 127.
info Visit https://yarnpkg.com/en/docs/cli/run for documentation about this command.
       For full logs, run 'nix log /nix/store/r22ka31mwsph8pinf24bfy09x437j711-frontend-0.0.1.drv'.
```

## Comment 2126698452

other (NONE) · I-Al-Istannen · 2024-05-23T09:54:01Z · https://github.com/NixOS/nix/issues/3973#issuecomment-2126698452

Sure :)

```
❯ nix --version
nix (Nix) 2.22.1
❯ cat /etc/os-release
NAME="Arch Linux"
PRETTY_NAME="Arch Linux"
ID=arch
BUILD_ID=rolling
ANSI_COLOR="38;2;23;147;209"
HOME_URL="https://archlinux.org/"
DOCUMENTATION_URL="https://wiki.archlinux.org/"
SUPPORT_URL="https://bbs.archlinux.org/"
BUG_REPORT_URL="https://gitlab.archlinux.org/groups/archlinux/-/issues"
PRIVACY_POLICY_URL="https://terms.archlinux.org/docs/privacy-policy/"
LOGO=archlinux-logo
❯ uname -a
Linux nidhogg 6.8.9-arch1-2 #1 SMP PREEMPT_DYNAMIC Tue, 07 May 2024 21:35:54 +0000 x86_64 GNU/Linux
```

```json
{
  "nodes": {
    "nixpkgs": {
      "locked": {
        "lastModified": 1716330097,
        "narHash": "sha256-8BO3B7e3BiyIDsaKA0tY8O88rClYRTjvAp66y+VBUeU=",
        "owner": "NixOS",
        "repo": "nixpkgs",
        "rev": "5710852ba686cc1fd0d3b8e22b3117d43ba374c2",
        "type": "github"
      },
      "original": {
        "owner": "NixOS",
        "ref": "nixos-unstable",
        "repo": "nixpkgs",
        "type": "github"
      }
    },
    "root": {
      "inputs": {
        "nixpkgs": "nixpkgs"
      }
    }
  },
  "root": "root",
  "version": 7
}
```

## Comment 2323013437

other (NONE) · voidus · 2024-08-31T18:50:41Z · https://github.com/NixOS/nix/issues/3973#issuecomment-2323013437

I have similar issues on arch linux in a reproducible way, I don't want to add too much noise here but if needed I'd be happy to participate in debugging. In the meantime, `nix shell nixpkgs#nix` is a good workaround.

Notably, I am also using `mkYarnPackage`.

I am getting different errors re-running the build:

- IOT instruction (core dumped)
- segmentation fault (core dumped)
- corrupted size vs. prev_size
- free(): invalid pointer

Building multiple derivations in a single command seems to report a random one, a single derivation always seems to be resulting in `segmentation fault`

<details><summary>Backtrace running <code>gdb --args nix build .#foo .#bar .#baz</code></summary>

```gdb
Thread 1 "nix" received signal SIGSEGV, Segmentation fault.
0x00007ffff7c9d1b7 in nix::EvalState::eqValues(nix::Value&, nix::Value&, nix::PosIdx, std::basic_string_view<char, std::char_traits<char> >) () from /usr/lib/libnixexpr.so
(gdb) bt
#0  0x00007ffff7c9d1b7 in nix::EvalState::eqValues(nix::Value&, nix::Value&, nix::PosIdx, std::basic_string_view<char, std::char_traits<char> >) () from /usr/lib/libnixexpr.so
#1  0x00007ffff7d18018 in ?? () from /usr/lib/libnixexpr.so
#2  0x00007ffff7c99517 in nix::EvalState::callFunction(nix::Value&, unsigned long, nix::Value**, nix::Value&, nix::PosIdx) () from /usr/lib/libnixexpr.so
#3  0x00007ffff7c9ba76 in nix::ExprCall::eval(nix::EvalState&, nix::Env&, nix::Value&) () from /usr/lib/libnixexpr.so
#4  0x00007ffff7c97221 in ?? () from /usr/lib/libnixexpr.so
#5  0x00007ffff7c97fd2 in nix::ExprOpAnd::eval(nix::EvalState&, nix::Env&, nix::Value&) () from /usr/lib/libnixexpr.so
#6  0x00007ffff7c97221 in ?? () from /usr/lib/libnixexpr.so
#7  0x00007ffff7c9806a in nix::ExprOpOr::eval(nix::EvalState&, nix::Env&, nix::Value&) () from /usr/lib/libnixexpr.so
#8  0x00007ffff7c95e70 in nix::ExprLet::eval(nix::EvalState&, nix::Env&, nix::Value&) () from /usr/lib/libnixexpr.so
#9  0x00007ffff7c993fe in nix::EvalState::callFunction(nix::Value&, unsigned long, nix::Value**, nix::Value&, nix::PosIdx) () from /usr/lib/libnixexpr.so
#10 0x00007ffff7d116b5 in nix::EvalState::callPathFilter(nix::Value*, nix::SourcePath const&, std::basic_string_view<char, std::char_traits<char> >, nix::PosIdx) () from /usr/lib/libnixexpr.so
#11 0x00007ffff7d244a9 in ?? () from /usr/lib/libnixexpr.so
#12 0x00007ffff7731e57 in ?? () from /usr/lib/libnixutil.so
#13 0x00007ffff77310b4 in nix::SourceAccessor::dumpPath(nix::CanonPath const&, nix::Sink&, std::function<bool (std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)>&) () from /usr/lib/libnixutil.so
#14 0x00007ffff778beeb in ?? () from /usr/lib/libnixutil.so
#15 0x00007ffff7e23157 in make_fcontext () from /usr/lib/libboost_context.so.1.83.0
#16 0x38782b7436416f41 in ?? ()
#17 0x70714157724c4d39 in ?? ()
#18 0x3d3d516938454466 in ?? ()
#19 0x6e6570656420200a in ?? ()
#20 0x3a736569636e6564 in ?? ()
#21 0x636361202020200a in ?? ()
#22 0x317e222073747065 in ?? ()
#23 0x20200a22352e332e in ?? ()
#24 0x0000000000020000 in ?? ()
#25 0x0000555571267a30 in ?? ()
#26 0x00007ffff77fecc0 in ?? () from /usr/lib/libnixutil.so
#27 0x00005555712679c0 in ?? ()
#28 0x0000555570fecab0 in ?? ()
#29 0x64202020200a2236 in ?? ()
#30 0x2e32222067756265 in ?? ()
#31 0x2020200a22392e36 in ?? ()
#32 0x646165682d6e6f20 in ?? ()
#33 0x2e317e2220737265 in ?? ()
#34 0x2020200a22322e30 in ?? ()
#35 0x75622d6566617320 in ?? ()
#36 0x2e35222072656666 in ?? ()
#37 0x2020200a22322e31 in ?? ()
#38 0x7e22207972617620 in ?? ()
#39 0x0a0a22322e312e31 in ?? ()
#40 0x64657475706d6f63 in ?? ()
#41 0x312e302e305e4073 in ?? ()
#42 0x7372657620200a3a in ?? ()
#43 0x302e3022206e6f69 in ?? ()
#44 0x657220200a22312e in ?? ()
#45 0x22206465766c6f73 in ?? ()
#46 0x2f2f3a7370747468 in ?? ()
#47 0x7972747369676572 in ?? ()
#48 0x0000000000000000 in ?? ()
(gdb) q
```
</details>

```
> nix --version 
nix (Nix) 2.23.3
> pacman -Qi nix
Name            : nix
Version         : 2.23.3-1
```

## Comment 3710166328

maintainer (MEMBER) · domenkozar · 2026-01-05T12:07:08Z · https://github.com/NixOS/nix/issues/3973#issuecomment-3710166328

I've started to see more of these since Nix switched to parallel GC.

## Comment 3711061498

maintainer (MEMBER) · domenkozar · 2026-01-05T16:04:30Z · https://github.com/NixOS/nix/issues/3973#issuecomment-3711061498

● Key observations from GC stats:

  1. Parallel GC - 16 processors, 15 mark helper threads
  2. Heap explosion: 256 KiB → 393,472 KiB (~384 MB) between collection 1 and 2
  3. 0 bytes freed in both collections, 0% in-use - suspicious
  4. Crash timing: Right after collection 2 finished, during "Adding block map" operations

  The sequence before crash:
  Finished marking for mark phase number 0
  GC #2 freed 0 bytes, heap 393472 KiB
  Complete collection took 0 ms 275239 ns
  Adding block map for size of 2 granules (32 bytes)
  Adding block map for size of 84 granules (1344 bytes)
  Adding block map for size of 0 granules (0 bytes)  <-- weird, 0 granules?
  Adding block map for size of 1 granules (16 bytes)
  Adding block map for size of 4 granules (64 bytes)
  Adding block map for size of 128 granules (2048 bytes)
  Adding block map for size of 3 granules (48 bytes)
  SIGSEGV

  Suspicious: "Adding block map for size of 0 granules (0 bytes)" - that looks like corruption or invalid state.

  Crash happens in block map allocation after parallel marking finishes. Could be a race between mark helpers and the main allocator thread.

## Comment 3711089773

other (CONTRIBUTOR) · xokdvium · 2026-01-05T16:09:03Z · https://github.com/NixOS/nix/issues/3973#issuecomment-3711089773

Any chance it could be a Boehm issue? Doesn't seem like currently stackful coroutines should be affecting it since we don't allocate anything on the Boehm heap now in coroutines?
