# How the skill works

## Triggering

Claude sees only the skill's `name` and `description` until a task seems relevant. The description therefore lists the situations that should load it (creating a Flutter project, adding a screen, connecting an API, localization, reviewing a codebase, or mentioning GetX) rather than describing the architecture.

## Progressive loading

| Level | What loads | When |
|---|---|---|
| 1 | `name` + `description` | Always |
| 2 | `SKILL.md` (about 80 lines) | When the task matches |
| 3 | `references/*.md`, `assets/templates/*`, `scripts/*` | Only when a step needs them |

Keeping detail out of `SKILL.md` means a quick question about a Flutter widget does not pay the cost of the whole playbook.

## The workflow Claude follows

1. **Inspect first**: read `pubspec.yaml`, the `lib/` layout and any project instructions.
2. **Choose the situation**: new project, existing project that already follows the layout, or existing project with a different architecture. The last case stops for a question instead of a rewrite.
3. **Act with the matching reference**: create a project, add a screen, connect an endpoint, localize, or audit.
4. **Verify**: `dart format`, the auditor, `flutter analyze`, `flutter test`, then report what was and was not verified.

## Design decisions

- **Rules come with reasons.** "No `async onInit`" is paired with the fact that GetX does not await it. Reasons let Claude handle cases the rules do not list.
- **A script for the checkable rules.** Anything a regular expression can verify (route parity, key parity, forbidden calls) is in `audit_conventions.py`, so reviews are fast and repeatable and Claude spends its effort on judgment.
- **Templates over prose.** The network layer and shared widgets are real, tested code from the starter, not descriptions, so generated projects start from something that compiles.
- **Conservative by default.** No invented endpoints or JSON fields, no architecture changes without approval, and no broad refactors before findings are reported.

## Limits

- The auditor is heuristic. It can miss problems (for example a `print` hidden behind a helper) and can flag harmless code. It never edits files.
- Templates target GetX 4.x and the current Flutter stable at the time of writing.
- The skill covers architecture and conventions. It does not design your UI or define your backend contract.
