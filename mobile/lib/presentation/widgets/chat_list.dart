import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../application/chat/chat_notifier.dart';
import '../../domain/entities/chat_message.dart';
import 'package:intl/intl.dart';

class ChatList extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final chatState = ref.watch(chatNotifierProvider);

    return chatState.when(
      data: (messages) => ListView.builder(
        itemCount: messages.length,
        itemBuilder: (context, index) {
          final message = messages[index];
          return ChatMessageTile(message: message);
        },
      ),
      loading: () => Center(child: CircularProgressIndicator()),
      error: (error, stackTrace) => Center(
        child: Text('Error loading chats: $error'),
      ),
    );
  }
}

class ChatMessageTile extends StatelessWidget {
  final ChatMessageReceive message;

  const ChatMessageTile({Key? key, required this.message}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ExpansionTile(
      title: Text(message.content),
      subtitle: Text(DateFormat('yyyy-MM-dd HH:mm').format(message.createdAt)),
      children: [
        if (message.response != null)
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Response:', style: TextStyle(fontWeight: FontWeight.bold)),
                SizedBox(height: 8),
                Text(message.response!.finalAnswer),
                SizedBox(height: 8),
                Text(
                  'Responded at: ${DateFormat('yyyy-MM-dd HH:mm').format(message.response!.createdAt)}',
                  style: TextStyle(fontSize: 12, color: Colors.grey),
                ),
              ],
            ),
          ),
      ],
    );
  }
}
