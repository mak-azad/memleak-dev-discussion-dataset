# Potential memory leak in CRehldsPlatformHolder

- URL: https://github.com/rehlds/ReHLDS/issues/377
- Repo: rehlds/ReHLDS (language: C++)
- State: open; created 2017-02-20T21:14:18Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · BlackPhrase · 2017-02-20T21:14:18Z · https://github.com/rehlds/ReHLDS/issues/377

Current impl of CRehldsPlatformHolder class creates a new default impl of IReHLDSPlatform interface in it's get method if it's m_Platform pointer is currently null:

https://github.com/dreamstalker/rehlds/blob/master/rehlds/rehlds/platform.cpp#L6-L7

It's set method allows to set a new impl for m_Platform without any check:

https://github.com/dreamstalker/rehlds/blob/master/rehlds/rehlds/platform.cpp#L14

so this code will occur in a memory leak:

```cpp
IReHLDSPlatform *pPlatform = CRehldsPlatformHolder::get(); // m_Platform points at null and default impl will be created
CRehldsPlatformHolder::set(nullptr); // m_Platform is now points at null again which makes default instantiated impl inaccessible
```

## Comment 281187797

maintainer (COLLABORATOR) · theAsmodai · 2017-02-20T21:40:37Z · https://github.com/rehlds/ReHLDS/issues/377#issuecomment-281187797

Or we can delete m_Platform when the setter used with nullptr.

## Comment 281191484

reporter (CONTRIBUTOR) · BlackPhrase · 2017-02-20T21:56:48Z · https://github.com/rehlds/ReHLDS/issues/377#issuecomment-281191484

If it's guaranteed that passed impl of IReHLDSPlatform in the set method is using the same crt (i.e. didn't came from any different dll from 3rd party) then there wouldn't be any problem to just delete it

This is handled in my solution too but commented for now

## Comment 281193834

maintainer (COLLABORATOR) · LevShisterov · 2017-02-20T22:10:52Z · https://github.com/rehlds/ReHLDS/issues/377#issuecomment-281193834

Actually, `set` is called only once in DllMain, so I see no reason there will be a leak.
But if imagination is applied, then you always can shoot in the leg with C++, for ex: yes, delete `m_Platform` in `set`, but if it was stored previously from the call to `get`, then it will crash on deleted object later, etc...

## Comment 281198921

reporter (CONTRIBUTOR) · BlackPhrase · 2017-02-20T22:41:47Z · https://github.com/rehlds/ReHLDS/issues/377#issuecomment-281198921

Even if you store a pointer you always should to validate it before use

Alternative solution to save some CPU cycles when calling the get method:

```cpp
class CRehldsPlatformHolder
{
private:
 	static IReHLDSPlatform* m_Platform;

 	static CSimplePlatform DefaultPlatform;
public:
	static void init(){m_Platform = &DefaultPlatform;}
	static IReHLDSPlatform& get(){return *m_Platform;}
	static void set(IReHLDSPlatform* p)
	{
		if (!p)
		{
			m_Platform = &DefaultPlatform;
			return;
		};

		m_Platform = p;
	};
};

## Comment 281204320

maintainer (COLLABORATOR) · LevShisterov · 2017-02-20T23:20:42Z · https://github.com/rehlds/ReHLDS/issues/377#issuecomment-281204320

There is no way to validate a pointer to deleted object. At least I dunno about direct ones.
Simplifying getter is a good idea.

## Comment 281215568

other (CONTRIBUTOR) · IgnacioFDM · 2017-02-21T00:55:04Z · https://github.com/rehlds/ReHLDS/issues/377#issuecomment-281215568

Indeed there is no way to validate pointers. There used to be some windows specific function some time ago, which was completely broken and has been dropped, and even then simply told you if it was "safe" to access, however the object could have been deleted, and a new unrelated object reside on the same address, therefore the pointer still being invalid.

## Comment 281261283

other (CONTRIBUTOR) · WPMGPRoSToTeMa · 2017-02-21T07:00:36Z · https://github.com/rehlds/ReHLDS/issues/377#issuecomment-281261283

We can use something like `unique_ptr` or `shared_ptr` to simplify this.

## Comment 281279386

reporter (CONTRIBUTOR) · BlackPhrase · 2017-02-21T08:42:32Z · https://github.com/rehlds/ReHLDS/issues/377#issuecomment-281279386

shared_ptr has a double size in mem consumption and a double size reduction in speed (because of ref counting mech) than the unique_ptr

UPD: unique_ptr should be fine since the CSimplePlatform is meant to be used only inside the CRehldsPlatformHolder

You just need to create it (better to use C++14 here):
```cpp
std::unique_ptr<CSimplePlatform> DefaultPlatform // inside the CRehldsPlatformHolder class declaration (private section)

DefaultPlatform = std::make_unique<CSimplePlatform>(); // static void init method

m_Platform = DefaultPlatform.get(); // set method when passed ptr is nullptr

## Comment 281344162

