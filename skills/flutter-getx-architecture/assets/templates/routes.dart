import 'package:{{package}}/constants/approutes.dart';
import 'package:{{package}}/helper/middleware/mymiddleware.dart';
import 'package:{{package}}/view_controller/home/home.dart';
import 'package:{{package}}/view_controller/home/home_controller.dart';
import 'package:{{package}}/view_controller/login/login.dart';
import 'package:{{package}}/view_controller/login/login_controller.dart';
import 'package:get/get.dart';

List<GetPage<dynamic>> routes = [
  GetPage(
    name: AppRoute.login,
    page: () => const Login(),
    binding: BindingsBuilder(() => Get.lazyPut(() => LoginController())),
    middlewares: [MyMiddleWare()],
  ),
  GetPage(
    name: AppRoute.home,
    page: () => const Home(),
    binding: BindingsBuilder(() => Get.lazyPut(() => HomeController())),
  ),
];
