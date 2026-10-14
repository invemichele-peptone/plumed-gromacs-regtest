#!/bin/bash
# Build everything for the before/after matrix: upstream and fixed patches of each PLUMED branch.
H=$(cd "$(dirname "$0")" && pwd)
export PLUMED_REPO=${PLUMED_REPO:-$H/../plumed2}
B=$H/build.sh
$B plumed v2.9       refs/remotes/upstream/v2.9
$B plumed v2.9-fix   gromacs-legacy-fixes
$B plumed v2.10      refs/remotes/upstream/v2.10
$B plumed v2.10-fix  gromacs-native-fixes
$B plumed master-fix gromacs-fixes-master
for v in 2020.7 2021.7 2022.5 2023.5 2024.3; do $B gromacs $v v2.9; $B gromacs $v v2.9-fix; done
for v in 2025.0 2026.4; do $B gromacs $v v2.10; $B gromacs $v v2.10-fix; done
