import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export const auth = {
  login: (credentials) => api.post('/login/', credentials),
  register: (userData) => api.post('/register/', userData),
  logout: () => api.post('/logout/'),
};

export const books = {
  getAll: (params) => api.get('/books/', { params }),
  get: (id) => api.get(`/books/${id}/`),
  create: (data) => api.post('/books/', data),
  update: (id, data) => api.put(`/books/${id}/`, data),
  delete: (id) => api.delete(`/books/${id}/`),
};

export const categories = {
  getAll: () => api.get('/categories/'),
  get: (id) => api.get(`/categories/${id}/`),
  create: (data) => api.post('/categories/', data),
  update: (id, data) => api.put(`/categories/${id}/`, data),
  delete: (id) => api.delete(`/categories/${id}/`),
};

export const transactions = {
  getAll: () => api.get('/transactions/'),
  get: (id) => api.get(`/transactions/${id}/`),
  create: (data) => api.post('/transactions/', data),
  update: (id, data) => api.put(`/transactions/${id}/`, data),
  getOverdue: () => api.get('/transactions/overdue/'),
};

export default api;
