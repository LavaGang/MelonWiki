# Requirements

- In order to run the Automated Installer and MelonLoader you must have [.NET Framework 4.8 Runtime](https://dotnet.microsoft.com/download/dotnet-framework/net48) installed.
- In order to run MelonLoader you must have [Microsoft Visual C++ 2015-2019 Redistributable](https://aka.ms/vs/16/release/vc_redist.x64.exe) installed.


# Automated Installation

1. Download [MelonLoader.Installer.exe](https://github.com/HerpDerpinstine/MelonLoader/releases/latest/download/MelonLoader.Installer.exe).
2. Run MelonLoader.Installer.exe.
3. Click the SELECT button.
4. Select and Open the Game's EXE in your Game's Installation Folder.
5. Select which Version of MelonLoader to install using the Drop-Down List.  (Or leave it as-is for the Latest Version.)
6. Click the INSTALL or RE-INSTALL button.

?> Make sure the version of MelonLoader you select is the one that your game uses. You can check by asking in the respective community. A list of them can be found in the `Officially Supported Games` tab.

# Manual Installation

> It's **highly** recommended to use the automated installation when you can.

1. - If your game is 32bit download [MelonLoader.x86.zip](https://github.com/LavaGang/MelonLoader/releases/download/v0.5.0/MelonLoader.x86.zip)
   - If your game is 64bit download [MelonLoader.x64.zip](https://github.com/LavaGang/MelonLoader/releases/download/v0.5.0/MelonLoader.x64.zip)
2. Extract the MelonLoader folder from the zip file you just downloaded to the Game's Installation Folder.
3. Extract version.dll as well from the zip file you just downloaded to the Game's Installation Folder. 

?> If you aren't sure if your game is 32bit or 64bit an easy way to find out is to to use the task manager. If your game is 32bit, the game name will be followed by (32 bit). Example: `Among Us.exe (32 bit)` vs `BONEWORKS.exe`

# Contact

If you need any help, feel free to ask us in the #melonloader-support channel of the [MelonLoader Discord](https://discord.gg/2Wn3N2P)!<br>
When contacting, please include the specific issue you're having, as well as a log file. Include as much information as possible, it just makes everyone' lives easier.

Or, if you see any issues with the wiki, please contact one of the editors in the [credits](credits.md) in the MelonLoader Discord


# Launch commands

MelonLoader has some launch arguments, listed here:

| Argument              | Description                              |
| --------------------- | ---------------------------------------- |
| --no-mods	| Launch game without loading Mods |
| --quitfix	| Fixes the Hanging Process Issue with some Games |
| --melonloader.hideconsole	| Hides the Normal Console |
| --melonloader.hidewarnings | Hides Warnings from Displaying |
| --melonloader.debug	| Debug Mode/Console |
| --melonloader.magenta	| Magenta Console Color |
| --melonloader.rainbow	| Rainbow Console Color |
| --melonloader.randomrainbow	| Random Rainbow Console Color |
| --melonloader.maxlogs	| Max Log Files [ Default: 10 ] [ Disable: 0 ] |
| --melonloader.maxwarnings	| Max Warnings per Log File [ Default: 100 ] [ Disable: 0 ] |
| --melonloader.maxerrors	| Max Errors per Log File [ Default: 100 ] [ Disable: 0 ] |
| --melonloader.loadmodeplugins	| Load Mode for Plugins [ Default: 0 ] |
| --melonloader.loadmodemods | Load Mode for Mods [ Default: 0 ] |
| --melonloader.agregenerate | Forces Assembly to be Regenerated on Il2Cpp Games |
| --melonloader.agfvunhollower | Forces use a Specified Version of Il2CppAssemblyUnhollower |
| --melonloader.consoleontop | Forces the Console over all other Applications |


MelonLoader 0.3.0 and up has slightly different launch arguments, listed here:

| Argument              | Description                              |
| --------------------- | ---------------------------------------- |
| --no-mods	| Launch game without loading any Plugins Mods |
| --quitfix	| Fixes the Hanging Process Issue with some Games |
| --melonloader.consoleontop | Forces the Console to always stay on-top of all other Applications |
| --melonloader.hideconsole	| Hides the Console |
| --melonloader.hidewarnings | Hides Warnings from Displaying |
| --melonloader.debug	| Debug Mode |
| --melonloader.dab	| Debug Analytics Blocker |
| --melonloader.magenta	| Magenta Console Color |
| --melonloader.rainbow	| Rainbow Console Color |
| --melonloader.randomrainbow	| Random Rainbow Console Color |
| --melonloader.maxlogs	| Max Log Files [ Default: 10 ] [ Disable: 0 ] |
| --melonloader.maxwarnings	| Max Warnings per Log File [ Default: 100 ] [ Disable: 0 ] |
| --melonloader.maxerrors	| Max Errors per Log File [ Default: 100 ] [ Disable: 0 ] |
| --melonloader.loadmodeplugins | Load Mode for Plugins [ Default: 0 ] |
| --melonloader.loadmodemods | Load Mode for Mods [ Default: 0 ] |
| --melonloader.agfregenerate	| Forces Regeneration of Assembly |
| --melonloader.agfvunity	| Forces use a Specified Version of Unity Dependencies |
| --melonloader.agfvdumper | Forces use a Specified Version of Dumper |
| --melonloader.agfvunhollower | Forces use a Specified Version of Il2CppAssemblyUnhollower |
