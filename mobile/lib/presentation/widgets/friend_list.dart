import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../application/friend/friend_notifier.dart';
import '../../domain/entities/friend.dart';

class FriendList extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final friendsAsyncValue = ref.watch(friendsProvider);

    return friendsAsyncValue.when(
      data: (friends) => _buildFriendList(friends),
      loading: () => Center(child: CircularProgressIndicator()),
      error: (error, stack) => Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Error: $error'),
            ElevatedButton(
              onPressed: () => ref.refresh(friendsProvider),
              child: Text('Retry'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFriendList(List<Friend> friends) {
    return ListView.builder(
      itemCount: friends.length,
      itemBuilder: (context, index) {
        final friend = friends[index];
        return ListTile(
          title: Text(friend.name),
          onTap: () {
            // TODO: Navigate to friend details page
          },
        );
      },
    );
  }
}
