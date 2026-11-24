class Home extends StatelessWidget {
  const Home({super.key});

  @override
  Widget build(BuildContext context) {
    return GetBuilder<HomeController>(
      builder: (controller) => Scaffold(
        appBar: AppBar(title: Text('home'.tr)),
        body: Text('home'.tr),
      ),
    );
  }
}
