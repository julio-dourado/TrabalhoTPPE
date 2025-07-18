import axios from 'axios'

const API_URL = process.env.API_URL || 'http://localhost:8000'

// Configuração do axios
const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptador para adicionar token de autenticação
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptador para lidar com respostas
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token inválido ou expirado
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Tipos para as respostas da API
export interface User {
  id: number
  name: string
  email: string
  is_active: boolean
  created_at: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user_id: number
}

export interface ApiError {
  detail: string
}

// Serviços da API
export const authService = {
  login: async (credentials: LoginRequest): Promise<LoginResponse> => {
    const response = await api.post<LoginResponse>('/auth/login', credentials)
    return response.data
  },

  register: async (userData: {
    name: string
    email: string
    password: string
    password_confirm: string
  }): Promise<User> => {
    const response = await api.post<User>('/auth/register', userData)
    return response.data
  },
}

export const userService = {
  getCurrentUser: async (): Promise<User> => {
    const response = await api.get<User>('/users/me')
    return response.data
  },
}

export const testService = {
  getRoot: async (): Promise<{ message: string }> => {
    const response = await axios.get(`${API_URL}/`)
    return response.data
  },
}

export default api 