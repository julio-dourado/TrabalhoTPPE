import React, { useState, useEffect } from 'react'
import { Activity, Clock, Flame, Weight, Star, TrendingUp, Dumbbell, Trophy } from 'lucide-react'
import { trainingService, userService } from '@/services/api'
import type { TrainingStatistics, User } from '@/types/api'

export default function Dashboard() {
  const [stats, setStats] = useState<TrainingStatistics | null>(null)
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsData, userData] = await Promise.all([
          trainingService.getTrainingStatistics(),
          userService.getCurrentUser()
        ])
        setStats(statsData)
        setUser(userData)
      } catch (err: any) {
        setError('Erro ao carregar dados')
        console.error('Erro:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  const formatTime = (minutes: number) => {
    const hours = Math.floor(minutes / 60)
    const mins = minutes % 60
    return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`
  }

  const formatCategoryLabel = (category: string) => {
    const labels: { [key: string]: string } = {
      'FORCA': 'Força',
      'CARDIO': 'Cardio',
      'FLEXIBILIDADE': 'Flexibilidade',
      'FUNCIONAL': 'Funcional',
      'RESISTENCIA': 'Resistência',
      'ESPORTES': 'Esportes',
      'REABILITACAO': 'Reabilitação'
    }
    return labels[category] || category
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="rounded-md bg-red-50 p-4">
        <p className="text-red-700">{error}</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              Bem-vindo, {user?.name}!
            </h1>
            <p className="text-gray-600">
              Aqui está um resumo da sua jornada fitness
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <Activity className="h-8 w-8 text-blue-600" />
            <span className="text-sm font-medium text-gray-500">
              Membro desde {user?.created_at ? new Date(user.created_at).toLocaleDateString() : '-'}
            </span>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-blue-100">
              <Dumbbell className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Total de Treinos</p>
              <p className="text-2xl font-bold text-gray-900">{stats?.total_trainings || 0}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-green-100">
              <Trophy className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Treinos Concluídos</p>
              <p className="text-2xl font-bold text-gray-900">{stats?.completed_trainings || 0}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-purple-100">
              <Clock className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Tempo Total</p>
              <p className="text-2xl font-bold text-gray-900">
                {formatTime(stats?.total_duration_min || 0)}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-orange-100">
              <Flame className="h-6 w-6 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Calorias Queimadas</p>
              <p className="text-2xl font-bold text-gray-900">
                {Math.round(stats?.total_calories_burned || 0)}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Additional Stats */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Desempenho</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <Weight className="h-5 w-5 text-gray-400 mr-2" />
                <span className="text-sm text-gray-600">Volume Total</span>
              </div>
              <span className="text-sm font-semibold text-gray-900">
                {Math.round(stats?.total_volume_kg || 0)} kg
              </span>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <Star className="h-5 w-5 text-gray-400 mr-2" />
                <span className="text-sm text-gray-600">Satisfação Média</span>
              </div>
              <div className="flex items-center">
                <span className="text-sm font-semibold text-gray-900 mr-1">
                  {(stats?.average_satisfaction || 0).toFixed(1)}
                </span>
                <div className="flex">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <Star
                      key={star}
                      className={`h-4 w-4 ${star <= (stats?.average_satisfaction || 0)
                          ? 'text-yellow-400 fill-current'
                          : 'text-gray-300'
                        }`}
                    />
                  ))}
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <TrendingUp className="h-5 w-5 text-gray-400 mr-2" />
                <span className="text-sm text-gray-600">Dificuldade Média</span>
              </div>
              <span className="text-sm font-semibold text-gray-900">
                {(stats?.average_difficulty || 0).toFixed(1)}/10
              </span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Informações Pessoais</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Categoria Favorita</span>
              <span className="text-sm font-semibold text-gray-900">
                {stats?.favorite_category
                  ? formatCategoryLabel(stats.favorite_category)
                  : 'Nenhuma'
                }
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Altura</span>
              <span className="text-sm font-semibold text-gray-900">
                {user?.height_cm ? `${user.height_cm} cm` : 'Não informado'}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Peso</span>
              <span className="text-sm font-semibold text-gray-900">
                {user?.weight_kg ? `${user.weight_kg} kg` : 'Não informado'}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Meta de Peso</span>
              <span className="text-sm font-semibold text-gray-900">
                {user?.target_weight_kg ? `${user.target_weight_kg} kg` : 'Não definido'}
              </span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Experiência</span>
              <span className="text-sm font-semibold text-gray-900">
                {user?.training_experience_years || 0} anos
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Progress Indicator */}
      {stats && stats.total_trainings > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Taxa de Conclusão</h3>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{
                width: `${((stats.completed_trainings / stats.total_trainings) * 100)}%`
              }}
            ></div>
          </div>
          <p className="text-sm text-gray-600 mt-2">
            {Math.round((stats.completed_trainings / stats.total_trainings) * 100)}% dos treinos concluídos
          </p>
        </div>
      )}
    </div>
  )
} 