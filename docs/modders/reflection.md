# Reflection

!> If you are modding an Il2Cpp game then all methods and classes will be made public by unhollower, so unless a game is obfuscated, you won't need to use reflection.

Reflection isn't exactly specific to MelonLoader, it's built into C#.<br>
However, it is extremely useful in modding obfuscated games, and even has some uses in unobfuscated games.

The reason it's useful in mods is because it allows you to dynamically call methods, without making direct references to them, and being able to change them during runtime.
Here is a just a list of it's uses:
 - In mono games, it let's you use non-public things. 
 - In obfuscated games, it let's you use [xref scanning](xrefscanning.md) to future proof mods.
 - In all games it's important to make optional dependencies.
 - In all games it's also important for method patching.

### Usage
Using reflection is pretty simple. A bit tedious at times though.

Let's define an example class:
```cs
public class Example
{
    public static Example Instance;

    internal string _myField;

    private static string _myString { get; set; }

    private static void PrivateMethod(string param1)
    {
        
    }
}
```

### Getting and Setting a Field

Now let's try getting and setting the value of the field.
To start off, make sure you are using the `System.Reflection` namespace. 
Next, we need to grab the type. To do this, simply do `typeof(Example)`.<br>
Then using return value of `typeof`, call `GetField`. The first argument should be the name of the field, so "_myField".
By default, `GetField` will only search for public static or public instance fields, so we have to specify that we want a non-public instance field.<br>
To do this, set `BindingFlags.NonPublic | BindingFlags.Instance` as the second parameter. And if you don't know, the `|` operator in this case, will combine Enum values.
 There's more to it, but that is all you need to know at this moment.<br>
 At this point your code should look something like this:
 ```cs
 using System.Reflection;

 // Inside the method body

 Type exampleType = typeof(Example);
 FieldInfo myField = exampleType.GetField("_myField", BindingFlags.NonPublic | BindingFlags.Instance);
 ```

Now we have the `FieldInfo` of our field. This is what Reflection uses to represent fields in an object.<br>
Finally, to set the value, simply call `SetValue`. The method takes 2 parameters, the first being the instance of the class of the field. If the field is static, you can pass in null. The second will be the value you want to set the field to. You may need to explicitly cast it to `object`.
In full, this looks like this:
```cs
myField.SetValue(null, "New value");
```

Then to get the value, simply call `GetValue`, It only has one parameter, which is the same as the first parameter of `SetValue`.<br>
Note that `GetValue` returns just an object, so you will have to explicitly cast it to the type you want.
This looks something like so:
```cs
string myFieldValue = (string)myField.GetValue(null);
```

### Getting and Setting a property

Getting and setting the value of a property is almost identical to doing the same with a field. This time we are using the `_myString` property.

Like before, we start off by using the `System.Reflection` namespace. Then, grab the type using `typeof(Example)`.<br>
After that, call the `GetProperty` method on the return value, and as our parameter, include the name of the property, so "_myString".<br>
Like `GetField`, `GetProperty` will automatically scan for public instance and public static properties, so there is no need to specify `BindingFlags`.<br>
In full, the code should look something like this:
```cs
using System.Reflection;

// Inside the method body

Type exampleType = typeof(Example);
PropertyInfo myString = exampleType.GetProperty("_myString");
```
Now, using the instance of `PropertyInfo` we have, we can call `SetValue`. Its parameters are the same as the parameters in `FieldInfo`'s `SetValue`.<br>
So the first parameter will be the instance of our `Example` class, and the second value will be the value we want to set the property to, which may need to be casted to an `object`.<br>
In full, it would look something like this:
```cs
myString.SetValue(Example.Instance, "New value");
```

To get the value, simply call `GetValue` on the `PropertyInfo` instance, and as the first and only parameter, use the instance of the `Example` class.<br>
Like fields, `GetValue` returns an `object`, which will likely need to be casted.<br>
Full code looks like this:
```cs
string myStringValue = (string)myString.GetValue(Example.Instance);
```

### Calling a Method Using Reflection

Calling a method is similar to properties and fields. Let's call the `PrivateMethod` method.

As always, we start off using `System.Reflection` and get the type by using `typeof(Example)` then let's call the `GetMethod` method on the return value.<br>
The first parameter will be the name of the method, so "PrivateMethod".<br>
Similarly to `GetField` and `GetProperty`, `GetMethod` will only look for public instance or public static methods. So we have to specify that we want a private static method.
We do this the same way as when we got the field. Except, instead of `BindingFlags.Instance`, we do `BindingFlags.Static`. <br>
In full, it would look like this:
```cs
using System.Reflection;

// Inside the method body

Type exampleType = typeof(Example);
MethodInfo privateMethod = exampleType.GetMethod("PrivateMethod");
```

Now to call the method, simply use the `Invoke` method. The first parameter would normally be an instance of the method's declaring type, but since it's static, the first parameter is null.<br>
The next parameter will be an array of objects that are the method's parameters.<br>
Invoke will also return the result of the method as an `object`. But since our method returns void, `Invoke` returns null.
Full code looks like so:
```cs
privateMethod.Invoke(null, new object[] { "param value" });
```

Now what if we had another method in the `Example` class that overloaded `PrivateMethod`:
```cs
private static void PrivateMethod(int param1)
{

}
```
We obviously couldn't just get the method from the name, because there are 2 methods with the same name.<br>
So, when we call `GetMethod` we have to pass in an array of `Type`s that matcht the parameters of the method.<br>
If we wanted the overload that takes an `int` as its first parameter, the code would look like this:
```cs
MethodInfo privateMethod = exampleType.GetMethod("PrivateMethod", new Type[] { typeof(int) });
```
And if we wanted the string overload, the code would like look this:
```cs
MethodInfo privateMethod = exampleType.GetMethod("PrivateMethod", new Type[] { typeof(string) });
```
