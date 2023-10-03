# Xref Scanning

Xref Scanning stands for Cross Reference Scanning. It is a technology that is almost integral to modding, especially for obfuscated and Il2Cpp games.

Normally while modding, modders would have to hope that an obfuscated method name does not change between updates.
Xref Scanning omits this completely allowing modders to futureproof their mods and not have them break every udpate.
It basically allows modders to get strings and methods used in a scanned method and also methods that use that scanned method.
They can then use this information to identify a method without using its name. 
Since the information Xref Scans gather is much more static than method names, mods can be more easily futureproofed.

Note that on Il2Cpp games Xref Scanning cannot find virtual method calls, delegate creation, and inline method calls.

!> The following guides assume you have basic knowledge of modding with MelonLoader. For a guide on modding with MelonLoader refer to the [Quick Start](/modders/quickstart)

### Finding Methods Calls Within a Method

First, ensure you have `Il2CppInterop.Common.dll` referenced. It can be found in the `MelonLoader/net6` folder.<br>
Now we can use `Il2CppInterop.Common.XrefScans.XrefScanner.XrefScan(methodBase)` to scan our method (`methodBase`) of choice in the form of a `MethodBase`.<br>
This will return an `IEnumerable<Il2CppInterop.Common.XrefScans.XrefInstance>`, which we can loop through.<br>
Here's what your code should look like so far:
```cs
var instances = Il2CppInterop.Common.XrefScans.XrefScanner.XrefScan(methodBase);
foreach (Il2CppInterop.Common.XrefScans.XrefInstance instance in instances) 
{
    
}
```

With this set up, we can now call `TryResolve()` on the `XrefInstance` to get the `MethodBase` representing a method called in the scanned method.<br>
The final code should look like this:
```cs
var instances = Il2CppInterop.Common.XrefScans.XrefScanner.XrefScan(methodBase);
foreach (Il2CppInterop.Common.XrefScans.XrefInstance instance in instances) 
{
    MethodBase calledMethod = instance.TryResolve();
    
    // The rest of your code using this information
}
```
Note that `TryResolve` may not always return a `MethodBase`. So, make sure to have a null check or to catch the exception

### Finding Methods That Use a Method

Doing this is almost identical to finding method calls within a method. The only difference is using `UsedBy` instead of `XrefScan`.

First, ensure you have `Il2CppInterop.Common.dll` referenced. It can be found in the `MelonLoader/net6` folder.<br>
Now we can use `Il2CppInterop.Common.XrefScans.XrefScanner.UsedBy(methodBase)` to scan our method of choice in the form of a `MethodBase`.<br>
This will return an `IEnumerable<Il2CppInterop.Common.XrefScans.XrefInstance>`, which we can loop through.<br>
Here's what your code should look like so far:
```cs
var instances = Il2CppInterop.Common.XrefScans.XrefScanner.UsedBy(methodBase);
foreach (Il2CppInterop.Common.XrefScans.XrefInstance instance in instances) 
{
    
}
```

With this set up, we can now call `TryResolve()` on the `XrefInstance` to get the `MethodBase` representing a method that used the scanned method.<br>
The final code should look like this:
```cs
var instances = Il2CppInterop.Common.XrefScans.XrefScanner.UsedBy(methodBase);
foreach (Il2CppInterop.Common.XrefScans.XrefInstance instance in instances) 
{
    MethodBase calledMethod = instance.TryResolve();
    
    // The rest of your code using this information
}
```
Note that `TryResolve` may not always return a `MethodBase`. So, make sure to have a null check or to catch the exception

### Finding Strings Used in a Method

The first steps of doing this are very similar to finding methods that use a method and finding methods called within a method.

First, ensure you have `Il2CppInterop.Common.dll` referenced. It can be found in the `MelonLoader/net6` folder.<br>
Now we can use `Il2CppInterop.Common.XrefScans.XrefScanner.XrefScan(methodBase)` to scan our method of choice in the form of a `MethodBase`.<br>
This will return an `IEnumerable<Il2CppInterop.Common.XrefScans.XrefInstance>`, which we can loop through.<br>
Here's what your code should look like so far:
```cs
var instances = Il2CppInterop.Common.XrefScans.XrefScanner.XrefScan(methodBase);
foreach (Il2CppInterop.Common.XrefScans.XrefInstance instance in instances) 
{
    
}
```

Now this is where finding strings splits.<br>
To find the strings, we must ensure that the `Il2CppInterop.Common.XrefScans.XrefType` of our instance is `Global`.<br>
This can be done like so:
```cs
var instances = Il2CppInterop.Common.XrefScans.XrefScanner.XrefScan(methodBase);
foreach (Il2CppInterop.Common.XrefScans.XrefInstance instance in instances) 
{
    if (instance.Type == Il2CppInterop.Common.XrefScans.XrefType.Global)
    {
        
    }
    else
    {
        continue;
    }
}
```

Now, we can call `ReadAsObject()` to get an `Il2CppSystem.Object` representing the scanned method. 
If we did not make sure our instance type was global, `ReadAsObject()` would return null.<br>
If we now call `ToString()` on the instance, we can get the strings used in the scanned method.<br>
This looks like this:
```cs
var instances = Il2CppInterop.Common.XrefScans.XrefScanner.XrefScan(methodBase);
foreach (Il2CppInterop.Common.XrefScans.XrefInstance instance in instances) 
{
    if (instance.Type == Il2CppInterop.Common.XrefScans.XrefType.Global)
    {
        Il2CppSystem.Object methodObject = instance.ReadAsObject();
        string usedString = methodObject.ToString();
        
        // Rest of your code
    }
    else
    {
        continue;
    }
}
```

### Example

For an example, let's use the method `foo` in the `Example` class, which gets called by `bar`.
Let's also assume that the `foo` method has the literal "Example Xref" in it.

If we were to use the literal to xref for the `foo` method, it would look something like this:
```cs
MethodInfo fooMethod = typeof(Example).GetMethods() // Get the methods in the Example class
    .First(mi => XrefScanner.XrefScan(mi) // Scan each method
        .Any(instance => instance.Type == XrefType.Global && instance.ReadAsObject() != null && instance.ReadAsObject().ToString() == "Example Xref")); // Determine if the method has the literal
```

Now, if we were to scan for the fact that `foo` gets called by `bar`, it would look like this:
```cs
MethodInfo fooMethod = typeof(Example).GetMethods() // Get the methods in the Example class
    .First(mi => XrefScanner.UsedBy(mi) // Scan each method
        .Any(instance => instance.Type == XrefType.Method && instance.TryResolve() != null && instance.TryResolve().Name == "bar")); // Determine if the method gets called by bar
```