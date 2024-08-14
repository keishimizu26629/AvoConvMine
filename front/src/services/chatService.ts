import { ChatMessageSend, ChatMessageReceive } from '@/interfaces/chat';

const API_URL = 'http://localhost:8000';

export const getChats = async (token: string): Promise<ChatMessageReceive[]> => {
  const response = await fetch(`${API_URL}/chats`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch chats: ${response.status} ${response.statusText}`);
  }

  return response.json();
};

export const sendMessage = async (message: ChatMessageSend, token: string): Promise<ChatMessageReceive> => {
  const response = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(message),
  });

  if (!response.ok) {
    throw new Error('Failed to send message');
  }

  return response.json();
};
