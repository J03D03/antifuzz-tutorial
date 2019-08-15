
======
common
======
unset RANLIB
unset CXXFLAGS
unset CPPFLAGS
unset LDFLAGS
unset CFLAGS
unset CC
unset CXX
unset AR

export RANLIB="llvm-ranlib"
export CC="/data/sslab/anti-fuzz/fuzzer/afl-2.51b-bbcheck/afl-clang-fast"
export CXX="/data/sslab/anti-fuzz/fuzzer/afl-2.51b-bbcheck/afl-clang-fast++"
export AR="llvm-ar"
export CFLAGS="-static -flto"
export CXXFLAGS="-static -flto"

===========
libpng
===========
tar xzvf archive/libpng-1.2.56.tar.gz -C target

./configure --disable-silent-rules --disable-shared 
make -j4 &> output1

- readpng
  compile: /data/sslab/anti-fuzz/fuzzer/afl-2.51b-bbcheck/afl-gcc ./readpng.c  ../../.libs/libpng16.a -o readpng -lm -lz
  fuzzing: /data/sslab/anti-fuzz/fuzzer/afl-2.51b-bbcheck/afl-fuzz -i input -o output -- ./readpng 

NEW VERSION
------------
tar xzvf archive/libpng-1.6.34.tar.gz -C target

/data/sslab/anti-fuzz/fuzzer/afl-2.51b-bbcheck/afl-clang-fast -flto -static ./readpng.c png.o pngerror.o pngget.o pngmem.o pngpread.o pngread.o pngrio.o pngrtran.o pngrutil.o pngset.o pngtrans.o pngwio.o pngwrite.o pngwtran.o pngwutil.o mips/mips_init.o mips/filter_msa_intrinsics.o intel/intel_init.o intel/filter_sse2_intrinsics.o powerpc/powerpc_init.o powerpc/filter_vsx_intrinsics.o -o readpng -lm -lz 

FUzzing command
----------------
/data/sslab/anti-fuzz/fuzzer/afl-2.51b/afl-fuzz -i input -o out -- ./libpng_huge 
/data/sslab/anti-fuzz/fuzzer/afl-2.51b/afl-fuzz -Q -i input -o out -- ./libpng_huge 

/home/jjung/anti-fuzz/repo/fuzzer/afl-2.51b-bbcheck/afl-fuzz -m none -i input -o out -- ./libpng_huge 

=======
libjpeg
=======
tar xzvf archive/libjpeg_b097.tar.gz -C target
autoreconf -fiv

./configure --disable-silent-rules
make &> output1

==========
binutils
==========
tar xzvf archive/binutils-2.15.tar.gz -C target

unset CFLAGS
export CFLAGS="-static -lpthread -std=gnu99"

./configure --disable-silent-rules
make &> output1

==========
libarchive
==========
tar xzvf archive/libarchive_51d7.tar.gz -C target

cd build
./autogen.sh
cd ..
./configure --without-xml2 --disable-silent-rules
make &> output1

output: bsdtar, bsdcpio

=======
libxml
=======
tar xzvf archive/libxml2.9.2.tar.gz -C target

./autogen.sh
./configure --disable-silent-rules
make &> output1

./testReader --count --valid --consumed a.xml

============
woff2 (ttf)
============
tar xzvf archive/woff2_latest.tar.gz -C target

make &> output1

==========
harf (tff)
==========
tar xzvf archive/harf_f73a.tar.gz -C target

./autogen.sh
./configure --disable-silent-rules
make &> output1

src/test ==> harftest binary

---
llvm-ar cru .libs/libharfbuzz.a  libharfbuzz_la-hb-blob.o libharfbuzz_la-hb-buffer-serialize.o libharfbuzz_la-hb-buffer.o libharfbuzz_la-hb-common.o libharfbuzz_la-hb-face.o libharfbuzz_la-hb-font.o libharfbuzz_la-hb-ot-tag.o libharfbuzz_la-hb-set.o libharfbuzz_la-hb-shape.o libharfbuzz_la-hb-shape-plan.o libharfbuzz_la-hb-shaper.o libharfbuzz_la-hb-unicode.o libharfbuzz_la-hb-warning.o libharfbuzz_la-hb-ot-font.o libharfbuzz_la-hb-ot-layout.o libharfbuzz_la-hb-ot-map.o libharfbuzz_la-hb-ot-shape.o libharfbuzz_la-hb-ot-shape-complex-arabic.o libharfbuzz_la-hb-ot-shape-complex-default.o libharfbuzz_la-hb-ot-shape-complex-hangul.o libharfbuzz_la-hb-ot-shape-complex-hebrew.o libharfbuzz_la-hb-ot-shape-complex-indic.o libharfbuzz_la-hb-ot-shape-complex-indic-table.o libharfbuzz_la-hb-ot-shape-complex-myanmar.o libharfbuzz_la-hb-ot-shape-complex-thai.o libharfbuzz_la-hb-ot-shape-complex-tibetan.o libharfbuzz_la-hb-ot-shape-complex-use.o libharfbuzz_la-hb-ot-shape-complex-use-table.o libharfbuzz_la-hb-ot-shape-normalize.o libharfbuzz_la-hb-ot-shape-fallback.o libharfbuzz_la-hb-fallback-shape.o libharfbuzz_la-hb-glib.o

/data/sslab/anti-fuzz/fuzzer/afl-2.51b-bbcheck/afl-clang-fast++ -DHAVE_CONFIG_H -I. -I..  -pthread -I/usr/include/glib-2.0 -I/usr/lib/x86_64-linux-gnu/glib-2.0/include           -static -flto -fno-rtti -fno-exceptions -Wcast-align -fvisibility-inlines-hidden --std=c++0x -MT test-test.o -MD -MP -MF .deps/test-test.Tpo -c -o test-test.o `test -f 'test.cc' || echo './'`test.cc

/data/sslab/anti-fuzz/fuzzer/afl-2.51b-bbcheck/afl-clang-fast++ -flto -fno-rtti -fno-exceptions -Wcast-align -fvisibility-inlines-hidden --std=c++0x -Bsymbolic-functions -o test test-test.o  ./.libs/libharfbuzz.a -lglib-2.0


=========
openssl
=========
tar xzvf archive/openssl_1.0.2.tar.gz -C target

mkdir ../build
cd ../build
../openssl/config --unified
make &> output1

======
pcre2
======
tar xzvf archive/pcre2-10.tar.gz -C target
./autogen.sh

./configure --disable-silent-rules
make &> output1

=======
libtiff
=======
tar xzvf archive/libtiff_c9a5.tar.gz -C target
./configure --disable-silent-rules --with-pic

make &> output1

==========
NO boringssl
==========
tar xzvf archive/boring_894a.tar.gz -C target

(should not use -static option)

cmake -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON -DBUILD_SHARED_LIBS=OFF -DCMAKE_C_COMPILER="$CC" -DCMAKE_C_FLAGS="$CFLAGS -Wno-deprecated-declarations" -DCMAKE_CXX_COMPILER="$CXX" -DCMAKE_CXX_FLAGS="$CXXFLAGS -Wno-error=main" ..

cd ..

make &> output1

=======
NO-re2
=======
tar xzvf archive/re2_499e.tar.gz -C target
make &> output1


========
NO json
========
cmake -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON .
make


========
NO-freetype
========
./autogen.sh
./configure --disable-silent-rules --with-harfbuzz=no --with-bzip2=no --with-png=no


