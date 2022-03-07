# Patching

Patching methods is extremely useful in modding. It allows us to run code exactly when and only when it needs to be ran.<br>
On top of this, it let's you modify how methods execute in some cases, giving you a ton of control over the game you're modding.

## Patching using Harmony

MelonLoader doesn't use base [Harmony](https://github.com/pardeike/Harmony). All versions of MelonLoader use modified versions. 
- MelonLoader 0.3.0 and lower uses a slightly modified version of Harmony 1.2 (it's modified to work on Il2Cpp games)
- After 0.3.0, MelonLoader started using a modified version of Harmony 2, called [HarmonyX](https://github.com/BepInEx/HarmonyX)

Please note that this guide will not be convering all aspects of Harmony.<br>
For a full documentation on patching methods with Harmony, please refer to [Harmony's Official Patching Guide](https://harmony.pardeike.net/articles/patching.html).

There are 2 very common ways of patching with Harmony. One of them is by using Harmony's attributes.<br>
This is less versatile, but has better readability and is quicker than the next method. Use this when you don't need a ton of future proofing, or need something quick.<br>
The other one is more versatile, but harder to read and takes a bit more time. It's generally better to use when you need to put in a ton of future proofing.<br>
Both of those contain vital information for patching with Harmony. Please give them a quick read.

Here is an example class we will be using in this guide:
```cs
public class Example
{
    public static Example Instance;

    internal string _myField;

    private static string _myString { get; set; }

    private static void PrivateMethod(string param1)
    {
        
    }

    private static void PrivateMethod(int param1)
    {
        
    }
}
```

!> In Il2Cpp games, transpilers DO NOT function (as there is no IL code to replace)

### Using Attributes

This will mostly be a repeat of what the [Harmony Docs](https://harmony.pardeike.net/articles/patching.html) say. But here we go!<br>
For this example, I will be patching `Example.PrivateMethod(int param1)`.

Harmony is included in `MelonLoader.dll`, so there's no need to download the nuget package or reference the dll.

Let's create a new class. It can be named anything and have any access modifiers, however, we must add the `HarmonyPatch` attribute for it to be picked up by Harmony.<br>
In the attribute, we specify what method we would like to patch. This is similar to [getting a method using Reflection](modders/reflection?id=calling-a-method-using-reflection).<br>
Our first argument will be the class of the method we want to patch. In this case it would be the type `Example` and can easily be obtained by doing `typeof(Example)`.<br>
As our second argument, it would just be the name of the method we would like to patch, so "PrivateMethod".<br>
Lastly, our third argument will be an array of types representing the methods arguments. So our third argument will be `new Type[] { typeof(int) }`

> This is only required because we are patching an overload. We can stop at the second parameter if the method we are patching doesn't have any overloads.

In all, our code will look something like this:
```cs
using HarmonyLib;

[HarmonyPatch(typeof(Example), "PrivateMethod", new Type[] { typeof(int) })]
private static class Patch
{

}
```

Next we add the code we want to run when the method calls.<br>
We do this by adding a static method to our `Patch` class called `Prefix` if we want it to run before the method we patched, or `Postfix` if we want it to run after.<br>
Then you just add your code into the method. It's that simple. It's also possible to get the method's arguments, the instance of the class that was passed into the method and even the return value of the method.<br>
All of this can be read about in the Harmony docs [here](https://harmony.pardeike.net/articles/patching-injections.html). I will not be writing about them in this guide.

After this, our code could look something like this:

!> Our `Prefix` and `Postfix` methods must be static.

```cs
using HarmonyLib;

[HarmonyPatch(typeof(Example), "PrivateMethod", new Type[] { typeof(int) })]
private static class Patch
{
    private static void Prefix()
    {
        // The code inside this method will run before 'PrivateMethod' is executed
    }
    
    private static void Postfix()
    {
        // The code inside this method will run after 'PrivateMethod' has executed
    }
}
```

If you've used Harmony before outside of MelonLoader mods you might know that for using attributes when patching that you'd need to use `PatchAll();` on your Harmony instance. What it essentially does is scan the current assembly for Harmony attributes and creates patches using them. However, you don't need to call `PatchAll();` for your mod's Harmony instance as MelonLoader will do it for you automatically (epic!). If you don't want that however, you can always use the [HarmonyDontPatchAll](modders/attributes?id=harmonydontpatchall) attribute.

If you would like to learn more (I realize I'm starting to sound like a broken record), please read the [Harmony docs](https://harmony.pardeike.net/articles/patching.html).

### Patching Manually

The second way to patch a method using Harmony is by doing it manually. This way gives you a bit more control over finding the method you are going to patch, and the code you want to run.

For this, you need to know how to do reflection. A guide can be found [here](modders/reflection). It's also recommended to read the previous guide, [here](modders/patching?id=using-attributes), for important information and context.

Let's start off by using the namespace `Harmony` if you're using MelonLoader 0.3.0, or the namespace `HarmonyLib` if you're using MelonLoader 0.4.0.
Now, we need to call the `Patch` method in our `HarmonyInstance`. The `HarmonyInstance` can be found as a property in an instance of your mod's main class. Depending on your MelonLoader version, the property will have different names:
 - In MelonLoader 0.3.0, it will be named `Harmony`
 - In MelonLoader 0.4.0 and later, it will be named `HarmonyInstance`

Then, as the first argument, we need to get the MethodInfo of the method we are patching. This is why patching manually is better for future proofing, as you can determine what method you're patching at runtime, rather than putting it in an attribute.<br>
Then, the second argument would be the prefix, the third argument would be the postfix, and the fourth would be the finalizer, which I will not cover. Reading about the finalizer can be found [here](https://harmony.pardeike.net/articles/patching-finalizer.html). For all 3 arguments, they are optional, however one must be non-null.<br>
So, if you don't want a postfix, but a prefix and finalizer, you would have something non-null as the second and fourth argument, and null as the third argument.<br>
Now, for the argument values themselves, you need to pass in a `HarmonyMethod`, whose constructor just takes a `MethodInfo` as the only argument. So simply pass in the `MethodInfo` of the method you want to run as the prefix, postfix, etc.<br>
Here is some example code:

!> Your postfix and prefix methods must be static.

```cs
using HarmonyLib;

// In a method, preferabally in OnInitializeMelon

HarmonyInstance harmony = this.HarmonyInstance;

MethodInfo privateMethod = typeof(Example).GetMethod("PrivateMethod", new Type [] { typeof(int) });

MethodInfo myPrefix = ;// Get the prefix here
MethodInfo myFinalizer = ;// Get the finalizer here

// Prefix and finalizer have values, however the postfix does not.
harmony.Patch(privateMethod, myPrefix, null, myFinalizer);
```

Our methods that run when the patched method runs can also have injections, which allow you to get the patched method's arguments and return value among other things.<br>
Read about them in the Harmony docs [here](https://harmony.pardeike.net/articles/patching-injections.html).

## Deinitialization

Your Melon can be deinitialized at any time during runtime by any other Plugin, Mod or by through the MelonConsole.<br>
Since it would be very annoying having to manually unpatch every single patch in `OnDeinitializeMelon`, MelonLoader will automatically unpatch all Harmony patches as soon as the Melon deinitialized.

## Patching using Native Hooks

!> Coming Soon

