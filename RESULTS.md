# Results

`matrix.py` on 2026-10-15, aarch64. PLUMED: v2.9 `8e9e512a2`, v2.10 `4b8956204`, master `b279e3a3a`. Columns: GROMACS version, the PLUMED branch whose patch was applied (vanilla: GROMACS without patches), and the kernel when it is not of that branch.

| test | 2020.7<br>v2.9 | 2021.7<br>v2.9 | 2022.5<br>v2.9 | 2023.5<br>v2.9 | 2024.3<br>v2.9 | 2022.5<br>v2.10 | 2023.5<br>v2.10 | 2024.3<br>v2.10 | 2025.5<br>v2.10 | 2026.4<br>v2.10 | 2024.3<br>master | 2025.5<br>master | 2026.4<br>master | 2025.5<br>vanilla<br>v2.10 | 2025.5<br>vanilla<br>master | 2026.4<br>vanilla<br>v2.10 | 2026.4<br>vanilla<br>master |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| energy | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| pull | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| pull-dd | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| pull-energy | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| pull-mts | ➖ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| mts-fast-step | ➖ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| vsite | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| energy-bias | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| energy-bias-dd | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| em | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| data | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| checkpoint | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| committor | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| committor-walkers | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| rerun | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| hrex | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ➖ | ➖ | ✅ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ |
| shells | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| expanded | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ➖ | ➖ | ✅ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ |
| md-vv | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| replex-nex | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ➖ | ➖ | ✅ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ |
| replex-bias | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| gpu-buffer-ops | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ | ➖ |

✅ pass, ❌ fail, ➖ not applicable

**2022.5/v2.10**
- pull-mts: PLUMED against pull code, 1 rank: max |dx| 1e-05 nm, |df|/max|f| at step 0 0.026, |dvirial| at step 0 3.8 kJ/mol, max 5.19 kJ/mol (virial ~ 8.08e+04)

**2023.5/v2.10**
- pull-mts: PLUMED against pull code, 1 rank: max |dx| 1e-05 nm, |df|/max|f| at step 0 0.026, |dvirial| at step 0 3.8 kJ/mol, max 5.16 kJ/mol (virial ~ 8.08e+04)

**2024.3/v2.10**
- pull-mts: PLUMED against pull code, 1 rank: max |dx| 1e-05 nm, |df|/max|f| at step 0 0.026, |dvirial| at step 0 3.8 kJ/mol, max 5.21 kJ/mol (virial ~ 8.08e+04)

**2025.5/v2.10**
- pull-mts: PLUMED against pull code, 1 rank: max |dx| 1e-05 nm, |df|/max|f| at step 0 0.026, |dvirial| at step 0 3.8 kJ/mol, max 5.15 kJ/mol (virial ~ 8.08e+04)
- rerun: rerun with COMMITTOR: committed at time 0.04, stopped after 3 of 11 frames (last time 0.08)
- shells: rerun of one frame: 4 COLVAR lines

**2026.4/v2.10**
- pull-mts: PLUMED against pull code, 1 rank: max |dx| 1e-05 nm, |df|/max|f| at step 0 0.026, |dvirial| at step 0 3.8 kJ/mol, max 5.15 kJ/mol (virial ~ 8.08e+04)
- rerun: rerun with COMMITTOR: committed at time 0.04, stopped after 3 of 11 frames (last time 0.08)
- shells: rerun of one frame: 4 COLVAR lines

**2024.3/master**
- pull-mts: PLUMED against pull code, 1 rank: max |dx| 1e-05 nm, |df|/max|f| at step 0 0.026, |dvirial| at step 0 3.8 kJ/mol, max 5.21 kJ/mol (virial ~ 8.08e+04)

**2025.5/master**
- pull-mts: PLUMED against pull code, 1 rank: max |dx| 1e-05 nm, |df|/max|f| at step 0 0.026, |dvirial| at step 0 3.8 kJ/mol, max 5.15 kJ/mol (virial ~ 8.08e+04)
- rerun: rerun with COMMITTOR: committed at time 0.04, stopped after 3 of 11 frames (last time 0.08)
- shells: rerun of one frame: 4 COLVAR lines

