# Requirements

- In order to run the Automated Installer and MelonLoader you must have [.NET Framework 4.8 Runtime](https://dotnet.microsoft.com/download/dotnet-framework/net48) installed.
- In order to run MelonLoader you must install:
  - [Microsoft Visual C++ 2015-2019 Redistributable 64 Bit](https://aka.ms/vs/16/release/vc_redist.x64.exe) for 64 bit games.
  - [Microsoft Visual C++ 2015-2019 Redistributable 32 Bit](https://aka.ms/vs/16/release/vc_redist.x86.exe) for 32 bit games.

?> If you aren't sure if your game is 32bit or 64bit an easy way to find out is to to use the task manager. If your game is 32bit, the game name will be followed by (32 bit). Example: `Among Us.exe (32 bit)` vs `BONEWORKS.exe`

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

1. - If your game is 32bit download [MelonLoader.x86.zip](https://github.com/LavaGang/MelonLoader/releases/latest/download/MelonLoader.x86.zip)
   - If your game is 64bit download [MelonLoader.x64.zip](https://github.com/LavaGang/MelonLoader/releases/latest/download/MelonLoader.x64.zip)
2. Extract the MelonLoader folder from the zip file you just downloaded to the Game's Installation Folder.
3. Extract version.dll as well from the zip file you just downloaded to the Game's Installation Folder. 

?> If you aren't sure if your game is 32bit or 64bit an easy way to find out is to to use the task manager. If your game is 32bit, the game name will be followed by (32 bit). Example: `Among Us.exe (32 bit)` vs `BONEWORKS.exe`

# Linux Instructions
>MelonLoader has no native Linux build available. These instructions are for getting MelonLoader working under Steam's Proton. Applies to Wine too, simply substitute `steamtricks [appid]` with `winetricks`

Please refer to your distribution's specific ways of installing Protontricks. <br>
Arch based distributions may find it in the AUR. Using an AUR helper like yay: `yay -S protontricks` or `yay -S protontricks-git`

Find your game's AppID using `protontricks -S [GameName]`

It is recommended to start over with a *clean* prefix.

Your game's (default) proton prefix will be located at ` ~/.local/share/Steam/steamapps/compatdata/[appid]`. Delete that folder, and start the game once.<br/>
You are now running a clean prefix.

Now run 
* `protontricks [appid] --force vcrun2019` (Let visual installers run)
* `protontricks [appid] --force dotnet472` (Cancel visual installer)

Note that both of these may take some time.

Then run `protontricks [appid] winecfg`<br/>
At the bottom, switch the Windows version to Windows 10.<br>
Go to the libraries tab, select `version` from the "new override for library" dropdown, and hit add<br/>
Then hit OK.

Now you can follow the Manual Installation instructions above, and MelonLoader should pop up on launch.

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
