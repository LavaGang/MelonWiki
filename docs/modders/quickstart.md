# Quick Start

!> This tutorial assumes that you know how to write mods using the C# programming language, and that you have some basic Visual Studio knowledge.

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
 - `OnModSettingsApplied()`: Called when a mod calls `MelonLoader.ModPrefs.SaveConfig()`, or when the application quits.
 - `VRChat_OnUiManagerInit()`: (VRChat only) Called if the `VRCUiManager` component has been initialized this frame. This method is called at the end of the frame, before OnUpdate.

!> - `OnGUI()` is currently broken. - `VRChat_OnUiManagerInit()` is also broken

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
 - `VRChat_OnUiManagerInit()`: (VRChat only) Called if the `VRCUiManager` component has been initialized this frame. This method is called at the end of the frame, before OnUpdate.

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

### Mod Preferences 

> If you are modding using MelonLoader 0.3.0, please refer to [Mod Preferences in MelonLoader 0.3.0](quickstart.md?id=Mod-Preferences-in-MelonLoader-0.3.0)

Often times when developing a mod, it is preferable to have some kind of config the user can edit.<br>
Luckily with MelonLoader, there is a built-in way to do this using the `MelonPrefs` class.
MelonLoader will save these preferences in `UserData\modprefs.ini`.<br>
To make a preference you first register a category using `RegisterCategory()`, then you can save preferences to that category using `RegisterInt()`, `RegisterFloat()`, `RegisterBool()` and `RegisterString()`.

Here's an example that will register the integer `intPreference` with the default value of 100, to the `MyMod` category, which will display as `MyMod Settings`.
```cs
// As early as possible, likely in OnApplicationStart()
string myCategory = "MyMod"; // This will serve as a sort of ID for your category

MelonPrefs.RegisterCategory(myCategory, "MyMod Settings"); 

int myInt = 100; // The int here is the default value
MelonPrefs.RegisterInt(myCategory, "intPreference", myInt, "My int Preference."); 
```

To access this newly saved preference, just use `GetInt()`, `GetBool()`, `GetFloat()`, or `GetString()` respectively.
```cs
int myInt = MelonPrefs.GetInt(myCategory, "intPreference");
```

Keep in mind that the override `OnModSettingsApplied()` is run when mod preferences are saved, so make sure to take advantage of this in your mods.

?> Multiple categories or preferences with the same name will cause errors!

### Mod Preferences in MelonLoader 0.3.0

There are a few differences between preferences in MelonLoader 0.2.7.4 and MelonLoader 0.3.0, most notably, the ability to define deserializers and serializers for custom classes.<br>
A few other differences are:
- Preferences are now saved in the TOML, instead of ini, format.
- Some Unity classes are already mapped. Specifically, `Vector4`, `Vector3`, `Vector2`, `Quaternion`, `Color` and `Color32`.
- And of course, the functions used to do this are different.

First let's walk through storing a `Color` in a preference.<br>
Like MelonLoader 0.2.7.4, we need to create a category first. We do this using `CreateCategory()` in the `MelonPreferences` class.
```cs
// Like MelonLoader 0.2.7.4, this code should run as early as possible
string myCategory = "MyMod"; // This will serve as a sort of ID for your category

MelonPreferences.CreateCategory(myCategory, "MyMod Settings");
```

Now, all that needs to be done is to call `CreateEntry<T>()` to create the entry.
```cs
// Like MelonLoader 0.2.7.4, this code should run as early as possible
string myCategory = "MyMod"; // This will serve as a sort of ID for your category

MelonPreferences.CreateCategory(myCategory, "MyMod Settings");

Color myColor = Color.white; // The default color value
MelonPreferences.CreateEntry(myCategory, "colorPreference", myColor, "My Color Preference.");
```

Now to access this preference, use `GetEntryValue<T>()`.
```cs
Color myColor = MelonPreferences.GetEntryValue<Color>(myCategory, "colorPreference");
```

?> Like MelonLoader 0.2.7.4, Multiple categories or preferences with the same name will cause errors!

To add your own serializer/deserializer to the mapper we use the `RegisterMapper<T>()` method in the `Mappers` class.<br>
As its parameters, we use a function called the deserializer, or reader as the first parameter, and a fcuntion called the serializer, or writer as the second parameter.<br>
The reader should take a `TomlObject` as its parameter and return something of type `T`. The writer does the opposite.

The custom class that will be stored in this example is defined like so:
```cs
public class MyObject
{
    string myString;
    int myInt;
}
```
First, in our reader, we will use the `ReadArray()` method in the `Mappers` class to parse the `TomlObject` parameter.
```cs
public static MyObject MyObjectReader(TomlObject value)
{
    string[] strings = MelonPreferences.Mappers.ReadArray<string>(value);
    return new MyObject() { myString = strings[0], myInt = float.Parse(strings[1]) };
}
```

Then, in the writer, we will use the `WriteArray<T>()` method in the `Mappers`.
```cs
public static TomlObject MyObjectWriter(MyObject value) 
{
    string[] strings = new string[] { value.myString, value.myInt.ToString() };
    return MelonPreferences.Mappers.WriteArray<string>(strings);
}
```
And we are done. Now it is possible to store something of type `MyObject` using `MelonPreferences`.
