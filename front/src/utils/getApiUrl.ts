export const getApiUrl = (): string => {
  if (process.env.ENVIRONMENT == 'production') {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;
    console.log(apiUrl);
    return apiUrl || '';
  } else {
    const apiUrl = 'http://localhost:8000';
    console.log(apiUrl);
    return apiUrl;
  }
};
