# Results

`./matrix.py` on 2026-10-14, aarch64 (GB10), GCC 13, OpenMPI, CUDA 13. Columns: GROMACS version / PLUMED patches (`v2.9`, `v2.10`: as released; `-fix`: with the fixes), and the PLUMED kernel when it is not the one of the patches (`k2.10`: v2.10, `k2.10f`: v2.10 with the fixes, `kmf`: master with the fixes). `-`: not applicable.

| test | 2020.7/v2.9 | 2020.7/v2.9-fix | 2021.7/v2.9 | 2021.7/v2.9-fix | 2022.5/v2.9 | 2022.5/v2.9-fix | 2023.5/v2.9 | 2023.5/v2.9-fix | 2024.3/v2.9 | 2024.3/v2.9-fix | 2024.3/v2.9:k2.10 | 2024.3/v2.9-fix:k2.10f | 2022.5/v2.9-fix:kmf | 2025.0/v2.10 | 2025.0/v2.10-fix | 2026.4/v2.10 | 2026.4/v2.10-fix | 2026.4/v2.10-fix:kmf | 2024.3-cuda/v2.9 | 2024.3-cuda/v2.9-fix |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| energy | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass |
| pull | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | pass | pass | pass | pass | pass | pass | **FAIL** | pass |
| pull-dd | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | pass | pass | pass | pass | pass | pass | **FAIL** | pass |
| pull-energy | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass |
| pull-mts | - | - | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | pass | pass | pass | pass | pass | pass | **FAIL** | pass |
| mts-fast-step | - | - | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | pass | **FAIL** | pass | **FAIL** | pass | pass | **FAIL** | pass |
| vsite | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | pass | **FAIL** | pass | **FAIL** | pass | pass | **FAIL** | pass |
| energy-bias | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass |
| energy-bias-dd | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | **FAIL** | pass | pass | **FAIL** | pass | **FAIL** | pass | pass | pass | pass |
| em | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | pass | **FAIL** | pass | **FAIL** | pass | pass | **FAIL** | pass |
| data | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass |
| checkpoint | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass |
| committor | pass | pass | pass | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | pass | **FAIL** | pass | **FAIL** | pass | pass | **FAIL** | pass |
| committor-walkers | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | pass | **FAIL** | pass | **FAIL** | pass | pass | **FAIL** | pass |
| rerun | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | pass | **FAIL** | pass | **FAIL** | pass | pass | **FAIL** | pass |
| hrex | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | pass | - | - | - | - | - | **FAIL** | pass |
| shells | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | pass | **FAIL** | pass | **FAIL** | pass | pass | **FAIL** | pass |
| expanded | pass | pass | pass | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | pass | - | - | - | - | - | **FAIL** | pass |
| md-vv | pass | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | pass | pass | pass | pass | pass | pass | **FAIL** | pass |
| replex-nex | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | **FAIL** | pass | pass | - | - | - | - | - | **FAIL** | pass |
| replex-bias | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | **FAIL** | pass | **FAIL** | pass | pass | pass | pass |
| gpu-buffer-ops | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | **FAIL** | pass |

The failures of the releases, with the numbers, are in `results/matrix.md` after a run.
