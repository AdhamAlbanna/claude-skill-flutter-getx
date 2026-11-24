import 'package:flutter/material.dart';
import 'package:{{package}}/Network/api.dart';
import 'package:{{package}}/Network/api_links.dart';
import 'package:{{package}}/constants/approutes.dart';
import 'package:{{package}}/helper/functions/user_info.dart';
import 'package:{{package}}/helper/services/services.dart';
import 'package:{{package}}/model/product.dart';
import 'package:get/get.dart';

class HomeController extends GetxController {
  List<Product> products = [];

  @override
  void onInit() {
    loadProducts();
    super.onInit();
  }

  Future<void> loadProducts() async {
    final response = await Api.makeApiRequest(
      url: ApiLinks.products,
      method: 'GET',
      query: {'limit': '20', 'select': 'id,title,price,thumbnail'},
    );

    if (response['success'] == true) {
      products = (response['products'] as List<dynamic>)
          .map((json) => Product.fromJson(json))
          .toList();
      update();
    }
  }

  Future<void> changeLanguage() async {
    final code = Get.locale?.languageCode == 'ar' ? 'en' : 'ar';
    await Get.find<MyServices>().saveLanguageCode(code);
    Get.updateLocale(Locale(code));
  }

  Future<void> logout() async {
    await UserSession.clear();
    Get.offAllNamed(AppRoute.login);
  }
}