other (CONTRIBUTOR) · WPMGPRoSToTeMa · 2017-02-21T13:28:47Z · https://github.com/rehlds/ReHLDS/issues/377#issuecomment-281344162

Also idk why we are using static class `CRehldsPlatformHolder` instead of global variable `unique_ptr<IReHLDSPlatform> g_RehldsPlatform`.

## Comment 311100809

reporter (CONTRIBUTOR) · BlackPhrase · 2017-06-26T15:51:57Z · https://github.com/rehlds/ReHLDS/issues/377#issuecomment-311100809

@WPMGPRoSToTeMa  It's useless to declare unique_ptr globally because it's used to automatically delete data allocated on the heap (instead of manually write a delete for it which is sometimes forgotten by devs and results in mem leaks).
IMHO better to use

```cpp
IRehldsPlatformHolder *gpPlatform;
```

or something like that then

What is the purpose of CRehldsPlatformHolder?
I saw some pieces of code where it was used only for Windows compilation and Unix was using POSIX directly
Maybe we should restore the direct usage of POSIX instead of platform holder where possible?

## Comment 311118008

other (CONTRIBUTOR) · WPMGPRoSToTeMa · 2017-06-26T16:53:58Z · https://github.com/rehlds/ReHLDS/issues/377#issuecomment-311118008

>It's useless to declare unique_ptr globally because it's used to automatically delete data allocated on the heap

Why?
>which is sometimes forgotten by devs and results in mem leaks

Here you write about it benefit, so why we shouldn't use it?

## Comment 311130055

reporter (CONTRIBUTOR) · BlackPhrase · 2017-06-26T17:40:51Z · https://github.com/rehlds/ReHLDS/issues/377#issuecomment-311130055

@WPMGPRoSToTeMa 
https://stackoverflow.com/questions/34534927/using-smart-pointers-as-global-variables
https://stackoverflow.com/questions/19867360/how-to-instantiate-a-global-smart-pointer-variable
http://en.cppreference.com/w/cpp/memory/unique_ptr

Because smart pointers are wrappers around raw pointers that managing the lifetime of dynamically-allocated objects (instead of new/delete which has a problem I mentioned above and which is currently present in the code of holder class)
If we declare it globally it's lifetime will be equal to app lifetime
I've proposed to use it for internal default platform impl CSimplePlatform, not for platform holder
Do you want to use it globally to be able to reset it to other impl? I mean unique_ptr could be used as holder itself so we could reset its internal pointer and use some other implementation

## Comment 311240707

other (CONTRIBUTOR) · IgnacioFDM · 2017-06-27T03:11:48Z · https://github.com/rehlds/ReHLDS/issues/377#issuecomment-311240707

Edit: Me being dumb

## Comment 311312255

reporter (CONTRIBUTOR) · BlackPhrase · 2017-06-27T09:59:47Z · https://github.com/rehlds/ReHLDS/issues/377#issuecomment-311312255

@WPMGPRoSToTeMa 
> Also idk why we are using static class CRehldsPlatformHolder instead of global variable unique_ptr<IReHLDSPlatform> g_RehldsPlatform.

CRehldsPlatformHolder has a small and simple interface - only get and set methods
How about using the smart pointer for internal IReHLDSPlatform interface of the platform holder?

## Comment 311312755

other (CONTRIBUTOR) · IgnacioFDM · 2017-06-27T10:02:00Z · https://github.com/rehlds/ReHLDS/issues/377#issuecomment-311312755

@Sh1ft0x0EF Yes you're right, I forgot about that. It can be very important in terms of properly releasing resources.



## Comment 311352286

other (CONTRIBUTOR) · WPMGPRoSToTeMa · 2017-06-27T13:06:40Z · https://github.com/rehlds/ReHLDS/issues/377#issuecomment-311352286

> How about using the smart pointer for internal IReHLDSPlatform interface of the platform holder?

Yeah its a good idea.

## Comment 311438830

maintainer (COLLABORATOR) · In-line · 2017-06-27T18:06:04Z · https://github.com/rehlds/ReHLDS/issues/377#issuecomment-311438830

We should also check libstdc++ version requirement for `std::unique_ptr`.

## Comment 316030015

other (CONTRIBUTOR) · hajimura · 2017-07-18T11:00:29Z · https://github.com/rehlds/ReHLDS/issues/377#issuecomment-316030015

So, is this bug is there now?

## Comment 316046049

reporter (CONTRIBUTOR) · BlackPhrase · 2017-07-18T12:17:00Z · https://github.com/rehlds/ReHLDS/issues/377#issuecomment-316046049

@Phantomsq 
Yep, it's still there
I think I'll fix it on this weekend

## Comment 316067253

maintainer (COLLABORATOR) · LevShisterov · 2017-07-18T13:41:54Z · https://github.com/rehlds/ReHLDS/issues/377#issuecomment-316067253

No bugs here, because CRehldsPlatformHolder::set is only used in testing suite. And even there it is executed only once on engine loading.
