export const getApiUrl = (): string => {
  if (process.env.NEXT_PUBLIC_ENVIRONMENT === 'production') {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;
    return apiUrl || '';
  } else {
    const apiUrl = 'http://localhost:8000';
    return apiUrl;
  }
};
