# Attributes

## Attributes in MelonLoader

### MelonInfo
MelonLoader relies on assembly info to get your mod description. Hence you'll need to add this attribute to your mod

MelonInfo contains 4 required parameters and 1 optional one:
- `type`: The main class of your mod (that inherits MelonMod or MelonPlugin).
- `name`: The name of your mod
- `version`: The version of the mod. It should respect the [semver format](https://semver.org/) (example: `1.0.0`)
- `author`: The name of author of the mod
- `downloadLink`: The link to download or find the mod, this is optional

```cs
using MelonLoader;
// ...
[assembly: MelonInfo(typeof(MyMod), "My Mod Name", "version", "Author Name")]
```



### MelonGame
This is another required assembly attribute similar to MelonInfo that MelonLoader relies on to get info on your mod. Hence you'll need to add this attribute to your mod also

MelonGame contains 2 parameters:
- `developer`: The name of the developer(s) of the game, as defined in the Unity settings.
- `name`: The name of the game, as defined in the Unity settings.

```cs
using MelonLoader;
// ...
[assembly: MelonGame("GameStudio", "GameName")]
```

?> You can leave this attribute empty if you want to mark your mod as universal for all games 

### MelonOptionalDependencies
This optional assembly attribute marks the assembly names of the dependencies that should be regarded as optional for your mod/plugin

MelonOptionalDependencies has a variable number of arguments all of which must be strings:
- `assemblyNames`

```cs
using MelonLoader;
// ...
[assembly: MelonOptionalDependencies("OtherMod", "AnotherMod")]
```

### MelonColor
This optional assembly attribute sets the color of the melon in the console

MelonColor contains 1 parameter:
- `color`

```cs
using MelonLoader;
// ...
[assembly: MelonColor(ConsoleColor.Green)]
```

### MelonAuthorColor
This optional assembly attribute sets the color of your name whenever it's printed to the console

MelonAuthorColor contains 1 parameter:
- `color`

```cs
using MelonLoader;
// ...
[assembly: MelonAuthorColor(ConsoleColor.Red)]
```

### MelonIncompatibleAssemblies
This optional assembly attribute marks the assembly names of the mods that are incompatible with your mod/plugin

MelonIncompatibleAssemblies has a variable number of arguments all of which must be strings:
- `assemblyNames`

```cs
using MelonLoader;
// ...
[assembly: MelonIncompatibleAssemblies("OtherMod", "AnotherMod")]
```

### MelonPriority
This optional assembly attribute marks the priority that your mod/plugin has

MelonPriority contains 1 parameter which is from the enum `MelonPriority`
- `priority`

```cs
using MelonLoader;
// ...
[assembly: MelonPriority(MelonBase.MelonPriority.LOW)]
```

!> This attribute was changed in ML v0.4.0

MelonPriority now has 1 parameter which is an int
- `priority`

Lower number = higher priority. Mods by default have a priority of 0 so if we had...

```cs
using MelonLoader;
// ...
[assembly: MelonPriority(100)]
```

...our mod would be loaded later than most mods

## Attributes Introduced in ML v0.4.0 


### MelonAdditionalDependencies
This optional assembly attribute marks the assembly names of the dependencies that aren't directly referenced but should be regarded as important for your mod/plugin

MelonAdditionalDependencies has a variable number of arguments all of which must be strings:
- `assemblyNames`

```cs
using MelonLoader;
// ...
[assembly: MelonAdditionalDependencies("OtherMod", "AnotherMod")]
```



### MelonPlatform
This optional assembly attribute marks the platforms that are compatible with your mod/plugin

MelonPlatform has a variable number of arguments all of which must be from the enum `CompatiblePlatforms`:
- `platforms`

```cs
using MelonLoader;
// ...
[assembly: MelonPlatform(MelonPlatformAttribute.CompatiblePlatforms.WINDOWS_X64)]
```

### MelonPlatformDomain
This optional assembly attribute marks the domain that your mod/plugin is compatible with

MelonPlatformDomain contains 1 parameter which must be from the enum `CompatibleDomains`:
- `platforms`

```cs
using MelonLoader;
// ...
[assembly: MelonPlatformDomain(MelonPlatformDomainAttribute.CompatibleDomains.IL2CPP)]
```

### RegisterTypeInIl2Cpp
If you read the section on this Wiki about Custom Components and IlCpp Type Inheritance [here](modders/il2cppdifferences?id=custom-components-il2cpp-type-inheritance) you might've noticed that you need to register the class before using it using `ClassInjector.RegisterTypeInIl2Cpp<T>()`. This attribute will let MelonLoader know to register it automatically so that you won't have to


```cs
[RegisterTypeInIl2Cpp]
class MyCustomComponent : MonoBehaviour
{
    public MyCustomComponent(IntPtr ptr) : base(ptr) {}

    // Optional, only used in cases where you want to instantiate this class in the mono-side
    // Don't use this on MonoBehaviours / Components!
    public MyCustomComponent() : base(ClassInjector.DerivedConstructorPointer<MyCustomComponent>()) => ClassInjector.DerivedConstructorBody(this);

    // Code, same as in a normal component
}
```

### VerifyLoaderBuild
This optional assembly attribute verifies the build HashCode of MelonLoader that you specify in your mod

VerifyLoaderBuild contains 1 parameter which is a string
- `hashcode`

```cs
using MelonLoader;
// ...
[assembly: VerifyLoaderBuild("Hash")]
```

### VerifyLoaderVersion
This optional assembly attribute verifies the version of MelonLoader that you specify in your mod

VerifyLoaderVersion has several overrides
1) - `major`, `minor`, `patch`
2) - `major`, `minor`, `patch`, `isminimum` 
3) - `major`, `minor`, `patch`, `revision`
4) - `major`, `minor`, `patch`, `revision`, `isminimum`    

> Please note: Due to a problem with Version checking in builds below 0.5.1, mods using `VerifyLoaderVersion` may not load on later major/minor versions.
> For Example: A mod using `VerifyLoaderVersion(0, 3, 0, true)` would not load on version 0.4.0, despite setting `isminimum` to true.
> This was fixed in MelonLoader 0.5.0 

```cs
using MelonLoader;
// ...
[assembly: VerifyLoaderVersion(0, 3, 0, true)] //This'll mark your mod as v0.3.0 being the minimum version for your mod
```

### HarmonyDontPatchAll
This optional assembly attribute tells MelonLoader to not call `PatchAll()` for your mod's harmony instance
  

```cs
using MelonLoader;
// ...
[assembly: HarmonyDontPatchAll] 
```







