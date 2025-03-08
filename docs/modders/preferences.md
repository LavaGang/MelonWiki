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
            if (Input.GetKeyDown(KeyCode.T))
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

> It is important to remember that both of these events will call when the value is set to, not necessarily when the value actually changes.

## Custom Save Paths

Since saving to a single file might end up in a huge mess, it's possible to save categories to custom paths, instead of the main `MelonPreferences.cfg` path.<br>
To do this, we can use the `SetFilePath` method after creating the category to set it's destination path. To save the category, use the `SaveToFile` method.<br>

```cs
myCategory.SetFilePath("Foo/Bar.cfg");

// Some code here

myCategory.SaveToFile();
```
Since calling `SetFilePath` will also automatically load all the category data from the said file, there is a special parameter to prevent that from happening: `autoload`.
```cs
myCategory.SetFilePath("Foo/Bar.cfg", autoload: false);

// Manually load the category data
myCategory.LoadFromFile();
```
