# Implement a DataStore to promote separation of concerns, decoupling, and strengthen scalability

- URL: https://github.com/godotengine/godot-proposals/issues/10537
- Repo: godotengine/godot-proposals (language: None)
- State: open; created 2024-08-23T04:51:23Z; status ok; passes main

## Issue body

reporter (NONE) · naturalarch3r · 2024-08-23T04:51:23Z · https://github.com/godotengine/godot-proposals/issues/10537

### Describe the project you are working on

An ambitous 3D project that has not been announced yet.

### Describe the problem or limitation you are having in your project

_**Disclaimer:** I am very familiar with using Godot, not its codebase. Please forgive any misunderstandings or mistakes I may make in relation to underlying implementations._

### The Problem
I have heard many times that "Godot doesn't scale". I have used Godot since shortly before the release of 3.x. I have seen many contributors come and go, and many an argument as to why "Godot doesn't scale". Many claim the problem is the scene tree itself. I disagree.

Although it is true that Godot does not currently (by itself) scale well, the scene tree is a very versatile and flexible architecture that is well suited to developing games at scale. However, the scene tree can only do so if complimented with good architecture that the user provides.

Through years of using Godot, and the development of countless small projects and prototypes with Godot, I have grown to be very familiar with the user experience of Godot.

**It is clear and evident that the scene tree is not currently utilized to its full potential.**

This problem is itself the sum of the lack of two critical pieces of architecture: a means to decouple data collaboration, and a means to fully decouple communication.

A skilled user will implement the solutions to these problems themselves within their own game architecture / framework. However, this poses a significant barrier to entry, and reduces the accessibility of the engine, all while (for inexperienced users) promoting anti-patterns.

_**Note:** This proposal addresses only the decoupling of **data**, not communication._

---

### Example of The Problem

Let's say a user is creating a character scene for a 2D game. They choose to use a `KinematicBody2D`.

The `KinematicBody` nodes are going to nearly always be moved using the `move_and_slide` function in GDScript. However, this function should only be called once per physics tick. 

Let's say the user wanted to modularize their code base by creating a `GravityNode`. Because we also need character movement, this raises the question of who is responsible for calling `move_and_slide`, which results from not having a good way to collaborate on the velocity vector passed into `move_and_slide`.

When an inexperienced user encounters this problem, they may confuse the problem of "how do I collaborate on a vector" for "who gets to be the one to call `move_and_slide`" or worse, "how do I call `move_and_slide` multiple times without problems".

A naive approach will utilize tight coupling. Perhaps the `GravityNode` is made observable, and a property is created on the `KinematicBody`s script to hold a reference to a `GravityNode` by clicking and dragging the node into the script editor.

This may seem fine for a small project, but quickly results in the creation of monolithic classes which are incredibly long. Inexperienced users will simply integrate all this functionality directly into their character controller, which can quickly grow to thousands of lines in length due to this.

When assessing the claims that "Godot doesn't scale", it became clear to me that the problem is not that it doesn't provide good foundations, but rather that Godot does not offer a means to decouple nodes in such scenarios as this.

The `KinematicBody` script doesn't really need to know what kinds of nodes are providing these velocity vectors. It only needs to know the sum of these vectors for use in `move_and_slide`.

**This is just one example of many why a solution to resolve data coupling will help Godot immensely, for both inexperienced and experienced users.**

### Describe the feature / enhancement and how it helps to overcome the problem or limitation

### Considerations

Because Godot is a general purpose engine, the solution will need to keep in mind the needs of the varied users and use cases of Godot. While a simple and naive implementation could be made with a simple dictionary, I am not entirely convinced that is a suitable solution.

Many users (myself included) need something that will be high-performance, and that will also be accessible from GDScript, C#, as well as GDExtension.

New users may not be entirely familiar with programming, software architecture and engineering, and certainly will be unfamiliar with Godot. Ensuring that the solution(s) are equally accessible to both experienced and new users is a necessity.

