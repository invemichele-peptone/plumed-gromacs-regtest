#!/usr/bin/env python3
"""Run regtest.py on several GROMACS/PLUMED combinations and tabulate the results.

    matrix.py [--matrix matrix.txt] [--jobs 4] [--tests REGEX] [--only REGEX] [--report-only]

Each non-comment line of the matrix file is: LABEL GROMACS_INSTALL KERNEL_INSTALL, where the installs are
directories under cache/gromacs and cache/plumed (or absolute paths). The runs are in results/LABEL. The table,
with one column per combination, is written to RESULTS.md (with emoji for the colors) and results/matrix.html;
a run of the whole matrix also adds a line to HISTORY.md.
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
    out = HERE / "results" / label
    out.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(HERE / "regtest.py"), "--gmx", str(install(gmx, "gromacs") / "bin" / "gmx_mpi"),
           "--kernel", str(install(kernel, "plumed") / "lib" / "libplumedKernel.so"), "--out", str(out),
           "--tests", tests]
    with open(out / "regtest.log", "w") as log:
        subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT)
    return label


MARK = {"PASS": "✅", "FAIL": "❌", "SKIP": "➖"}
SYMBOL = {"PASS": "✓", "FAIL": "✗", "SKIP": "–"}
ANSI = {"PASS": "\033[32m", "FAIL": "\033[1;31m", "SKIP": "\033[2m"}


def read_matrix(path):
    """The combinations (label, gromacs, kernel) of a matrix file, and their groups (title, description, labels):
    a comment just before a combination starts a group, named by the text before its first colon."""
    combos, groups, comment = [], [], None
    for line in Path(path).read_text().splitlines():
        if line.startswith("#"):
            comment = line[1:].strip()
        elif line.strip():
            combos.append(tuple(line.split()[:3]))
            if comment is not None or not groups:
                title, _, desc = (comment or "").partition(":")
                groups.append((title.strip(), desc.strip(), []))
                comment = None
            groups[-1][2].append(combos[-1][0])
    return combos, groups


def header(label, sep):
    """2026.4/vanilla:v2.10 -> GROMACS version, patches (a PLUMED branch, or vanilla) and the kernel if given"""
    rest, _, kernel = label.partition(":")
    return sep.join(x for x in rest.split("/", 1) + [kernel] if x)


def plumed_commits(combos):
    """{kernel label: full commit} of the PLUMED builds used by the combinations"""
    commits = {}
    for _, _, kernel in combos:
        f = install(kernel, "plumed") / "GITREF"
        if kernel not in commits and f.exists():
            commits[kernel] = f.read_text().strip()
    return commits


def summary(labels, fails, builds, commits, run_date):
    """The table at the start of README.md: the PLUMED branches down, the patched GROMACS versions across, a cell
    green if all the tests pass and red if some fail or the build failed"""
    import re
    cells, branches, versions = {}, [], []

    def add(branch, version, mark):
        branches.extend([branch] if branch not in branches else [])
        versions.extend([version] if version not in versions else [])
        cells[branch, version] = mark

    for l in labels:
        rest, _, kernel = l.partition(":")
        version, _, branch = rest.partition("/")
        if branch != "vanilla" and not kernel:
            add(branch, version, MARK["FAIL"] if fails[l] else MARK["PASS"])
    for b in builds:
        m = re.fullmatch(r"GROMACS (\S+)( with CUDA and| with) PLUMED (\S+)", b)
        if m:
            add(m.group(3), m.group(1) + ("-cuda" if "CUDA" in m.group(2) else ""), MARK["FAIL"] + " build")
        elif b.startswith("PLUMED "):
            branches.extend([b.split()[1]] if b.split()[1] not in branches else [])
            cells[b.split()[1], None] = "build failed"
    versions.sort(key=lambda v: ([int(x) for x in v.split("-")[0].split(".")], v))
    link = lambda k, c: f"{k} [`{c[:9]}`](https://github.com/plumed/plumed2/commit/{c})"
    lines = [f"**Last run: {run_date}**, with PLUMED " + ", ".join(link(k, c) for k, c in commits.items()) + ".", "",
             "| PLUMED \\ GROMACS | " + " | ".join(versions) + " |", "|---|" + ":---:|" * len(versions)]
    for b in branches:
        name = f"{b} (build failed)" if (b, None) in cells else b
        lines.append(f"| {name} | " + " | ".join(cells.get((b, v), "") for v in versions) + " |")
    lines += ["", f"{MARK['PASS']} all the tests pass, {MARK['FAIL']} some fail (or the build failed), empty: no patch "
              "for that version of GROMACS. GROMACS without patches, which fails the tests of what only the patches "
              "of PLUMED add, is in the full results.", "",
              "- Full results, with the tests and the numbers: [RESULTS.md](RESULTS.md)",
              "- One line for each run: [HISTORY.md](HISTORY.md)", "", "---"]
    return "\n".join(lines)


def write_summary(text):
    """Replace the text between the summary markers of README.md"""
    readme = HERE / "README.md"
    begin, end = "<!-- summary: written by matrix.py -->", "<!-- /summary -->"
    s = readme.read_text()
    if begin in s and end in s:
        s = s[:s.index(begin) + len(begin)] + "\n" + text + "\n" + s[s.index(end):]
        readme.write_text(s)


def report(combos, groups, history=False):
    from datetime import date
    import platform
    data, mtimes = {}, []
    for label, _, _ in combos:
        f = HERE / "results" / label / "results.json"
        if f.exists():
            data[label] = json.loads(f.read_text())
            mtimes.append(f.stat().st_mtime)
    # the date of the results (a report written again later keeps it)
    run_date = date.fromtimestamp(max(mtimes)).isoformat() if mtimes else date.today().isoformat()
    tests = []
    for r in data.values():
        tests += [t for t in r if t not in tests]
    labels = [c[0] for c in combos if c[0] in data]
    status = {(t, l): data[l].get(t, {}).get("status", "") for t in tests for l in labels}
    fails = {l: [(t, r["message"]) for t, r in data[l].items() if r["status"] == "FAIL"] for l in labels}

    # markdown, with emoji for the colors (GitHub renders them)
    commits = plumed_commits(combos)
    lines = ["# Results", "",
             f"`matrix.py` on {run_date}, {platform.machine()}. PLUMED: "
             + ", ".join(f"{k} `{c[:9]}`" for k, c in commits.items()) + ". Columns: GROMACS version, the PLUMED branch "
             "whose patch was applied (vanilla: GROMACS without patches), and the kernel when it is not of that "
             "branch.", "",
             "| test | " + " | ".join(header(l, "<br>") for l in labels) + " |", "|---|" + ":---:|" * len(labels)]
    for t in tests:
        lines.append(f"| {t} | " + " | ".join(MARK.get(status[t, l], "") for l in labels) + " |")
    lines += ["", f"{MARK['PASS']} pass, {MARK['FAIL']} fail, {MARK['SKIP']} not applicable", ""]
    f = HERE / "cache" / "build-failures.txt"
    builds = [l for l in f.read_text().splitlines() if l.strip()] if f.exists() else []
    if builds:
        lines += ["Builds that failed (see `cache/logs`), not tested:", ""] + [f"- {l}" for l in builds] + [""]
    for l in labels:
        if fails[l]:
            lines += [f"**{l}**"] + [f"- {t}: {m}" for t, m in fails[l]] + [""]
    (HERE / "RESULTS.md").write_text("\n".join(lines))
    write_summary(summary(labels, fails, builds, commits, run_date))
    (HERE / "results" / "matrix.html").write_text(html_report(data, tests, labels, groups, status, fails))
    if history:
        f = HERE / "HISTORY.md"
        if not f.exists():
            f.write_text("# History\n\nOne line for each run of the whole matrix: the PLUMED commits tested, and the "
                         "combinations that fail, with their failing tests.\n\n| date | PLUMED | failures |\n|---|---|---|\n")
        failing = "; ".join([f"build of {l}" for l in builds]
                            + [f"{l}: {' '.join(t for t, _ in fails[l])}" for l in labels if fails[l]]) or "none"
        with open(f, "a") as h:
            h.write(f"| {run_date} | {', '.join(f'{k} {c[:9]}' for k, c in commits.items())} | {failing} |\n")

    # terminal: one line per combination
    color = sys.stdout.isatty()
    for l in labels:
        n = {k: sum(r["status"] == k for r in data[l].values()) for k in MARK}
        counts = "  ".join((ANSI[k] if color and n[k] else "") + f"{SYMBOL[k]} {n[k]:2d}" + ("\033[0m" if color else "")
                           for k in MARK)
        print(f"{l:24s} {counts}   {' '.join(t for t, _ in fails[l])}")
    print(f"tables: {HERE / 'README.md'} (summary), {HERE / 'RESULTS.md'}, {HERE / 'results' / 'matrix.html'}")


def html_report(data, tests, labels, groups, status, fails):
    import html
    import platform
    from datetime import date
    try:
        import regtest
        docs = {name: " ".join((f.__doc__ or "").split()) for name, f in regtest.TESTS}
    except Exception:
        docs = {}
    e = lambda x: html.escape(str(x), quote=True)
    groups = [(t, d, [l for l in ls if l in data]) for t, d, ls in groups]
    groups = [g for g in groups if g[2]]
    first = {g[2][0] for g in groups}

    def colhead(l):
        parts = header(l, "\n").split("\n")
        spans = [f'<span class="ver">{e(parts[0])}</span>', f'<span class="patch">{e(parts[1])}</span>']
        if len(parts) > 2:
            spans.append(f'<span class="kern">kernel {e(parts[2])}</span>')
        return f'<th scope="col" class="{"g" if l in first else ""}" title="{e(l)}">{"".join(spans)}</th>'

    def cell(t, l):
        s = status[t, l]
        r = data[l].get(t, {})
        tip = f"{l} · {t}: {r.get('message', 'not run')}" + (f" ({r['seconds']} s)" if "seconds" in r else "")
        g = " g" if l in first else ""
        return f'<td class="{s or "none"}{g}" title="{e(tip)}">{SYMBOL.get(s, "")}</td>'

    nfail = {l: len(fails[l]) for l in labels}
    rows = ['<tr class="sum"><th scope="row">failures</th>' + "".join(
        f'<td class="{"FAIL" if nfail[l] else "PASS"}{" g" if l in first else ""}">{nfail[l]}</td>' for l in labels)
        + "</tr>"]
    for t in tests:
        rows.append(f'<tr><th scope="row" title="{e(docs.get(t, ""))}">{e(t)}</th>'
                    + "".join(cell(t, l) for l in labels) + "</tr>")
    detail = []
    for l in labels:
        if fails[l]:
            items = "".join(f"<dt>{e(t)}</dt><dd>{e(m)}</dd>" for t, m in fails[l])
            detail.append(f'<section><h3>{e(l)}</h3><dl>{items}</dl></section>')
    total = sum(nfail.values())
    clean = sum(1 for l in labels if not nfail[l])
    return HTML.format(
        date=date.today().isoformat(), machine=e(platform.machine()), ncombo=len(labels), ntest=len(tests),
        clean=clean, total=total,
        groups="".join(f'<th scope="colgroup" colspan="{len(ls)}" class="g" title="{e(d)}">{e(t)}</th>'
                       for t, d, ls in groups),
        heads="".join(colhead(l) for l in labels), rows="\n".join(rows), detail="\n".join(detail) or "<p>None.</p>")


HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<!-- page -->
<title>PLUMED GROMACS Regtests</title>
<style>
/* one matrix, tests down and combinations across, grouped like matrix.txt; the failures in full below */
:root {{
  --bg: #f5f7f8; --surface: #ffffff; --fg: #1b2229; --muted: #5d6973; --line: #d6dce1;
  --pass: #17663f; --pass-bg: #d5efdf; --fail: #a4231b; --fail-bg: #f9d6d1; --na: #8c969f; --na-bg: #edf0f2;
  --sans: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
  --mono: ui-monospace, "SF Mono", "Cascadia Mono", Menlo, Consolas, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #12161a; --surface: #192026; --fg: #e2e7eb; --muted: #9aa5af; --line: #2c343c;
  --pass: #79d7a2; --pass-bg: #163626; --fail: #ff9387; --fail-bg: #4b1c18; --na: #66717b; --na-bg: #20272d;
  color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --bg: #12161a; --surface: #192026; --fg: #e2e7eb; --muted: #9aa5af; --line: #2c343c;
  --pass: #79d7a2; --pass-bg: #163626; --fail: #ff9387; --fail-bg: #4b1c18; --na: #66717b; --na-bg: #20272d;
  color-scheme: dark; }}
body {{ background: var(--bg); color: var(--fg); font: 14px/1.45 var(--sans); margin: 0; }}
main {{ padding-inline: 16px; padding-block: 24px 40px; max-width: 1400px; margin: 0 auto; display: grid; gap: 20px; }}
h1 {{ font-size: 1.5rem; margin: 0; text-wrap: balance; }}
h2 {{ font-size: 1.1rem; margin: 0 0 8px; }}
h3 {{ font: 600 0.95rem var(--mono); margin: 0 0 6px; }}
p {{ margin: 0; max-width: 70ch; }}
.meta, .legend {{ color: var(--muted); }}
.legend {{ display: flex; flex-wrap: wrap; gap: 6px 18px; align-items: center; }}
.key {{ display: inline-grid; place-items: center; width: 1.6em; height: 1.6em; border-radius: 3px; font-weight: 700;
  margin-right: 6px; }}
.scroll {{ overflow-x: auto; background: var(--surface); border: 1px solid var(--line); border-radius: 6px; }}
table {{ border-collapse: collapse; font-variant-numeric: tabular-nums; }}
th, td {{ border: 1px solid var(--line); }}
thead th {{ font-weight: 400; padding: 6px 4px; vertical-align: bottom; }}
thead tr:first-child th {{ font-weight: 600; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.04em;
  color: var(--muted); text-align: left; padding: 6px 8px; }}
thead th span {{ display: block; font-family: var(--mono); font-size: 0.78rem; white-space: nowrap; }}
.ver {{ font-weight: 700; }}
.kern {{ color: var(--muted); }}
tbody th {{ text-align: left; font: 500 0.85rem var(--mono); padding: 4px 10px; white-space: nowrap; }}
tbody th, thead th:first-child {{ position: sticky; left: 0; background: var(--surface); z-index: 1; }}
td {{ text-align: center; font-weight: 700; min-width: 2.2em; height: 1.9em; }}
td.PASS, .key.PASS {{ background: var(--pass-bg); color: var(--pass); }}
td.FAIL, .key.FAIL {{ background: var(--fail-bg); color: var(--fail); }}
td.SKIP, .key.SKIP {{ background: var(--na-bg); color: var(--na); }}
td.none {{ background: var(--surface); }}
tr.sum td, tr.sum th {{ border-bottom: 2px solid var(--muted); }}
.g {{ border-left: 2px solid var(--muted); }}
[title]:hover {{ outline: 2px solid var(--fg); outline-offset: -2px; }}
.fails {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 34rem), 1fr)); gap: 16px; }}
.fails section {{ min-width: 0; }}
dl {{ margin: 0; display: grid; grid-template-columns: max-content minmax(0, 1fr); gap: 3px 12px; }}
dt {{ font: 500 0.82rem var(--mono); color: var(--fail); }}
dd {{ margin: 0; font-size: 0.85rem; overflow-wrap: anywhere; }}
</style>
<!-- /page -->
</head>
<body>
<!-- page -->
<main>
<header>
<h1>PLUMED + GROMACS regtests</h1>
<p class="meta">matrix.py, {date}, {machine}: {ncombo} combinations of GROMACS, PLUMED patches and PLUMED kernel,
{ntest} tests. {clean} combinations pass everything; {total} failures in all.</p>
</header>
<div class="legend"><span><span class="key PASS">✓</span>pass</span><span><span class="key FAIL">✗</span>fail</span>
<span><span class="key SKIP">–</span>not applicable to this combination</span>
<span>Columns: GROMACS version, the PLUMED branch whose patch was applied (vanilla: GROMACS without patches), and
the kernel when it is not of that branch. Hover a test or a cell for what it checks and the numbers.</span></div>
<div class="scroll">
<table>
<thead>
<tr><th></th>{groups}</tr>
<tr><th scope="col">test</th>{heads}</tr>
</thead>
<tbody>
{rows}
</tbody>
</table>
</div>
<div>
<h2>Failures</h2>
<div class="fails">
{detail}
</div>
</div>
</main>
<!-- /page -->
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--matrix", default=str(HERE / "matrix.txt"))
    ap.add_argument("--jobs", type=int, default=4, help="combinations run at the same time")
    ap.add_argument("--tests", default=".", help="regular expression selecting the tests")
    ap.add_argument("--only", default="", help="regular expression selecting the combinations")
    ap.add_argument("--report-only", action="store_true")
    a = ap.parse_args()
    import re
    combos, groups = read_matrix(a.matrix)
    selected = [c for c in combos if re.search(a.only, c[0])]
    if not a.report_only:
        with ThreadPoolExecutor(a.jobs) as pool:
            for label in pool.map(lambda c: run(c, a.tests), selected):
                print(f"done {label}", flush=True)
    report(combos, groups, history=not a.report_only and a.only == "" and a.tests == ".")


if __name__ == "__main__":
    main()
