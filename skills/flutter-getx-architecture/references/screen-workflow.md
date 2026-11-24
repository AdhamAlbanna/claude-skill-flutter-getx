# Add a screen (checklist)

Replace `profile` / `Profile` with the real name. Templates to copy from: `assets/templates/view_controller/`.

1. **Folder:** `lib/view_controller/profile/` with `profile.dart` and `profile_controller.dart`; widgets used only here go in `items/<thing>_item.dart`.
2. **Route constant:** in `constants/approutes.dart`: `static const String profile = "/profile";` (string equals the name).
3. **Route entry:** in `routes.dart`:
   ```dart
   GetPage(
     name: AppRoute.profile,
     page: () => const Profile(),
     binding: BindingsBuilder(() => Get.lazyPut(() => ProfileController())),
   ),
   ```
   Add `middlewares: [MyMiddleWare()]` when the route needs a guard. No binding for a screen without a controller.
4. **Controller:**
   ```dart
   class ProfileController extends GetxController {
     @override
     void onInit() {
       // create TextEditingControllers here
       loadProfile();            // separate Future method; onInit is never async
       super.onInit();
     }

     @override
     void onClose() {
       // dispose what this controller owns
       super.onClose();
     }
   }
   ```
5. **UI:** `StatelessWidget` -> `GetBuilder<ProfileController>(builder: (controller) => Scaffold(...))`. Use `CustomAppBar`, `CustomTextField`, `CustomButton`. Call `controller.xxx()` for every action. Colors from `AppColor`. Wrap only the small reactive part in `Obx`.
6. **Translations:** add every visible string to both `ar` and `en`, then use `'key'.tr`.
7. **API:** follow `network-layer.md` if the screen loads or submits data.
8. **Navigate to it:** `Get.toNamed(AppRoute.profile, arguments: {...})`; read `Get.arguments` in the controller's `onInit`.
9. **Tests:** model `fromJson`, validators, and any pure logic the controller exposes.
10. **Verify:** `dart format lib test`, `python3 scripts/audit_conventions.py .`, `flutter analyze`, `flutter test`, then open the screen in the app.

If the screen class name collides with a model (a `Profile` screen and a `Profile` model), rename the model (`UserProfile`) rather than adding a `Screen` suffix to the screen; if the collision cannot be avoided, a `Screen` suffix is an acceptable exception, so say so in the summary.

Do not invent behaviour that was not specified; ask for missing requirements instead.
