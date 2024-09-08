import 'package:mobile/main.dart';
import 'package:riverpod/riverpod.dart';
import '../infrastructure/auth/auth_service.dart';
import 'auth/auth_notifier.dart';
import 'auth/auth_state.dart';

final authServiceProvider = Provider<AuthService>((ref) {
  final dio = ref.watch(dioProvider);
  return AuthService(dio);
});

final authNotifierProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  final authService = ref.watch(authServiceProvider);
  return AuthNotifier(authService);
});
