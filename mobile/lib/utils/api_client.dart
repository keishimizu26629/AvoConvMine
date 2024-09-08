import 'package:dio/dio.dart';
import '../domain/entities/friend.dart';
import '../domain/entities/chat_message.dart';
import '../utils/logger.dart';

class ApiClient {
  final Dio _dio;
  final String baseUrl = 'http://localhost:8000';

  ApiClient(String token) : _dio = Dio(BaseOptions(
    baseUrl: 'http://localhost:8000',
    headers: {'Authorization': 'Bearer $token'},
  ));

  Future<String> login(String email, String password) async {
    try {
      final response = await _dio.post(
        '/auth/login',
        data: {
          'email': email,
          'password': password,
        },
      );
      if (response.statusCode == 200) {
        return response.data['access_token'];
      } else {
        throw DioException(
          requestOptions: response.requestOptions,
          response: response,
          type: DioExceptionType.badResponse,
        );
      }
    } on DioException catch (e) {
      log.info('Login failed', e);
      if (e.response?.statusCode == 401) {
        throw Exception('Invalid credentials');
      }
      throw Exception('Failed to login: ${e.message}');
    }
  }

  Future<List<Friend>> getFriends() async {
    try {
      final response = await _dio.get('/friends/');
      if (response.statusCode == 200) {
        final List<dynamic> friendsJson = response.data;
        return friendsJson.map((json) => Friend.fromJson(json)).toList();
      } else {
        throw DioException(
          requestOptions: response.requestOptions,
          response: response,
          type: DioExceptionType.badResponse,
        );
      }
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        throw Exception('Invalid credentials');
      }
      throw Exception('Failed to fetch friends: ${e.message}');
    }
  }

  Future<Friend> createFriend(String name) async {
    try {
      final response = await _dio.post(
        '/friends/',
        data: {'name': name},
      );
      if (response.statusCode == 201) {
        return Friend.fromJson(response.data);
      } else {
        throw DioException(
          requestOptions: response.requestOptions,
          response: response,
          type: DioExceptionType.badResponse,
        );
      }
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        throw Exception('Invalid credentials');
      }
      throw Exception('Failed to create friend: ${e.message}');
    }
  }

  Future<List<ChatMessageReceive>> getChats() async {
    try {
      final response = await _dio.get('/chats/');
      if (response.statusCode == 200) {
        final List<dynamic> chatsJson = response.data;
        return chatsJson.map((json) => ChatMessageReceive.fromJson(json)).toList();
      } else {
        throw DioException(
          requestOptions: response.requestOptions,
          response: response,
          type: DioExceptionType.badResponse,
        );
      }
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        throw Exception('Invalid credentials');
      }
      throw Exception('Failed to fetch chats: ${e.message}');
    }
  }

  Future<void> sendMessage(String content) async {
    try {
      final response = await _dio.post(
        '/chats/',
        data: {'content': content},
      );
      if (response.statusCode != 200 && response.statusCode != 201) {
        throw DioException(
          requestOptions: response.requestOptions,
          response: response,
          type: DioExceptionType.badResponse,
        );
      }
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        throw Exception('Invalid credentials');
      }
      throw Exception('Failed to send message: ${e.message}');
    }
  }
}
