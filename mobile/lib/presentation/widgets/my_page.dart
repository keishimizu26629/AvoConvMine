import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../application/auth/auth_notifier.dart';

class MyPage extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Center(
      child: ElevatedButton(
        onPressed: () async {
          await ref.read(authNotifierProvider.notifier).logout();
          // No need to navigate here, HomePage will handle it
        },
        child: const Text('Logout'),
      ),
    );
  }
}
