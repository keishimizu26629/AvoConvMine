import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mobile/utils/providers.dart';
import '../../domain/entities/chat_message.dart';
import '../../utils/api_client.dart';

class ChatRepository {
  final ApiClient _apiClient;

  ChatRepository(this._apiClient);

  Future<List<ChatMessageReceive>> getChats() async {
    return await _apiClient.getChats();
  }

  Future<void> sendMessage(String content) async {
    await _apiClient.sendMessage(content);
  }
}

final chatRepositoryProvider = Provider<ChatRepository>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  return ChatRepository(apiClient);
});
