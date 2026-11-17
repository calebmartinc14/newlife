"""Validate the static website with Python's standard library and Node.js."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import os
import re
import shutil
import subprocess
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1] / "dist"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = []
        self.references = []
        self.inline_scripts = []
        self.errors = []
        self.language = ""
        self.title = ""
        self.has_description = False
        self.has_viewport = False
        self._in_title = False
        self._script = None

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        line = self.getpos()[0]
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "html":
            self.language = attrs.get("lang", "")
        if tag == "title":
            self._in_title = True
        if tag == "meta" and attrs.get("content", "").strip():
            self.has_description |= attrs.get("name") == "description"
            self.has_viewport |= attrs.get("name") == "viewport"
        if tag == "img" and "alt" not in attrs:
            self.errors.append(f"line {line}: image is missing an alt attribute")
        if tag == "img" and not all(
            attrs.get(name, "").isdigit() and int(attrs[name]) > 0
            for name in ("width", "height")
        ):
            self.errors.append(f"line {line}: image needs positive width and height attributes")
        for name in ("href", "src"):
            if attrs.get(name):
                self.references.append((line, attrs[name]))
        if attrs.get("srcset"):
            self.references.extend(
                (line, candidate.strip().split()[0])
                for candidate in attrs["srcset"].split(",") if candidate.strip()
            )
        for name in ("aria-controls", "aria-labelledby", "aria-describedby"):
            self.references.extend((line, f"#{identifier}") for identifier in attrs.get(name, "").split())
        if tag == "script":
            script_type = attrs.get("type", "").lower()
            if "src" not in attrs and script_type in (
                "", "text/javascript", "application/javascript", "module"
            ):
                self._script = (line, script_type == "module", [])

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "script" and self._script is not None:
            line, module, chunks = self._script
            self.inline_scripts.append((line, module, "".join(chunks)))
            self._script = None

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._script is not None:
            self._script[2].append(data)


def exact_file(path):
    """Check filename case even on Windows, since Pages uses Linux."""
    if not path.is_file():
        return False
    relative = path.relative_to(ROOT)
    current = ROOT
    for part in relative.parts:
        if part not in {child.name for child in current.iterdir()}:
            return False
        current /= part
    return True


def main():
    errors = []
    pages = {}
    if not (ROOT / "index.html").is_file():
        print("FAIL: dist/index.html is missing", file=sys.stderr)
        return 1

    for path in sorted(ROOT.rglob("*.html")):
        page = Page(path)
        page.feed(path.read_text(encoding="utf-8"))
        page.close()
        pages[path] = page
        errors.extend(f"{path.relative_to(ROOT)}: {error}" for error in page.errors)
        for label, valid in (
            ("document language", page.language.strip()),
            ("page title", page.title.strip()),
            ("meta description", page.has_description),
            ("viewport metadata", page.has_viewport),
        ):
            if not valid:
                errors.append(f"{path.relative_to(ROOT)}: missing {label}")
        for identifier, count in Counter(page.ids).items():
            if count > 1:
                errors.append(f"{path.relative_to(ROOT)}: duplicate ID {identifier!r}")

    references = 0
    for path, page in pages.items():
        for line, reference in page.references:
            url = urlsplit(reference)
            if url.scheme or url.netloc:
                continue
            references += 1
            prefix = f"{path.relative_to(ROOT)}:{line}"
            local_path = unquote(url.path)
            if local_path.startswith("/"):
                errors.append(f"{prefix}: use a relative URL for Pages: {reference}")
                continue
            target = Path(os.path.abspath(path.parent / local_path)) if local_path else path
            if not target.is_relative_to(ROOT):
                errors.append(f"{prefix}: reference escapes dist/: {reference}")
                continue
            if target.is_dir():
                target /= "index.html"
            if not exact_file(target):
                errors.append(f"{prefix}: missing file or incorrect casing: {reference}")
                continue
            fragment = unquote(url.fragment)
            if fragment and target in pages and fragment not in pages[target].ids:
                errors.append(f"{prefix}: missing fragment target: {reference}")

    node = shutil.which("node")
    presentation = ROOT / "presentation.js"
    if presentation.is_file():
        for section in re.findall(r"\bsection:\s*['\"]([^'\"]+)", presentation.read_text(encoding="utf-8")):
            if section not in pages[ROOT / "index.html"].ids:
                errors.append(f"presentation.js: missing destination section {section!r}")
    scripts = 0
    if node is None:
        errors.append("Node.js is required for JavaScript syntax checks")
    else:
        sources = [
            (str(path.relative_to(ROOT)), path.suffix == ".mjs", path.read_text(encoding="utf-8"))
            for path in sorted(ROOT.rglob("*"))
            if path.suffix in (".js", ".mjs")
        ]
        for path, page in pages.items():
            sources.extend(
                (f"{path.relative_to(ROOT)}:{line} (inline)", module, source)
                for line, module, source in page.inline_scripts
            )
        for label, module, source in sources:
            result = subprocess.run(
                [node, "--check", f"--input-type={'module' if module else 'commonjs'}"],
                input=source, capture_output=True, text=True, encoding="utf-8", check=False,
            )
            scripts += 1
            if result.returncode:
                errors.append(f"{label}: JavaScript syntax error\n{result.stderr.strip()}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {len(pages)} HTML page(s), {references} local references, {scripts} JavaScript source(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
