import { ChatMessage, ChatResponse } from '@/interfaces/chat';

const API_URL = 'http://localhost:8000';

export const sendMessage = async (message: ChatMessage): Promise<ChatResponse> => {
  const response = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(message),
  });

  if (!response.ok) {
    throw new Error('Failed to send message');
  }

  return response.json();
};
