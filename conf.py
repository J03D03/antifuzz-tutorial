
# assume that anti-fuzz and anti-fuzz-eval2 repos are in the same directory
COMPILER  = "../fuzzer/afl-2.51b-bbcheck/afl-clang-fast"
TARGETS = { "binutil": "binutils-2.23.tar.gz" }
EXTRACT = { "binutil": "binutils-2.23" }

TEMP_WORK = "temp"
MAKEOUT   = "makeout"
ORI_BIN_DIR = "test/binaries"
PATCH_DIR = "test/patches"
