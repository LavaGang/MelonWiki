# Melon Plugins

Melon Plugins are a different type of Melons. Plugins can be used to manage Mods and MelonLoader itself.<br>
Compared to Mods, Plugins are loaded way earlier, as soon as the managed part of MelonLoader starts initializing.

### Creating a Melon Plugin

The process of creating a Melon Plugin is as simple as creating a Melon Mod.<br>
The only differrence in creating a Melon Plugin is that your Melon has to derive from the `MelonPlugin` class.

```cs
using System;
using MelonLoader;

[MelonInfo(typeof(Test.TestPlugin), "Test", "1.0.0", "SlidyDev")]
[MelonColor(ConsoleColor.Blue)]
[MelonGame("SomeCoolDevTeam", "SomeCoolGame")]

namespace Test
{
    public class TestPlugin : MelonPlugin
    {
    }
}
```

### Virtual Callbacks

Compared to Mods, Plugins have some additional virtual callbacks that can be overriden:
- `OnPreInitialization`: Called as soon as all Plugins from the Plugins folder have initialized.
- `OnApplicationEarlyStart`: Called after Game Initialization, before OnApplicationStart and before Assembly Generation on Il2Cpp games.
- `OnPreModsLoaded`: Called before all Mods from the Mods folder are loaded.
- `OnPreSupportModule`: Called before the Support Module is loaded and right after all Mods from the Mods folder have initialized.
- `OnApplicationStarted`: Called after all MelonLoader components are fully initialized.
- `OnApplicationLateStart`: Called after the Engine is fully initialized.

Like in Mods, you can also subscribe to Melon Events which may be useful in some cases.

### Managing Other Melons

MelonLoader allows Melons to manage other Melons by loading, registering and unregistering them.

Before we can start doing anything, we should first look at how Melons are loaded.<br>
Assemblies that contain Melons are called `Melon Assemblies`. MelonLoader has a special class for loading and managing those assemblies: `MelonLoader.MelonAssembly`.<br>
The `MelonAssembly` class is responsible for loading Melon Assemblies and resolving Melons from them.<br>
To load a Melon Assembly, we can use the `MelonAssembly::LoadMelonAssembly` method. If a Melon Assembly is already loaded, it will return the existing `MelonAssembly` instance.<br>
Loading a Melon Assembly will instantly resolve all Melons from the assembly, which will be stored in the `MelonAssembly::LoadedMelons` property.<br>
Any Melons that failed to resolve will be stored in the `MelonAssembly::RottenMelons` property.

Once Melons are loaded, they have to be registered to become functional. You can register a Melon with the `MelonBase::Register` method.<br>
Registering a Melon calls its `OnInitializeMelon` callback. It also registers all Harmony patches (unless the `HarmonyDontPatchAll` attribute is present).

Sometimes it's necessary to register Melons in the right order. For example, a Melon with a higher priority should be registered first.<br>
Melon's with the same priority may have to be loaded in the right order too. For example, if Melon A references Melon B, Melon B should be registered before Melon A.<br>
Fortunately, the `MelonBase` class comes with a static `RegisterSorted` method that automatically registers a list of Melons in the right order.

It is also possible to unregister Melons.<br>
Unregistering a Melon will deactive it by unsubscribing it from all Melon Events, unpatching all its Harmony patches, and by calling the `OnDeinitializeMelon` callback.
