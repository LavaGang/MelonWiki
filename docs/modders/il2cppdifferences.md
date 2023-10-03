# Il2Cpp Differences

MelonLoader have some "small" things that doesn't work the exact same as if you were modding a Mono game.

> If you find something that doesn't seems natural with Il2Cpp and that isn't listed here, please ping _loukylor#0001_ on the [MelonLoader Discord](https://discord.gg/2Wn3N2P).

### Il2cppInterop Generated Names

?> You may ignore this section if your game is not obfuscated

Il2cppInterop is what is used to generate proxy mono assemblies from Il2Cpp code. It will automatically assign auto-generated to obfuscated names. 

The names are generated following certain rules:
For fields and properties:
- Names will start with `field` for fields, and `prop` for properties
- Then it will be the access modifier: `Public`, `Private`, etc.
- Then it will have an integer which is added to prevent name overlap
- All of these are split by underscores

For methods:
- Names will start with `Method`
- Then the access modifier/s listed, separated by underscores
- Then a list of the parameter Types in order, separated by underscores
- Then the return type
- Optionally, there will be `PDM`, standing for "Possibly Dead Method", which is added if there is no reference to the method in the code, but not that inline references are not counted as references due to limitations and methods with `PDM` may still be called by the game
- Then it will have an integer which is added to prevent name overlap
- All of these are separated by underscores

For classes:
- Names will start with the inherited type or `Enum` for enums, or `Interface` for interfaces. If the type inherited is obfuscated the name will start with the first non-obfuscated name with an integer representing the inheritance depth to get to the non-obfuscated class.
- Then the access modifier/s
- Then the first 2 letters of various members listed limited to 10 members. If an enum has a number it will be the number of entries minus one
- Then `Unique` if the name is unique, or if there is another class with the same name, an integer

### Custom Components / Il2Cpp Type Inheritance

> For more info, please check [Il2CppInterop's readme on github](https://github.com/BepInEx/Il2CppInterop/blob/master/Documentation/Class-Injection.md)

When making a class inheriting from an Il2Cpp type, we have to follow these 4 rules:
 - Inherit from a non-abstract Il2Cpp class
 - Have a constructor taking an IntPtr and passing it to a base constructor (called by the Il2Cpp side)
 - Register the class before using it by adding the `MelonLoader.RegisterTypeInIl2Cpp` attribute to the class or using `Il2CppInterop.Runtime.Injection.ClassInjector.RegisterTypeInIl2Cpp.RegisterTypeInIl2Cpp<T>()` 
 - If you need to instantiate it from the mono-side, you need to have a constructor calling `Il2CppInterop.Runtime.Injection.ClassInjector.DerivedConstructorPointer<T>()` and `Il2CppInterop.Runtime.Injection.ClassInjector.DerivedConstructorBody(this)`

Note that `MelonLoader.RegisterTypeInIl2Cpp` will register all parent types if added to a child class. It is good practice to add the attribute to every custom injected class however.

Here is a very basic example:
```cs
// You must reference `Il2cppInterop.Runtime.dll` for this to work
using Il2CppInterop.Runtime;

[RegisterTypeInIl2Cpp]
class MyCustomComponent : MonoBehaviour
{
    public MyCustomComponent(IntPtr ptr) : base(ptr) {}

    // Optional, only used in case you want to instantiate this class in the mono-side
    // Don't use this on MonoBehaviours / Components!
    public MyCustomComponent() : base(ClassInjector.DerivedConstructorPointer<MyCustomComponent>()) => ClassInjector.DerivedConstructorBody(this);

    // Code, same as in a normal component
}
```

If you choose to manually call `ClassInjector.RegisterTypeInIl2Cpp<T>()`, it would look like this.<br/>
Keep in mind, it must be called before the class is ever used.<br>
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

In a standard Mono game, you would use `StartCoroutine`. Since MelonMod isn't a component, and we also can't use a Mono IEnumerator on Il2Cpp due to how those are handled in C#, we need to do it another way.

To do that, MelonLoader includes replacement class: `MelonLoader.MelonCoroutines`!
 - `object Start(IEnumerator routine)`: Starts a new coroutine, which will be ran at the end of the frame.
 - `void Stop(object coroutineToken)`: Stops a running coroutine.

Otherwise, coroutines work nearly identically to regular unity:
```cs
System.Collections.IEnumerator myCoroutine() {
    LoggerInstance.Msg("This logs immediately");
    yield return null;

    LoggerInstance.Msg("This logs on the next frame");
    yield return new WaitForSeconds(5.0);

    LoggerInstance.Msg("This logs after 5 seconds of the last log");
}

// ... in some method
object routine = MelonCoroutines.Start(myCoroutine());

// If you ever decide to stop the routine, pass the return value of
// Start into Stop
MelonCoroutines.Stop(routine);
```

### Usage of Il2Cpp Types

In case you want to run an Il2Cpp method taking a type, you may want to use `.GetType()`.<br/>
`.GetType()` would actually returns the Mono type, and not the original Il2Cpp type. To do so, we need to replace it with `Il2CppInterop.Runtime.Il2CppType.Of<T>()`.
```cs
// You must reference `Il2cppInterop.Runtime.dll` for this.
using Il2CppInterop.Runtime;

Resources.FindObjectsOfTypeAll(Il2CppType.Of<Camera>());
```
Note: you can use the Mono type directly in generic methods:
```cs
Resources.FindObjectsOfTypeAll<Camera>();
```

### Casting Il2Cpp Types
!> This code is subject to change and become easier with the upcoming updates

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
using Il2CppInterop.Runtime;
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
