> **WARNING:** Android support is **WIP (work in progress)**.
>
> Use it at your own risk.
# Installation
## Required Tools
- ADB (android debug bridge)
- JDK (java development kit)
- Java  
- Python 3.9+
- Unity (you will be prompted to install the correct version. make sure to enable android support)
- [ML Android Installer](https://github.com/SirCoolness/MelonLoader/releases/tag/0.0.1)

## Guide
- configure installer to use correct paths, via `config.json`
    - Make sure that the JDK version is correct in `"KeytoolPath"`

**First Time Installation:**
- This can only be done once.
- Enable `USB Debugging` and connect your Android device.
- Run `py full_installer.py <package name>`
    - You can list all packages via `adb shell pm list packages`
- If there were no errors, the game will have MelonLoader installed.

**Modifying Installation:**
- After the first installation, you will find a directory `build/<package name>`.
- You can run `py update.py .\build\<package name>`
- This will update the installation

## Compatibility
Some games will not like unstripped unity. A workaround will be available for release `0.0.2`. Until then, those games are incompatible.

## Monitoring
You can use `adb logcat` to watch the progress of your MelonLoader installation.

Command: `adb logcat -v time MelonLoader:D CRASH:D Mono:D mono:D mono-rt:D Zygote:D A64_HOOK:V DEBUG:D funchook:D Unity:D Binder:D AndroidRuntime:D *:S`

# Scripts
## full_installer.py
### WARNING: Don't run twice on the same package
usage: `py full_installer.py <package name>`

description: If you're just want it to work, run this and it will go through all the installation steps.


## install_to_apk.py
usage: `py install_to_apk.py <path to apk>`

description: Installs MelonLoader on an apk.

## deploy.py
usage: `py deploy.py <path to apk>`

description:
Installs target apk

## sign.py
usage: `py sign.py <path to apk>`

description: Tool that helps with the signing process. Keep in mind that the key is not secure and is only used to make installation simpler.

## start.py
usage: `py start.py <package name>`

description: Starts a unity game on target device.

## update.py
usage: `py update.py <path to extracted apk>`

description: Installs MelonLoader to an extracted apk. It will then install the updated apk on the device.
If you used `full_installer.py` on a package already, you can find the extracted dir in `build\<package name>`.
