# Melon Preferences 
Melon preferences are very useful in modding for a ton of reasons. They let Melons create configs and save data that's persistent, which may be needed in many situations. 

## Setting up Melon Preferences

To create any Melon Preference Entries, we will first need to create a Melon Preference Category. To demonstrate this, let's use this simple example mod:
```cs
using MelonLoader;
using UnityEngine;

namespace MyProject
{
    public class MyMod : MelonMod
    {
        public override void OnUpdate()
        {
            if(Input.GetKeyDown(KeyCode.T))
            {
                LoggerInstance.Log("You just pressed T");
            }
        }
    }
}
```

The following example shows how to create a simple Melon Preference Category. It is recommended initialize all your Categories and Entries before a Melon has been fully initialized, therefore, we will only be using a `OnInitializeMelon` callback for that.
```cs
private MelonPreferences_Category ourFirstCategory;

public override void OnInitializeMelon()
{
    ourFirstCategory = MelonPreferences.CreateCategory("OurFirstCategory");
}
```

?> Creating a Melon Preference Category will not override any existing categories and will only create one if it doesn't exist yet.

And that's it!<br>
You may also find it necessary to add multiple categories if your mod has a lot of preferences. Luckily, this is also very simple. You can create as many categories as needed; there's no limitations to how many categories a mod can make.

Now, let's start actually making preferences. For this, we just need to call the `CreateEntry` method from our category instance.<br>
You can use any Type for entries as long as it's serializable by [Tomlet](https://github.com/SamboyCoding/Tomlet).<br>
For this instance, let's simply use a Boolean
```cs
private MelonPreferences_Category ourFirstCategory;
private MelonPreferences_Entry<bool> ourFirstEntry;

public override void OnInitializeMelon()
{
    ourFirstCategory = MelonPreferences.CreateCategory("OurFirstCategory");
    
    ourFirstEntry = ourFirstCategory.CreateEntry<bool>("OurFirstEntry", true);
}
```

Once an entry has been created, it is ready for use.<br>
Any entry instance has it's own `Value` property which allows us to get and set it's value.<br>
The following example demonstrates its usage:
```cs
private MelonPreferences_Entry<bool> ourFirstEntry;

public override void OnUpdate()
{
    if (Input.GetKeyDown(KeyCode.T))
    {
        bool oldEntryValue = ourFirstEntry.Value;
        ourFirstEntry.Value = !oldEntryValue; // Toggles the entry boolean

        LoggerInstance.Log($"Our first entry value is {ourFirstEntry.Value}");
    }
}
```

> It's worth noting that entry values will not be automatically saved to the `MelonPreferences.cfg` file until `MelonPreferences.Save()` is called. The `Save` method is automatically called on the `MelonEvents::OnApplicationQuit` event, meaning all preferences will still be automatically saved before a game is closed.

Within our entry, there are 2 Melon Events that are called when the value is changed.<br>
The first, `OnEntryValueChangedUntyped` is non-generic and has 2 boxed parameters: `oldValue` and `newValue`.
The second, `OnEntryValueChanged` has 2 parameters: `oldValue` and `newValue`.

> It is important to remember that both of these events will call when the value is set to, not necessarily whent the value actually changes.

## Additions in MelonLoader 0.4.0 and later

In MelonLoader 0.4.0, there is no change in syntax while creating and using prefs. However, there are many improvements with the system as a whole.

The two largest differences between preferences in MelonLoader 0.4.0 and 0.3.0 is the use of the `Tomlet` lib instead of `Tomlyn` as our Toml lib,
and the use of object oriented conventions while saving and using preferences.

The main difference between the two libs, is that custom serializers are almost never needed, as Tomlet will handle most of that for you.
In fact, Tomlet will handle deserializing and serializing most Unity types for you.
To demonstrate this, let's say we had this type:
```cs
public class MyCustomType
{
    public Vector3 myVector;
    public List<int> myList;
}
```
We could simply make the entry's type `MyCustomType` while creating it, and Tomlet would save the entry fine.

Another addition to MelonLoader 0.4.0 is the ability to save categories to specific files instead of the main `MelonPreferences.cfg` file.<br>
To do this, we simply call the `SetFilePath` method after creating the category and when we want to save, we call the `SaveToFile` method.<br>
This would look something like this:
```cs
myCategory.SetFilePath("Foo/Bar.cfg");

// Some code here

myCategory.SaveToFile();
```
If we wanted to set the category's file path, but not load the preferences from the file yet, simply set the `autoload` param in `SetFilePath` to false, and manually call `LoadFromFile`.
```cs
myCategory.SetFilePath("Foo/Bar.cfg", autoload: false);

// When you want to load the prefs from the file

myCategory.LoadFromFile();
```
