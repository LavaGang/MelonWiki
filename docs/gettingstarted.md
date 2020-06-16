# Requirements

- In order to run the Automated Installer and MelonLoader you must have [.NET Framework 4.7.2 Runtime](https://dotnet.microsoft.com/download/dotnet-framework/net472) installed.
- In order to run MelonLoader you must have [Microsoft Visual C++ 2015-2019 Redistributable](https://aka.ms/vs/16/release/vc_redist.x64.exe) installed.


# Getting Started

MelonLoader is a Mod loader working on most Unity games both Il2Cpp and Mono.  
To use it, you will first need to install it to the desired game.

!> Please note that MelonLoader doesn't do anything on its own. You will have to install some mods to make changes to your game.


# Automated Installation

1. Download [MelonLoader.Installer.exe](https://github.com/HerpDerpinstine/MelonLoader/releases/latest/download/MelonLoader.Installer.exe).
2. Run MelonLoader.Installer.exe.
3. Click the SELECT button.
4. Select and Open the Game's EXE in your Game's Installation Folder.
5. Select which Version of MelonLoader to install using the Drop-Down List.  (Or leave it as-is for the Latest Version.)
6. Click the INSTALL or RE-INSTALL button.


# Manual Installation

1. Download [MelonLoader.zip](https://github.com/HerpDerpinstine/MelonLoader/releases/latest/download/MelonLoader.zip).
2. Extract the MelonLoader folder from MelonLoader.zip to the Game's Installation Folder.
3. Extract version.dll from MelonLoader.zip to the Game's Installation Folder.


# Contact
?> If you need any help, feel free to ask us in the #melonloader-support channel of the [MelonLoader Discord](https://discord.gg/2Wn3N2P)!


# Launch commands

- MelonLoader has some launch arguments, as defined here:

| Argument              | Description                              |
| --------------------- | ---------------------------------------- |
| --no-mods | Launch game without loading Mods |
| --quitfix | Fixes the Hanging Process Issue with some Games |
| --melonloader.hideconsole | Hides the Normal Console |
| --melonloader.debug | Debug Console |
| --melonloader.rainbow | Rainbow Console Color |
| --melonloader.randomrainbow | Random Rainbow Console Color |
| --melonloader.maxlogs | Max Log Files   [ Default: 10 ] [ Disable: 0 ] |
| --melonloader.devmodsonly | Loads only Mods with the "-dev.dll" extension |
| --melonloader.agregenerate | Forces Assembly to be Regenerated on Il2Cpp Games |
