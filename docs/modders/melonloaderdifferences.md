# MelonLoader Differences

MelonLoader have some "small" things that doesn't work the exact same as if you were modding a Mono game.

> If you find something that doesn't seems natural with Il2Cpp and that isn't listed here, please ping _Slaynash#2879_ on the [MelonLoader Discord](https://discord.gg/2Wn3N2P).

### Il2CppAssemblyUnhollower Generated Names

?> You may ignore this section if your game is not obfuscated

Il2CppAssemblyUnhollower is what is used to generate proxy mono assemblies from Il2Cpp code. It will automatically assign auto-generated names to obfuscated names. 

The names are generated following certain rules:<br>
For fields and properties:
- Names will start with `field` for fields, and `prop` for properties
- Then it will be the access modifier: `Public`, `Private`, etc.
- Then it will have an integer which is added to prevent name overlap
- All of these are separated by underscores

For methods:
- Names will start with `Method`
- Then the access modifier/s listed, separated by underscores
- Then a list of the parameter Types in order, separated by underscores
- Then the return type
- Optionally, there will be `PDM`, standing for "Possibly Dead Method", which is added if there is no reference to the method in the code, but note that inline references are not counted as references due to limitations and methods with `PDM` may still be called by the game
- Then it will have an integer which is added to prevent name overlap
- All of these are separated by underscores

For classes:
- Names will start with the inherited type or `Enum` for enums, or `Interface` for interfaces. If the type inherited is obfuscated the name will start with the first non-obfuscated name with an integer representing the inheritance depth needed to get to the non-obfuscated class.
- Then the access modifier/s
- Then the first 2 letters of various members listed limited to 10 members. If an enum has a number it will be the number of entries minus one, the member order is pseudo-random
- Then `Unique` if the name is unique, or if there is another class with the same name, an integer

### Custom Components / Il2Cpp Type Inheritance

> For more info, please check [Il2CppAssemblyUnhollower's readme on github](https://github.com/knah/Il2CppAssemblyUnhollower#class-injection)

When making a class inheriting from an Il2Cpp type, we have to follow these 4 rules:
 - Inherit from a non-abstract Il2Cpp class
 - Have a constructor taking an IntPtr and passing it to a base constructor (called by the Il2Cpp side)
 - Register the class before using it, using `ClassInjector.RegisterTypeInIl2Cpp<T>()`
 - If you need to instantiate it from the mono-side, you need to have a constructor calling `ClassInjector.DerivedConstructorPointer<T>()` and `ClassInjector.DerivedConstructorBody(this)`

Here is a very basic example:
```cs
class MyCustomComponent : MonoBehaviour
{
    public MyCustomComponent(IntPtr ptr) : base(ptr) {}

    // Optional, only used in case you want to instantiate this class in the mono-side
    // Don't use this on MonoBehaviours / Components!
    public MyCustomComponent() : base(ClassInjector.DerivedConstructorPointer<MyCustomComponent>()) => ClassInjector.DerivedConstructorBody(this);

    // Code, same as in a normal component
}
```

A good practice is to call `ClassInjector.RegisterTypeInIl2Cpp<T>()` as early as possible to avoid issue.<br/>
In a mod, it would look like this:
```cs
class MyMod : MelonMod
{
    public override void OnApplicationStart()
    {
        ClassInjector.RegisterTypeInIl2Cpp<MyCustomComponent>();

        // ...

        // And then, add it to a component:
        ourGameObject.AddComponent<MyCustomComponent>();

        // Or in case you want to instantiate it:
        new MyCustomComponent(); // Requires the default constructor shown above
    }
}
```

Limitations:
 - Interfaces can't be implemented
 - Virtual methods can't be overridden
 - Only instance methods are exposed to IL2CPP side - no fields, properties, events or static methods will be visible to IL2CPP reflection
 - Only a limited set of types are supported for method signatures

If you don't want to expose a method to the Il2Cpp side (either because it's not required or to avoid errors), you can add the `[HideFromIl2Cpp]` attribute to the method

### Coroutines

!> This part contains some unreleased code.

In a standard Mono game, you would use `StartCoroutine`. Since MelonMod isn't a component, and that anyway we can't use a Mono IEnumerator on Il2Cpp due to how those are handled in C#, we need to do it another way.

