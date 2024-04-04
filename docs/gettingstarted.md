# What is MelonLoader
MelonLoader is a Universal Mod-Loader for Games built in the [Unity Engine](https://unity.com).

You can find mods for games by asking in their respective communities or by looking through our Officially Supported Games list.

!> Please note that MelonLoader does not condone the use of malicious mods. e.g. mods that allow for cheating in online games, among other things.

# Requirements

- In order to run the Automated Installer and MelonLoader you must have [.NET Framework 4.8 Runtime](https://dotnet.microsoft.com/download/dotnet-framework/net48) installed.
- In order to run MelonLoader you must install:
  - [Microsoft Visual C++ 2015-2019 Redistributable 64 Bit](https://aka.ms/vs/16/release/vc_redist.x64.exe) for 64 bit games.
  - [Microsoft Visual C++ 2015-2019 Redistributable 32 Bit](https://aka.ms/vs/16/release/vc_redist.x86.exe) for 32 bit games.
- Il2Cpp games require [dotnet 6.0](https://dotnet.microsoft.com/en-us/download/dotnet/6.0#runtime-desktop-6.0.19). We recommend the .NET Desktop Runtime, x64 or x86 depending on if your game is 64 bit or 32 bit

?> If you aren't sure if your game is 32bit or 64bit an easy way to find out is to to use the task manager. If your game is 32bit, the game name will be followed by (32 bit).

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

1. - If your game is 64bit, download [MelonLoader.x64.zip](https://github.com/LavaGang/MelonLoader/releases/latest/download/MelonLoader.x64.zip)
   - If your game is 32bit, download [MelonLoader.x86.zip](https://github.com/LavaGang/MelonLoader/releases/latest/download/MelonLoader.x86.zip)
2. Extract the MelonLoader folder from the zip file you just downloaded to the Game's Installation Folder.
3. Extract version.dll as well from the zip file you just downloaded to the Game's Installation Folder. 

?> If you aren't sure if your game is 32bit or 64bit an easy way to find out is to to use the task manager. If your game is 32bit, the game name will be followed by (32 bit).

# Linux Instructions

## Windows Games
Please refer to your distribution's specific ways of installing Protontricks. <br>
Arch based distributions may find it in the AUR. Using an AUR helper like paru: `paru -S protontricks` or `paru -S protontricks-git`

Find your game's AppID using `protontricks -s [GameName]`

It is recommended to start over with a *clean* prefix.

Your game's (default) proton prefix will be located at ` ~/.local/share/Steam/steamapps/compatdata/[appid]`. Delete that folder, and start the game once.<br/>
You are now running a clean prefix.

Run `protontricks [appid] winecfg`<br/>
At the bottom, switch the Windows version to Windows 10.<br>
Go to the libraries tab, select `version` from the "new override for library" dropdown, and hit add<br/>
Then hit OK.

!> Il2Cpp games require the Windows version of [dotnet 6.0](https://dotnet.microsoft.com/en-us/download/dotnet/6.0#runtime-desktop-6.0.28). We recommend the .NET Desktop Runtime, x64 or x86 depending on if your game is 64 bit or 32 bit.

To install it automatically, run `protontricks [appid] dotnetdesktop6`.

To install it manually, run `protontricks [appid] uninstaller`, click `Install...`, switch `Files of Type` to `.exe` and run the .NET 6.0 installer from the link above.

Now you can follow the Manual Installation instructions above, or run the Automated installer through wine (until we make it cross-platform) and MelonLoader should pop up on launch.

Should this not work, you can try installing both `vcrun2019`, and `dotnet472`. Note that these should NOT be required, usually.
* `protontricks [appid] --force vcrun2019` (Let visual installers run)
* `protontricks [appid] --force dotnet472` (Cancel visual installer)

## Linux Native Games
MelonLoader offers native linux builds, since version 0.6.0. <br>
download the linux zip from our [Releases](https://github.com/LavaGang/MelonLoader/releases), and place the files inside of it in your game folder. <br>
to make MelonLoader load with the game, you need to use `LD_PRELOAD`

From the command line: `export LD_PRELOAD=$LD_PRELOAD:/path/to/game/folder/libversion.so` <br>
In the Steam Launch Options: `LD_PRELOAD=$LD_PRELOAD:/path/to/game/folder/libversion.so %command%`

!> Il2Cpp games require .NET 6.0.

Please refer to your distribution's package manager on how to install it. <br>
Arch based distributions may find it in the AUR. Using an AUR helper like paru: `paru -S dotnet-runtime-6.0`

### Pitfalls
* Cpp2IL doesn't currently come in a zip on linux, so permissions aren't carried over. You may need to `chmod +x /path/to/game/folder/MelonLoader/Dependencies/Il2CppAssemblyGenerator/Cpp2IL/Cpp2IL` it.

# Contact

If you need any help, feel free to ask us in the #melonloader-support channel of the [MelonLoader Discord](https://discord.gg/2Wn3N2P)!<br>
When contacting, please include the specific issue you're having, as well as a log file. Include as much information as possible, it just makes everyone' lives easier.

Or, if you see any issues with the wiki, please contact one of the editors in the [credits](credits.md) in the MelonLoader Discord


# Launch Arguments

| Argument              | Description                              |
| --------------------- | ---------------------------------------- |
| --no-mods	| Launch game without loading any Plugins Mods |
| --quitfix	| Fixes the Hanging Process Issue with some Games |
| --melonloader.consoleontop | Forces the Console to always stay on-top of all other Applications |
| --melonloader.hideconsole	| Hides the Console |
| --melonloader.disablestartscreen | Disables the Melon Start Screen |
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
