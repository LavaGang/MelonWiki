# Mod Preferences 
Often times when creating a mod, it is needed to have some sort of config the user can edit.<br>
Luckily, in both MelonLoader 0.2.7.4 and 0.3.0, this is built-in to MelonLoader.

### Mod Preferences in MelonLoader 0.2.7.4
> If you are modding using MelonLoader 0.3.0, please refer to [Mod Preferences in MelonLoader 0.3.0](preferences.md?id=Mod-Preferences-in-MelonLoader-0.3.0)

The built-in way MelonLoader handles preferences is by using the `MelonPrefs` class.
MelonLoader will save these preferences in `UserData\modprefs.ini`.<br>
To make a preference, first you register a category using `RegisterCategory()`, then you can save preferences to that category using `RegisterInt()`, `RegisterFloat()`, `RegisterBool()` and `RegisterString()`.

Here's an example that will register the integer `"myInt"` with the ID of `"intPreference"` and the default value of 100, to the `"MyMod"` category, which will display as `"MyMod Settings"`.
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
- The TOML serializer supports more classes. Specifically, `string`, `bool`, `long`, `int`, `byte`, `short`, `double`, and `float`.
- Some Unity classes are already mapped using custom serializers. Specifically, `UnityEngine.Vector4`, `UnityEngine.Vector3`, `UnityEngine.Vector2`, `UnityEngine.Quaternion`, `UnityEngine.Color` and `UnityEngine.Color32`.
- Preferences are now stored in `UserData\MelonPreferences.cfg`.
- And of course, the methods used to do this are different.

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
string myColorId = "colorPreference"; // The preference's ID
MelonPreferences.CreateEntry(myCategory, myColorId, myColor, "My Color Preference.");
```

Now to access this preference, use `GetEntryValue<T>()`.
```cs
Color myColor = MelonPreferences.GetEntryValue<Color>(myCategory, myColorId);
```

?> Like MelonLoader 0.2.7.4, Multiple categories or preferences with the same name will cause errors!

To add your own serializer/deserializer to the mapper we use the `RegisterMapper<T>()` method in the `Mappers` class.<br>
As its parameters, we use a function called the deserializer, or reader as the first parameter, and a function called the serializer, or writer as the second parameter.<br>
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
    if (strings == null || strings.Length != 2) \\ Check if the data was corrupted somehow
        return default;
    return new MyObject() { myString = strings[0], myInt = float.Parse(strings[1]) };
}
```

Then, in the writer, we will use the `WriteArray<T>()` method in the `Mappers` class.
```cs
public static TomlObject MyObjectWriter(MyObject value) 
{
    string[] strings = new string[] { value.myString, value.myInt.ToString() };
    return MelonPreferences.Mappers.WriteArray<string>(strings);
}
```

Lastly, we need to register the reader and writer. We can simply do this by using the `RegisterMapper<T>()` method in the `Mappers` class.
```cs
// Run this as early as possible, before you register preferences
MelonPreferences.Mappers.RegisterMapper(MyObjectReader, MyObjectWriter);
```

And that is it. Now it is possible to store something of type `MyObject` using `MelonPreferences`.

?> Make sure the type `T` in `Mappers.WriteArray<T>()` is the same as type `T` in `Mappers.ReadArray<T>()` or else issues will occur while serializing/deserializing.
