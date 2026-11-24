class HomeController extends GetxController {
  late TextEditingController search;

  @override
  void onInit() {
    search = TextEditingController();
    loadItems();
    super.onInit();
  }

  @override
  void onClose() {
    search.dispose();
    super.onClose();
  }

  Future<void> loadItems() async {}
}
