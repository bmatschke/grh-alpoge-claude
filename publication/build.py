#!/usr/bin/env python3
"""Build both reading editions of the RH and Dirichlet GRH manuscript."""
import argparse
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import quote, unquote, urlsplit
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MANUSCRIPT = ROOT / "manuscript" / "overview.md"
TEMPLATES = HERE / "templates"
REPOSITORY = "https://github.com/bmatschke/grh-alpoge-claude"


def git(*args):
    return subprocess.check_output(["git", "-C", ROOT, *args], text=True).strip()


def pandoc(source, source_format, target_format, *flags):
    result = subprocess.run(["pandoc", "--from", source_format, "--to", target_format, *flags],
                            input=source, text=True, capture_output=True, check=True)
    if result.stderr.strip():
        raise ValueError("Pandoc reported a conversion issue:\n" + result.stderr.strip())
    return result.stdout


def transform(nodes, revision):
    """Rewrite only parsed link nodes. Brackets inside an equation stay literal."""
    if isinstance(nodes, list):
        for child in nodes:
            transform(child, revision)
    elif isinstance(nodes, dict):
        kind, value = nodes.get("t"), nodes.get("c")
        if kind == "Link":
            target = value[2][0]
            url = urlsplit(target)
            if not url.scheme and not url.netloc and url.path:
                file = (MANUSCRIPT.parent / unquote(url.path)).resolve()
                if url.query or not file.is_relative_to(ROOT) or not file.is_file():
                    raise ValueError(f"Missing manuscript citation {target}")
                repository_path = file.relative_to(ROOT).as_posix()
                value[2][0] = f"{REPOSITORY}/blob/{revision}/{quote(repository_path)}"
                if url.fragment:
                    value[2][0] += "#" + url.fragment
        elif kind == "Math":
            value[1] = re.sub(r"\{\\rm\s+([^{}]+)\}", r"{\\mathrm{\1}}", value[1])
            value[1] = value[1].replace(r"\Sha", r"\operatorname{Sha}")
        for child in nodes.values():
            transform(child, revision)


def template(name, values):
    source = (TEMPLATES / name).read_text()
    return re.sub(r"@@([A-Z]+)@@", lambda match: values[match[1]], source)


def metadata(revision, label, timestamp):
    numbered = re.fullmatch(r"edition-([0-9]+(?:\.[0-9]+)*)", label)
    edition_url = f"{REPOSITORY}/releases/tag/{label}" if numbered else f"{REPOSITORY}/tree/{revision}"
    display_label = f"Edition {numbered[1]}" if numbered else label
    return {"EDITION": display_label, "DATE": datetime.fromtimestamp(timestamp, timezone.utc).date().isoformat(),
            "SHA": revision, "SHORT": revision[:12], "REPO": REPOSITORY, "EDITIONURL": edition_url}


def overview(work, values, overview_only):
    source = MANUSCRIPT.read_text()
    heading, subtitle, body = source.split("\n\n", 2)
    if not heading.startswith("# ") or subtitle.strip() != "*Overview*":
        raise ValueError("Expected the overview title and subtitle at the start of the manuscript")
    title = heading[2:].strip()
    ast = json.loads(pandoc(body, "markdown+tex_math_dollars", "json"))
    transform(ast["blocks"], values["SHA"])
    document = json.dumps(ast, ensure_ascii=False)
    latex = pandoc(document, "json", "latex", "--shift-heading-level-by=-1").replace("·", r"\textperiodcentered{}")
    html = pandoc(document, "json", "html5", "--mathml")
    tex_title = pandoc(title, "markdown", "latex").strip()
    tex_values = {**values, "TITLE": tex_title, "EDITION": pandoc(values["EDITION"], "markdown", "latex").strip(),
                  "BODY": latex}
    (work / "overview.tex").write_text(template("overview.tex", tex_values))
    values["TITLE"] = title
    toc = "\n".join(f'<li><a href="#{escape(block["c"][1][0])}">{escape(match.group(1))}</a></li>'
                    for block, match in zip(
                        (b for b in ast["blocks"] if b["t"] == "Header" and b["c"][0] == 2),
                        re.finditer(r"^## (.+)$", body, re.M), strict=True))
    meta = (f'{escape(values["EDITION"])} · {values["DATE"]} · '
            f'<a href="{REPOSITORY}/tree/{values["SHA"]}">Source {values["SHORT"]}</a>')
    backlink = (f'<a href="{REPOSITORY}/tree/{values["SHA"]}">Source repository</a>'
                if overview_only else '<a href="index.html">Manuscript</a>')
    (work / "overview.html").write_text(
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
        'content="width=device-width,initial-scale=1"><link rel="stylesheet" href="style.css">'
        f'<title>{escape(title)} — Overview</title></head><body><nav>{backlink} · '
        f'<a href="overview.pdf">Overview PDF</a></nav><article><header><h1>{escape(title)}</h1>'
        f'<p>Overview</p><p class="meta">{meta}</p></header>'
        f'<details><summary>Contents</summary><ul>{toc}</ul></details>{html}</article></body></html>\n')
    shutil.copyfile(TEMPLATES / "style.css", work / "style.css")


