import axios from 'axios';

// Determine API base URL based on environment
const getApiBaseUrl = () => {
  // If NEXT_PUBLIC_API_URL is set, use it
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }
  
  // In browser, construct URL based on current location
  if (typeof window !== 'undefined') {
    const protocol = window.location.protocol;
    const hostname = window.location.hostname;
    
    // If in Codespaces (preview.app.github.dev), use port 8000 forwarded URL
    if (hostname.includes('github.dev')) {
      // Replace 3000 with 8000 in the URL
      const apiHost = window.location.host.replace('-3000.', '-8000.');
      return `${protocol}//${apiHost}/api`;
    }
    
    // For local development
    return 'http://localhost:8000/api';
  }
  
  // Fallback
  return 'http://localhost:8000/api';
};

const API_BASE_URL = getApiBaseUrl();

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add CSRF token to requests
api.interceptors.request.use((config: any) => {
  // Get CSRF token from cookie
  const csrfToken = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
  
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  
  return config;
});

export const authAPI = {
  login: (credentials: { username: string; password: string }) =>
    api.post('/auth/login/', credentials),
  
  register: (data: any) =>
    api.post('/auth/register/', data),
  
  logout: () =>
    api.post('/auth/logout/'),
  
  getCurrentUser: () =>
    api.get('/auth/me/'),
};

export const priestsAPI = {
  getAll: (params?: any) =>
    api.get('/priests/', { params }),
  
  getById: (id: number) =>
    api.get(`/priests/${id}/`),
};

export const servicesAPI = {
  getAll: (params?: any) =>
    api.get('/services/', { params }),
  
  getById: (id: number) =>
    api.get(`/services/${id}/`),
};

export const bookingsAPI = {
  getAll: () =>
    api.get('/bookings/'),
  
  create: (data: any) =>
    api.post('/bookings/', data),
  
  getById: (id: number) =>
    api.get(`/bookings/${id}/`),
  
  confirm: (id: number) =>
    api.post(`/bookings/${id}/confirm/`),
  
  complete: (id: number, data: any) =>
    api.post(`/bookings/${id}/complete/`, data),
  
  rate: (id: number, data: any) =>
    api.post(`/bookings/${id}/rate/`, data),
};

export const productsAPI = {
  getAll: (params?: any) =>
    api.get('/products/', { params }),
  
  getById: (id: number) =>
    api.get(`/products/${id}/`),
  
  getCategories: () =>
    api.get('/categories/'),
};

export const cartAPI = {
  get: () =>
    api.get('/cart/'),
  
  addItem: (data: any) =>
    api.post('/cart/add_item/', data),
  
  updateItem: (data: any) =>
    api.post('/cart/update_item/', data),
  
  removeItem: (data: any) =>
    api.post('/cart/remove_item/', data),
  
  clear: () =>
    api.post('/cart/clear/'),
};

export const ordersAPI = {
  getAll: () =>
    api.get('/orders/'),
  
  checkout: (data: any) =>
    api.post('/orders/checkout/', data),
  
  getById: (id: number) =>
    api.get(`/orders/${id}/`),
};

export default api;
