# Melon Console Modding

!> The Melon Console relies on Unity's IMGUI module and may not work on some games that might have some parts of the module stripped.
!> We are planning on switching to another rendering library in the future to solve this issue.

The [Melon Console](ExtraFeatures/MelonConsole.md) allows Mods to register their own Melon Commands.<br>
Mod commands can be useful for non-GUI Mod features, but also for debugging.

### Registering Commands

The process of registering Melon Commands is very simple.

The following example demonstrates how to register parameterless commands:
```cs
public override void OnInitializeMelon()
{
    var testCommand = new MelonCommand("test", "Just a simple test.", new Action(TestCommand));
    MelonConsole.RegisterCommand(testCommand);
}

private void TestCommand()
{
    LoggerInstance.Msg("Testing!");
}
```

Sometimes you will want to take in some arguments before executing a command.<br>
The process of registering commands with parameters is also very simple. The only difference is that you will have to manually define those parameters.<br>
The last parameter of `RegisterCommand` takes in an array of `MelonCommand.Paramater`s, which we will have to use to define command parameters.<br>
Melon Command Parameters can be of any Type as long as they're convertable by `System.Convert::ChangeType` (from a string).

For this instance, let's create 2 parameters of 2 different Types:
```cs
public override void OnInitializeMelon()
{
    var spawnHumanCommand = new MelonCommand("spawnhuman", "Spawns a new human.", new Action<string, int>(SpawnHuman), new MelonCommand.Parameter("name", typeof(string)), new MelonCommand.Parameter("age", typeof(int)));
    MelonConsole.RegisterCommand(spawnHumanCommand);
}

private void SpawnHuman(string name, int age)
{
    LoggerInstance.Msg($"Spawned {name}! {name} is {age} years old.");
}
```

Here is an example usage of the command: `spawnhuman "Bob Derp" 80`

### Unregister Commands

Normally, once your Mod has deinitialized, MelonConsole will automatically unregister any commands that you have registered.<br>
However, you can still unregister any command manually.

The following example shows how to unregister a command:
```cs
private MelonCommand spawnHumanCommand;

public override void OnInitializeMelon()
{
    spawnHumanCommand = new MelonCommand("spawnhuman", "Spawns a new human.", new Action<string, int>(SpawnHuman), new MelonCommand.Parameter("name", typeof(string)), new MelonCommand.Parameter("age", typeof(int)));
}

public override void OnSceneWasInitialized(int buildIndex, string sceneName)
{
    if (buildIndex == 1)
    {
        MelonConsole.RegisterCommand(spawnHumanCommand);
    }
    else
    {
        MelonConsole.UnregisterCommand(spawnHumanCommand.name);
    }
    // This piece of code will only register our command in one specific scene and unregister it in any other scene.
}
```
