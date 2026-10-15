# Results

`matrix.py` on 2026-10-15, aarch64. PLUMED: v2.9 `8e9e512a2`, v2.10 `75d6916f6`, master `386d0d9b7`. Columns: GROMACS version, the PLUMED branch whose patch was applied (vanilla: GROMACS without patches), and the kernel when it is not of that branch.

| test | 2020.7<br>v2.9 | 2021.7<br>v2.9 | 2022.5<br>v2.9 | 2023.5<br>v2.9 | 2024.3<br>v2.9 | 2022.5<br>v2.10 | 2023.5<br>v2.10 | 2024.3<br>v2.10 | 2025.5<br>v2.10 | 2026.4<br>v2.10 | 2024.3<br>master | 2025.5<br>master | 2026.4<br>master | 2025.5<br>vanilla<br>v2.10 | 2025.5<br>vanilla<br>master | 2026.4<br>vanilla<br>v2.10 | 2026.4<br>vanilla<br>master |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| energy | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| pull | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| pull-dd | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| pull-energy | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| pull-mts | ➖ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| mts-fast-step | ➖ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| vsite | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| energy-bias | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| energy-bias-dd | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| em | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| data | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| checkpoint | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| committor | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| committor-walkers | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| rerun | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| hrex | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ➖ | ➖ | ✅ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ |
| shells | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| expanded | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ➖ | ➖ | ✅ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ |
| md-vv | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| replex-nex | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ➖ | ➖ | ✅ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ |
| replex-bias | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| gpu-buffer-ops | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ |

✅ pass, ❌ fail, ➖ not applicable

**2025.5/vanilla:v2.10**
- energy: 1 ranks: ENERGY differs from the potential energy by 1 (relative)
- mts-fast-step: mdrun exit 0, with no error about MTS
- energy-bias: forces differ from 0.5 times the unbiased ones by up to 0.999 of the largest force
- checkpoint: 1 ranks: states at steps [5725, 8525, 12375, 16300, 20000], checkpoints at [4700, 7500, 11350, 15275, 18975, 20000]
- committor: 1 ranks: committed at step 250, ran to step 20000
- committor-walkers: last steps [20000, 20000]
- rerun: rerun with COMMITTOR: committed at time 0.04, stopped after 11 of 11 frames (last time 0.4)
- shells: 44 COLVAR lines (21 distinct), 6 hills
- replex-bias: mdrun ran replica exchange without the PLUMED bias in the exchange criterion, and without an error

**2025.5/vanilla:master**
- energy: 1 ranks: ENERGY differs from the potential energy by 1 (relative)
- mts-fast-step: mdrun exit 0, with no error about MTS
- energy-bias: forces differ from 0.5 times the unbiased ones by up to 0.999 of the largest force
- checkpoint: 1 ranks: states at steps [5700, 8650, 12100, 16150, 20000], checkpoints at [4700, 7650, 11100, 15150, 19000, 20000]
- committor: 1 ranks: committed at step 250, ran to step 20000
- committor-walkers: last steps [20000, 20000]
- rerun: rerun with COMMITTOR: committed at time 0.04, stopped after 11 of 11 frames (last time 0.4)
- shells: 44 COLVAR lines (21 distinct), 6 hills
- replex-bias: mdrun ran replica exchange without the PLUMED bias in the exchange criterion, and without an error

**2026.4/vanilla:v2.10**
- energy: 1 ranks: ENERGY differs from the potential energy by 1 (relative)
- mts-fast-step: mdrun exit 0, with no error about MTS
- energy-bias: forces differ from 0.5 times the unbiased ones by up to 0.999 of the largest force
- checkpoint: 1 ranks: states at steps [5700, 8450, 12225, 16200, 20000], checkpoints at [4675, 7425, 11200, 15175, 18975, 20000]
- committor: 1 ranks: committed at step 250, ran to step 20000
- committor-walkers: last steps [20000, 20000]
- rerun: rerun with COMMITTOR: committed at time 0.04, stopped after 11 of 11 frames (last time 0.4)
- shells: 44 COLVAR lines (21 distinct), 6 hills
- replex-bias: mdrun ran replica exchange without the PLUMED bias in the exchange criterion, and without an error

**2026.4/vanilla:master**
- energy: 1 ranks: ENERGY differs from the potential energy by 1 (relative)
- mts-fast-step: mdrun exit 0, with no error about MTS
- energy-bias: forces differ from 0.5 times the unbiased ones by up to 0.999 of the largest force
- checkpoint: 1 ranks: states at steps [6625, 8975, 12475, 16250, 20000], checkpoints at [4700, 7050, 10550, 14325, 18075, 20000]
- committor: 1 ranks: committed at step 250, ran to step 20000
- committor-walkers: last steps [20000, 20000]
- rerun: rerun with COMMITTOR: committed at time 0.04, stopped after 11 of 11 frames (last time 0.4)
- shells: 44 COLVAR lines (21 distinct), 6 hills
- replex-bias: mdrun ran replica exchange without the PLUMED bias in the exchange criterion, and without an error
