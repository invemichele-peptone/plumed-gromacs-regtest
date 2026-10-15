# Regression tests for PLUMED with GROMACS

<!-- summary: written by matrix.py -->
**Last run: 2026-10-15**, with PLUMED v2.9 [`8e9e512a2`](https://github.com/plumed/plumed2/commit/8e9e512a200c9d78e952b885d18622e0a9fefb8f), v2.10 [`4b8956204`](https://github.com/plumed/plumed2/commit/4b8956204984c2bfbfc6335f0577d576882c13e3), master [`b279e3a3a`](https://github.com/plumed/plumed2/commit/b279e3a3ab8df63ca1515204a4ed20aa09db7617).

| PLUMED \ GROMACS | 2020.7 | 2021.7 | 2022.5 | 2023.5 | 2024.3 | 2025.5 | 2026.4 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| v2.9 | ✅ | ✅ | ✅ | ✅ | ✅ |  |  |
| v2.10 |  |  | ❌ | ❌ | ❌ | ❌ | ❌ |
| master |  |  |  |  | ❌ | ❌ | ❌ |

✅ all the tests pass, ❌ some fail (or the build failed), empty: no patch for that version of GROMACS. GROMACS without patches, which fails the tests of what only the patches of PLUMED add, is in the full results.

- Full results, with the tests and the numbers: [RESULTS.md](RESULTS.md)
- One line for each run: [HISTORY.md](HISTORY.md)

---
<!-- /summary -->

This repository keeps track of which combinations of PLUMED and GROMACS work, and which break. It builds the
branches of [PLUMED](https://github.com/plumed/plumed2) (`v2.9`, `v2.10` and `master`), patches each GROMACS
version that a branch has a patch for, builds GROMACS without patches (with the PLUMED module that GROMACS
includes since version 2025), and runs the same regression tests on all the combinations.

PLUMED's own regtests run PLUMED alone (through `plumed driver`), so nothing in PLUMED tests the GROMACS
patches, which are large and differ for each GROMACS version. The [PLUMED testcenter](https://plumed-testcenter.github.io)
checks that GROMACS passes positions, masses, charges, the timestep and the energy, and that a bias on the
volume gives the right pressure. These tests check the rest of the interface: forces on atoms and their
virial, virtual sites, multiple time stepping, domain decomposition, checkpoints, stop requests, reruns,
energy minimization, replica exchange, multiple walkers, expanded ensemble and shells. The testcenter runs
the same tests (`tests/gromacs/regtests`) every week on the latest GROMACS, patched and without patches;
this repository runs them on all the versions that PLUMED can patch.

## Approach

No test stores reference results: every test checks a property that must hold for any GROMACS version,
any PLUMED version and any way of patching GROMACS. The same tests then run on all their combinations.

- **Independent reference.** A PLUMED `RESTRAINT` on the distance between two atoms must act as the
  GROMACS pull code (an umbrella on the same distance, with the same constant): the same trajectory, the
  same forces and the same virial (`pull*` tests). The pull code is part of GROMACS and does not depend on
  PLUMED or on the patch.
- **Invariances.** The same simulation must give the same results with and without `ENERGY` in the PLUMED
  input (with it, PLUMED runs after the energy is complete, a different code path: `pull-energy`, `vsite`,
  `em`), and on 1, 2 or 3 ranks (`pull-dd`, `energy-bias-dd`, `em`, `rerun`, `hrex`).
- **Exact relations.** `ENERGY` equals the potential energy of GROMACS; a bias s·`ENERGY` multiplies all
  the forces by 1+s; a rerun gives the CVs that PLUMED computed during the run; PLUMED's `lambda` is the
  lambda state of GROMACS; two identical replicas have a zero exchange energy.
- **Protocols.** PLUMED writes its state at the checkpoints of GROMACS; `COMMITTOR` stops mdrun, with a
  final checkpoint, also with several simulations and in reruns; shells, `-nex` and energies on MTS fast
  steps are refused with an error where they are not supported.

Comparisons use tolerances that cover single precision and the 6 digits printed by `gmx dump`; the bugs
these tests were written for give differences that are orders of magnitude larger (e.g. a double-counted
virial of 1.7e3 kJ/mol against a tolerance of 0.1 kJ/mol at the first step). A test is skipped (➖) when the
combination does not have the feature, e.g. `-hrex` with the PLUMED module of GROMACS 2025 and later.
GROMACS without patches fails the tests of what only the patches of PLUMED add (e.g. `ENERGY`, `COMMITTOR`
and the checkpoints of PLUMED): this is expected, and shows what the patches add.

## Usage

```bash
export MPI_HOME=/path/to/mpi   # if mpirun and mpicc are not in the PATH
./build-all.sh                 # build the PLUMED branches and GROMACS in cache/, and write matrix.txt
./matrix.py --jobs 4           # run the tests on all the combinations: RESULTS.md, HISTORY.md, results/
git add README.md RESULTS.md HISTORY.md && git commit -m "Results of $(date +%F)"
```

`build-all.sh` builds PLUMED from the current heads of the branches (from a mirror of the PLUMED repository in
`cache/`), and GROMACS with each patch that a branch has, in runtime mode, with that branch's kernel. It also
builds the latest releases of GROMACS 2025 and 2026 without patches, tested with the kernels of `v2.10` and
`master`. Environment variables choose other branches (`BRANCHES`), versions without patches (`VANILLA`) and
their kernels (`VANILLA_KERNELS`); `CUDA=1` also builds the newest patched GROMACS of each branch with CUDA, for
the GPU test. Each GROMACS version is compiled once: the other patches are applied to the same tree, and only
the files that they change are recompiled. On a 20-core machine, the first build takes about half an hour,
the following ones about 6 minutes. A build that fails is listed in `RESULTS.md` and `HISTORY.md`, and its
combinations are left out. A patch named after the first release of a series (e.g. `gromacs-2026.0`, which is
applied as a diff to any 2026 release) is tested on the latest release of the series.

`matrix.py` runs `regtest.py` on each combination of `matrix.txt` (the runs, with their inputs and logs, are in
`results/`), writes the summary at the start of this README, and the full table to `RESULTS.md` and
`results/matrix.html`. A run of the whole matrix also adds a line to `HISTORY.md`. `--only REGEX` selects combinations, `--tests REGEX` selects tests, `--report-only`
writes the tables again from the existing results.

A single combination, or any GROMACS built with MPI:

```bash
./regtest.py --list      # the tests and what they check
./regtest.py --gmx cache/gromacs/2026.0-v2.10/bin/gmx_mpi --kernel cache/plumed/v2.10/lib/libplumedKernel.so
./regtest.py --gmx ... --kernel ... --tests 'pull|vsite' --out mytest
```

Each test takes from a fraction of a second to a few seconds (small systems: alanine dipeptide in vacuum, a
TIP4P water box of 3636 atoms, a polarizable water dimer); a combination takes about half a minute, and the
whole matrix a few minutes with `--jobs 4`, unless a run hangs (it is killed after 2 minutes, or 5 for the
longer run of the `committor` test).

`regtest.py` and `systems/` are the same as in `tests/gromacs/regtests` of the testcenter: change them there
too.

## Adding a test

A test is a function in `regtest.py` decorated with `@test("name")`, whose docstring says what it checks.
It prepares runs with `env.dir()`, `env.grompp()` (an input of `systems/` with mdp overrides) and
`env.mdrun()`, reads the results with `env.frames()` (trr), `env.energy()` (edr) and `colvar()`, and raises
`Fail` (with the numbers) or `Skip` (feature not available in this combination), or returns a message.
Prefer properties that hold everywhere over reference values.

## Not covered

- thread-MPI builds (the patches support only one rank with thread-MPI, which they check);
- GPU runs other than the force buffer test (they need a CUDA build);
- performance, and simulations long enough to compare averages.
