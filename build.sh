#!/bin/bash
# Build the PLUMED kernels and the GROMACS versions that the regtests run on, in cache/.
#
#   build.sh plumed  LABEL [GITREF]   build PLUMED from GITREF (default: the branch LABEL) of github.com/plumed/plumed2
#                                     into cache/plumed/LABEL
#   build.sh gromacs VERSION LABEL    patch GROMACS VERSION (runtime mode) with the patches of the PLUMED build
#                                     cache/plumed/LABEL, install in cache/gromacs/VERSION-LABEL
#   build.sh vanilla VERSION          GROMACS VERSION without patches, with its PLUMED module (GMX_USE_PLUMED),
#                                     install in cache/gromacs/VERSION-vanilla
#
# GROMACS is built with MPI, without GPU (GPU=CUDA for a CUDA build, CUDA_ARCH to choose the architecture).
# Each GROMACS version is configured and compiled once: other patch sets are applied to the same tree and only
# the files they change are recompiled. Sources are downloaded to cache/. Environment: PLUMED_REPO (a plumed2
# git repository to use instead of the mirror of github.com/plumed/plumed2 in cache/plumed2.git), MPI_HOME, JOBS.
set -e
H=$(cd "$(dirname "$0")" && pwd); C=$H/cache
JOBS=${JOBS:-$(nproc)}
if [ -n "$MPI_HOME" ]; then export PATH=$MPI_HOME/bin:$PATH LD_LIBRARY_PATH=$MPI_HOME/lib:$LD_LIBRARY_PATH; fi
mkdir -p $C/logs $C/dl

# the GROMACS sources of VERSION, extracted in directory DIR (once)
gromacs_source() {
  local v=$1 dir=$2
  [ -f $C/dl/gromacs-$v.tar.gz ] || curl -fsSL -o $C/dl/gromacs-$v.tar.gz https://ftp.gromacs.org/gromacs/gromacs-$v.tar.gz
  if [ ! -d $dir ]; then
    mkdir -p $dir; tar xzf $C/dl/gromacs-$v.tar.gz -C $dir --strip-components=1
  fi
}

# configure (once), compile and install the GROMACS tree DIR of VERSION into PREFIX, with extra cmake options
gromacs_build() {
  local v=$1 dir=$2 prefix=$3 log=$4; shift 4
  # old GROMACS versions miss some includes that recent compilers need
  local extra=""; case $v in 2020.*|2021.*) extra="-include cstdint -include limits";; esac
  local gpu="-DGMX_GPU=OFF"
  if [ "$GPU" = CUDA ]; then
    # CUDA 13 makes global template stubs static by default, which GROMACS < 2025 does not expect
    gpu="-DGMX_GPU=CUDA -DCMAKE_CUDA_ARCHITECTURES=${CUDA_ARCH:-native} -DCUDA_NVCC_FLAGS=-static-global-template-stub=false"
  fi
  mkdir -p $dir/build; cd $dir/build
  cmake .. -DCMAKE_BUILD_TYPE=Release -DGMX_MPI=ON $gpu -DGMX_FFT_LIBRARY=fftpack -DGMX_HWLOC=OFF \
    -DCMAKE_C_COMPILER=mpicc -DCMAKE_CXX_COMPILER=mpicxx -DCMAKE_CXX_FLAGS="$extra" \
    -DCMAKE_INSTALL_PREFIX=$prefix "$@" > $C/logs/$log-cmake.log 2>&1
  make -j$JOBS install > $C/logs/$log-make.log 2>&1
}

case $1 in
plumed)
  label=$2; ref=${3:-$2}; src=$C/src/plumed-$label; prefix=$C/plumed/$label
  if [ -z "$PLUMED_REPO" ]; then
    PLUMED_REPO=$C/plumed2.git
    [ -d $PLUMED_REPO ] || git clone -q --mirror https://github.com/plumed/plumed2.git $PLUMED_REPO
    git -C $PLUMED_REPO remote update --prune > /dev/null
  fi
  rm -rf $src $prefix; mkdir -p $src
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
  # the patch for GROMACS 2026.x is called gromacs-2026.0 (same for the other series)
  engine=$(ls $P/lib/plumed/patches | sed -n "s/^\(gromacs-${v%.*}\.[0-9]*\)\.diff$/\1/p" | head -1)
  [ -n "$engine" ] || { echo "no patch for GROMACS $v in $label"; exit 1; }
  gromacs_source $v $G
  export PATH=$P/bin:$PATH LD_LIBRARY_PATH=$P/lib:$LD_LIBRARY_PATH
  cd $G
  if [ -e .plumed-engine ]; then plumed patch -R -e "$(cat .plumed-engine)" > $C/logs/gromacs-$v$tag-$label-patch.log 2>&1; fi
  plumed patch -p -e $engine --runtime >> $C/logs/gromacs-$v$tag-$label-patch.log 2>&1
  echo $engine > .plumed-engine
  log=$C/logs/gromacs-$v$tag-$label-patch.log
  if grep -q "on-the-fly diff" $log; then
    # the patch is applied as a diff, which works for all the releases of a series: every hunk must apply, or be
    # there already (a later release can include a change of the patch)
    if grep -q "Hunk #[0-9]* FAILED" $log; then echo "GROMACS $v: the $label patch does not apply"; exit 1; fi
  else
    # the patched files must be exactly the files of the patch
    D=$P/lib/plumed/patches/$engine.diff
    for f in $(cd $D && find . -type f ! -name "*.preplumed"); do
      cmp -s $D/$f $f || { echo "GROMACS $v: $f differs from the $label patch"; exit 1; }
    done
  fi
  gromacs_build $v $G $prefix gromacs-$v$tag-$label
  echo "built GROMACS $v$tag with the $engine patch of $label"
  ;;
vanilla)
  v=$2; tag=${GPU:+-$(echo $GPU | tr A-Z a-z)}
  G=$C/src/gromacs-$v-vanilla$tag; prefix=$C/gromacs/$v-vanilla$tag
  gromacs_source $v $G
  gromacs_build $v $G $prefix gromacs-$v-vanilla$tag -DGMX_USE_PLUMED=ON
  echo "built GROMACS $v$tag without patches"
  ;;
*)
  sed -n '2,15p' "$0"; exit 1
  ;;
esac
