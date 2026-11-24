# Claude Skill: Flutter GetX Architecture

A [Claude](https://claude.com) skill that teaches Claude to build and review Flutter apps with a strict, scalable **GetX** architecture: one UI file plus one controller file per screen, a single centralized network layer, a persisted user session, route middleware, and Arabic / English localization with RTL.

It is the knowledge behind [flutter-getx-starter](https://github.com/AdhamAlbanna/flutter-getx-starter), packaged so Claude applies the same conventions in any Flutter project.

## What it does

When you ask Claude to create a Flutter project, add a screen, connect a screen to an API, add translations or RTL, or review a codebase, the skill gives Claude:

- the folder structure, naming rules and the reasons behind them,
- step-by-step workflows (new project, new screen, new endpoint, localization),
- ready-to-adapt code templates taken from the starter,
- a **convention auditor** that checks a project in seconds.

It does **not** force this architecture on projects that use something else. If the project uses Bloc, Riverpod or Provider, Claude is told to report the conflict and ask first.

## Install

**Claude Code (personal skill):**

```bash
git clone https://github.com/AdhamAlbanna/claude-skill-flutter-getx.git
mkdir -p ~/.claude/skills
cp -R claude-skill-flutter-getx/skills/flutter-getx-architecture ~/.claude/skills/
```

**Claude Code (one project):** copy the same folder into `<your-project>/.claude/skills/`.

Restart Claude Code, then try one of the prompts below. Claude loads the skill automatically when the task matches.

## Example prompts

- "Create a new Flutter app called `shop` with GetX, Arabic and English."
- "Add a Profile screen that loads `GET /users/me` and shows the name and email."
- "Review `lib/` against the GetX conventions and list the violations before changing anything."
- "Move every hard-coded string in the checkout screens into translations."

## The auditor

Run it yourself, no Claude needed (Python 3):

```bash
python3 skills/flutter-getx-architecture/scripts/audit_conventions.py path/to/flutter_project
```

It checks `async onInit`, `print`, `http` outside `Network/`, `setState` in screens, API calls in UI files, route constants vs `GetPage`s, Arabic/English key parity, undisposed controllers, screens missing a UI file, commented-out code and hard-coded UI strings. It prints errors first and exits with status 1 when it finds any.

## Contents

```text
skills/flutter-getx-architecture/
  SKILL.md                      entry point: when to use it and the core workflow
  references/
    conventions.md              structure, naming, state, UI and code rules
    network-layer.md            the Api contract, adding endpoints, known pitfalls
    screen-workflow.md          checklist for adding a screen
  scripts/audit_conventions.py  read-only convention checker
  assets/templates/             code templates from the starter ({{package}} placeholder)
```

## Notes

- The templates target current Flutter and GetX 4.x. Recent Flutter versions deprecate `package:flutter/material.dart`, but GetX still depends on it, so the skill keeps the app on that import (see the skill for details).
- Templates use `{{package}}` for the app's package name; replace it when copying.

## Contributing

Issues and pull requests are welcome. Keep `SKILL.md` short, explain the reason behind each rule, and put detail in `references/`.

## License

[MIT](LICENSE) © Adham Albanna
