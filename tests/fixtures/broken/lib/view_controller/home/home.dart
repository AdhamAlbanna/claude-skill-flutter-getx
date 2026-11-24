class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  @override
  Widget build(BuildContext context) {
    // final unused = 1;
    return Scaffold(
      appBar: AppBar(title: Text('Home')),
      body: ElevatedButton(
        onPressed: () => setState(() {}),
        child: Text('Load'),
      ),
    );
  }
}

Future<void> load() async {
  await Api.makeApiRequest(url: 'x', method: 'GET');
}