**Safety:**
- Storing pointers / references in a data store may result in dangling pointers.
- A high performance solution may avoid casting or coercion, which may make safe data retrieval difficult depending on the implementation.

**Performance:**
- Many experienced developers (myself included) will lean heavily into such a feature for its flexibility, and thus it will need to be suitable for use in large projects.
- New developers may use the store(s) without knowing of alternatives, and may use it sub-optimally. While this is not within contributor's control, increasing performance for these users is.
- New developers may not remember or even know that they need to remove / free any KVPs they create. This can quickly eat up memory.

---

### The Solution
**I propose the creation of a centralized data store.**

_Note: I am not particular on the specific name chosen for this data store. It could be called `Store`, `DataStore`, `Blackboard`, `Cache`, or by some other name. I personally prefer `Store` over `Cache` over `Blackboard` over `DataStore`, but feel its naming should go to the implementing contributor._

For the sake of addressing accessibility, I propose that the store be centralized, rather than a node. As users are very unlikely to need multiple instances of the store, any such users who do may implement such a node themselves. This will greatly reduce boilerplate. Further, making the store a node undermines the purpose of its existence.

I propose that the store have a means to store and retrieve temporary data as well as more long lived data. Serialization is also desirable, as it will give a "game save"-like feature _**for free**_, and it will be _**built-in**_, which would be a major selling point for Godot to inexperienced users.

---

### How it Helps

The presence of (a) data store(s) would enable the decoupling of data between nodes, which will only strengthen the existing architecture immensely. 

The scene tree is not problematic, in fact it offers a very high degree of flexibility. By decoupling data collaboration and retrieval, one of two problems which are (in my opinion) the cause of the claim "Godot doesn't scale" will be solved. No ECS or other drastic measure is desirable or necessary. 

**By offering built-in data decoupling solution(s), in combination with communication decoupling, Godot's scene tree can finally be fully utilized to its full potential for _all_ users, not just those of us who are experienced enough to make our own framework.**

### Describe how your proposal will work, with code, pseudo-code, mock-ups, and/or diagrams

**There are a large variety of possible implementations. The ideas in this proposal should not be considered the sole possible solution.** 

As this must be a real-time solution for games, and is key to leveraging the scene tree to create games at scale, the implementation will _**need**_ to be high-performance, and low overhead. This means that it should avoid type-casting where possible. The actual technical implementation details will need to be planned and decided by a contributor with a greater understanding of the existing code base and C++.

I see many possible means by which it may be implemented at a high-level however.

It should support three levels of data lifetime: temporary, process, and persistent:

#### Temporary
The temporary data should be stored in a way that we can utilize an eviction strategy or strategies. New and inexperienced users can safely utilize the temporary store without worry of memory leaks. Because an inexperienced user will be unlikely to know they need to remove unused KVPs, a temporary segment is very desirable. Further, it will greatly simplify the management of such temporary data for _all_ users, not just new users.

_**Note**: for clarity, the segment itself is not temporary but is instead for storing temporary data._

#### Process
This data is in either the scenario that the users do not want the data to be either temporary or serialized, or in the scenario where they intend to serialize or otherwise manage the data themselves. 

#### Persistent
This data should have the capability of being serialized and de-serialized. Because of the nature of a data store, Godot could then have a game-save like feature _**nearly for free**_ and _**built-in**_ by merely serializing the store. 

Because we do not want to serialize all data, and serialized data is not temporary, it makes sense to in some way segregate serializable data in the data store.

#### Technical Implementation Suggestions
**These are merely suggestions, not rules.**

Essentially, the temporary data store segment is a different data structure, as far as I see. I personally feel that the temporary segment should be implemented as a `Cache` which utilizes an eviction strategy. Because the user will be the one who knows what the amount of temporary data they will have, the cache should be configurable, either through the project settings or through code.

