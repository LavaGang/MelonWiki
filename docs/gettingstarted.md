# Requirements

- In order to run the Automated Installer and MelonLoader you must have [.NET Framework 4.7.2 Runtime](https://dotnet.microsoft.com/download/dotnet-framework/net472) installed.
- In order to run MelonLoader you must have [Microsoft Visual C++ 2015-2019 Redistributable](https://aka.ms/vs/16/release/vc_redist.x64.exe) installed.


# Automated Installation

1. Download [MelonLoader.Installer.exe](https://github.com/HerpDerpinstine/MelonLoader/releases/latest/download/MelonLoader.Installer.exe).
2. Run MelonLoader.Installer.exe.
3. Click the SELECT button.
4. Select and Open the Game's EXE in your Game's Installation Folder.
5. Select which Version of MelonLoader to install using the Drop-Down List.  (Or leave it as-is for the Latest Version.)
6. Click the INSTALL or RE-INSTALL button.

?> If you would like to install MelonLoader 0.3.0 (practically required for VRChat modding) turn on `Show ALPHA Pre-Releases` in the installer settings

# Manual Installation

1. Download [MelonLoader.zip](https://github.com/HerpDerpinstine/MelonLoader/releases/latest/download/MelonLoader.zip).
2. Extract the MelonLoader folder from MelonLoader.zip to the Game's Installation Folder.
3. Extract version.dll from MelonLoader.zip to the Game's Installation Folder.


# Contact
?> If you need any help, feel free to ask us in the #melonloader-support channel of the [MelonLoader Discord](https://discord.gg/2Wn3N2P)!


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


MelonLoader 0.3.0 has slightly different launch arguments, listed here:

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
