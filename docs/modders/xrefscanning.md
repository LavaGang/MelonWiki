# Xref Scanning

Xref Scanning stands for Cross Reference Scanning. It is a technology that is almost integral to modding, especially for obfuscated and Il2Cpp games.

Normally while modding, modders would have to hope that an obfuscated method name does not change between updates.
Xref Scanning omits this completely allowing modders to futureproof their mods and not have them break every udpate.
It basically allows modders to get strings and methods used in a scanned method and also methods that use that scanned method.
They can then use this information to identify a method without using its name. 
Since the information Xref Scans gather is much more static than method names, mods can be more easily futureproofed.

Note that on Il2Cpp games Xref Scanning cannot find virtual method calls, delegate creation, and inline method calls.

!> The following guides assume you have basic knowledge of modding with MelonLoader. For a guide on modding with MelonLoader refer to the [Quick Start](https://melonwiki.xyz/#/modders/quickstart)

### Finding Methods Calls Within a Method

First, ensure you have `UnhollowerBaseLib.dll` referenced. It can be found in the `MelonLoader/Managed` folder.<br>
Now we can use `UnhollowerRuntimeLib.XrefScans.XrefScanner.XrefScan(methodBase)` to scan our method (`methodBase`) of choice in the form of a `MethodBase`.<br>
This will return an `IEnumerable<UnhollowerRuntimeLib.XrefScans.XrefInstance>`, which we can loop through.<br>
Here's what your code should look like so far:
```cs
var instances = UnhollowerRuntimeLib.XrefScans.XrefScanner.XrefScan(methodBase);
foreach (UnhollowerRuntimeLib.XrefScans.XrefInstance instance in instances) 
{
    
}
```

With this set up, we can now call `TryResolve()` on the `XrefInstance` to get the `MethodBase` representing a method called in the scanned method.<br>
The final code should look like this:
```cs
var instances = UnhollowerRuntimeLib.XrefScans.XrefScanner.XrefScan(methodBase);
foreach (UnhollowerRuntimeLib.XrefScans.XrefInstance instance in instances) 
{
    MethodBase calledMethod = instance.TryResolve();
    
    // The rest of your code using this information
}
```
Note that `TryResolve` may not always return a `MethodBase`. So, make sure to have a null check or to catch the exception

### Finding Methods That Use a Method

Doing this is almost identical to finding method calls within a method. The only difference is using `UsedBy` instead of `XrefScan`.

First, ensure you have `UnhollowerBaseLib.dll` referenced. It can be found in the `MelonLoader/Managed` folder.<br>
Now we can use `UnhollowerRuntimeLib.XrefScans.XrefScanner.UsedBy(methodBase)` to scan our method of choice in the form of a `MethodBase`.<br>
This will return an `IEnumerable<UnhollowerRuntimeLib.XrefScans.XrefInstance>`, which we can loop through.<br>
Here's what your code should look like so far:
```cs
var instances = UnhollowerRuntimeLib.XrefScans.XrefScanner.UsedBy(methodBase);
foreach (UnhollowerRuntimeLib.XrefScans.XrefInstance instance in instances) 
{
    
}
```

With this set up, we can now call `TryResolve()` on the `XrefInstance` to get the `MethodBase` representing a method that used the scanned method.<br>
The final code should look like this:
```cs
var instances = UnhollowerRuntimeLib.XrefScans.XrefScanner.UsedBy(methodBase);
foreach (UnhollowerRuntimeLib.XrefScans.XrefInstance instance in instances) 
{
    MethodBase calledMethod = instance.TryResolve();
    
    // The rest of your code using this information
}
```
Note that `TryResolve` may not always return a `MethodBase`. So, make sure to have a null check or to catch the exception

### Finding Strings Used in a Method

The first steps of doing this are very similar to finding methods that use a method and finding methods called within a method.

First, ensure you have `UnhollowerBaseLib.dll` referenced. It can be found in the `MelonLoader/Managed` folder.<br>
Now we can use `UnhollowerRuntimeLib.XrefScans.XrefScanner.XrefScan(methodBase)` to scan our method of choice in the form of a `MethodBase`.<br>
This will return an `IEnumerable<UnhollowerRuntimeLib.XrefScans.XrefInstance>`, which we can loop through.<br>
Here's what your code should look like so far:
```cs
var instances = UnhollowerRuntimeLib.XrefScans.XrefScanner.XrefScan(methodBase);
foreach (UnhollowerRuntimeLib.XrefScans.XrefInstance instance in instances) 
{
    
}
```

Now this is where finding strings splits.<br>
To find the strings, we must ensure that the `UnhollowerRuntimeLib.XrefScans.XrefType` of our instance is `Global`.<br>
This can be done like so:
```cs
var instances = UnhollowerRuntimeLib.XrefScans.XrefScanner.XrefScan(methodBase);
foreach (UnhollowerRuntimeLib.XrefScans.XrefInstance instance in instances) 
{
    if (instance.Type == UnhollowerRuntimeLib.XrefScans.XrefType.Global)
    {
        
    }
    else
    {
        continue;
    }
}
```

Now, we can call `ReadAsObject()` to get an `Il2CppSystem.Object` representing the scanned method. 
If we did not make sure our instance type was global, `ReadAsObject()` would return false.<br>
If we now call `ToString()` on the instance, we can get the strings used in the scanned method.<br>
This looks like this:
```cs
var instances = UnhollowerRuntimeLib.XrefScans.XrefScanner.XrefScan(methodBase);
foreach (UnhollowerRuntimeLib.XrefScans.XrefInstance instance in instances) 
{
    if (instance.Type == UnhollowerRuntimeLib.XrefScans.XrefType.Global)
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

### Actual Example

Here is an example of Xref Scanning in a mod. This is taken from loukylor's mod [UserInfoExtensions](https://github.com/loukylor/UserInfoExtensions/blob/main/Utilities.cs), and slightly changed to match this guide's style.<br>
This Xref Scan will get the method responsible to opening a UI popup.
```cs
MethodBase popupV2 = typeof(VRCUiPopupManager).GetMethods()
    .Where(mb => mb.Name.StartsWith("Method_Public_Void_String_String_String_Action_Action_1_VRCUiPopup_") && !mb.Name.Contains("PDM") && UnhollowerRuntimeLib.XrefScans.XrefScanner.XrefScan(mb) // Filter out certain methods using basic reflection and start the Xref Scan
    .Where(instance => instance.Type == UnhollowerRuntimeLib.XrefScans.XrefType.Global && instance.ReadAsObject().ToString() == "UserInterface/MenuContent/Popups/StandardPopupV2").Any()).First() // Check for the string "UserInterface/MenuContent/Popups/StandardPopupV2" in the method using Xref Scanning
```            
