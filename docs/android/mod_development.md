> **WARNING:** Android support is **WIP (work in progress)**.
>
> Use it at your own risk.
# Mod Development
General mod development, should be the same as the mainline version of MelonLoader.

## Information
### MelonLoader Directories
- `/storage/emulated/0/Android/data/<package name>/files` Base Directory
    - `./Mods` Mods folder
    - `./Plugins` Plugins folder
    - `./UserData` Mod Prefs
    - `./melonloader/etc` Melon Loader Files
        - `./managed` All the used assemblies (use the assemblies in this directory if you need to compile mods)
        - `./support` Support module assemblies
        - `./assembly_generation` Directory for all tools used during assembly generation
            - `./Il2CppDumper` Output for Il2CppDumper
            - `./Il2CppAssemblyUnhollower` Output for Unhollower
            - `./managed` Assemblies used for assembly generation
            - `./unity` Source unity assemblies
    
## Logging Commands
### Normal
```
adb logcat -v time MelonLoader:D CRASH:D Mono:W mono:D mono-rt:D Zygote:D A64_HOOK:V DEBUG:D Binder:D AndroidRuntime:D *:S
```
### Verbose
```
adb logcat -v time MelonLoader:D CRASH:D Mono:D mono:D mono-rt:D Zygote:D A64_HOOK:V DEBUG:D funchook:D Unity:D Binder:D AndroidRuntime:D *:S
```

## Bug Reporting
Please report your ML Android bugs in [the dedicated discord server](https://discord.gg/czfkRNTSpt). All bug reports are super helpful, and can be used to make ML Android more stable. 