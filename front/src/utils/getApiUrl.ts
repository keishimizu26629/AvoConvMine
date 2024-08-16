export const getApiUrl = (): string => {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  console.log('API URL:', apiUrl);
  return apiUrl;
};
