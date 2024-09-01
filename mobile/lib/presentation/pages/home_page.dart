import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../application/friend/friend_notifier.dart';
import '../../domain/entities/friend.dart';
import '../../utils/api_client.dart';

final apiClientProvider = Provider((ref) => ApiClient('your_token_here'));

final friendNotifierProvider = StateNotifierProvider<FriendNotifier, AsyncValue<List<Friend>>>(
  (ref) => FriendNotifier(ref.watch(apiClientProvider)),
);

class HomePage extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final friendsState = ref.watch(friendNotifierProvider);

    return Scaffold(
      appBar: AppBar(title: Text('Friends')),
      body: friendsState.when(
        data: (friends) => RefreshIndicator(
          onRefresh: () => ref.read(friendNotifierProvider.notifier).fetchFriends(),
          child: ListView.builder(
            itemCount: friends.length,
            itemBuilder: (context, index) {
              final friend = friends[index];
              return ListTile(
                title: Text(friend.name),
                subtitle: Text('ID: ${friend.id}'),
              );
            },
          ),
        ),
        loading: () => Center(child: CircularProgressIndicator()),
        error: (error, stack) => Center(child: Text('Error: $error')),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _showAddFriendDialog(context, ref),
        child: Icon(Icons.add),
      ),
    );
  }

  void _showAddFriendDialog(BuildContext context, WidgetRef ref) {
    showDialog(
      context: context,
      builder: (context) {
        String name = '';
        return AlertDialog(
          title: Text('Add Friend'),
          content: TextField(
            onChanged: (value) => name = value,
            decoration: InputDecoration(hintText: "Friend's name"),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text('Cancel'),
            ),
            TextButton(
              onPressed: () {
                if (name.isNotEmpty) {
                  ref.read(friendNotifierProvider.notifier).createFriend(name);
                  Navigator.pop(context);
                }
              },
              child: Text('Add'),
            ),
          ],
        );
      },
    );
  }
}
