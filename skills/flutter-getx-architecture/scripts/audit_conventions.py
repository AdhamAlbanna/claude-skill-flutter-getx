#!/usr/bin/env python3
"""Audit a Flutter GetX project against the flutter-getx-architecture conventions.

Usage: python3 audit_conventions.py <project-root>

Prints findings grouped by severity (ERROR, WARN) and exits with status 1 when
there is at least one ERROR. It reads files only; it never modifies them.
"""

import re
import sys
from pathlib import Path

findings = []  # (severity, rule, path, line, message)


def add(severity, rule, path, line, message):
    findings.append((severity, rule, path, line, message))


def read_lines(path):
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return []


def strip_comment(line):
    """Drop a trailing // comment (good enough for these heuristics)."""
    index = line.find("//")
    return line if index < 0 else line[:index]


def check_file_rules(root, lib):
    for path in sorted(lib.rglob("*.dart")):
        rel = path.relative_to(root)
        parts = rel.parts  # ('lib', ...)
        in_network = len(parts) > 1 and parts[1] == "Network"
        in_view = len(parts) > 1 and parts[1] == "view_controller"
        is_controller = path.name.endswith("_controller.dart")
        is_screen_ui = in_view and not is_controller and "items" not in parts

        for number, raw in enumerate(read_lines(path), 1):
            code = strip_comment(raw)
            stripped = raw.strip()

            if re.search(r"\bonInit\s*\(\s*\)\s*async", code):
                add("ERROR", "async-oninit", rel, number,
                    "onInit must not be async; call a separate Future method instead")

            if re.search(r"(?<![\w.])print\s*\(", code) or ".printError(" in code:
                add("ERROR", "no-print", rel, number,
                    "use debugPrint behind kDebugMode instead of print")

            # print_curl_command.dart only needs the http request type for logging.
            if "package:http/" in code and not in_network \
                    and path.name != "print_curl_command.dart":
                add("ERROR", "http-outside-network", rel, number,
                    "import http only inside lib/Network/ (use Api.makeApiRequest)")

            if in_view and re.search(r"\bsetState\s*\(", code):
                add("ERROR", "no-setstate", rel, number,
                    "no setState in screens; keep state in the controller")

            if is_screen_ui and "Api.makeApiRequest" in code:
                add("ERROR", "api-in-ui", rel, number,
                    "API calls belong in the controller, not the UI file")

            if is_screen_ui and re.search(r"\bGet\.put\s*\(", code):
                add("WARN", "put-in-build", rel, number,
                    "Get.put in a screen; use a binding in routes.dart when the route owns the controller")

            if re.match(r"//\s*(final|var|const|if|for|return|await|Get\.|[A-Za-z_][\w.]*\(.*\)\s*;|\}|\{)", stripped) \
                    and not stripped.startswith("///"):
                add("WARN", "commented-code", rel, number,
                    "looks like commented-out code; delete it")

            if is_screen_ui:
                if re.search(r"""\bText\(\s*(['"])(?!\1)[^'"]*\1\s*[,)]""", code):
                    add("WARN", "hardcoded-string", rel, number,
                        "hard-coded UI string; use a translation key with .tr")
                if re.search(r"""\b(?:hintText|labelText|title|text|tooltip)\s*:\s*(['"])[A-Za-z][^'"]*\1(?!\s*\.tr)""", code):
                    add("WARN", "hardcoded-string", rel, number,
                        "hard-coded UI string; use a translation key with .tr")

        if is_controller:
            text = "\n".join(read_lines(path))
            created = len(re.findall(r"TextEditingController\s*\(", text))
            disposed = len(re.findall(r"\.dispose\s*\(\s*\)", text))
            if created > disposed:
                add("WARN", "dispose", rel, 1,
                    f"{created} TextEditingController(s) created but only {disposed} disposed in onClose")


def check_screen_pairs(root, lib):
    view = lib / "view_controller"
    if not view.is_dir():
        return
    for folder in sorted(p for p in view.iterdir() if p.is_dir()):
        rel = folder.relative_to(root)
        ui = folder / f"{folder.name}.dart"
        controller = folder / f"{folder.name}_controller.dart"
        if not ui.exists():
            add("ERROR", "screen-ui-missing", rel, 1,
                f"expected {folder.name}/{folder.name}.dart (UI file)")
        for extra in folder.glob("*.dart"):
            if extra not in (ui, controller):
                add("WARN", "screen-extra-file", extra.relative_to(root), 1,
                    "a screen folder holds the UI file and the controller; "
                    "put screen-only widgets in items/")


def check_routes(root, lib):
    routes_file = lib / "constants" / "approutes.dart"
    pages_file = lib / "routes.dart"
    if not routes_file.exists() or not pages_file.exists():
        return
    consts = re.findall(r"static\s+const\s+String\s+(\w+)\s*=\s*[\"']([^\"']*)[\"']",
                        routes_file.read_text(encoding="utf-8"))
    pages = pages_file.read_text(encoding="utf-8")
    rel_consts = routes_file.relative_to(root)
    for name, value in consts:
        if value != f"/{name}":
            add("WARN", "route-string", rel_consts, 1,
                f'AppRoute.{name} is "{value}"; the string should be "/{name}"')
        if not re.search(rf"name:\s*AppRoute\.{re.escape(name)}\b", pages):
            add("ERROR", "route-unregistered", rel_consts, 1,
                f"AppRoute.{name} has no GetPage in routes.dart")
    for used in sorted(set(re.findall(r"name:\s*AppRoute\.(\w+)", pages))):
        if used not in {name for name, _ in consts}:
            add("ERROR", "route-unknown", pages_file.relative_to(root), 1,
                f"GetPage uses AppRoute.{used}, which is not declared")


def check_translations(root, lib):
    path = lib / "localization" / "mylocalization.dart"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    maps = {}
    for lang in ("ar", "en"):
        match = re.search(rf"[\"']{lang}[\"']\s*:\s*\{{(.*?)\n\s*\}}", text, re.S)
        if match:
            maps[lang] = set(re.findall(r"[\"']([\w ]+)[\"']\s*:", match.group(1)))
    if len(maps) == 2 and maps["ar"] != maps["en"]:
        rel = path.relative_to(root)
        for key in sorted(maps["ar"] - maps["en"]):
            add("ERROR", "translation-missing", rel, 1, f'"{key}" is in ar but not in en')
        for key in sorted(maps["en"] - maps["ar"]):
            add("ERROR", "translation-missing", rel, 1, f'"{key}" is in en but not in ar')


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    root = Path(sys.argv[1]).resolve()
    lib = root / "lib"
    if not (root / "pubspec.yaml").exists() or not lib.is_dir():
        print(f"{root} does not look like a Flutter project (no pubspec.yaml or lib/).")
        return 2

    check_file_rules(root, lib)
    check_screen_pairs(root, lib)
    check_routes(root, lib)
    check_translations(root, lib)

    errors = [f for f in findings if f[0] == "ERROR"]
    warns = [f for f in findings if f[0] == "WARN"]

    for label, items in (("ERROR", errors), ("WARN", warns)):
        if not items:
            continue
        print(f"\n{label} ({len(items)})")
        for _, rule, path, line, message in sorted(items, key=lambda f: (str(f[2]), f[3])):
            print(f"  {path}:{line}  [{rule}]  {message}")

    print(f"\n{len(errors)} error(s), {len(warns)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