For the process lifetime and persistent data, the use of a `B-Tree` may be desirable, as it maintains `O(log n)`. A `B-Tree` implementation should give these portions of the data store the scaling needed to support a very wide array of game projects while remaining very fast. Storing the process lifetime and serializable data separately is probably not the best of ideas, because it would potentially mean searching a `B-Tree` a second time for the data we are looking for. While this makes serialization more complicated, it is ultimately the superior option for the sake of performance. Perhaps the `B-Tree` entry could have a single boolean flag to indicate whether or not it should be serialized.

#### Short Comings
The `B-Tree` would suffer the problem of needing to have data lifetime managed by the users themselves rather than the store. However, as far as I am aware, this manual management is a necessary evil to achieve the level of performance experienced users will need. Simple games can simply utilize only the temporary segment.

The documentation for the store and examples on its usage should explain how failing to erase unused data causes a memory leak and why, as well as how to avoid the problem.

_**Note:** the data store doesn't necessarily have to be segmented, or use a `Cache` & `B-Tree` architecture. I do feel, however, that the design I suggested may offer substantial performance, user simplicity, and substantial scalability._

---

### Psuedo-Code Usage Examples

_**Disclaimer:** the following is merely an example, and not intended to represent final design or naming._

#### GD Script
```gdscript
# Can have just a `set()` func:
var ok := Store.set("foo", bar, true) # add(string: key, T: value, bool: serialize)
ok = Store.set("foo", baz) # keeps existing serialize flag
ok = Store.set("foo", bar, false) # would be able to change serialize flag

# or a set & add (my preference by far):
ok = Store.add("foo", bar, true) # serialize flag is immutable after add.
ok = Store.set("foo", baz) # can't mutate flag, enforcing separation of responsibility

var foo = Store.get_or_default("foo")
ok = Store.serialize_json("some/path/here") # serialize BST to JSON

# Can have temp cache separate (which I think is the better solution):
ok = Cache.set("foo", bar)

# Or part of the store:
ok = Store.set_temp("foo", baz)

# Must be able to remove from store:
ok = Store.remove("foo")
```

#### C#
```c#
// add values to store...
var ok = Store.Set<int>("foo", bar);
ok = Store.Set("foo", baz);
var baz = Store.GetOrDefault<int>("foo");

if (!Store.Remove("foo")) throw new Exception();
```

### If this enhancement will not be used often, can it be worked around with a few lines of script?

This is fundamental to game architecture and is non-trivial to implement for inexperienced developers. While experienced developers are able to work around these problems, it is a relatively complicated issue to solve given the performance requirement and level of integration desired.

In short, it cannot be worked around with a few lines of script.

### Is there a reason why this should be core and not an add-on in the asset library?

This is fundamentally about improving the core experience of using the engine as-is out of the box, and thus should be core.

While it _can be_ implemented as a plugin or module, I strongly feel that it _should not be._ This is as it _should_ integrate with the engine to where it can be used and accessed from any script, plugin, extension, or module. This, at least insofar as I know, would more or less require core integration.

As the implementation of this feature aims to compliment the existing feature set and address criticisms of Godot's "inability to scale", not making this core will more or less undermine the majority of this feature's reason to exist, as the current asset store makes plugins and extensions hard to find and sink into obscurity.

## Comment 2308447388

other (NONE) · shanayyy · 2024-08-24T16:26:11Z · https://github.com/godotengine/godot-proposals/issues/10537#issuecomment-2308447388

I may be the inexperienced user. I can feel that what you said makes sense, but I don’t quite understand the example of KinematicBody you gave. Can you explain more? Thank you.

## Comment 2308652903

reporter (NONE) · naturalarch3r · 2024-08-25T04:42:08Z · https://github.com/godotengine/godot-proposals/issues/10537#issuecomment-2308652903

> I may be the inexperienced user. I can feel that what you said makes sense, but I don’t quite understand the example of KinematicBody you gave. Can you explain more? Thank you.

