# Patching

## Patching using Harmony
- MelonLoader uses a modified version of [Harmony](https://github.com/pardeike/Harmony)
- In MelonLoader versions v0.3.0 and versions before Harmony 1.2 is used
- In MelonLoader v0.4.0 (and later) Harmony 2 is used
- With Mono games, patching with Harmony should be similar if you've used it before. Prefixes, Postfixes and Transpiler patches etc. 
- With Il2Cpp games, Prefix and Postfix patches will work on both the Il2Cpp side and Mono side however Transpiler patches won't work on the IL2Cpp side.
- MelonLoader provides a Harmony instance for mods to use through MelonMod\MelonPlugin meaning you shouldn't have to create an instance in your own mod\plugin
- Documentation on how to use Harmony 1.2 can be found [here](https://github.com/pardeike/Harmony/wiki)
- Documentation on how to use Harmony 2 can be found [here](https://harmony.pardeike.net/)

## Patching using Native Hooks

!> Coming Soon

