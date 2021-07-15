# Mod Preferences 
Often times when creating a mod, it is needed to have some sort of config the user can edit.<br>
Luckily, in both MelonLoader 0.2.7.4 and 0.3.0, this is built-in to MelonLoader.

### Mod Preferences in MelonLoader 0.2.7.4
> If you are modding using MelonLoader 0.3.0, please refer to [Mod Preferences in MelonLoader 0.3.0](modders/preferences?id=mod-preferences-in-melonloader-030)

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

There is a huge difference between preferences in MelonLoader 0.3.0 and 0.2.7.4. In fact, the 2 systems are barely comparable.<br>
MelonLoader 0.2.7.4 uses the `.ini` format, while MelonLoader 0.3.0 uses `.toml`. Also that, preferences are now object oriented. Which present a whole slew of advantages that will be explained during the guide.

So let's start off the guide.<br>
Starting off as always, we will create a new category. Let's call it `MyCategory`.
```cs
MelonPreferences_Category myCategory = MelonPreferences.CreateCategory("MyCategory", "MyCategory");
```

As I mentioned before, this is now object oriented, making creating and getting entries in a category easier.

Next, let's make a bool entry called `MyBoolEntry`.
```cs
MelonPreferences_Entry<bool> myBoolEntry = myCategory.CreateEntry("MyBoolEntry", false) // Store this in a field or property for later use
```
An advantage to the object oriented conevention being used now, is that to access the value or assign it a new value, simply use the `value` property.
```cs
myBoolEntry.value = true;
MelonLogger.Msg(myBoolEntry.value); // true
```
 > Keep in mind that changes to the entry's value will not be saved in the preferences file until `MelonPreferences.Save()` is called.

Another advantage to object oriented conventions is the ability to add events for when the value of a pref changes.

Within the `MelonPreferences_Entry<T>` class, there are 2 events that are called when the value is changed.<br>
The first, `OnValueChangedUntyped` is non-generic and has no parameters.
The second, `OnValueChanged` has two parameters, `oldValue` and `newValue`.

 > It is important to remember that both of these events will call when the value is set to, not necessarily whent the value actually changes.

### Mod Preferences in MelonLoader 0.4.0 and later

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
