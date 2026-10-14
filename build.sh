#!/bin/bash
# Build the PLUMED kernels and the patched GROMACS versions that the regtests run on.
#
#   build.sh plumed  LABEL GITREF          build PLUMED from GITREF of $PLUMED_REPO into cache/plumed/LABEL
#   build.sh gromacs VERSION LABEL KERNEL  patch GROMACS VERSION (runtime mode) with the patches of the
#                                          PLUMED install cache/plumed/LABEL, install in cache/gromacs/VERSION-LABEL
#
# GROMACS is built with MPI, without GPU (GPU=CUDA for a CUDA build, CUDA_ARCH to choose the architecture).
# Each GROMACS version is configured and compiled once: other patch sets are applied to the same tree and only
# the files they change are recompiled. Environment: PLUMED_REPO (a plumed2 git checkout), MPI_HOME, JOBS.
set -e
H=$(cd "$(dirname "$0")" && pwd); C=$H/cache
PLUMED_REPO=${PLUMED_REPO:-$H/../plumed2}
JOBS=${JOBS:-$(nproc)}
if [ -n "$MPI_HOME" ]; then export PATH=$MPI_HOME/bin:$PATH LD_LIBRARY_PATH=$MPI_HOME/lib:$LD_LIBRARY_PATH; fi
mkdir -p $C/logs

case $1 in
plumed)
  label=$2; ref=$3; src=$C/src/plumed-$label; prefix=$C/plumed/$label
  rm -rf $src; mkdir -p $src
  git -C "$PLUMED_REPO" archive "$ref" | tar -x -C $src
  git -C "$PLUMED_REPO" rev-parse "$ref" > $src/GITREF
  cd $src
  ./configure --prefix=$prefix --enable-mpi --enable-modules=+opes --disable-python --disable-doc \
    CXX=mpic++ CC=mpicc > $C/logs/plumed-$label-configure.log 2>&1
  make -j$JOBS > $C/logs/plumed-$label-make.log 2>&1
  make install > $C/logs/plumed-$label-install.log 2>&1
  cp $src/GITREF $prefix/GITREF
  echo "built PLUMED $label ($ref = $(cut -c1-9 $src/GITREF))"
  ;;
gromacs)
  v=$2; label=$3; P=$C/plumed/$label
  tag=${GPU:+-$(echo $GPU | tr A-Z a-z)}
  G=$C/src/gromacs-$v$tag; prefix=$C/gromacs/$v-$label$tag
  # the patch for GROMACS 2026.x is called gromacs-2026.0 (same for 2025.x)
  engine=$(ls $P/lib/plumed/patches | sed -n "s/^\(gromacs-${v%.*}\.[0-9]*\)\.diff$/\1/p" | head -1)
  [ -n "$engine" ] || { echo "no patch for GROMACS $v in $label"; exit 1; }
  if [ ! -d $G ]; then
    mkdir -p $G; tar xzf $C/dl/gromacs-$v.tar.gz -C $G --strip-components=1
  fi
  export PATH=$P/bin:$PATH LD_LIBRARY_PATH=$P/lib:$LD_LIBRARY_PATH
  cd $G
  if [ -e .plumed-engine ]; then plumed patch -R -e "$(cat .plumed-engine)" > $C/logs/gromacs-$v$tag-$label-patch.log 2>&1; fi
  plumed patch -p -e $engine --runtime >> $C/logs/gromacs-$v$tag-$label-patch.log 2>&1
  echo $engine > .plumed-engine
  # the patched files must be exactly the files of the patch
  D=$P/lib/plumed/patches/$engine.diff
  for f in $(cd $D && find . -type f ! -name "*.preplumed"); do
    cmp -s $D/$f $f || { echo "GROMACS $v: $f differs from the $label patch"; exit 1; }
  done
  # old GROMACS versions miss some includes that recent compilers need
  extra=""; case $v in 2020.*|2021.*) extra="-include cstdint -include limits";; esac
  gpu="-DGMX_GPU=OFF"
  if [ "$GPU" = CUDA ]; then
    # CUDA 13 makes global template stubs static by default, which GROMACS < 2025 does not expect
    gpu="-DGMX_GPU=CUDA -DCMAKE_CUDA_ARCHITECTURES=${CUDA_ARCH:-native} -DCUDA_NVCC_FLAGS=-static-global-template-stub=false"
  fi
  mkdir -p build; cd build
  cmake .. -DCMAKE_BUILD_TYPE=Release -DGMX_MPI=ON $gpu -DGMX_FFT_LIBRARY=fftpack -DGMX_HWLOC=OFF \
    -DCMAKE_C_COMPILER=mpicc -DCMAKE_CXX_COMPILER=mpicxx -DCMAKE_CXX_FLAGS="$extra" \
    -DCMAKE_INSTALL_PREFIX=$prefix > $C/logs/gromacs-$v$tag-$label-cmake.log 2>&1
  make -j$JOBS install > $C/logs/gromacs-$v$tag-$label-make.log 2>&1
  echo "built GROMACS $v$tag with the $engine patch of $label"
  ;;
*)
  sed -n '2,12p' "$0"; exit 1
  ;;
esac
