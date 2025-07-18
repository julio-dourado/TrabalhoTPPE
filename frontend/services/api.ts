import axios from 'axios'
import type {
  User,
  UserCreate,
  UserUpdate,
  LoginRequest,
  LoginResponse,
  UserRegistrationRequest,
  Exercise,
  ExerciseCreate,
  Training,
  TrainingCreate,
  TrainingUpdate,
  TrainingStatistics,
  MuscleGroup,
  Difficulty
} from '../types/api'

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

// Serviços de Autenticação
export const authService = {
  login: async (credentials: LoginRequest): Promise<LoginResponse> => {
    const response = await api.post<LoginResponse>('/auth/login', credentials)
    return response.data
  },

  register: async (userData: UserRegistrationRequest): Promise<User> => {
    const response = await api.post<User>('/auth/register', userData)
    return response.data
  },
}

// Serviços de Usuário
export const userService = {
  getCurrentUser: async (): Promise<User> => {
    const response = await api.get<User>('/users/me')
    return response.data
  },

  updateCurrentUser: async (userData: UserUpdate): Promise<User> => {
    const response = await api.put<User>('/users/me', userData)
    return response.data
  },

  createUser: async (userData: UserCreate): Promise<User> => {
    const response = await api.post<User>('/users/', userData)
    return response.data
  },

  getUsers: async (skip = 0, limit = 100): Promise<User[]> => {
    const response = await api.get<User[]>(`/users/?skip=${skip}&limit=${limit}`)
    return response.data
  },

  getUserById: async (userId: number): Promise<User> => {
    const response = await api.get<User>(`/users/${userId}`)
    return response.data
  },

  updateUser: async (userId: number, userData: UserUpdate): Promise<User> => {
    const response = await api.put<User>(`/users/${userId}`, userData)
    return response.data
  },

  deleteUser: async (userId: number): Promise<void> => {
    await api.delete(`/users/${userId}`)
  },

  deactivateUser: async (userId: number): Promise<void> => {
    await api.post(`/users/${userId}/deactivate`)
  },

  activateUser: async (userId: number): Promise<void> => {
    await api.post(`/users/${userId}/activate`)
  },
}

// Serviços de Exercício
export const exerciseService = {
  getExercises: async (skip = 0, limit = 100): Promise<Exercise[]> => {
    const response = await api.get<Exercise[]>(`/exercises/?skip=${skip}&limit=${limit}`)
    return response.data
  },

  getExerciseById: async (exerciseId: number): Promise<Exercise> => {
    const response = await api.get<Exercise>(`/exercises/${exerciseId}`)
    return response.data
  },

  createExercise: async (exerciseData: ExerciseCreate): Promise<Exercise> => {
    const response = await api.post<Exercise>('/exercises/', exerciseData)
    return response.data
  },

  updateExercise: async (exerciseId: number, exerciseData: Partial<ExerciseCreate>): Promise<Exercise> => {
    const response = await api.put<Exercise>(`/exercises/${exerciseId}`, exerciseData)
    return response.data
  },

  deleteExercise: async (exerciseId: number): Promise<void> => {
    await api.delete(`/exercises/${exerciseId}`)
  },

  getExercisesByMuscleGroup: async (muscleGroup: string): Promise<Exercise[]> => {
    const response = await api.get<Exercise[]>(`/exercises/muscle-group/${muscleGroup}`)
    return response.data
  },

  getExercisesByDifficulty: async (difficulty: string): Promise<Exercise[]> => {
    const response = await api.get<Exercise[]>(`/exercises/difficulty/${difficulty}`)
    return response.data
  },
}

// Serviços de Treino
export const trainingService = {
  getTrainings: async (skip = 0, limit = 100): Promise<Training[]> => {
    const response = await api.get<Training[]>(`/training/?skip=${skip}&limit=${limit}`)
    return response.data
  },

  getTrainingById: async (trainingId: number): Promise<Training> => {
    const response = await api.get<Training>(`/training/${trainingId}`)
    return response.data
  },

  createTraining: async (trainingData: TrainingCreate): Promise<Training> => {
    const response = await api.post<Training>('/training/', trainingData)
    return response.data
  },

  updateTraining: async (trainingId: number, trainingData: TrainingUpdate): Promise<Training> => {
    const response = await api.put<Training>(`/training/${trainingId}`, trainingData)
    return response.data
  },

  deleteTraining: async (trainingId: number): Promise<void> => {
    await api.delete(`/training/${trainingId}`)
  },

  startTraining: async (trainingId: number): Promise<Training> => {
    const response = await api.post<Training>(`/training/${trainingId}/start`)
    return response.data
  },

  finishTraining: async (trainingId: number, trainingData: TrainingUpdate): Promise<Training> => {
    const response = await api.post<Training>(`/training/${trainingId}/finish`, trainingData)
    return response.data
  },

  getTrainingStatistics: async (): Promise<TrainingStatistics> => {
    const response = await api.get<TrainingStatistics>('/training/statistics')
    return response.data
  },
}

// Serviço de teste
export const testService = {
  getRoot: async (): Promise<{ message: string }> => {
    const response = await axios.get(`${API_URL}/`)
    return response.data
  },

  getHealth: async (): Promise<{ status: string; version: string }> => {
    const response = await axios.get(`${API_URL}/health`)
    return response.data
  },
}

export default api 