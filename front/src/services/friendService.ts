import { Friend, FriendDetails } from '@/interfaces/friend';

const API_URL = 'http://localhost:8000';

export const getFriends = async (token: string): Promise<Friend[]> => {
  const response = await fetch(`${API_URL}/friends/`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (!response.ok) {
    if (response.status === 401) {
      const errorData = await response.json();
      if (errorData.detail === "Could not validate credentials") {
        throw new Error('Invalid credentials');
      }
    }
    throw new Error('Failed to fetch friends');
  }

  return response.json();
};

// 既存の関数はそのままで、以下を追加

export const getFriendDetails = async (token: string, friendId: number): Promise<FriendDetails> => {
  const response = await fetch(`${API_URL}/friend/details`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ friend_id: friendId }),
  });

  if (!response.ok) {
    throw new Error('Failed to fetch friend details');
  }

  return response.json();
};

export const addConversation = async (token: string, friendId: number, context: string, conversationDate: string): Promise<void> => {
  const response = await fetch(`${API_URL}/friends/extract_attributes`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      friend_id: friendId,
      context: context,
      conversation_date: conversationDate
    })
  });

  if (!response.ok) {
    throw new Error('Failed to create conversation');
  }
};
