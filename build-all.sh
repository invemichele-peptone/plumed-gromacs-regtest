#!/bin/bash
# Build the PLUMED branches, GROMACS for each patch that they have, and GROMACS without patches, and write
# matrix.txt with the combinations to test. A build that fails is listed in cache/build-failures.txt (which
# matrix.py reports) and left out of the matrix. A patch named after the first release of a series (e.g.
# gromacs-2026.0, applied as a diff to any 2026 release) is tested on the latest release of the series.
#
#   BRANCHES  PLUMED branches (default: v2.9 v2.10 master)
#   VANILLA   GROMACS versions without patches (default: the latest releases of GROMACS 2025 and 2026), tested
#             with the kernels of VANILLA_KERNELS (default: v2.10 master)
#   CUDA=1    also build the newest patched GROMACS of each branch with CUDA, for the GPU test
H=$(cd "$(dirname "$0")" && pwd); B=$H/build.sh; M=$H/matrix.txt
BRANCHES=${BRANCHES:-"v2.9 v2.10 master"}
latest() { git ls-remote --tags --refs https://gitlab.com/gromacs/gromacs.git "v$1.*" | sed 's|.*refs/tags/v||' \
  | grep -E '^[0-9]+\.[0-9]+$' | sort -V | tail -n 1; }
VANILLA=${VANILLA:-"$(latest 2025) $(latest 2026)"}
VANILLA_KERNELS=${VANILLA_KERNELS:-"v2.10 master"}
line() { printf '%-26s %-26s %s\n' "$1" "$2" "$3" >> $M; }
F=$H/cache/build-failures.txt; mkdir -p $H/cache; : > $F
failed() { echo "FAILED: $1"; echo "$1" >> $F; }

cat > $M <<EOF
# LABEL                    GROMACS install (cache/gromacs)  PLUMED kernel (cache/plumed)
# Written by build-all.sh. A comment just before a group of combinations names the group in the report: "# Title: description"
EOF
for b in $BRANCHES; do
  $B plumed $b || { failed "PLUMED $b"; continue; }
  echo "# PLUMED $b: GROMACS with each patch of PLUMED $b, and its kernel" >> $M
  versions=$(ls $H/cache/plumed/$b/lib/plumed/patches | sed -n 's/^gromacs-\(.*\)\.diff$/\1/p' | sort -V \
    | while read -r v; do case $v in *.0) latest ${v%.0};; *) echo $v;; esac; done)
  for v in $versions; do
    if $B gromacs $v $b; then line "$v/$b" "$v-$b" $b; else failed "GROMACS $v with PLUMED $b"; fi
  done
  newest=$(echo "$versions" | tail -n 1)
  if [ -n "$CUDA" ] && [ -n "$newest" ]; then
    if GPU=CUDA $B gromacs $newest $b; then line "$newest-cuda/$b" "$newest-$b-cuda" $b
    else failed "GROMACS $newest with CUDA and PLUMED $b"; fi
  fi
done
echo "# GROMACS without patches: its PLUMED module, with the kernels of PLUMED $VANILLA_KERNELS" >> $M
for v in $VANILLA; do
  $B vanilla $v || { failed "GROMACS $v without patches"; continue; }
  for k in $VANILLA_KERNELS; do [ -d $H/cache/plumed/$k ] && line "$v/vanilla:$k" "$v-vanilla" $k; done
done
echo "matrix: $M"