Sure, I can explain it! Sorry for the confusing, somewhat ramble-ish proprosal.

I was referring to the concept of "separation of concerns", also known as "single responsibility", the first principle in SOLID.

By making the gravity force a separate node, you can isolate all the gravity specific code into just that node, keeping the script on `KinematicBody` clean. It also allows you to reuse the gravity node between different `KinematicBody` scenes.

Imagine that you have four characters: a `Player`, a `Spider`, a `Ghost`, and an `NPC`. The `Player` is human, so they have just a `GravityNode`, as does `NPC`. But, the `Ghost` floats and flies, so it doesn't have a `GravityNode`. The `Spider` has a `GravityNode`, but it is configured to give gravity inverse to the surface normal, letting the spider walk on walls and ceiling.

This allows us to have a single `GravityNode`, rather than re-writing the same functionality for each character. 

However, because `move_and_slide` can really only be called once per physics tick, this confuses a lot of users about how to achieve this separation. While you _can_ hold a reference to the `GravityNode` in your `SpiderController`, this is not going to scale well. It works for very simple games, but not for production. 

So, if you couple them, it will look something like:

```gdscript
# simple pseudo code example, not an actual controller or gdscript.

var gravity_node : GravityNode = @"./GravityNode"

func _physics_process(delta) # use physics process because we don't want to be frame rate dependent

# calculate movement velocity or something...

velocity += gravity_node.force

# integrate other forces and compensate for delta...

move_and_slide(velocity)
```

But you would have to do this for each and every force you plan to integrate, separately. This means that for every node like `GravityNode`, E.G. a `JumpNode`, you need to get and keep a direct reference to these nodes. This is called `coupling`, because we have coupled the `SpiderController` to the `GravityNode`, like attaching train cars together, or links in a chain. This also creates another problem: we now have to create a separate script for each `KinematicBody` scene we have, because they will have different, unique compositions.

The truth is that we don't really care whether we even have a `GravityNode` or a `JumpNode`. We only need to know what forces we need to integrate into the velocity passed into `move_and_slide`. But, because Godot currently has no way to share or collaborate on data, this coupling seems necessary to those who don't know about the solutions to this problem.

But, if we had a place where we could share variables between nodes, we wouldn't need to directly know about which other nodes are present, or even if they are there. This way, we could separate out the character specific code and the code to integrate these forces. Now we can have a `PlayerController`, an `AIController`, etc. that are in charge of just decision making and inputs, while we can have a `Character` script we attach to the `KinematicBody`, like so:

```gdscript

public class GravityNode
    const max_speed : double = 128.00 # some max fall velocity : ^ )
    private var direction: Vector3 = Vector3.zero
    private var force : Vector3 = Vector3.zero
    private var acceleration : double = 9.81

    func _physics_process(delta):
        if (parent.is_on_ground)
            force = Vector3.zero
            return

        var speed = force.dot(direction)
        if (speed < max_speed)
            force += direction * acceleration

        var velocity = Store.get_or_default("velocity") # we don't care whether this is an empty vector or not.
        Store.set("velocity", velocity + force) # combine gravity force into the velocity accumulator

public class Character
    func _physics_process(delta):
        var vel = Store.get_or_default("velocity")
        vel.x = math.absolute(vel.x)
        vel.y = math.absolute(vel.y)
        vel.z = math.absolute(vel.z)
        # prevent floating point weirdness with multiply
        if (vel.x < double.epsilon && vel.y < double.epsilon && vel.z < double.epsilon) return 

        move_and_slide(vel * delta)
        Store.set("velocity", Vector3.zero) # reset or slide around like on ice forever
```

Now we have a way to sum the velocities without needing to know which velocities are coming from where or why. This ensures that each node can now only have a single responsibility. `Character` only needs to pass the `velocity` vector into `move_and_slide`, then reset it. `GravityNode` only needs to care about gravity, not whether its gravity is being used.

