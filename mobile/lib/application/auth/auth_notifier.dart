import 'package:riverpod/riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../infrastructure/auth/auth_service.dart';
import '../../domain/auth/login_credentials.dart';
import '../../domain/auth/registration_data.dart';
import '../../domain/auth/auth_token.dart';
import 'auth_state.dart';

class AuthNotifier extends StateNotifier<AuthState> {
  final AuthService _authService;

  AuthNotifier(this._authService) : super(const AuthState.initial()) {
    _checkAuthStatus();
  }

  Future<void> _checkAuthStatus() async {
    state = const AuthState.loading();
    final storedToken = await _authService.getStoredToken();
    if (storedToken != null) {
      final isValid = await _authService.isTokenValid(storedToken);
      if (isValid) {
        state = AuthState.authenticated(storedToken);
      } else {
        state = const AuthState.unauthenticated();
      }
    } else {
      state = const AuthState.unauthenticated();
    }
  }

  Future<void> login(String email, String password) async {
    state = const AuthState.loading();
    try {
      final credentials = LoginCredentials(email: email, password: password);
      final authToken = await _authService.login(credentials);
      print('Login successful, token: ${authToken.accessToken}');
      state = AuthState.authenticated(authToken);
    } catch (e) {
      print('Login error: ${e.toString()}');
      state = AuthState.error(e.toString());
    }
  }

  Future<void> register(String name, String email, String password) async {
    state = const AuthState.loading();
    try {
      final registrationData =
          RegistrationData(name: name, email: email, password: password);
      final authToken = await _authService.register(registrationData);
      await _saveAuthToken(authToken);
      state = AuthState.authenticated(authToken);
    } catch (e) {
      state = AuthState.error(e.toString());
    }
  }

  Future<void> logout() async {
    state = const AuthState.loading();
    try {
      await _authService.logout();
      await _removeAuthToken();
      state = const AuthState.unauthenticated();
    } catch (e) {
      state = AuthState.error(e.toString());
    }
  }

  Future<void> _saveAuthToken(AuthToken token) async {
    // トークンをローカルストレージに保存する処理
    // 例: SharedPreferences を使用する場合
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('auth_token', token.accessToken);
  }

  Future<void> _removeAuthToken() async {
    // トークンをローカルストレージから削除する処理
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('auth_token');
  }
}