To do that, MelonLoader includes replacement class: `MelonLoader.MelonCoroutines`!
 - `CoroD Start<T>(T routine)`: Starts a new coroutine, which will be ran at the end of the frame.
 - `void Stop(CoroD routine)`: Stops a running coroutine.

### Usage of Il2Cpp Types

In case you want to run an Il2Cpp method taking a type, you may want to use `.GetType()`.<br/>
`.GetType()` would actually returns the Mono type, and not the original Il2Cpp type. To do so, we need to replace it with `.Il2CppType`.
```cs
Resources.FindObjectsOfTypeAll(Camera.Il2CppType);
```
Note: you can use the Mono type directly in case of generic method:
```cs
Resources.FindObjectsOfTypeAll<Camera>();
```

### Casting Il2Cpp Types

In a standard Mono game, casting is quite easy.<br/>
Let's say we have a class `MyChildClass`, which inherit from `MyParentClass`.<br />
Casting it in Mono would go like that:
```cs
MyParentClass childInstance; // This values is already defined

MyChildClass childInstanceCasted = childInstance as MyChildClass;
// or
MyChildClass childInstanceCasted = (MyChildClass) childInstance;
```
We can't do that with Il2Cpp objects. We have to use some methods from Il2CppAssemblyUnhollower:
```cs
using UnhollowerBaseLib;
// ...
MyChildClass childInstanceCasted = childInstance.TryCast<MyChildClass>();
// or
MyChildClass childInstanceCasted = childInstance.Cast<MyChildClass>();
```

### System.String vs Il2CppSystem.String

in a lot of languages, the type `string` is used the same way as if it was a primitive type. `string` isn't a primitive type, so the same rules as Il2Cpp objects apply.

Most methods that was asking for a `string` (`System.String`) will now ask for an `Il2CppSystem.String`. Thankfully, `Il2CppSystem.String` has an explicit cast for `string`.<br/>
This means we can use it like this:
```cs
Debug.Log((Il2CppSystem.String) "Hello World!");
```

### Actions

We know, you all love delegates. Except they do not work as-is with Il2Cpp.

Most Unity events have an implicit cast of `System.Action`, which is a delegate type.<br>
The current issue is that an Il2Cpp event will now take an `Il2CppSystem.Action`, which isn't a delegate type anymore. We will have to use the implicit cast of `Il2CppSystem.Action` to cast an `System.Action`.

Let's say we have a method `MyComponent.AddAction(Action<Component> onComponentDidSomething)`. We can use it like this:
```cs
MyComponent.AddAction(new System.Action<Component>(component => {
    MelonModLogger.Log($"The component {component.name} did something!");
}))
```
or with `MyComponent.AddUnityEvent(UnityEngine.UnityEvent<Component> onComponentDidSomething)`:
```cs
MyComponent.AddUnityEvent(new System.Action<Component>(component => {
    MelonModLogger.Log($"The component {component.name} did something!");
}))
```

### Events

!> This code is subject to change and become easier with the upcoming updates

Events in unity are kinda similar to properties.<br/>
let's imagine you have an `event Action<Player> onPlayerJoin;`. This code will generate the following methods:
 - `add_onPlayerJoin(Action<Player>)`: equivalent of doing `onPlayerJoin +=`
 - `remove_onPlayerJoin(Action<Player>)`: equivalent of doing `onPlayerJoin -=`

As expected, the `+=` and `-=` methods can't be used on an Il2Cpp type, since the type has already been processed. We will have to use the generated methods. Since these methods were using some `System.Action`, these have been converted to `Il2CppSystem.Action`.<br/>
Using MelonLoader, our event is now something like this:
```cs
Action<Player> onPlayerJoin;
public void add_onPlayerJoin(Il2CppSystem.Action<Player> value) { /* does stuff with onPlayerJoin */ }
public void remove_onPlayerJoin(Il2CppSystem.Action<Player> value) { /* does stuff with onPlayerJoin */ }
```

In the case we want to add an event calling `void MyEventListener(Player player)`, we now have to do the following:
```cs
playerManagerInstance.add_onPlayerJoin(new Action<Player>(MyEventListener));
// ...
void MyEventListener(Player player) { /* Do things */ }
```

Sometime, the `add_` and `remove_` methods are stripped by the Il2Cpp compiler. In such cases, we have to use the `CombineImpl` method:
```cs
playerManagerInstance.onPlayerJoin
    .CombineImpl((Il2CppSystem.Action<Player>) MyEventListener)
```
