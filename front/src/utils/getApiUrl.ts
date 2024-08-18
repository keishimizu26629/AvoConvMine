export const getApiUrl = (): string => {
  if (process.env.ENVIRONMENT == 'f') {
    const apiUrl = 'http://localhost:8000';
    console.log(apiUrl);
    return apiUrl;
  } else {
    // const apiUrl = 'https://avo-conv-mine-6c40b00157f0.herokuapp.com';
    const apiUrl = 'http://localhost:8000';
    console.log(apiUrl);
    return apiUrl || '';
  }
};
