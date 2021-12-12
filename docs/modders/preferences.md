# Mod Preferences 
Mod preferences are very useful in modding, for a ton of reasons. They let create configs, and save data that's persistent which may be needed in many situations. Luckily, implimenting this is MelonLoader is very simple.<br>

## Mod Preferences in MelonLoader

First, you need to create a category. To demonstrate this, I will build off of the code in the [QuickStart](modders/quickstart.md), which should look something like this:
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

Since we only want one category, we can add it in one of `MelonMod`'s overloads called `OnApplicationStart`. It is called only once when the game starts.
```cs
public override void OnApplicationStart()
{

}
```

Now to create the category, we can simply call `MelonPreferences.CreateCategory` and give it the identifier `OurFirstCategory`:
```cs
MelonPreferences.CreateCategory("OurFirstCategory");
```

Because we want to save it for later use in our mod, let's store the result in static field.
```cs
public static MelonPreferences_Category ourFirstCategory;
public override void OnApplicationStart()
{
    ourFirstCategory = MelonPreferences.CreateCategory("OurFirstCategory");
}
```

And that's it!<br>
You also may find it necessary to add multiple categories if your mod had a lot of preferences. Luckily, this is also very simple. Just create a new one! There's no limitations to how many categories a mod can make.

Now, let's start actually making preferences. For this, we just need to call the `CreateEntry` method on our category instance. Let's also make it a bool.
```cs
// In the OnApplicationStart overload
                           // Identifier// Default value
ourFirstCategory.CreateEntry("ourFirstEntry", false);
```

We should also save it in a static field for use later.
```cs
// In the class definition
public static MelonPreferences_Entry<bool> ourFirstEntry;

// In OnApplicationStart
ourFirstEntry = ourFirstCategory.CreateEntry("ourFirstEntry", false);
```

Now, we can actually use it. Let's say we want to use this entry to enable/disable our `OnUpdate` method. This is pretty simple:
```cs
// In the OnUpdate overload
// If our entry is false, then return
if (!ourFirstEntry.value)
    return;
```

We can also use the `value` property on our entry for the inverse, or, setting the entry value. To do so we just have to assign a value to it:
```cs
ourFirstEntry.value = true;
LoggerInstance.Msg(ourFirstEntry.value); // true
```

Entries are very flexible in MelonLoader. They can hold almost any serializable object and categories aren't limited to how many preferences can be stored.

> Its worth noting that, the preference's value will not be reflected in the `MelonPreferences.cfg` file, where all preferences are saved, until `MelonPreferences.Save()` is called or in MelonLoader 0.4.0 and later, the `Save` method is called on your category.

Overall, our final code should look something like so:

```cs
using MelonLoader;
using UnityEngine;

namespace MyProject
{
    public class MyMod : MelonMod
    {
        public static MelonPreferences_Category ourFirstCategory;
        public static MelonPreferences_Entry<bool> ourFirstEntry;
        
        public override void OnApplicationStart()
        {
            ourFirstCategory = MelonPreferences.CreateCategory("OurFirstCategory");
            ourFirstEntry = ourFirstCategory.CreateEntry("ourFirstEntry", false);
        }

        public override void OnUpdate()
        {
            if (!ourFirstEntry.value)
                return;

            if(Input.GetKeyDown(KeyCode.T))
            {
                LoggerInstance.Msg("You just pressed T")
            }
        }
    }
}
```

Within our entry, there are 2 events that are called when the value is changed.<br>
The first, `OnValueChangedUntyped` is non-generic and has no parameters.
The second, `OnValueChanged` has two parameters, `oldValue` and `newValue`.
These will call during the setter of the `value` property, not necessarily when the value actually changes.

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
