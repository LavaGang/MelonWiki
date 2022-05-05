# Quick Start

!> This tutorial assumes that you have a fair grasp of the C# programming language and basic knowledge of Visual Studio and Unity Engine.

### Basic mod setup

!> MelonLoader currently only supports C# mods, made using .NET Framework up to version 4.7.2.

At first, you will need to create a new project of type `Class Library (.NET Framework)`, and select a version up to 4.7.2.<br>
Doing so will create a new empty cs file, called `Class1`. This will be our mod main class.<br>
I'll rename it `MyMod`. You can change it to whatever you would like though.

You will now need to reference the main MelonLoader assembly. Right click the `Reference` directory, `Add a reference...`, and click `Browse`.<br/>
Find to the folder of the game you installed MelonLoader on. The file you need to reference from here is `MelonLoader/MelonLoader.dll`.

Any type of mod requires a `MelonInfo` assembly attribute for MelonLoader to know what mod it's loading.<br>
To set one up, go to the `Properties` directory and add these 3 lines to `AssemblyInfo.cs`:
```cs
using MelonLoader;
using MyProject; // The namespace of your mod class
// ...
[assembly: MelonInfo(typeof(MyMod), "My Mod Name", "version", "Author Name")]
```
MelonInfo contains 4 required parameters and an optional one:
- `MyMod`: The main class of your mod. We will talk about it later
- `My Mod Name`: The name of your mod
- `version`: The version of the mod. It should respect the [semver format](https://semver.org/) (example: `1.0.0`)
- `Author Name`: The name of author of the mod
- `Download Link`: The link to download or find the mod [optional]

### The MelonMod class

We are almost ready. Let's go back to our `MyMod` class and turn it into a Melon.<br>
First, let's add `using MelonLoader;` and make our `MyMod` class inherit from `MelonMod`.

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

Your mod is now a valid Melon and can be loaded by MelonLoader.<br>
In the following paragraphs, you will learn how to add some functionality to it.

### Melon Callbacks

MelonMod comes with a few virtual callbacks that can be overridden:
- `OnInitializeMelon`: Called when the Melon is registered. Executes before the Melon's info is printed to the console.<br>
  This callback may run before the Support Module is loaded and before the Engine is fully initialized.<br>
  Do not reference any game/Unity members in this callback or override `OnLoaderInitialized` instead.
- `OnLoaderInitialized`: Called after the Melon was registered. This callback waits until MelonLoader has fully initialized<br>
  It is safe to make any game/Unity calls from this callback.
- `OnLoaderLateInitialized`: Called after `OnLoaderInitialized`. This callback waits until Unity has invoked the first 'Start' messages.
- `OnDeinitializeMelon`: Called before the Melon is unregistered.
- `OnUpdate`: Called once per frame.
- `OnFixedUpdate`: Called every 0.02 seconds, unless `Time.fixedDeltaTime` has a different value. It is recommended to do all important Physics loops inside this Callback.
- `OnLateUpdate`: Called once per frame after all `OnUpdate` callbacks have finished.
- `OnGUI`: Called at every [IMGUI](https://docs.unity3d.com/Manual/GUIScriptingGuide.html) event. Only use this for drawing IMGUI Elements.
- `OnApplicationQuit`: Called when the game is told to close.
- `OnSceneWasLoaded`: Called when a new Scene is loaded.
- `OnSceneWasInitialized`: Called once the active Scene is fully initialized.
- `OnSceneWasUnloaded`: Called once a Scene unloads.
- `OnPreferencesSaved`: Called when Melon Preferences get saved.
- `OnPreferencesLoaded`: Called when Melon Preferences get loaded.

The following example shows how to implement those callbacks:
```cs
using MelonLoader;

namespace MyProject
{
    public class MyMod : MelonMod
    {
        public override void OnSceneWasLoaded(int buildIndex, string sceneName)
        {
            LoggerInstance.Msg($"Scene {sceneName} with build index {buildIndex} has been loaded!");
        }
    }
}
```

### Melon Events

Some callbacks mentioned in the previous paragraph are just shorthand for MelonLoader's global MelonEvents.

MelonEvents are special events that Melons can subscribe to without having to worry about deinitialization.<br>
MelonEvents were programmed to automatically dispose any subscribtions from deinitialized Melons.

The advantage of using MelonEvents instead of virtual callbacks is the ability to subscribe to events with a custom priority.<br>
This is useful in cases your callback has to run earlier/later than a callback from any other mod.<br>
Another advantage of MelonEvents is the ability to subscribe to events in other classes which can help keeping a cleaner mod structure.

Most global MelonEvents can be found in the public `MelonLoader.MelonEvents` class.

?> The following example references the `UnityEngine.IMGUIModule` assembly.

This example shows how to draw a GUI element on top of most other mods through a MelonEvent:
```cs
public class MyMod : MelonMod
{
    public override void OnInitializeMelon()
    {
        MelonEvents.OnGUI.Subscribe(DrawMenu, -100); // Any Melon subscribed to this event with a higher priority will be called earlier.
    }
    
    private void DrawMenu()
    {
        GUI.Box(new Rect(0, 0, 300, 500), "My Menu");
    }
}
```

### Logging

In modding, logging is very important for making the mod users aware of what your mod is doing, but also for diagnosing issues.<br>
Fortunately, MelonLoader has it's own logging system which is also available to mods.

Any `MelonMod` has it's own logger instance which can be accessed through the `LoggerInstance` property:
```cs
public override void OnLoaderInitialized()
{
    LoggerInstance.Msg("Hello World!");
}
```

Unfortunately, the logger instance cannot be simply accessed by a static method.<br>
However, since there will always be only 1 instance of your mod class, you can simply store the instance in a static field so other static methods can find it.
Here is one way of doing it:
```cs
public class MyMod : MelonMod
{
    public static MyMod instance;
    
    public override void OnInitializeMelon()
    {
        instance = this;
    }
    
    public override void OnLoaderInitialized()
    {
        HelloWorld();
    }
    
    public static void HelloWorld()
    {
        instance.LoggerInstance.Msg("Hello World from a static method!");
    }
}
```

### Assembly References

As seen in the previous `OnGUI` example, calling game/Unity methods is as simple as in a normal unity script.<br>
However, compared to Unity, you have to reference all the game and Unity assemblies manually.

For games using the [Mono runtime](https://www.mono-project.com), all the game/Unity assemblies can be found in `[Game Directory]\[Game Name]_data\Managed\`.<br>
For games using the IL2CPP runtime, all the game/Unity assemblies can be found in `[Game Directory]\MelonLoader\Managed\` (make sure you have ran the game at least once with MelonLoader!).

Since IL2CPP converts all game assemblies to C++, MelonLoader is using [Il2CppAssemblyUnhollower](https://github.com/knah/Il2CppAssemblyUnhollower), an IL2CPP proxy assembly generator which allows us to use IL2CPP assemblies from C#.
Before we can use any assemblies generated by the Unhollower, it's required to reference the following assemblies first:
- `il2cppmscorlib`
- `UnhollowerBaseLib`

At this point, you're ready to make your first functional Melon.

### Basic Mod Example

?> The following example mod references the `UnityEngine.CoreModule`, `UnityEngine.InputLegacyModule` and `UnityEngine.IMGUIModule` assemblies.

This example mod allows the user to freeze and unfreeze the game by pressing the spacebar:
```cs
using UnityEngine;
using MelonLoader;

[assembly: MelonInfo(typeof(TimeFreezer.TimeFreezerMod), "Time Freezer", "1.0.0", "SlidyDev")]

namespace TimeFreezer
{
    public class TimeFreezerMod : MelonMod
    {
        public static TimeFreezerMod instance;
        
        private static KeyCode freezeToggleKey;
        
        private static bool frozen;
        private static float baseTimeScale;

        public override void OnInitializeMelon()
        {
            instance = this;
            freezeToggleKey = KeyCode.Space;
        }

        public override void OnLateUpdate()
        {
            if (Input.GetKeyDown(freezeToggleKey))
            {
                ToggleFreeze();
            }
        }
        
        public static void DrawFrozenText()
        {
            GUI.Label(new Rect(20, 20, 1000, 200), "<b><color=cyan><size=100>Frozen</size></color></b>");
        }

        private static void ToggleFreeze()
        {
            frozen = !frozen;

            if (frozen)
            {
                instance.LoggerInstance.Msg("Freezing");
                
                MelonEvents.OnGUI.Subscribe(DrawFrozenText, -100); // Register the 'Frozen' label
                baseTimeScale = Time.timeScale; // Save the original time scale before freezing
                Time.timeScale = 0;
            }
            else
            {
                instance.LoggerInstance.Msg("Unfreezing");
                
                MelonEvents.OnGUI.Unsubscribe(typeof(TimeFreezerMod).GetMethod(nameof(DrawFrozenText))); // Unregister the 'Frozen' label
                Time.timeScale = baseTimeScale; // Reset the time scale to what it was before we froze the time
            }
        }

        public override void OnDeinitializeMelon()
        {
            if (frozen)
            {
                ToggleFreeze(); // Unfreeze the game in case the melon gets unregistered
            }
        }
    }
}
```
