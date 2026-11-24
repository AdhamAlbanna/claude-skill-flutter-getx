# Contributing

Thanks for helping improve the skill.

## Principles

- **Keep `SKILL.md` short.** Put detail in `references/` and tell Claude when to read it.
- **Explain why.** Each rule should carry its reason, so Claude can apply judgment instead of rote checks.
- **Prefer code over prose** for anything repeatable: templates in `assets/templates/`, checks in the auditor.
- **Stay conservative.** The skill must not change an existing architecture without asking.

## Changing the auditor

1. Add or adjust a rule in `skills/flutter-getx-architecture/scripts/audit_conventions.py`.
2. Plant a violation in `tests/fixtures/broken` and make sure `tests/fixtures/clean` stays clean.
3. Add the rule name to `test_broken_project_reports_every_planted_violation` in `tests/test_audit.py`.
4. Run the tests:

```bash
python3 -m unittest discover -s tests -v
```

## Changing templates

Templates come from [flutter-getx-starter](https://github.com/AdhamAlbanna/flutter-getx-starter) with the package name replaced by `{{package}}`. Change the starter first (it has analysis and tests), then sync the template.

## Pull requests

Describe what changed and why, and include test output for auditor changes.
