import axios from 'axios';

// Determine API base URL based on environment
const getApiBaseUrl = () => {
  // Server-side: use localhost
  if (typeof window === 'undefined') {
    return 'http://localhost:8000/api';
  }
  
  // Client-side: detect environment
  const hostname = window.location.hostname;
  const protocol = window.location.protocol;
  
  // If in Codespaces or GitHub preview
  if (hostname.includes('github.dev') || hostname.includes('githubpreview.dev') || hostname.includes('app.github.dev')) {
    // Extract the base codespace name and replace port
    // From: legendary-goggles-5jg47gppq562jrq-3000.app.github.dev
    // To:   legendary-goggles-5jg47gppq562jrq-8000.app.github.dev
    const backendHost = hostname.replace('-3000.', '-8000.');
    const apiUrl = `${protocol}//${backendHost}/api`;
    console.log('🔗 Punyaka API URL (Codespaces):', apiUrl);
    console.log('🌍 Frontend hostname:', hostname);
    console.log('🎯 Backend hostname:', backendHost);
    return apiUrl;
  }
  
  // For local development
  console.log('🔗 Punyaka API URL (Local):', 'http://localhost:8000/api');
  return 'http://localhost:8000/api';
};

const api = axios.create({
  baseURL: '/',  // Start with relative, will be updated on client-side
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Update baseURL on client-side
if (typeof window !== 'undefined') {
  api.defaults.baseURL = getApiBaseUrl();
}

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

// Add response interceptor for better error logging
api.interceptors.response.use(
  (response: any) => response,
  (error: any) => {
    console.error('API Error:', {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status,
      data: error.response?.data,
      message: error.message
    });
    return Promise.reject(error);
  }
);

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
