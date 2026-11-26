"""Assemble the detailed RH and Dirichlet GRH edition as a standalone TeX file."""

import argparse
from datetime import datetime, timezone
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
REPOSITORY = "https://github.com/bmatschke/grh-alpoge-claude"
MAIN = "manuscript/overview.md"


def latex(value):
    escapes = {"\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "&": r"\&",
               "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "^": r"\textasciicircum{}",
               "~": r"\textasciitilde{}"}
    return "".join(escapes.get(ch, ch) for ch in value)


def pandoc(data, source_format, output_format):
    return subprocess.run(
        ["pandoc", "--from", source_format, "--to", output_format, "--wrap=preserve"],
        input=data, text=True, check=True, stdout=subprocess.PIPE,
    ).stdout


def nodes(element):
    if isinstance(element, list):
        for child in element:
            yield from nodes(child)
    if isinstance(element, dict):
        yield element
        yield from nodes(element.get("c"))


def source_anchor(path):
    return "ms-" + re.sub(r"[^a-z0-9]+", "-", path.casefold()).strip("-")


def latex_target(identifier):
    return r"\hypertarget{" + identifier + r"}{}\phantomsection\label{" + identifier + "}"


def git_url(revision, path, fragment=""):
    return (f"{REPOSITORY}/blob/{revision}/{quote(path, safe='/')}"
            + ("#" + quote(fragment, safe="-_") if fragment else ""))


def read_markdown(name):
    raw = (ROOT / name).read_text()
    document = json.loads(pandoc(raw, "markdown+tex_math_dollars", "json"))
    if name == MAIN:
        blocks = document["blocks"]
        # The shared front matter has its own title and date in this edition.
        start = next(i for i, b in enumerate(blocks) if b["t"] == "Para"
                     and any(n["t"] == "Str" and n["c"] == "Dirichlet" for n in nodes(b))
                     and any(n["t"] == "Math" for n in nodes(b)))
        document["blocks"] = blocks[start:]
    return document


def prepare_headers(name, document):
    mapping = {}
    anchor = source_anchor(name)
    for node in nodes(document["blocks"]):
        if node["t"] == "Span":
            attr, body = node["c"]
            if not body and re.fullmatch(r"claim:[A-Z0-9]+", attr[0]):
                node.update(t="RawInline", c=["latex", latex_target(attr[0])])
        if node["t"] != "Header":
            continue
        level, attr, _ = node["c"]
        original = attr[0]
        destination = anchor + "-" + original
        mapping[original] = destination
        attr[0] = destination
        if name == MAIN:
            node["c"][0] = max(1, level - 1)
    return mapping


def change_links(name, document, revision, headings, included):
    for node in nodes(document["blocks"]):
        if node["t"] != "Link":
            continue
        target = node["c"][2]
        address = urlsplit(target[0])
        if address.netloc or address.scheme:
            continue
        local = unquote(address.path)
        dest = os.path.normpath(os.path.join(os.path.dirname(name), local)) if local else name
        fragment = unquote(address.fragment)
        if dest in included and not fragment:
            target[0] = "#" + source_anchor(dest)
        elif dest in headings and fragment in headings[dest]:
            target[0] = "#" + headings[dest][fragment]
        else:
            target[0] = git_url(revision, dest, fragment)


def source_link(revision, name, title):
    return r"\href{" + git_url(revision, name) + "}{" + latex(title) + "}"


def render_reading(template, original):
    """Insert inclusive ranges of the native proof at the marked lines of a reading."""
    lines = original.splitlines()
    def boundary(marker):
        if lines.count(marker) != 1:
            raise ValueError(f"{template.name}: expected one source line matching {marker!r}")
        return lines.index(marker)

    result = []
    for line in template.read_text().splitlines():
        if not line.startswith("% excerpt: "):
            result.append(line)
            continue
        first, last = line.removeprefix("% excerpt: ").split(" || ")
        start = 0 if first == "BOF" else boundary(first)
        stop = len(lines) if last == "EOF" else boundary(last) + 1
        if start >= stop:
            raise ValueError(f"{template.name}: empty or reversed excerpt {line!r}")
        result.extend(lines[start:stop])
    return "\n".join(result) + "\n"


