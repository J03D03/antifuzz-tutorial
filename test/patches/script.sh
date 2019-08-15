#!/bin/bash
cp readelf.c readelf_init.c
python simple_injector.py readelf.c 13762 2
python jtable_inject.py readelf.c 13762
python anti-taint.py readelf.c readelf_anti.c 15

python simple_injector.py objdump.c 3418 2
python jtable_inject.py objdump.c 3418
python anti-taint.py objdump.c objdump_anti.c 30

python simple_injector.py nm.c 1524 1
python jtable_inject.py nm.c 1524
python anti-taint.py nm.c nm_anti.c 30 
cp nm.c nm-new.c
cp nm_anti.c nm-new_anti.c

python simple_injector.py objcopy.c 3317 2
python jtable_inject.py objcopy.c 3317
python anti-taint.py objcopy.c objcopy_anti.c 30