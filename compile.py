#!/usr/bin/env python2

import os
import sys
import time
import errno
import shutil
import inspect

from conf import *
from build_template import *

def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)

def extract_target(pn):    
    print "ext"
    os.system("tar xzvf %s" % (pn))

    # FIXME
    src = "binutils-2.23/"
    dst = "temp/"

    files = os.listdir(src)
    for f in files:
        try:
            shutil.move (src + f, dst)
        except:
            pass

    os.system("rm -rf binutils-2.23")

def mkdirs(pn):
    try:
        os.makedirs(pn)
    except OSError as e:
        pass

def return_funcname(line):
    if '_' in line:
    	return line.split("_")[1].strip()
    return line

def cleanup_temp_dir():
    os.system("rm -rf %s" % TEMP_WORK)
    mkdirs(TEMP_WORK)

def load_filelist_from_dir(dirname, ext=None, onlyfile = True):
    extension_path = []

    for root, dirs, files in os.walk(dirname):
        for filename in files:
            if onlyfile:
                if ext is None:
                    extension_path.append(filename)
                elif "."+ext in filename:
                    extension_path.append(filename)
            else:
                if ext is None:
                    extension_path.append(root + "/" + filename)
                elif "."+ext in filename:
                    extension_path.append(root + "/" + filename)
                
    return extension_path

def add_postfix(filename, postfix):
    # assuming always .o file
    filename = filename[:-2]
    return filename+postfix+".o"


def duplicate_object_files(filelist, postfix):
    for filename in filelist:
        new_pn = add_postfix(filename, postfix)
        print "cp %s %s" % (filename, new_pn)
        os.system("cp %s %s" % (filename, new_pn))

def copy_original_bin(dir, target_bin, change_name=None):
    # e.g., # e.g., copy_original_bin("binutils", "readelf")
    pn = os.path.join(TEMP_WORK, dir, target_bin)

    if change_name is None:
        target_pn = os.path.join(ORI_BIN_DIR, target_bin)
    else:
        target_pn = os.path.join(ORI_BIN_DIR, change_name)

    print "cp %s %s" % (pn, target_pn)
    os.system("cp %s %s" % (pn, target_pn))
    os.system("chmod +x %s" % target_pn)

def parse_command(cmd, inst):  
  tmp = cmd.split('[[')[1].split(']]')[0].strip()
  tmparr =  tmp.split(' ')
  out = []
  basename = []
  instname = []
  for item in tmparr:
    out.append(item.split('.o')[0])
    basename.append(os.path.basename(item))
    instname.append(item.split('.o')[0]+"_%s.o" % inst)
  return tmp, " ".join(instname)

def modify_for_inst(line, instname):
    orig, modified_cmd = parse_command(line, instname) 
    line = line.replace(orig, modified_cmd)
    line = line.replace("[[", "")
    line = line.replace("]]", "")    
    return line

def generate_sh(target, srcfile, sub=None):
    cmd = COMMAND[target]
    obj_cmd = COMMAND["%s.o" % target]
    #injector_cmd = INJECTOR_ARGS[target]

    # 1. replace for init
    cmd_init = cmd.replace("{object}", "huge_dummy.o") 
    cmd_init = cmd_init.replace("[[", "")
    cmd_init = cmd_init.replace("]]", "")
    out_cmd = TEMP.replace("{CMD_INIT}", cmd_init)

    init_obj_cmd = obj_cmd.replace("{SRC}", srcfile+".c")
    out_cmd = out_cmd.replace("{OBJ_INIT}", init_obj_cmd)

    # 2. replace for bump
    cmd_bump = cmd.replace("{object}", "delay.o huge_dummy.o") 
    cmd_bump = modify_for_inst(cmd_bump, "bump")    
    out_cmd = out_cmd.replace("{CMD_SLOW}", cmd_bump)

    #cmd_bump = cmd.replace("{object}", "delay.o huge_dummy.o")     
    #out_cmd = out_cmd.replace("{CMD_SLOW_TEMP}", cmd_bump)
    
    bump_obj_cmd = obj_cmd.replace("{SRC}", srcfile+".c")
    out_cmd = out_cmd.replace("{OBJ_SLOW}", bump_obj_cmd)

    # 3. replace for coverage
    # 3-1) for trap
    #out_cmd = out_cmd.replace("{injector}", injector_cmd)
    cov_obj_cmd = obj_cmd.replace("{SRC}", srcfile+"_trap.c")
    out_cmd = out_cmd.replace("{OBJ_TRAP}", cov_obj_cmd)

    # 3-2) for pandora
    cmd_panora = cmd.replace("{object}", PANDORAS + " rop_dummy.o huge.o") 
    cmd_panora = modify_for_inst(cmd_panora, "coverage")
    out_cmd = out_cmd.replace("{CMD_PANDORA}", cmd_panora)

    # 4-1) for anti-symbolic execution
    cmd_antisym = cmd.replace("{object}", "antilib.o huge_dummy.o") 
    cmd_antisym = modify_for_inst(cmd_antisym, "anti")
    out_cmd = out_cmd.replace("{CMD_ANTI}", cmd_antisym)    

    cmd_antisym2 = cmd.replace("{object}", "antilib.o huge_dummy.o") 
    cmd_antisym2 = cmd_antisym2.replace("[[", "")
    cmd_antisym2 = cmd_antisym2.replace("]]", "")
    out_cmd = out_cmd.replace("{CMD_ANTI_TEMP}", cmd_antisym2)    

    anti_obj_cmd = obj_cmd.replace("{SRC}", srcfile+"_anti.c")
    out_cmd = out_cmd.replace("{OBJ_ANTI}", anti_obj_cmd)

    # 5) all instrumentation
    cmd_all = cmd.replace("{object}", PANDORAS + " antilib.o huge.o delay.o rop_dummy.o") 
    cmd_all = modify_for_inst(cmd_all, "all")
    out_cmd = out_cmd.replace("{CMD_ALL}", cmd_all)
    out_cmd = out_cmd.replace("{DELAY_PATH}", DELAY_PWD)
    
    if sub is not None:
        save_pn = os.path.join(TEMP_WORK, sub, "build-%s.sh" % target)
    else:
        save_pn = os.path.join(TEMP_WORK, "build-%s.sh" % target)

    with open(save_pn, 'w')  as f:
        f.write(out_cmd)    
    os.system("chmod +x %s" % save_pn)

