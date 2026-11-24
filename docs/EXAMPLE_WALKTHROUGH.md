# Example walk-through: adding a Profile screen

Request: *"Add a Profile screen that loads `GET /users/{id}` and shows the name and email."*

This is the sequence the skill's workflow produces. It was verified on a copy of [flutter-getx-starter](https://github.com/AdhamAlbanna/flutter-getx-starter): the auditor reported 0 errors and 0 warnings, `flutter analyze` was clean and all tests passed.

## Files touched

```text
lib/
  Network/api_links.dart                      + user endpoint
  constants/approutes.dart                    + AppRoute.profile = "/profile"
  localization/mylocalization.dart            + "profile", "email" in ar and en
  model/profile.dart                          new: Profile.fromJson
  routes.dart                                 + GetPage with BindingsBuilder
  view_controller/profile/
    profile.dart                              new: UI only
    profile_controller.dart                   new: loads the profile
test/profile_test.dart                        new: full payload + empty payload
```

## The controller

```dart
class ProfileController extends GetxController {
  Profile? profile;

  @override
  void onInit() {
    loadProfile();           // separate Future method; onInit is never async
    super.onInit();
  }

  Future<void> loadProfile() async {
    final response = await Api.makeApiRequest(
      url: "${ApiLinks.user}/${UserSession.userId}",
      method: 'GET',
    );

    if (response['success'] == true) {
      profile = Profile.fromJson(response);
      update();
    }
  }
}
```

Note what is absent: no `http` import, no `try/catch`, no error dialog. `Api` already showed the error if the request failed.

## The screen

```dart
class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return GetBuilder<ProfileController>(
      builder: (controller) => Scaffold(
        appBar: CustomAppBar(title: 'profile'.tr),
        body: /* presentation only */,
      ),
    );
  }
}
```

## A naming collision, handled

The model is `Profile`, so the screen class could not also be `Profile`. The skill says to rename the model (`UserProfile`) in preference to adding a `Screen` suffix, and to say so in the summary if the suffix is unavoidable. The example above used the suffix.

## Verification

```bash
python3 skills/flutter-getx-architecture/scripts/audit_conventions.py .
dart format lib test
flutter analyze
flutter test
```
