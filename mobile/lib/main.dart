import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mobile/presentation/pages/login_page.dart';
import 'presentation/pages/home_page.dart';
import 'application/auth/auth_notifier.dart';

void main() {
  runApp(
    const ProviderScope(
      child: MyApp(),
    ),
  );
}

class MyApp extends ConsumerWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authNotifierProvider);

    return MaterialApp(
      title: 'Friend App',
      theme: ThemeData(
        appBarTheme: Theme.of(context).appBarTheme.copyWith(centerTitle: true),
      ),
      home: authState.when(
        data: (isAuthenticated) =>
            isAuthenticated ? HomePage() : const LoginPage(),
        loading: () => const CircularProgressIndicator(),
        error: (_, __) => const LoginPage(),
      ),
      debugShowCheckedModeBanner: false,
    );
  }
}
