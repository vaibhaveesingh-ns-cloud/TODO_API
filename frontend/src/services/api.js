import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: async (userData) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  login: async (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await api.post('/auth/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  verifyEmail: async (token) => {
    const response = await api.get(`/auth/verify-email?token=${token}`);
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// Todos API
export const todosAPI = {
  getTodos: async () => {
    const response = await api.get('/todos/');
    return response.data;
  },

  createTodo: async (todoData) => {
    const response = await api.post('/todos/', todoData);
    return response.data;
  },

  updateTodo: async (todoId, todoData) => {
    const response = await api.put(`/todos/${todoId}`, todoData);
    return response.data;
  },

  deleteTodo: async (todoId) => {
    const response = await api.delete(`/todos/${todoId}`);
    return response.data;
  },

  getTodo: async (todoId) => {
    const response = await api.get(`/todos/${todoId}`);
    return response.data;
  },
};

// Admin API
export const adminAPI = {
  // Dashboard stats
  getDashboardStats: async () => {
    const response = await api.get('/admin/dashboard/stats');
    return response.data;
  },

  // Users management
  getUsers: async () => {
    const response = await api.get('/admin/users');
    return response.data;
  },

  getUsersWithStats: async () => {
    const response = await api.get('/admin/users/detailed');
    return response.data;
  },

  getUserTodos: async (userId) => {
    const response = await api.get(`/admin/users/${userId}/todos`);
    return response.data;
  },

  promoteUser: async (userId) => {
    const response = await api.post(`/admin/users/${userId}/promote`);
    return response.data;
  },

  demoteUser: async (userId) => {
    const response = await api.post(`/admin/users/${userId}/demote`);
    return response.data;
  },

  activateUser: async (userId) => {
    const response = await api.post(`/admin/users/${userId}/activate`);
    return response.data;
  },

  deactivateUser: async (userId) => {
    const response = await api.post(`/admin/users/${userId}/deactivate`);
    return response.data;
  },

  deleteUser: async (userId) => {
    const response = await api.delete(`/admin/users/${userId}`);
    return response.data;
  },

  // Todos management
  getAllTodos: async (filters = {}) => {
    const params = new URLSearchParams();
    if (filters.user_id) params.append('user_id', filters.user_id);
    if (filters.completed !== undefined) params.append('completed', filters.completed);
    if (filters.limit) params.append('limit', filters.limit);
    if (filters.offset) params.append('offset', filters.offset);
    
    const response = await api.get(`/admin/todos?${params.toString()}`);
    return response.data;
  },

  deleteTodo: async (todoId) => {
    const response = await api.delete(`/admin/todos/${todoId}`);
    return response.data;
  },
};

export default api;
