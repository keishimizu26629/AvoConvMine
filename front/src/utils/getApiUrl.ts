export const getApiUrl = (): string => {
  if (process.env.ENVIRONMENT == 'development') {
    return 'http://localhost:8000';
  } else {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;
    return apiUrl || '';
  }
};
