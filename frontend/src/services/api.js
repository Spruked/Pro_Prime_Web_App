import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_URL}/auth/refresh`, {
          refresh_token: refreshToken
        });
        localStorage.setItem('access_token', response.data.access_token);
        api.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Redirect to login
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export const systemsApi = {
  getAll: () => api.get('/systems'),
  getBySlug: (slug) => api.get(`/systems/${slug}`),
  create: (data) => api.post('/systems', data),
  update: (id, data) => api.put(`/systems/${id}`, data),
  delete: (id) => api.delete(`/systems/${id}`),
};

export const socialApi = {
  getAll: () => api.get('/social'),
  create: (data) => api.post('/social', data),
  update: (id, data) => api.put(`/social/${id}`, data),
  delete: (id) => api.delete(`/social/${id}`),
};

export const pagesApi = {
  getByName: (name) => api.get(`/pages/${name}`),
  update: (id, data) => api.put(`/pages/${id}`, data),
};

export const authApi = {
  login: (credentials) => api.post('/auth/login', credentials),
  refresh: (refreshToken) => api.post('/auth/refresh', { refresh_token: refreshToken }),
};

export default api;