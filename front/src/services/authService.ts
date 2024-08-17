import { LoginData, RegisterData, AuthResponse } from '@/interfaces/auth';
import Cookies from 'js-cookie';
import { getApiUrl } from '@/utils/getApiUrl';

const API_URL = getApiUrl() + '/auth';

console.log('test2')

const setTokenCookie = (token: string) => {
  Cookies.set('auth_token', token, { expires: 7 }); // 7日間有効
};

export const login = async (data: LoginData): Promise<AuthResponse> => {
  const response = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: data.email,
      password: data.password
    }),
    credentials: 'include',
  });

  if (!response.ok) {
    throw new Error('Login failed');
  }

  const result = await response.json();
  setTokenCookie(result.access_token);
  return result;
};

export const register = async (data: RegisterData): Promise<AuthResponse> => {
  const response = await fetch(`${API_URL}/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
    credentials: 'include',
  });

  if (!response.ok) {
    throw new Error('Registration failed');
  }

  const result = await response.json();
  setTokenCookie(result.access_token);
  return result;
};

export const logout = async (): Promise<void> => {
  await fetch(`${API_URL}/logout`, {
    method: 'POST',
    credentials: 'include',
  });
  Cookies.remove('auth_token');
};