We don't even have to worry about order of execution here, because any forces missed this physics frame by the reset happening first will be integrated in the next tick.

This is the true power of the scene tree (and SOLID)--reusing our code as much as possible so that we do as little work as possible to achieve our goals.

Does this make more sense?

## Comment 2308778296

other (NONE) · shanayyy · 2024-08-25T10:51:42Z · https://github.com/godotengine/godot-proposals/issues/10537#issuecomment-2308778296

Thank you, I didn't expect this Store to be used in this way. This really gave me a new perspective on how to design nodes. I support your idea of ​​data decoupling. I will try to use this design in development.

## Comment 2317581311

other (NONE) · and-rad · 2024-08-29T12:54:48Z · https://github.com/godotengine/godot-proposals/issues/10537#issuecomment-2317581311

What about multithreading? If you have a centralized store, odds are it's going to be written to and read from by multiple threads. What kind of locking mechanism would you use here in order to prevent unnecessary locks and waiting periods?

Also, what does the data store provide that a simple autoloaded script doesn't? Especially since it looks like the values are accessed by string keys which I'm also not a huge fan of with regards to how error-prone and cache-unfriendly they are.

## Comment 2319796824

reporter (NONE) · naturalarch3r · 2024-08-30T03:06:35Z · https://github.com/godotengine/godot-proposals/issues/10537#issuecomment-2319796824

> What about multithreading? If you have a centralized store, odds are it's going to be written to and read from by multiple threads. What kind of locking mechanism would you use here in order to prevent unnecessary locks and waiting periods?
> 
> Also, what does the data store provide that a simple autoloaded script doesn't? Especially since it looks like the values are accessed by string keys which I'm also not a huge fan of with regards to how error-prone and cache-unfriendly they are.

Yeah, I agree. As I said, the examples I showed were just one possible solution. I was more concerned with demonstrating how the store would promote modularity and why such a store could benefit the engine.

As for specific implementation details, those are not yet concrete. However, I certainly agree that multi threading needs to be a major consideration, as the engine can be toggled to run the servers on separate threads.

I both agree and disagree on string keys. Godot already has a something like a centralized store for project settings. It can be used (in advanced mode) to create your own settings for your game, which can be any of Godot's primitive types such as a float or vector. The settings store is accessed with strings in a path like format. https://docs.godotengine.org/en/stable/classes/class_projectsettings.html

The sad truth is that as error prone and troublesome as string keys are, they are the option that is both simplest to implement, most flexible, and simplest to use.

For those of us who are able to create our own frameworks, using a context type makes more sense when string keys are a problem.

As for why I originally wanted it to be centralized, there a handful of good reasons for it.

First, I felt that it reduces boilerplate, which keeps code more clean and lowers barrier to entry. Second, I felt it doesn't really need to know about or make use of the scene tree. Third, by making it centralized, Godot could have game save / load infrastructure _practically for free_ by just serializing the data in the store marked for it.

However, making it centralized does introduce a new hurdle:

_How do you differentiate entries on a per instance basis?_

One way to do this would be to segment the store. But, this would introduce further complexity and a little overhead.

But, if it is made a node, there are quite a few positives there too, including solving deserialization.

If it is a node, it could have a property which could be used for serialization and deserialization. This would make instance differentiation easier. The user could determine a unique instance id and even change this dynamically at runtime if need be. This would probably be the best solution, given the simplification will also increase performance.

Further, if the node is serializable, using node groups to serialize them all at once should be quite easy too. While not as simple and easy as a centralized store, it would still be easier than how it is done by most now.

Even with needing to couple the store node, coupling one node is substantially better than coupling many.

Another problem to consider is reference validity. If the node is removed from the scene tree, its consumers will need to be notified. While giving the node a signal for it would work, all of these things increase boilerplate and raises the barrier to entry.

While in ways I prefer a centralized store, in others I fully acknowledge that using a node makes a great deal of sense too.

