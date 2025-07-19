import axios from 'axios';
import Cookies from 'js-cookie';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Criar instância do axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token de autenticação
api.interceptors.request.use((config) => {
  const token = Cookies.get('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para tratar erros de autenticação
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      Cookies.remove('token');
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// Tipos TypeScript
export interface User {
  id: number;
  nome: string;
  email: string;
  is_active: boolean;
  created_at: string;
}

export interface Treino {
  id: number;
  nome: string;
  descricao?: string;
  created_at: string;
  usuario_id: number;
}

export interface TreinoWithExercicios extends Treino {
  exercicios: Exercicio[];
}

export interface Exercicio {
  id: number;
  nome: string;
  tipo: 'com_peso' | 'sem_peso';  // CORRIGIDO: usando formato do backend
  musculo?: string;
  repeticoes?: number;
  sets?: number;
  carga?: number;
  tempo?: number;
  distancia?: number;
  treino_id: number;
  created_at: string;
}

export interface LoginData {
  username: string;
  password: string;
}

export interface RegisterData {
  nome: string;
  email: string;
  password: string;
}

// Funções da API
export const authAPI = {
  login: (data: LoginData) => api.post<{ access_token: string; token_type: string }>('/auth/login', data, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }),
  register: (data: RegisterData) => api.post<User>('/auth/register', data),
};

export const userAPI = {
  getProfile: () => api.get<User>('/usuarios/me/profile'),
  getProfileComplete: () => api.get<User & { treinos: Treino[] }>('/usuarios/me/profile-complete'),
  updateProfile: (data: Partial<RegisterData>) => api.put<User>('/usuarios/me', data),
};

export const treinoAPI = {
  getAll: () => api.get<Treino[]>('/treinos/'),
  getById: (id: number) => api.get<Treino>(`/treinos/${id}`),
  getByIdWithExercicios: (id: number) => api.get<TreinoWithExercicios>(`/treinos/${id}/with-exercicios`),
  create: (data: { nome: string; descricao?: string }) => api.post<Treino>('/treinos/', data),
  update: (id: number, data: { nome: string; descricao?: string }) => api.put<Treino>(`/treinos/${id}`, data),
  delete: (id: number) => api.delete(`/treinos/${id}`),
};

export const exercicioAPI = {
  getByTreino: (treinoId: number) => api.get<Exercicio[]>(`/exercicios/treinos/${treinoId}/exercicios`),
  getById: (id: number) => api.get<Exercicio>(`/exercicios/${id}`),
  create: (treinoId: number, data: Omit<Exercicio, 'id' | 'treino_id' | 'created_at'>) =>
    api.post<Exercicio>(`/exercicios/treinos/${treinoId}/exercicios`, data),
  update: (id: number, data: Partial<Omit<Exercicio, 'id' | 'treino_id' | 'created_at'>>) =>
    api.put<Exercicio>(`/exercicios/${id}`, data),
  delete: (id: number) => api.delete(`/exercicios/${id}`),
};

export default api; 