# Melon Console

!> Please note that Melon Console is still a 'work in progress' feature. The console might not work on all games.

Melon Console is a built-in console that allows users to execute MelonLoader's debug commands and custom Mod commands.

### Toggling

The Melon Console can be toggled using the [Backquote Key](https://www.computerhope.com/jargon/b/backquot.htm).

> For the following example, I will be using [Welcome to the Game II](https://store.steampowered.com/app/720250/Welcome_to_the_Game_II/) as my test game.

Once you have toggled the Console, it should look somewhat like this:<br>
![image](https://user-images.githubusercontent.com/61495410/157124552-2ede1699-aa8e-4d9e-b842-e80da0323062.png)

The bottom black panel is the command input field. Once you have opened the console, the command input field will be automatically selected and ready for any user input.

### Executing Commands

The Melon Console Commands format is pretty straight forward: `[commandName] [argument1] [argument2] [argument3] etc...`

Arguments that contain any spaces should be put between quotation marks to not get split by the argument splitter.<br>
For example: `melonassembly.register "C:\Some Mod With Spaces.dll"`

### MelonLoader Commands

The Melon Console comes with some additional built-in commands. Here is a full list:
| Command              | Description                              |
| -------------------- | ---------------------------------------- |
| commands	| Prints a list of all registered Melon Commands. |
| help [commandName]	| Describes the usage of a specific command. |
| exit	| Closes the game. |
| forceexit	| Forcefully closes the game by killing it's process. |
| melonassembly.load [path]	| Loads a Melon Assembly. |
| melonassembly.register [path]	| Registers all Melons in a Melon Assembly. |
| melonassembly.unregister [path]	| Unregisters all Melons in a Melon Assembly. |
| melon.isregistered [name] \[author]	| Prints `true` if a Melon with the given info is already registered, otherwise prints `false`. |

Modders also have the ability to register their own Melon Commands in their Mods! More on registering Melon Commands in the [Modders Guide](modders/MelonConsoleModders.md).

### Previous Commands

The Melon Console allows you to scroll through your previously executed Commands to easily repeat commands without the effort of having to rewrite them.<br>
You can simply navigate through the executed commands history with the `up` and `down` arrow keys.