Ultimately, my proposal is not intended to be a set in stone "do this and do it this way", but rather to put forward the idea of _a_ data store, not _the_ data store. I'm mainly looking to foster discussion like this on the topic, guage interest, and get the vague idea of data decoupling solutions into the background of contributors minds.

Ultimately, contributors who work on core and the nodes will know better than I what specific solutions would be the best fit in this engine.

## Comment 2320279519

other (NONE) · and-rad · 2024-08-30T07:03:59Z · https://github.com/godotengine/godot-proposals/issues/10537#issuecomment-2320279519

> I was more concerned with demonstrating how the store would promote modularity and why such a store could benefit the engine.

I don't think it does promote modularity. I think it does the opposite.

You mentioned SOLID before, so I assume you're familiar with design patterns, specifically singletons, global state, and all the pro-con discussions around them. The way I see it, a central data store is just global state with a fancy name. Now, I am by no means a purist when it comes to avoiding global state at all costs. That's a silly position especially in gamedev, but it does provide a larger attack surface for bugs because every single item in the data store can be accessed by anything in the code base. That does not sound like good encapsulation practices to me.

I like to think about modularity in terms of this question: *If I take away this one thing, how many other things are now broken?* You have high modularity when few other parts of the codebase break and low modularity when a lot of the other parts break. So here's the bigger problem with regards to modularity: Take away the data store and everything breaks. Gravity node? Broken. Jump node? Dead. Health node? Gone.

High modularity requires data to be as localized as possible, and a centralized data store just goes against that.

## Comment 2322623618

reporter (NONE) · naturalarch3r · 2024-08-31T00:09:54Z · https://github.com/godotengine/godot-proposals/issues/10537#issuecomment-2322623618

> > I was more concerned with demonstrating how the store would promote modularity and why such a store could benefit the engine.
> 
> I don't think it does promote modularity. I think it does the opposite.

Clearly you and I have a very different idea of what modularity is. 

How else would you make your nodes modular? If you hold a direct reference to the `KinematicBody` in the `GravityNode`, any changes in the implementation of the script on `KinematicBody` can necessitate changing the `GravityNode` too. Under my architecture model, I can add or remove a `GravityNode`, a `WindNode`, a `JumpNode` or a `MagnetNode` any time I want, all on the fly without breaking anything else or affecting anything else. I can remove the `GravityNode` from the project entirely if need be, and not affect anything else at all.

> You mentioned SOLID before, so I assume you're familiar with design patterns, specifically singletons, global state, and all the pro-con discussions around them. The way I see it, a central data store is just global state with a fancy name. Now, I am by no means a purist when it comes to avoiding global state at all costs. That's a silly position especially in gamedev, but it does provide a larger attack surface for bugs because every single item in the data store can be accessed by anything in the code base. That does not sound like good encapsulation practices to me.
> 

A data store (blackboard) is not the same as global state per se. The blackboard pattern is a fairly common pattern in various software industries, including gamedev. https://en.wikipedia.org/wiki/Blackboard_(design_pattern). Would you say that using an event bus is bad because it is globally accessible? Of course not, because that is absurd. What makes such architecture potentially problematic lies largely with the user.

While it is true that a blackboard is in some ways _similar_ to global state it is _not_ the _same_ as global state. The difference lies in how access is managed, and how individual users utilize and interact with the data. A good implementation will allow us to maintain minimal global state, and would include encapsulation mechanisms. Further, it is the responsibility of the user to determine the way in which they use the data store. A user can have global state even without this architecture.

There are many ways to mitigate the risks associated with a global state.

I actually thought that my proposal had discussed this, but it would seem that I forgot it. I wrote the proposal across several different sessions, and it would seem that the encapsulation mechanism ideas I thought of were left out on accident.

