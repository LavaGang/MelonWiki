# MelonLoader Differences

MelonLoader have some "small" things that doesn't work the exact same as if you were modding a Mono game.

### Custom Components

Custom components (and custom Types in general) are currently not supported by MelonLoader over Il2Cpp.<br/>
This means you can't create a new class that extends `Component`, `MonoBehaviour`, or another existing Il2Cpp type.

### Coroutines

!> This part contains some unreleased code.

In a standard Mono game, you would use `StartCoroutine`. Since MelonMod isn't a component, and that anyway we can't use a Mono IEnumerator on Il2Cpp due to how those are handled in C#, we need to do it another way.

To do that, MelonLoader includes replacement class: `MelonLoader.MelonCoroutines`!
 - `CoroD Start<T>(T routine)`: Starts a new coroutine, which will be ran at the end of the frame.
 - `void Stop(CoroD routine)`: Stops a running coroutine.

### Il2Cpp types and casting

In a standard Mono game, casting is quite easy.<br/>
Let's say we have a class `MyChildClass`, which inherit from `MyParentClass`.<br />
Casting it in Mono would go like that:
```cs
MyParentClass childInstance; // This values is already defined

MyChildClass childInstanceCasted = childInstance as MyChildClass;
// or
MyChildClass childInstanceCasted = (MyChildClass) childInstance;
```
We can't do that with Il2Cpp objects. We have to use some methods from Il2CppAssemblyUnhollower:
```cs
using UnhollowerBaseLib;
// ...
MyChildClass childInstanceCasted = childInstance.TryCast<MyChildClass>();
// or
MyChildClass childInstanceCasted = childInstance.Cast<MyChildClass>();
```

### System.String vs Il2CppSystem.String

in a lot of languages, the type `string` is used the same way as if it was a primitive type. This isn't a primitive type, so the same rules as Il2Cpp objects apply.

Most methods that was asking for a `string` (`System.String`) will now ask for an `Il2CppSystem.String`. Thankfully, `Il2CppSystem.String` has an explicit cast for `string`.<br/>
This means we can use it like this:
```cs
Debug.Log((Il2CppSystem.String) "Hello World!");
```