**2026.4/master**
- pull-mts: PLUMED against pull code, 1 rank: max |dx| 1e-05 nm, |df|/max|f| at step 0 0.026, |dvirial| at step 0 3.8 kJ/mol, max 5.15 kJ/mol (virial ~ 8.08e+04)
- rerun: rerun with COMMITTOR: committed at time 0.04, stopped after 3 of 11 frames (last time 0.08)
- shells: rerun of one frame: 4 COLVAR lines

**2025.5/vanilla:v2.10**
- energy: 1 ranks: ENERGY differs from the potential energy by 1 (relative)
- mts-fast-step: mdrun exit 0, with no error about MTS
- energy-bias: forces differ from 0.5 times the unbiased ones by up to 0.999 of the largest force
- checkpoint: 1 ranks: states at steps [4775, 8525, 12275, 16250, 20000], checkpoints at [4500, 8250, 12000, 15975, 19725, 20000]
- committor: 1 ranks: committed at step 250, ran to step 20000
- committor-walkers: last steps [20000, 20000]
- rerun: rerun with COMMITTOR: committed at time 0.04, stopped after 11 of 11 frames (last time 0.4)
- shells: 44 COLVAR lines (21 distinct), 6 hills
- replex-bias: mdrun ran replica exchange without the PLUMED bias in the exchange criterion, and without an error

**2025.5/vanilla:master**
- energy: 1 ranks: ENERGY differs from the potential energy by 1 (relative)
- mts-fast-step: mdrun exit 0, with no error about MTS
- energy-bias: forces differ from 0.5 times the unbiased ones by up to 0.999 of the largest force
- checkpoint: 1 ranks: states at steps [4950, 8475, 12275, 16200, 20000], checkpoints at [4650, 8175, 11975, 15900, 19700, 20000]
- committor: 1 ranks: committed at step 250, ran to step 20000
- committor-walkers: last steps [20000, 20000]
- rerun: rerun with COMMITTOR: committed at time 0.04, stopped after 11 of 11 frames (last time 0.4)
- shells: 44 COLVAR lines (21 distinct), 6 hills
- replex-bias: mdrun ran replica exchange without the PLUMED bias in the exchange criterion, and without an error

**2026.4/vanilla:v2.10**
- energy: 1 ranks: ENERGY differs from the potential energy by 1 (relative)
- mts-fast-step: mdrun exit 0, with no error about MTS
- energy-bias: forces differ from 0.5 times the unbiased ones by up to 0.999 of the largest force
- checkpoint: 1 ranks: states at steps [5750, 8800, 12100, 15975, 20000], checkpoints at [4675, 7725, 11025, 14900, 18925, 20000]
- committor: 1 ranks: committed at step 250, ran to step 20000
- committor-walkers: last steps [20000, 20000]
- rerun: rerun with COMMITTOR: committed at time 0.04, stopped after 11 of 11 frames (last time 0.4)
- shells: 44 COLVAR lines (21 distinct), 6 hills
- replex-bias: mdrun ran replica exchange without the PLUMED bias in the exchange criterion, and without an error

**2026.4/vanilla:master**
- energy: 1 ranks: ENERGY differs from the potential energy by 1 (relative)
- mts-fast-step: mdrun exit 0, with no error about MTS
- energy-bias: forces differ from 0.5 times the unbiased ones by up to 0.999 of the largest force
- checkpoint: 1 ranks: states at steps [6050, 8650, 12250, 16100, 20000], checkpoints at [4700, 7300, 10900, 14750, 18650, 20000]
- committor: 1 ranks: committed at step 250, ran to step 20000
- committor-walkers: last steps [20000, 20000]
- rerun: rerun with COMMITTOR: committed at time 0.04, stopped after 11 of 11 frames (last time 0.4)
- shells: 44 COLVAR lines (21 distinct), 6 hills
- replex-bias: mdrun ran replica exchange without the PLUMED bias in the exchange criterion, and without an error