First, we could segment the data store by `ulong`. The instance ID of nodes is unique, and a `ulong`. This would mean that we could allow the user to request a segment using the ulong of a known node, effectively encapsulating data access to only nodes immediately known. Then, the store could return either the segment itself, or better yet, a proxy accessor to the segment. The proxy would mean that access, lifetime, and ownership of the segment can remain properly managed by the store, increase encapsulation, and not incur a significant performance loss as the proxy would ideally be cached locally in the consumer. This would even mean that the method to get an accessor could look like: `Store.get_scope(self)` or `Store.get_scope(get_parent())`

Another option is Role Based Access Control (RBAC). Each segment of the store could be tagged with a role, and only a matching role can access it. These segments and related roles could even be defined in the project settings. Then, when creating a node in the scene tree, a role could be assigned to it in the editor, similarly to the physics layers and masks.

Another option would be to use the scene tree hierarchy to control access. 

You could even use a token based access.

Those are just the options available if using a centralized store. 

Alternatively, if a the store is created as a node, scope access and control is effectively achieved for free through the scene tree hierarchy, as nodes will only be able to easily access a data store node within their own scene. This is another reason to use a node rather than a centralized store. While a centralized store certainly makes for a simpler usage, it can also introduce a greater potential for problems if not handled with care. It also means that scenes that don't need or shouldn't use a blackboard don't need to have one.

While originally, I thought I would prefer to use a centralized store, I've come around to the idea of a `BlackboardNode` more and more, and currently prefer a node solution.

> I like to think about modularity in terms of this question: _If I take away this one thing, how many other things are now broken?_ You have high modularity when few other parts of the codebase break and low modularity when a lot of the other parts break. So here's the bigger problem with regards to modularity: Take away the data store and everything breaks. Gravity node? Broken. Jump node? Dead. Health node? Gone.
> 
> High modularity requires data to be as localized as possible, and a centralized data store just goes against that.

I don't think that this reasoning is sound.

Removing a centralized data store would only break things because it is the _chosen architecture_ for managing shared state across the game. The same argument applies to any essential system component. If I were to remove the physics engine, all physics based nodes cease to work. If I remove the renderer, what use is the rest of the engine? To state that removing an essential system component means the rest of the system isn't modular is _**non sequitur.**_

I already gave an example in a previous comment explaining how such an architecture promotes modularity, and how tightly coupling does the opposite.

The key is whether or not the system is designed in a way that components are decoupled and can be independently modified, which my approach facilitates by allowing nodes to interact through a medium rather than having direct dependencies.

Further, nodes don't _need_ to use the blackboard. It is entirely optional. Users can choose to couple nodes if they prefer. They can implement some other architecture of their own, such as using source generation to create context types. If the store is implemented as a node, it is possible to design ones nodes that they can function through a blackboard if it is present, or through other means if not. This design could enable nodes to work by utilizing different kinds of architecture flexibly.

If scoped access control is so important (and I agree it is, my own personal game framework engine extensions already solved this problem), it is a problem that is fairly easily solved. Throwing out the idea of decoupling and single responsibility just because "shared data bad" is ridiculous. Even if we were to tightly couple the `GravityNode` and the `Character`, they would still need to collaborate on some shared state.

You can live in spaghetti land if you would like, you don't have to use such an architecture if you do not want to. Even if implemented centralized, nobody is forcing you to use it like global state. No-one has a gun to your head.

This proposal is intended to address the scaling and flexibility of large and/or complex projects in a way that is accessible to _all_ users.

I have actually come to prefer a `BlackboardNode` (or whatever it should be called) for numerous reasons, my self.

But, solving the access problems with a centralized store is something that has been done many times in software and will continue to be done many times. The pattern of a blackboard is up there with event busses in use for its ability to decouple complex software at scale. Shared state is itself not necessarily evil, and in fact, is paramount to some architectures such as ECS, or even the entirety of Data Oriented Design. In an ECS, systems have access to all components of a certain type. This means that a system could potentially be misused and access all data like global state. Likewise, a blackboard's usage is what dictates whether or not it is bad.
