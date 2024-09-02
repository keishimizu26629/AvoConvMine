import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../widgets/friend_list.dart';
import '../widgets/chat_list.dart';
import '../widgets/my_page.dart';
import '../../application/auth/auth_notifier.dart';

final currentIndexProvider = StateProvider<int>((ref) => 0);

class HomePage extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final currentIndex = ref.watch(currentIndexProvider);
    final authState = ref.watch(authNotifierProvider);

    // Check if the user is not authenticated and redirect to login page
    if (authState.value == false) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        Navigator.of(context).pushReplacementNamed('/login');
      });
    }

    return Scaffold(
      appBar: AppBar(
        title: Text(_getTitleForIndex(currentIndex)),
      ),
      body: IndexedStack(
        index: currentIndex,
        children: [
          FriendList(),
          ChatList(),
          MyPage(),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: currentIndex,
        onTap: (index) => ref.read(currentIndexProvider.notifier).state = index,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.people),
            label: 'Friends',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.chat),
            label: 'Chat',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.person),
            label: 'Mypage',
          ),
        ],
      ),
    );
  }

  String _getTitleForIndex(int index) {
    switch (index) {
      case 0:
        return 'Friends';
      case 1:
        return 'Chat';
      case 2:
        return 'My Page';
      default:
        return 'Friend App';
    }
  }
}
