import 'package:flutter/material.dart';
import 'package:{{package}}/constants/appcolor.dart';
import 'package:{{package}}/helper/functions/validinput.dart';
import 'package:{{package}}/helper/widgets/buttons/custombutton.dart';
import 'package:{{package}}/helper/widgets/textfields/customtextfield.dart';
import 'package:{{package}}/view_controller/login/login_controller.dart';
import 'package:get/get.dart';

class Login extends StatelessWidget {
  const Login({super.key});

  @override
  Widget build(BuildContext context) {
    return GetBuilder<LoginController>(
      builder: (controller) => Scaffold(
        backgroundColor: AppColor.white,
        appBar: AppBar(backgroundColor: AppColor.white, elevation: 0),
        body: Form(
          key: controller.formstate,
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 24),
            width: double.infinity,
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 40),
                  Text(
                    'login'.tr,
                    style: const TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                      color: AppColor.black,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'login_subtitle'.tr,
                    style: const TextStyle(color: AppColor.grey),
                  ),
                  const SizedBox(height: 32),
                  CustomTextField(
                    mycontroller: controller.username,
                    hint: 'username'.tr,
                    valid: (value) => validInput(value, 3, 30, 'username'),
                  ),
                  const SizedBox(height: 16),
                  Obx(
                    () => CustomTextField(
                      mycontroller: controller.password,
                      hint: 'password'.tr,
                      obscureText: controller.hidePassword.value,
                      valid: (value) => validInput(value, 6, 40, 'password'),
                      suffixIcon: IconButton(
                        onPressed: controller.togglePasswordVisibility,
                        icon: Icon(
                          controller.hidePassword.value
                              ? Icons.visibility_off_outlined
                              : Icons.visibility_outlined,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    'demo_hint'.tr,
                    style: const TextStyle(color: AppColor.grey, fontSize: 12),
                  ),
                  const SizedBox(height: 32),
                  CustomButton(
                    text: 'login'.tr,
                    onPressed: () => controller.login(),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