def copy_tools(pn):
    candidates = ["../src/llvm_pass/trap/huge_injector.py",   \
                  "../src/llvm_pass/trap/jtable_inject.py",   \
                  "../src/llvm_pass/trap/rop_dummy.o",        \
                  "../src/llvm_pass/trap/simple_injector.py", \
                  "../src/llvm_pass/trap/huge.o",             \
                  "../src/llvm_pass/trap/delay_slp1.o",       \
                  "../src/llvm_pass/trap/delay_slp2.o",       \
                  "../src/llvm_pass/trap/delay_slp3.o",       \
                  "../src/llvm_pass/trap/delay_slp4.o",       \
                  "../src/llvm_pass/trap/delay_slp5.o",       \
                  "../src/llvm_pass/trap/delay_slp6.o",       \
                  "../src/llvm_pass/trap/huge_dummy.o",       \
                  "../src/llvm_pass/anti/antilib.o",          \
                  "../src/llvm_pass/anti/antilib_dummy.o",    \
                  "../src/llvm_pass/antitaint/anti-taint.py" ]

    for candidate in candidates:
        print "cp %s %s" % (candidate, pn)
        os.system("cp %s %s" % (candidate, pn))
    
# copy already built patch
def apply_patches(modify_candidates, target_dir, phase):

    #e.g., apply_patches("readelf", "temp/binutils", "init")

    for candidate in modify_candidates:
        src_pn = os.path.join(PATCH_DIR, candidate, "*.c")
        #target_pn = os.path.join(target_dir, candidate+".c")
        target_pn = os.path.join(target_dir)

        # copy already patched file        
        os.system("cp %s %s" % (src_pn, target_pn))

        # initially built the system        
        os.system("cd %s; ./build-%s.sh %s 0 init" % (target_dir, candidate, candidate))


def common_execution():
    cleanup_temp_dir()
    os.environ["CC"]      = os.path.abspath(COMPILER)
    os.environ["RANLIB"]  = "llvm-ranlib"
    os.environ["AR"]      = "llvm-ar"
    os.environ["CFLAGS"]  = "-O0 -flto -std=c11 -lpthread"
    os.environ["LDFLAGS"] = "-flto "

def compile_binutil():    
    if not os.environ.has_key("DEBUG"):
        print "="*50
        print "generate all new"
        # 1. clean up the working dir
        common_execution()
        
        # 2. extract target to temp dir
        target = return_funcname(inspect.stack()[0][3])
        target_pn = os.path.join("archive", TARGETS["binutil"])    
        extract_target(target_pn)

        print "=" * 50
        src_pn = os.path.abspath(os.path.join(TEMP_WORK, EXTRACT[target])) 
        des_pn = os.path.abspath(os.path.join(TEMP_WORK))

        # 3. compile using afl-clang-fast
        print "Compiling binutils"
        print "=" * 50                
        os.system("cd %s; pwd; ./configure --disable-werror --disable-silent-rules" % (TEMP_WORK))        
        os.system("cd %s; pwd; make -j 4 > %s 2>&1" % (TEMP_WORK, MAKEOUT))
        
        # 4. copy object file for inst
        # e.g., a.o ==> a_inst.o a_orginst.o
        filelist = load_filelist_from_dir(TEMP_WORK, ext="o", onlyfile=False)
        print filelist
        duplicate_object_files(filelist, "_inst")
        duplicate_object_files(filelist, "_orginst")

    # 6. generate build.sh (slow, trap, pandora, antisym, anti-taint)
    generate_sh("readelf", "readelf", sub="binutils")
    generate_sh("objdump", "objdump", sub="binutils")
    generate_sh("nm-new", "nm-new", sub="binutils")
    generate_sh("objcopy", "objcopy", sub="binutils")

    # 7. apply necessary patch for easy instrumentation
    modify_src = ["readelf", "objdump", "nm-new", "objcopy"]
    pn = os.path.join("temp", "binutils")
    copy_tools(pn)
    apply_patches(modify_src, pn, "init")

    copy_original_bin("binutils", "readelf")
    copy_original_bin("binutils", "objdump")
    copy_original_bin("binutils", "nm-new")
    copy_original_bin("binutils", "objcopy")    
           
def main():        
    compile_binutil()    

if __name__ == "__main__":
    main()
