# Conventions

## Contents
1. Folder structure
2. Where things go
3. Naming
4. State, navigation and bindings
5. UI rules
6. Code habits

## 1. Folder structure

```text
lib/
  main.dart                      init services, run GetMaterialApp
  routes.dart                    the single List<GetPage>
  constants/
    appcolor.dart                AppColor (static const)
    approutes.dart               AppRoute (static const)
  localization/
    mylocalization.dart          Translations: ar + en
  model/                         plain data classes with fromJson
  Network/
    api_links.dart               endpoint constants only
    api.dart                     Api.makeApiRequest, the only HTTP code
  helper/
    functions/                   validinput, user_info, showdialog, checkinternet,
                                 print_curl_command, savedata
    middleware/                  GetMiddleware route guards
    services/                    GetxService + initialServices()
    widgets/<group>/             shared Custom* widgets (buttons/, textfields/, appbar/)
  view_controller/
    <screen>/
      <screen>.dart              UI only
      <screen>_controller.dart   logic only
      items/<thing>_item.dart    widgets used by this screen only
assets/ fonts/ images/
test/
```

A screen with no logic may omit the controller. Imports are always absolute: `package:<app>/...`.

## 2. Where things go

| Thing | Location |
|---|---|
| New screen | `view_controller/<screen>/` |
| Widget used by one screen | that screen's `items/` |
| Widget used by two or more screens | `helper/widgets/<group>/` |
| Colors, route names, app constants | `constants/` |
| Endpoint URL | `Network/api_links.dart` |
| HTTP code | `Network/api.dart` only |
| Server data model | `model/` |
| Validation, dialogs, storage, session helpers | `helper/functions/` |
| Long-lived singleton | `helper/services/` |
| Route guard | `helper/middleware/` |
| Translations | `localization/mylocalization.dart` |

Never duplicate these: one route list, one set of endpoint constants, one HTTP implementation, one color file, one translation file.

## 3. Naming

| Item | Rule | Example |
|---|---|---|
| Screen folder/file | snake_case, same name; numbered for multi-step flows | `login/login.dart`, `checkout_1/` |
| Controller file/class | `<screen>_controller.dart` / `<Screen>Controller` (no `Imp`) | `LoginController` |
| Screen class | PascalCase noun, no `Screen` suffix | `Login` |
| Screen-only widget | ends in `Item` | `ProductItem` |
| Shared widget | `Custom` prefix | `CustomButton` |
| Constants class | `App` prefix, `static const` | `AppColor.primaryColor` |
| Route | `AppRoute.camelCase`; the string equals the name | `AppRoute.homeUser` = `"/homeUser"` |
| Model | singular PascalCase + `fromJson` | `Product` |
| Method | camelCase, verb first | `loadItems`, `goToNextPage` |
| Form key | `formstate` | `GlobalKey<FormState> formstate` |
| Translation key | English snake_case | `login_account` |

Check spelling before creating references: a typo in a class or route name spreads everywhere.

## 4. State, navigation and bindings

- **State:** controller extends `GetxController`, mutates plain fields, calls `update()`; UI reads it through `GetBuilder<XController>`. Use `.obs` plus `Obx` only for a small reactive value (selected index, password visibility).
- **Creation:** each routed screen gets `binding: BindingsBuilder(() => Get.lazyPut(() => XController()))` in its `GetPage`. Only a screen without its own route (a tab child) uses `Get.put(XController())` at the top of `build`.
- **Lifecycle:** create `TextEditingController`s in `onInit` (never `async`); start loading from a separate `Future` method; dispose in `onClose`.
- **Services:** `class MyServices extends GetxService` wraps `SharedPreferences`; `initialServices()` registers it with `Get.putAsync` then `await UserSession.init()`; awaited in `main()` before `runApp`.
- **Navigation:** named routes only. `Get.toNamed(AppRoute.x)`, `Get.offAllNamed(...)` to reset the stack, `Get.back()` to pop. Do not mix `Navigator.pop` with `Get.back()`.
- **Arguments:** `Get.toNamed(route, arguments: {...})` with a `Map`; read `Get.arguments` in the destination controller's `onInit`. Return values with `Get.back(result: value)` and read them via `Get.toNamed(...)!.then(...)`, handling `null`.
- **Guards:** `GetMiddleware` with `priority` and `redirect()` reading `UserSession`; attach to the `GetPage`.
- **Persistence:** `UserSession` (`helper/functions/user_info.dart`) is loaded once at startup and read synchronously (`UserSession.token`). Small key/value maps for multi-step flows go through `saveDataWithKey` / `getDataWithKey` / `deleteDataWithKey`.

## 5. UI rules

- Screens are `StatelessWidget` with `const` constructors and `super.key`; no `setState`.
- Baseline layout: `Scaffold` -> optional app bar -> `Form(key: controller.formstate)` -> padded `SingleChildScrollView` -> `Column(crossAxisAlignment: start)`, 24 horizontal padding, `SizedBox` spacing. Treat it as a default, not a reason to flatten a custom design.
- Use `CustomButton`, `CustomTextField`, `CustomAppBar` rather than restyling Material widgets in each screen. Shared widgets take `final` fields and `required` params and expose `onPressed`, `valid`, `hint`, `mycontroller`.
- Item widgets receive data and callbacks through constructor params and never touch controllers.
- Screens call controller methods (`onPressed: () => controller.login()`); no API calls or workflow decisions. A static `Get.toNamed` link is acceptable.
- Colors from `AppColor`, font via `ThemeData(fontFamily: ...)`.
- Validation: shared `validInput(value, min, max, type)` as the `TextFormField` validator; the controller triggers it with `formstate.currentState!.validate()`.
- Prefer `start`/`end` over `left`/`right`.
- Dismiss the keyboard globally with a `GestureDetector` around `GetMaterialApp`.

## 6. Code habits

- Comments are short and only for non-obvious intent. No commented-out code.
- Helpers have explicit return types.
- Models: `final` fields, `required` named constructor, `factory X.fromJson` with safe defaults (`?? ''`).
- Lints: `flutter_lints` plus `avoid_print` and `prefer_const_constructors`.
- Run `dart format`, `flutter analyze` and `flutter test` before finishing.
