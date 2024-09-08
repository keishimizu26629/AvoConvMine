import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../domain/entities/chat_message.dart';
import '../../infrastructure/repositories/chat_repository.dart';

class ChatNotifier extends StateNotifier<AsyncValue<List<ChatMessageReceive>>> {
  final ChatRepository _chatRepository;

  ChatNotifier(this._chatRepository) : super(AsyncValue.loading()) {
    fetchChats();
  }

  Future<void> fetchChats() async {
    state = AsyncValue.loading();
    try {
      final chats = await _chatRepository.getChats();
      state = AsyncValue.data(chats);
    } catch (e) {
      state = AsyncValue.error(e, StackTrace.current);
    }
  }
}

final chatNotifierProvider = StateNotifierProvider<ChatNotifier, AsyncValue<List<ChatMessageReceive>>>((ref) {
  final chatRepository = ref.watch(chatRepositoryProvider);
  return ChatNotifier(chatRepository);
});
