# Network layer

Two files own all server communication: `Network/api_links.dart` (URLs only) and `Network/api.dart` (`Api.makeApiRequest`). The full implementation is in `assets/templates/Network/api.dart`; copy it and adapt imports instead of rewriting it.

## Contract

```dart
final response = await Api.makeApiRequest(
  url: ApiLinks.login,
  method: 'POST',            // GET | POST | PUT | DELETE
  body: {'username': u},     // JSON body
  query: {'limit': '20'},    // optional query parameters
  files: {'avatar': file},   // optional multipart (PlatformFile)
  fields: {'name': 'Sam'},   // optional multipart fields
);
if (response['success'] == true) { ... }
```

Every response is a `Map<String, dynamic>` with `success`. On failure `Api` shows one error dialog and returns `{'success': false, 'message': ...}`. Controllers therefore never wrap requests in `try/catch`, never show a second dialog, and never import `http`.

## What `Api` is responsible for

connectivity check, auth header from `UserSession.token`, GET/POST/PUT/DELETE, JSON encoding and decoding (UTF-8), multipart uploads, a 30 s timeout, the loading dialog (always closed in `finally`), a single translated error dialog, and a consistent failure map. Backends that do not send `success` get it derived from the HTTP status.

## Adding an endpoint

1. `api_links.dart`: `static const String items = "$server/items";`
2. `model/item.dart`: typed fields, `required` constructor, `fromJson` with safe defaults. Match the backend's real JSON keys; do not guess them.
3. Controller method:

```dart
Future<void> loadItems() async {
  final response = await Api.makeApiRequest(url: ApiLinks.items, method: 'GET');
  if (response['success'] == true) {
    items = (response['data'] as List<dynamic>)
        .map((json) => Item.fromJson(json))
        .toList();
    update();
  }
}
```

4. Validate input in the controller before sending (`formstate.currentState!.validate()` or an alert on empty required fields).
5. Add a test for `Item.fromJson` (full payload, empty payload).

## Session

`UserSession.init()` runs once inside `initialServices()`. After that `UserSession.token`, `.userId`, `.name` are synchronous. Save after login with `await UserSession.save({...})`, clear on logout with `UserSession.clear()`. The default header sends the raw token; change `Authorization` formatting (for example `Bearer $token`) in one place inside `api.dart` if the backend requires it.

## Pitfalls that have bitten before

1. Loading dialog stays on screen after a failed request -> close it in `finally`.
2. `files.forEach((k, f) async {...})` does not wait for uploads -> use `for ... in files.entries` with `await`.
3. Manually setting `Content-Type: multipart/form-data` breaks the boundary -> let `http` set it.
4. Returning `{'error': ...}` while controllers check `success == false` -> always return `success: false`.
5. `Get.back()` after the dialog is already gone pops a screen -> check `Get.isDialogOpen`.
6. Logging cURL with headers leaks tokens -> debug-only and redact `Authorization` (`printCurlCommand` does).
7. Inverted `validInput` conditions -> test both valid and invalid values.
