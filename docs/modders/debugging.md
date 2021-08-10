# Debugging

## Using dnSpy

?> For this, you need to have dnSpy installed, obviously. Install it [here](https://github.com/dnSpy/dnSpy).

For those who don't know, MelonLoader is fully set up to use dnSpy's built in debugger.<br>
To attach it, follow these steps:
 - Go into dnSpy, then in the top, select `Debug` -> `Start Debugging` and select `Unity` as the debug engine.
 - Then, for the executable, select your game's executable
 - And in the `Arguments` box, add `--melonloader.debug` and any other arguments you want
 - Finally, to add breakpoints, simply drag and drop the mod you want to debug into dnSpy's Assembly Explorer, then add breakpoints regularly.

If you've followed all the steps, properly, this should all work.

!> If you have any other doorstops or loaders installed on the game, that do not support dnSpy's debugger, then the game will crash on load.

## Reading Exceptions

In MelonLoader, there are no line numbers when errors are logged making debugging from logs supplied by users difficult. However, there is an alternative.<br>
Take this example exception:

```cs
System.Exception: An exception was thrown
  at MyFirstMod.MainClass.OnUpdate () [0x0001a] in <e2601fbc36fa4891b5bcba3b789203ba>:0 
```

You can find where this error was thrown in your code by using the hex value surrounded by brackets. In this example, it would be `[0x0001a]`.<br>
This hex value is the IL offset which the error was thrown at. So, to figure out which line errored specifically, you can look in any .NET Decompiler that shows an assembly's IL code as well as IL offset.

In the case of dnSpy, you can right click the method that errored, then select `Edit IL Instructions...`. In the window that popped up, you can see each IL code and it's offset.<br>
If you're having trouble converting this into a line number, select a random line in the erroring method's body, then open the IL window. The IL codes that are associated with that line will be highlighted. Using this, you could find which code points to which line.

Of course, there are other decompilers that can view IL codes, but dnSpy is the most convenient one given it is needed to debug your mods.