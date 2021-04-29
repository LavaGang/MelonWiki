# Quick Start

!> This tutorial assumes that you have a fair grasp of the C# programming language and basic knowledge of Visual Studio and Unity Engine.

### Basic mod setup

!> MelonLoader currently only supports C# mods, made using .NET Framework up to version 4.7.2.

At first, you will need to create a new project of type `Class Library (.NET Framework)`, and select a version up to 4.7.2.<br>
Doing so will create a new empty cs file, called `Class1`. This will be our mod main class.<br>
I'll rename it `MyMod`. You can change it to whatever you would like though.

You will now need to reference the main MelonLoader assembly. Right click the `Reference` directory, `Add a reference...`, and click `Browse`.<br/>
Find to the folder of the game you installed MelonLoader on. The file you need to reference from here is `MelonLoader/MelonLoader.ModHandler.dll`, or if you are using MelonLoader 0.3.0: `MelonLoader/MelonLoader.dll`.

MelonLoader relies on assembly info to get your mod description. We will have to setup them up.<br>
To do that, go to the `Properties` directory, and add these three lines to `AssemblyInfo.cs`:
```cs
using MelonLoader;
// ...
[assembly: MelonInfo(typeof(MyMod), "My Mod Name", "version", "Author Name")]
[assembly: MelonGame("GameStudio", "GameName")]
```
MelonInfo contains 4 required parameters and 1 optional one:
- `MyMod`: The main class of your mod. We will talk about it later
- `My Mod Name`: The name of your mod
- `version`: The version of the mod. It should respect the [semver format](https://semver.org/) (example: `1.0.0`)
- `Author Name`: The name of author of the mod
- `Download Link`: The link to download or find the mod, this is optional

MelonGame contains 2 parameters:
- `GameStudio`: The name of the developer(s) of the game, as defined in the Unity settings.
- `GameName`: The name of the game, as defined in the Unity settings.

?> You can get the value of `GameName` and `GameStudio` of the game you are modding at the top of one of its Log file.<br/>You can also set these two parameters to `null` if you want you mod to be Universal.

We are almost ready. Let's go back to our `MyMod` class, add a `using MelonLoader;` to the import MelonLoader, and make our `MyMod` class inherit from `MelonMod`.

### The MelonMod class

At this point, your `MyMod` class should looks like this:
```cs
using MelonLoader;

namespace MyProject
{
    public class MyMod : MelonMod
    {

    }
}
```

MelonMod has a few virtual methods that can be overridden:
 - `OnApplicationStart()`: Called after every mod is loaded into the current Mono Domain
 - `OnApplicationQuit()`: Called when the application is closing
 - `OnLevelWasInitialized(int level)`: Called when a scene is initialized
 - `OnLevelWasLoaded(int level)`: Called when a scene is loaded
 - `OnUpdate()`: Called at the end of each `Update` call
 - `OnLateUpdate()`: Called at the end of each `Update` call
 - `OnFixedUpdate()`: Called at the end of each `Update` call
 - `OnGUI()`: Called during the GUI update
 - `OnModSettingsApplied()`: Called when a mod calls `MelonLoader.ModPrefs.SaveConfig()`, or when the application quits.OnUpdate.



In MelonLoader 0.3.0, MelonMod's overrides are a little different:
 - `OnApplicationStart()`: Called after every mod is loaded into the current Mono Domain
 - `OnApplicationQuit()`: Called when the application is closing
 - `OnSceneWasInitialized(int buildIndex, string sceneName)`: Called when a scene is initialized
 - `OnSceneWasLoaded(int buildIndex, string sceneName)`: Called when a scene is loaded
 - `OnUpdate()`: Called at the end of each `Update` call
 - `OnLateUpdate()`: Called at the end of each `Update` call
 - `OnFixedUpdate()`: Called at the end of each `Update` call
 - `OnGUI()`: Called during the GUI update
 - `OnPreferencesLoaded()`: Called when mod preferences are loaded.
 - `OnPreferencesSaved()`: Called when a mod calls `MelonLoader.MelonPreferences.Save()`, or when the application quits.
 - `BONEWORKS_OnLoadingScreen()`: (BONEWORKS only) called when the loading screen shows as BONEWORKS loads scene differently.

### Basic method calling

Thanks to Il2CppAssemblyUnhollower, we have a fair pack of generated proxy assemblies. These can be used as reference to call, get, and set the methods, properties, and fields.

Let's print something to the console.<br>
First, you will need to add a reference to `UnityEngine.CoreModule.dll` and `Il2Cppmscorlib.dll`. Both of them are in `MelonLoader/Managed/`.
> Games made using Unity 2019.4+ also requires `UnityEngine.InputModule.dll` to work.

```cs
public override void OnUpdate()
{
    if(Input.GetKeyDown(KeyCode.T))
    {
        MelonModLogger.Log("You just pressed T") // Note that in MelonLoader 0.3.0 you should use MelonModLogger.Msg() as MelonModLogger.Log() is obsolete
    }
}
```

You now have a mod that prints "You just pressed T" when you, well press the T key!

!> In MelonLoader 0.3.0, due to protections against loading control flow obfuscated assemblies, assemblies under ~5kb will not load properly. If you have a very small mod that throws a `BadImageFormatException` while trying to load it, consider adding more of anything really until it loads. This does not apply to Melonloader 0.2.7.4 and below.
