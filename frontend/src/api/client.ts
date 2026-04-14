import axios from 'axios';

// 백엔드 API 베이스 URL 설정
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30초 (AI 답변 대기 고려)
});

// 요청 인터셉터 (향후 인증 등이 필요할 경우 활용)
client.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 응답 인터셉터 (에러 공통 처리)
client.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Call Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default client;