def native_section(name, revision):
    path = ROOT / name
    content = path.read_text()
    reading = HERE / "readings" / (path.parent.name + ".tex")
    if reading.is_file():
        content = render_reading(reading, content)
    if re.search(r"\\(?:input|include|includegraphics)\s*\{", content):
        raise ValueError(f"{name} requires an external TeX input")
    if not re.search(r"\\section\{", content):
        raise ValueError(f"{name} does not begin a mathematical section")
    # Technical source identifiers and literal paths may share a text line.
    # Break them at existing component boundaries when typesetting the book.
    def break_identifier(match):
        identifier = match.group(1)
        if len(identifier) < 16:
            return match.group(0)
        if re.fullmatch(r"[0-9a-f]{40,64}", identifier):
            parts = [identifier[i:i + 8] for i in range(0, len(identifier), 8)]
        else:
            parts = re.split(r"(?<=[./])|(?<=[a-z])(?=[A-Z])", identifier)
        return r"\texttt{" + r"\allowbreak{}".join(parts) + "}"

    content = re.sub(r"\\texttt\{([A-Za-z0-9._/\\-]+)\}", break_identifier, content)
    directory = path.parent
    links = [source_link(revision, name, "Source of this derivation")]
    if reading.is_file():
        links.append(source_link(revision, reading.relative_to(ROOT).as_posix(), "Reading edition"))
    for filename, title in (("source_locators.txt", "Formal sources by claim"),
                            ("provenance.json", "Claim provenance"),
                            ("claims.json", "Proof records and source ranges"),
                            ("published_inputs.json", "Published inputs"),
                            ("classical_inputs.json", "Classical inputs")):
        candidate = directory / filename
        if candidate.is_file():
            links.append(source_link(revision, candidate.relative_to(ROOT).as_posix(), title))
    return content + "\n\\par\\smallskip {\\small " + r" \textperiodcentered{} ".join(links) + "}\\par\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--edition", default="Detailed edition")
    parser.add_argument("--revision", help="Public source commit; defaults to HEAD")
    args = parser.parse_args()
    revision = args.revision or subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    if not re.fullmatch(r"[0-9a-fA-F]{40}", revision):
        parser.error("--revision must be a full 40-digit commit identifier")
    subprocess.run([sys.executable, ROOT / "research/register/verify_claim_records.py"], check=True)
    groups = json.loads((HERE / "contents.json").read_text())
    names = [name for group in groups for name in group["sources"]]
    if len(names) != len(set(names)):
        raise ValueError("A section appears twice in contents.json")
    documents = {n: read_markdown(n) for n in names if n.endswith(".md")}
    headings = {n: prepare_headers(n, d) for n, d in documents.items()}
    preamble = (HERE / "preamble.tex").read_text()
    preamble = preamble.replace("@EDITION@", latex(args.edition))
    preamble = preamble.replace("@REVISION@", revision)
    timestamp = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", "-s", "--format=%ct", revision], text=True).strip()
    date = datetime.fromtimestamp(int(timestamp), timezone.utc).date().isoformat()
    preamble = preamble.replace("@DATE@", date)
    pieces = [preamble]
    for group in groups:
        pieces.append(r"\chapter{" + latex(group["title"]) + "}\n" + latex(group["guide"]) + "\n")
        for name in group["sources"]:
            pieces.append("\n% Manuscript source: " + name + "\n")
            anchor = source_anchor(name)
            pieces.append(r"\Needspace{5\baselineskip}" + latex_target(anchor) + "\n")
            if name in documents:
                change_links(name, documents[name], revision, headings, set(names))
                body = pandoc(json.dumps(documents[name]), "json", "latex")
                pieces.append(body)
            else:
                pieces.append(native_section(name, revision))
    pieces.append(r"\end{document}" + "\n")
    args.output.mkdir(exist_ok=True, parents=True)
    result = args.output / "full.tex"
    result.write_text("\n".join(pieces))
    print(f"Detailed edition assembled from {len(names)} sources in {len(groups)} chapters: {result}")


if __name__ == "__main__":
    main()