def typeset(work, stem, timestamp):
    env = {**os.environ, "SOURCE_DATE_EPOCH": str(timestamp), "FORCE_SOURCE_DATE": "1", "TZ": "UTC"}
    command = ["pdflatex", "-no-shell-escape", "-halt-on-error", "-file-line-error",
               "-interaction=batchmode", stem + ".tex"]
    for _ in range(4):
        result = subprocess.run(command, cwd=work, env=env, capture_output=True, text=True)
        log_path = work / (stem + ".log")
        log = log_path.read_text(errors="replace") if log_path.is_file() else ""
        if result.returncode:
            raise RuntimeError(f"Failed to compile {stem}.tex:\n" + (log or result.stdout or result.stderr)[-8000:])
        if "Rerun to get" not in log and "Rerun LaTeX" not in log and "rerun LaTeX" not in log:
            if re.search(r"There were undefined references|Reference .+ undefined on input line|Citation .+ undefined", log):
                raise RuntimeError(f"Unresolved LaTeX references in {stem}.tex")
            return
    raise RuntimeError(f"References did not settle in {stem}.tex")


def bundle(work, timestamp, values):
    guide = (f'{values["TITLE"]}\n{values["EDITION"]} · {values["DATE"]}\n'
             f'Source revision {values["SHA"]}\n\n'
             'The two .tex files are self-contained. With TeX Live installed, run pdflatex '
             'on overview.tex and full.tex until cross-references settle (normally two runs).\n'
             f'The editable chapters and publication builder are at {REPOSITORY}/tree/{values["SHA"]}.\n')
    files = {"README.txt": guide.encode()}
    for name in ["overview.tex", "full.tex"]:
        files[name] = (work / name).read_bytes()
    with zipfile.ZipFile(work / "proof-source.zip", "w") as archive:
        for name, data in sorted(files.items()):
            date = datetime.fromtimestamp(max(timestamp, 315532800), timezone.utc)
            item = zipfile.ZipInfo(name, date.timetuple()[:6])
            item.external_attr = 0o100644 << 16
            archive.writestr(item, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "build")
    parser.add_argument("--revision", help="Git commit of the checkout (default: HEAD)")
    parser.add_argument("--edition", default="Working edition", help="Version label shown in the PDFs")
    parser.add_argument("--overview-only", action="store_true", help="Build just the overview PDF, HTML and TeX")
    args = parser.parse_args()
    head = git("rev-parse", "HEAD")
    if args.revision and git("rev-parse", "--verify", args.revision + "^{commit}") != head:
        parser.error("the requested revision must match the current checkout")
    if not re.fullmatch(r"[\w .-]{1,80}", args.edition):
        parser.error("use a short edition label containing words, periods, spaces or hyphens")
    timestamp = int(git("show", "-s", "--format=%ct", head))
    values = metadata(head, args.edition, timestamp)
    args.output.mkdir(exist_ok=True, parents=True)
    with tempfile.TemporaryDirectory(dir=args.output) as tmp:
        work = Path(tmp).resolve()
        overview(work, values, args.overview_only)
        typeset(work, "overview", timestamp)
        names = ["overview.tex", "overview.pdf", "overview.html", "style.css"]
        if not args.overview_only:
            subprocess.run([sys.executable, HERE / "full" / "build.py", "--output", work,
                            "--revision", head, "--edition", values["EDITION"]], check=True, cwd=ROOT)
            typeset(work, "full", timestamp)
            bundle(work, timestamp, values)
            values["AUDIT"] = f'{REPOSITORY}/blob/{head}/publication/audit/completeness.md'
            (work / "index.html").write_text(template("index.html", {k: escape(v) for k,v in values.items()}))
            names += ["full.tex", "full.pdf", "proof-source.zip", "index.html"]
        for name in names:
            (work / name).replace(args.output / name)
    print(f"Built {', '.join(names)} in {args.output.resolve()}")


if __name__ == "__main__":
    main()
