import os
PWD = os.path.dirname(os.path.abspath(__file__))
DELAY_PWD = os.path.abspath(os.path.join("..", "src", "llvm_pass", "bump", "delaysrc"))

COMMAND = {}
COMMAND["readelf"] = "/bin/bash ./libtool --tag=CC --mode=link afl-clang-fast -W -Wall -Wstrict-prototypes -Wmissing-prototypes -Wshadow -O0 -flto -std=c11 -lpthread  -flto  -o $1 {object} [[readelf.o version.o unwind-ia64.o dwarf.o elfcomm.o]]  ../libiberty/libiberty.a -lz 1> /dev/null 2> /dev/null"
COMMAND["readelf.o"] = 'afl-clang-fast -DHAVE_CONFIG_H -I.  -I. -I. -I../bfd -I./../bfd -I./../include -DLOCALEDIR="\\"/usr/local/share/locale\\"" -Dbin_dummy_emulation=bin_vanilla_emulation  -W -Wall -Wstrict-prototypes -Wmissing-prototypes -Wshadow -O0 -flto -std=c11 -lpthread -MT readelf.o -MD -MP -MF .deps/readelf.Tpo -c -o readelf.o {SRC} 1> /dev/null 2> /tmp/makeout'

COMMAND["objdump"] = "/bin/bash ./libtool --tag=CC   --mode=link afl-clang-fast -W -Wall -Wstrict-prototypes -Wmissing-prototypes -Wshadow -O0 -flto -std=c11 -lpthread  -flto  -o $1 {object} [[objdump.o dwarf.o prdbg.o rddbg.o debug.o stabs.o ieee.o rdcoff.o bucomm.o version.o filemode.o elfcomm.o]]  ../opcodes/libopcodes.la ../bfd/libbfd.la ../libiberty/libiberty.a  -lz 1> /dev/null 2> /dev/null"
COMMAND["objdump.o"] = 'afl-clang-fast -DHAVE_CONFIG_H -I.  -I. -I. -I../bfd -I./../bfd -I./../include -DLOCALEDIR="\\"/usr/local/share/locale\\"" -Dbin_dummy_emulation=bin_vanilla_emulation  -W -Wall -Wstrict-prototypes -Wmissing-prototypes -Wshadow -O0 -flto -std=c11 -lpthread -MT objdump.o -MD -MP -MF .deps/objdump.Tpo -c -o objdump.o -DOBJDUMP_PRIVATE_VECTORS="" ./{SRC}  1> /dev/null 2> /tmp/makeout'

COMMAND["nm-new"] = "/bin/bash ./libtool --tag=CC   --mode=link afl-clang-fast -W -Wall -Wstrict-prototypes -Wmissing-prototypes -Wshadow -O0 -flto -std=c11 -lpthread  -flto  -o $1 {object} [[nm.o bucomm.o version.o filemode.o]] ../bfd/libbfd.la ../libiberty/libiberty.a  -lz  1> /dev/null 2> /dev/null"
COMMAND["nm-new.o"] = 'afl-clang-fast -DHAVE_CONFIG_H -I.  -I. -I. -I../bfd -I./../bfd -I./../include -DLOCALEDIR="\\"/usr/local/share/locale\\"" -Dbin_dummy_emulation=bin_vanilla_emulation  -W -Wall -Wstrict-prototypes -Wmissing-prototypes -Wshadow -O0 -flto -std=c11 -lpthread -MT nm.o -MD -MP -MF .deps/nm.Tpo -c -o nm.o {SRC}  1> /dev/null 2> /tmp/makeout'

COMMAND["objcopy"] = "/bin/bash ./libtool --tag=CC   --mode=link afl-clang-fast -W -Wall -Wstrict-prototypes -Wmissing-prototypes -Wshadow -O0 -flto -std=c11 -lpthread  -flto  -o $1 {object} [[objcopy.o not-strip.o rename.o rddbg.o debug.o stabs.o ieee.o rdcoff.o wrstabs.o bucomm.o version.o filemode.o]] ../bfd/libbfd.la ../libiberty/libiberty.a  -lz  1> /dev/null 2> /dev/null"
COMMAND["objcopy.o"] = 'afl-clang-fast -DHAVE_CONFIG_H -I.  -I. -I. -I../bfd -I./../bfd -I./../include -DLOCALEDIR="\\"/usr/local/share/locale\\"" -Dbin_dummy_emulation=bin_vanilla_emulation  -W -Wall -Wstrict-prototypes -Wmissing-prototypes -Wshadow -O0 -flto -std=c11 -lpthread -MT objcopy.o -MD -MP -MF .deps/objcopy.Tpo -c -o objcopy.o {SRC}  1> /dev/null 2> /tmp/makeout'

# target filename, line: header, line: wrapper for openfile, argv_num
# argv_num: readelf -a /bin/sh ==> argv[2]
TEMP = """#!/bin/bash

if [ "$3" == "init" ]
  then
    {OBJ_INIT}
    {CMD_INIT}
    mkdir -p ../../test/binaries/
    cp $1 ../../test/binaries/

elif [ "$3" == "slow" ]
  then
    #{OBJ_SLOW}
    cp {DELAY_PATH}/delay_$2.o ./delay.o
    {CMD_SLOW}

elif [ "$3" == "coverage" ]
  then
    {CMD_PANDORA}

    #echo "rop"

elif [ "$3" == "makeanti" ]
  then
    {OBJ_ANTI}
    {CMD_ANTI_TEMP}

elif [ "$3" == "anti" ]
  then
    {CMD_ANTI}

elif [ "$3" == "all" ]
  then
    cp {DELAY_PATH}/delay_$2.o ./delay.o
    {CMD_ALL}
fi
"""

# 1) Huge branches enough to saturate the bitmap structure (64K)
#  - problem: large size
#PANDORAS = "delay_slp10.o delay_slp11.o delay_slp12.o delay_slp13.o delay_slp1.o delay_slp2.o delay_slp3.o delay_slp4.o delay_slp5.o delay_slp6.o delay_slp7.o delay_slp8.o delay_slp9.o"

# 2) very tiny huge_branches
#PANDORAS = "delay_tiny1.o delay_tiny2.o"

# 1) Huge branches (medium size: 1.3MB)
#  - 40~50% saturation
PANDORAS = "delay_slp1.o delay_slp2.o"