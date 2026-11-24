import 'package:http/http.dart' as http;

class HomeController extends GetxController {
  late TextEditingController search;

  @override
  Future<void> onInit() async {
    search = TextEditingController();
    print('loading');
    super.onInit();
  }
}
