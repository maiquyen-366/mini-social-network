// Tầng API: cấu hình axios, tự gắn JWT và refresh access token.
import axios from "axios";
import { API_BASE_URL } from "../config/environment";

const axiosClient = axios.create({ baseURL: API_BASE_URL });

axiosClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

axiosClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      const refresh = localStorage.getItem("refresh_token");
      if (refresh) {
        original._retry = true;
        try {
          const response = await axios.post(`${API_BASE_URL}/accounts/refresh/`, { refresh });
          localStorage.setItem("access_token", response.data.data.access);
          original.headers.Authorization = `Bearer ${response.data.data.access}`;
          return axiosClient(original);
        } catch {
          localStorage.clear();
        }
      }
    }
    return Promise.reject(error);
  },
);

export default axiosClient;
