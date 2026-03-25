# What is MelonLoader
MelonLoader is a Universal Mod-Loader for Games built in the [Unity Engine](https://unity.com).

You can find mods for games by asking in their respective communities or by looking through our Officially Supported Games list.

!> Please note that MelonLoader does not condone the use of malicious mods. e.g. mods that allow for cheating in online games, among other things.

# Requirements

- In order to run MelonLoader you must install:
  - [Microsoft Visual C++ 2015-2019 Redistributable 64 Bit](https://aka.ms/vs/16/release/vc_redist.x64.exe) for 64 bit games.
  - [Microsoft Visual C++ 2015-2019 Redistributable 32 Bit](https://aka.ms/vs/16/release/vc_redist.x86.exe) for 32 bit games.
- Il2Cpp games require [dotnet 6.0](https://dotnet.microsoft.com/en-us/download/dotnet/6.0#runtime-desktop-6.0.19). We recommend the .NET Desktop Runtime, x64 or x86 depending on if your game is 64 bit or 32 bit

?> If you aren't sure if your game is 32bit or 64bit an easy way to find out is to to use the task manager. If your game is 32bit, the game name will be followed by (32 bit).

# Automated Installation

<a href="https://github.com/LavaGang/MelonLoader.Installer/releases/latest/download/MelonLoader.Installer.exe"><img src="https://img.shields.io/github/downloads/LavaGang/MelonLoader.Installer/latest/MelonLoader.Installer.exe?style=for-the-badge&label=Download%20Latest%20for%20Windows"></a><br>
<a href="https://github.com/LavaGang/MelonLoader.Installer/releases/latest/download/MelonLoader.Installer.Linux"><img src="https://img.shields.io/github/downloads/LavaGang/MelonLoader.Installer/latest/MelonLoader.Installer.Linux?style=for-the-badge&label=Download%20Latest%20for%20Linux"></a>

The installer should automatically list installed Unity games on your machine.

### Supported game launchers on Windows
- Steam
- Epic Games Store
- GOG

### Supported game launchers on Linux
- Steam

### Games from unsupported launchers
If the game you're trying to mod isn't listed, you can locate it manually by clicking on the `Add Game Manually` button.

### MelonLoader Installation
To install MelonLoader, click on the game you wish to mod. Next, select your preferred version and hit the big `Install` button.

?> Make sure the version of MelonLoader you select is the one that your game uses. You can check by asking in the respective community. A list of them can be found in the `Officially Supported Games` tab.

### Nightly builds
!> We strongly advise against enabling Nightly builds unless you know what you're doing.

Nightly builds are bleeding-edge builds, generated right after any changes are made to the project. They can be enabled with the switch under the version selection menu.

# Manual Installation

> It's **highly** recommended to use the automated installation when you can.

1. - If your game is 64bit, download [MelonLoader.x64.zip](https://github.com/LavaGang/MelonLoader/releases/latest/download/MelonLoader.x64.zip)
   - If your game is 32bit, download [MelonLoader.x86.zip](https://github.com/LavaGang/MelonLoader/releases/latest/download/MelonLoader.x86.zip)
2. Extract the MelonLoader folder from the zip file you just downloaded to the Game's Installation Folder.
3. Extract version.dll as well from the zip file you just downloaded to the Game's Installation Folder. 

?> If you aren't sure if your game is 32bit or 64bit an easy way to find out is to to use the task manager. If your game is 32bit, the game name will be followed by (32 bit).

# Linux Launch Instructions

## Windows Games (Wine/Proton)

To allow MelonLoader to load, you'll need to export the following environment variable:
`WINEDLLOVERRIDES="version=n,b"`

On Steam, you can set the launch options to:
`WINEDLLOVERRIDES="version=n,b" %command%`

### Il2Cpp Games
!> Il2Cpp games require the Windows version of [dotnet 6.0](https://dotnet.microsoft.com/en-us/download/dotnet/6.0#runtime-desktop-6.0.28). We recommend the .NET Desktop Runtime, x64 or x86 depending on if your game is 64 bit or 32 bit.

?> Please refer to your distribution's specific ways of installing Protontricks. <br>
Arch based distributions may find it in the AUR. Using an AUR helper like paru: `paru -S protontricks` or `paru -S protontricks-git`

Find your game's AppID using `protontricks -s [GameName]`

It is recommended to start over with a *clean* prefix.

Your game's (default) proton prefix will be located at ` ~/.local/share/Steam/steamapps/compatdata/[appid]`. Delete that folder, and start the game once.<br/>
You are now running a clean prefix.

To install dotnet automatically, run `protontricks [appid] dotnetdesktop6`.

To install it manually, run `protontricks [appid] uninstaller`, click `Install...`, switch `Files of Type` to `.exe` and run the .NET 6.0 installer from the link above.

## Linux Native Games

#### Important: Proper Library Loading

  For compatibility and security reasons, do not point`LD_PRELOAD`to a specific file path. Using a path in`LD_PRELOAD`can cause the loader to ignore the library during secure execution (setuid) and may prevent the library from finding its own dependencies.

  1. Add the game folder to your`LD_LIBRARY_PATH` environment variable.
  2. Reference the library by filename only in`LD_PRELOAD`.

  __Non-Steam launch options__:
  ```sh
  LD_LIBRARY_PATH="/full/path/to/game/directory:$LD_LIBRARY_PATH" LD_PRELOAD="MelonLoader.Bootstrap.so:$LD_PRELOAD" ./game_binary
  ```

  __Steam launch options__:
  ```sh
  LD_LIBRARY_PATH="/full/path/to/game/directory:$LD_LIBRARY_PATH" LD_PRELOAD="MelonLoader.Bootstrap.so:$LD_PRELOAD" %command%
  ```

  ### Linux Native Il2Cpp Games
  !> Il2Cpp-based games require the .NET 6.0 Runtime to function.

  Please refer to your distribution's package manager on how to install it.
  * __Debian / Ubuntu:__
  ```bash
  sudo apt update && sudo apt install dotnet-runtime-6.0
  ```
  * __Fedora:__
  ```bash
  sudo dnf install dotnet-runtime-6.0
  ```
  Arch Linux:
  Available in the AUR. Using an AUR helper like`paru`:
  ```bash
  paru -S dotnet-runtime-6.0
  ```
#### Sandboxed Environments
  If you are using __Flatpak__, __Snap__, __AppImage__, which is common on Immutable OS-s (such as __Bazzite__), the application is isolated from your host system's environment variables and directories.

  To allow MelonLoader to find the required files, you must manually point it to your .NET installation using the `DOTNET_ROOT` variable. Without this, the loader will fail, typically showing the following error in your MelonLoader logs:

  ```cs
  [10:01:42.483] [MelonLoader.Bootstrap] Failed to load Hostfxr
  ```

  To fix this, pass the variable directly when launching the game:
  ```bash
  DOTNET_ROOT="/path/to/your/dotnet" ./game_binary
  ```

### Pitfalls
* __Permissions Issue__: Since Cpp2IL is currently distributed without preserved Linux permissions, you may need to manually mark the binary as executable. Failure to do so will prevent the Assembly Generator from running.
```sh
chmod +x /path/to/game/folder/MelonLoader/Dependencies/Il2CppAssemblyGenerator/Cpp2IL/Cpp2IL
```
This process is automated starting from the release version 7.2 and onwards.

# Contact

If you need any help, feel free to ask us in the #melonloader-support channel of the [MelonLoader Discord](https://discord.gg/2Wn3N2P)!<br>
When contacting, please include the specific issue you're having, as well as a log file. Include as much information as possible, it just makes everyone' lives easier.

Or, if you see any issues with the wiki, please contact one of the editors in the [credits](credits.md) in the MelonLoader Discord


# Launch Arguments

| Argument              | Description                              |
| --------------------- | ---------------------------------------- |
| --no-mods | Launches the Game without loading any Plugins or Mods |
| --quitfix | Fixes the Hanging Process Issue with some Games |
| --melonloader.consolemode | Changes the Theme Display Mode of the Console [ Default = 0 ] |
| --melonloader.consoleontop | Forces the Console to always stay on-top of all other Applications |
| --melonloader.consoledst | Keeps the Console Title as Original |
| --melonloader.hideconsole | Hides the Console |
| --melonloader.hidewarnings | Hides Warnings from Displaying |
| --melonloader.debug | Debug Mode |
| --melonloader.maxlogs | Max Log Files [ Default: 10 ] [ NoCap: 0 ] |
| --melonloader.loadmodeplugins | Load Mode for Plugins [ Default: 0 ] |
| --melonloader.loadmodemods | Load Mode for Mods [ Default: 0 ] |
| --melonloader.basedir | Changes the Proxy's Load Directory for the Bootstrap |
| --melonloader.disablestartscreen | Disable the Start Screen |
