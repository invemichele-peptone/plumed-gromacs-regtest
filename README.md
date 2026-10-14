# Regression tests for PLUMED with GROMACS

PLUMED's regtests run PLUMED alone (through `plumed driver`); nothing tests the GROMACS patches, which are
large and differ for each GROMACS version. The [PLUMED testcenter](https://plumed-testcenter.github.io)
checks that one patched GROMACS passes positions, masses, charges, the timestep and the energy, and that a
bias on the volume gives the right pressure. These tests check the rest of the interface: forces on atoms
and their virial, virtual sites, multiple time stepping, domain decomposition, checkpoints, stop requests,
reruns, energy minimization, replica exchange, multiple walkers, expanded ensemble and shells.

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
  final checkpoint, also with several simulations; shells, `-nex` and energies on MTS fast steps are
  refused with an error where they are not supported.

Comparisons use tolerances that cover single precision and the 6 digits printed by `gmx dump`; the bugs
these tests were written for give differences that are orders of magnitude larger (e.g. a double-counted
virial of 1.7e3 kJ/mol against a tolerance of 8).

## Usage

```bash
# build the PLUMED kernels and the patched GROMACS versions listed in build-all.sh (cache/, ~1-2 h)
MPI_HOME=/path/to/mpi PLUMED_REPO=/path/to/plumed2 ./build-all.sh

# run the tests on one combination
./regtest.py --gmx cache/gromacs/2024.3-v2.9-fix/bin/gmx_mpi --kernel cache/plumed/v2.9-fix/lib/libplumedKernel.so

# run them on all the combinations of matrix.txt and write results/matrix.md and results/matrix.html
./matrix.py --jobs 4

./regtest.py --list      # the tests and what they check
```

`build.sh plumed LABEL GITREF` builds PLUMED from a git reference; `build.sh gromacs VERSION LABEL` patches
GROMACS with the patches of a PLUMED build (runtime mode, so that any kernel can be used with it) and
checks that the patched files are exactly the files of the patch. Each GROMACS version is compiled once;
other patches are applied to the same tree. `GPU=CUDA` builds GROMACS with CUDA, for the GPU test.

Each test takes from a fraction of a second to a few seconds (small systems: alanine dipeptide in vacuum, a
TIP4P water box of 3636 atoms, a polarizable water dimer); a combination takes about a minute, unless a
test waits for a run that hangs (killed after 2 minutes).

## Adding a test

A test is a function in `regtest.py` decorated with `@test("name")`, whose docstring says what it checks.
It prepares runs with `env.dir()`, `env.grompp()` (an input of `systems/` with mdp overrides) and
`env.mdrun()`, reads the results with `env.frames()` (trr), `env.energy()` (edr) and `colvar()`, and raises
`Fail` (with the numbers) or `Skip` (feature not available in this combination), or returns a message.
Prefer properties that hold everywhere over reference values.

## Not covered

- thread-MPI builds (the patches support only one rank with thread-MPI, which they now check);
- GPU runs other than the force buffer test (they need a CUDA build);
- performance, and simulations long enough to compare averages;
- with multiple time stepping, the forces written to the trajectory on the steps when PLUMED runs after
  the force calculation do not include PLUMED's forces (it applies them to the buffer used by the update):
  `pull-mts` compares positions and virial only.
