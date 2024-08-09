import { Friend } from '@/interfaces/friend';

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
