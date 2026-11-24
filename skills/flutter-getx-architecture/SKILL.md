---
name: flutter-getx-architecture
description: Build and extend Flutter apps with a strict, scalable GetX architecture - one UI file plus one controller file per screen, a single centralized network layer (Api.makeApiRequest), UserSession, route middleware, and Arabic/English localization with RTL. Use this skill whenever the user creates a Flutter project, adds a screen, connects a screen to an API, adds translations or RTL support, sets up GetX routing/bindings/controllers, reviews or audits a Flutter codebase for structure, or mentions GetX, "view_controller", "makeApiRequest", or "UI/logic separation" - even if they do not name this architecture explicitly.
---

# Flutter GetX architecture

A small set of conventions that keeps a GetX app predictable as it grows. The reference implementation is the open-source starter at https://github.com/AdhamAlbanna/flutter-getx-starter, and everything under `assets/templates/` is taken from it.

## Why these conventions exist

Most GetX codebases rot the same way: logic leaks into widgets, HTTP calls get copied into controllers, and nobody knows where a route or a string lives. These rules each remove one source of that rot:

- **One UI file + one controller file per screen** - a reviewer can see presentation and behaviour separately, and controllers can be tested without widgets.
- **One network layer** - error handling, auth headers, timeouts and loading dialogs exist once, so every request behaves the same and controllers shrink to "call, check `success`, update".
- **One route list, one translation file, one color file** - there is exactly one place to look and one place to edit.
- **Everything user-visible is a translation key** - adding a language later is a data change, not a refactor.

Explain the reason when you push back on a deviation; the rules are tools, not taste.

## First: inspect before you change anything

1. Read `pubspec.yaml`, `lib/` layout, and any `CLAUDE.md`/`AGENTS.md`.
2. Decide which situation you are in:
   - **New project** -> follow "Create a project".
   - **Existing GetX project that already follows (most of) this layout** -> extend it in place with the matching workflow below.
   - **Existing project with a different architecture or state management** (Bloc, Riverpod, Provider, ...) -> do **not** convert it. Tell the user about the conflict and ask. Apply these conventions only to new code if they agree.
3. Match the project's package name, GetX version and existing naming. Never invent backend endpoints, JSON fields or design details; ask when they are missing.

## Create a project

1. Prefer the starter: `git clone https://github.com/AdhamAlbanna/flutter-getx-starter <name>`, then rename the package (`pubspec.yaml` `name:` and every `package:flutter_getx_starter/` import), set bundle/application IDs, and remove the demo `Login`/`Home` content you do not need. If cloning is not possible, run `flutter create <name>` and copy from `assets/templates/` (replace `{{package}}` with the package name).
2. Create the folder structure from `references/conventions.md`.
3. Keep only the dependencies the project uses: `get`, `shared_preferences`, `http`, `http_parser`, `file_picker` are the baseline (the last two are for multipart uploads).
4. Set the primary color in `constants/appcolor.dart`, point `Network/api_links.dart` at the real backend, add the font if any.
5. Run `flutter analyze` and `flutter test`, then run the app once.

## Add a screen

Follow `references/screen-workflow.md`. In short: folder under `view_controller/<name>/` with `<name>.dart` (UI only) and `<name>_controller.dart` (logic only), an `AppRoute` constant, a `GetPage` with a `BindingsBuilder`, translations in both languages, shared `Custom*` widgets instead of restyled Material widgets.

## Connect a screen to an API

Follow `references/network-layer.md`. In short: endpoint constant in `api_links.dart`, call `Api.makeApiRequest` from the controller, check `response['success'] == true`, parse with a model `fromJson`. No `http` import and no request-level `try/catch` in controllers, because `Api` already handles and displays failures.

## Localize / RTL

Every user-visible string - labels, validation messages, dialog titles and buttons, empty states - is a snake_case English key present in **both** `ar` and `en` maps of `localization/mylocalization.dart`, rendered with `'key'.tr` (or `.trParams`). Direction follows the active language in `main.dart`. Flag domain-specific terms whose Arabic wording you are unsure about instead of guessing.

## Review or audit a project

Run the bundled checker first, it is faster and more reliable than reading every file:

```bash
python3 <skill-dir>/scripts/audit_conventions.py <project-root>
```

It reports (errors first): `async onInit`, `print`, `http` outside `Network/`, `setState` in screens, route constant/`GetPage` mismatches, translation key mismatches between `ar` and `en`, undisposed controllers, screens missing a UI file, likely commented-out code and hard-coded UI strings. Report findings grouped by severity and **ask before making broad changes**; then fix approved items one at a time without changing behaviour. Finish with `flutter analyze` and `flutter test`.

## Hard rules (and the reason behind each)

- No API calls or business decisions in UI files - they cannot be tested or reused there.
- No `async` on `onInit` - GetX does not await it; start loading from a separate `Future` method.
- No `setState` in screens - state lives in controllers (`update()` + `GetBuilder`, or a small `Rx` value with `Obx`).
- Do not wrap a whole screen in `Obx` - rebuild only the subtree that changes.
- No `print` - use `debugPrint` behind `kDebugMode`; never log tokens (`printCurlCommand` redacts `Authorization`).
- Dismiss loading dialogs in `finally`, and check `Get.isDialogOpen` before `Get.back()`, or a failed request leaves a spinner or closes the wrong screen.
- Multipart uploads: use a plain `for` loop with `await` (not `forEach`), and let `http` set the multipart `Content-Type` boundary.
- Do not `Get.put` a controller in `build` when the route already has a binding.
- Dispose what a controller owns (`TextEditingController`, focus nodes) in `onClose`.
- Add tests for `validInput` (valid **and** invalid cases) and for each model's `fromJson`.

## Known framework note

Recent Flutter releases deprecate `package:flutter/material.dart` in favour of `package:material_ui`. GetX 4.x still builds on the old import, and mixing the two packages breaks `Theme` lookups at runtime, so keep the whole app on `package:flutter/material.dart` and silence `deprecated_member_use` in `analysis_options.yaml` until GetX migrates.

## After coding

Format, run `flutter analyze` and `flutter test`, and report: files changed, behaviour implemented, commands run and results, and anything not verified on a simulator or device.
