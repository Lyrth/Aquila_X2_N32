import os
Import("env")

# Relocate firmware from 0x08000000 to 0x08007000
to_remove = None
for define in env['CPPDEFINES']:
    if define[0] == "VECT_TAB_ADDR":
        to_remove = define

if to_remove is not None:
    env['CPPDEFINES'].remove(to_remove)

env['CPPDEFINES'].append(("VECT_TAB_ADDR", "0x08007000"))

custom_ld_script = os.path.abspath("buildroot/share/PlatformIO/ldscripts/creality.ld")

for i, flag in enumerate(env['LINKFLAGS']):
    if "-Wl,-T" in flag:
        env['LINKFLAGS'][i] = "-Wl,-T" + custom_ld_script
    elif flag == "-T":
        env['LINKFLAGS'][i + 1] = custom_ld_script

env.AddPostAction(
    "$BUILD_DIR/${PROGNAME}.elf",
    env.VerboseAction(" ".join([
        "$OBJCOPY", "-O", "ihex", "-R", ".eeprom",
        "$BUILD_DIR/${PROGNAME}.elf", "$BUILD_DIR/${PROGNAME}.hex"
    ]), "Building $BUILD_DIR/${PROGNAME}.hex")
)
