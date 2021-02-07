# Patching

Patching methods is basically adding your own code on top of a game's method. This is obviously very helpful when you want code to run at a specific time.

### Harmony

?> MelonLoader uses and old version of Harmony, Harmony 1.2, while the documentation is on latest, 2.0.4. Although differences are somewhat minimal.

The library used by MelonLoader for patching methods is called Harmony. Its documentation can be found [here](https://harmony.pardeike.net/). It's recommended to read the page on patching specifically, found [here](https://harmony.pardeike.net/articles/patching.html) and to read the page on injections, found [here](https://harmony.pardeike.net/articles/patching-injections.html), before consulting the documentation itself. 

### Hooks

!> Hooks use [unsafe code](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/unsafe-code-pointers/), and this guide assumes you know how to use unsafe code.

Another way of patching in MelonLoader is by using hooks. MelonLoader offers this natively in `MelonLoader.ModHandler.dll`, using `Imports.Hook()`.<br>
Its usage is simple, just provide the `IntPtr` of the original method, and the `IntPtr` of the detour. Keep in mind this is a detour, meaning the method given will completely replace the original method.
```cs
using MelonLoader;

// On application start, or as early as possible

Imports.Hook((IntPtr) &originalMethod, (IntPtr) &detour);
```

?> `Imports.Hook` is deprecated in MelonLoader 0.3.0, please use `MelonUtils.NativeHookAttach` instead.

To get the `IntPtr` of a game method
