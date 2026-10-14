#!/usr/bin/env python3
"""Run regtest.py on several GROMACS/PLUMED combinations and tabulate the results.

    matrix.py [--matrix matrix.txt] [--jobs 4] [--tests REGEX] [--only REGEX] [--report-only]

Each non-comment line of the matrix file is: LABEL GROMACS_INSTALL KERNEL_INSTALL, where the installs are
directories under cache/gromacs and cache/plumed (or absolute paths). The table is written to
results/matrix.md, with one column per combination.
"""
import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent


def install(path, kind):
    p = Path(path)
    return p if p.is_absolute() else HERE / "cache" / kind / path


def run(combo, tests):
    label, gmx, kernel = combo
    cmd = [sys.executable, str(HERE / "regtest.py"), "--gmx", str(install(gmx, "gromacs") / "bin" / "gmx_mpi"),
           "--kernel", str(install(kernel, "plumed") / "lib" / "libplumedKernel.so"), "--label", label,
           "--tests", tests]
    out = HERE / "results" / label
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "regtest.log", "w") as log:
        subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT)
    return label


def report(combos):
    data = {}
    for label, _, _ in combos:
        f = HERE / "results" / label / "results.json"
        if f.exists():
            data[label] = json.loads(f.read_text())["results"]
    tests = []
    for r in data.values():
        tests += [t for t in r if t not in tests]
    mark = {"PASS": "pass", "FAIL": "**FAIL**", "SKIP": "-"}
    labels = [c[0] for c in combos if c[0] in data]
    lines = ["| test | " + " | ".join(labels) + " |", "|---|" + "---|" * len(labels)]
    for t in tests:
        lines.append(f"| {t} | " + " | ".join(mark.get(data[l].get(t, {}).get("status"), "") for l in labels) + " |")
    lines.append("")
    for l in labels:
        fails = [(t, r["message"]) for t, r in data[l].items() if r["status"] == "FAIL"]
        if fails:
            lines.append(f"**{l}**")
            lines += [f"- {t}: {m}" for t, m in fails]
            lines.append("")
    (HERE / "results" / "matrix.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--matrix", default=str(HERE / "matrix.txt"))
    ap.add_argument("--jobs", type=int, default=4, help="combinations run at the same time")
    ap.add_argument("--tests", default=".", help="regular expression selecting the tests")
    ap.add_argument("--only", default="", help="regular expression selecting the combinations")
    ap.add_argument("--report-only", action="store_true")
    a = ap.parse_args()
    import re
    combos = [tuple(l.split()[:3]) for l in Path(a.matrix).read_text().splitlines()
              if l.strip() and not l.startswith("#")]
    selected = [c for c in combos if re.search(a.only, c[0])]
    if not a.report_only:
        with ThreadPoolExecutor(a.jobs) as pool:
            for label in pool.map(lambda c: run(c, a.tests), selected):
                print(f"done {label}", flush=True)
    report(combos)


if __name__ == "__main__":
    main()
