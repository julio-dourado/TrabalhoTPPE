import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import Layout from '@/components/Layout'
import { Plus, Edit2, Trash2, Eye, Calendar, Clock, Activity } from 'lucide-react'

interface Training {
  id: number
  name: string
  description?: string
  category: string
  status: string
  estimated_duration_min: number
  user_id: number
  created_at: string
}

export default function Trainings() {
  const [trainings, setTrainings] = useState<Training[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [selectedTraining, setSelectedTraining] = useState<Training | null>(null)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    category: 'STRENGTH',
    estimated_duration_min: 60
  })
  const router = useRouter()

  useEffect(() => {
    fetchTrainings()
  }, [])

  const fetchTrainings = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('http://localhost:8000/api/v1/trainings/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        setTrainings(data)
      }
    } catch (error) {
      console.error('Erro ao buscar treinos:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const token = localStorage.getItem('token')
      const url = selectedTraining
        ? `http://localhost:8000/api/v1/trainings/${selectedTraining.id}`
        : 'http://localhost:8000/api/v1/trainings/'

      const response = await fetch(url, {
        method: selectedTraining ? 'PUT' : 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      })

      if (response.ok) {
        fetchTrainings()
        setShowModal(false)
        resetForm()
      }
    } catch (error) {
      console.error('Erro ao salvar treino:', error)
    }
  }

  const handleDelete = async (id: number) => {
    if (confirm('Tem certeza que deseja excluir este treino?')) {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`http://localhost:8000/api/v1/trainings/${id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (response.ok) {
          fetchTrainings()
        }
      } catch (error) {
        console.error('Erro ao deletar treino:', error)
      }
    }
  }

  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      category: 'STRENGTH',
      estimated_duration_min: 60
    })
    setSelectedTraining(null)
  }

  const openModal = (training?: Training) => {
    if (training) {
      setSelectedTraining(training)
      setFormData({
        name: training.name,
        description: training.description || '',
        category: training.category,
        estimated_duration_min: training.estimated_duration_min
      })
    } else {
      resetForm()
    }
    setShowModal(true)
  }

  const viewTrainingExercises = (trainingId: number) => {
    router.push(`/trainings/${trainingId}/exercises`)
  }

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'STRENGTH': return 'bg-red-100 text-red-800'
      case 'CARDIO': return 'bg-blue-100 text-blue-800'
      case 'FLEXIBILITY': return 'bg-green-100 text-green-800'
      case 'MIXED': return 'bg-purple-100 text-purple-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'PLANNED': return 'bg-yellow-100 text-yellow-800'
      case 'IN_PROGRESS': return 'bg-blue-100 text-blue-800'
      case 'COMPLETED': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  if (isLoading) {
    return (
      <Layout>
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Meus Treinos</h1>
            <p className="text-gray-600">Gerencie seus treinos e acompanhe seu progresso</p>
          </div>
          <button
            onClick={() => openModal()}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
          >
            <Plus className="h-5 w-5" />
            Novo Treino
          </button>
        </div>

        {/* Lista de Treinos */}
        {trainings.length === 0 ? (
          <div className="text-center py-12">
            <Activity className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Nenhum treino encontrado</h3>
            <p className="text-gray-500 mb-4">Crie seu primeiro treino para começar</p>
            <button
              onClick={() => openModal()}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
            >
              Criar Treino
            </button>
          </div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {trainings.map((training) => (
              <div key={training.id} className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">{training.name}</h3>
                  <div className="flex gap-2">
                    <button
                      onClick={() => viewTrainingExercises(training.id)}
                      className="text-blue-600 hover:text-blue-800"
                      title="Ver exercícios"
                    >
                      <Eye className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => openModal(training)}
                      className="text-gray-600 hover:text-gray-800"
                      title="Editar"
                    >
                      <Edit2 className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDelete(training.id)}
                      className="text-red-600 hover:text-red-800"
                      title="Excluir"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>

                {training.description && (
                  <p className="text-gray-600 text-sm mb-4">{training.description}</p>
                )}

                <div className="flex gap-2 mb-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getCategoryColor(training.category)}`}>
                    {training.category}
                  </span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(training.status)}`}>
                    {training.status}
                  </span>
                </div>

                <div className="flex items-center gap-4 text-sm text-gray-500">
                  <div className="flex items-center gap-1">
                    <Clock className="h-4 w-4" />
                    {training.estimated_duration_min} min
                  </div>
                  <div className="flex items-center gap-1">
                    <Calendar className="h-4 w-4" />
                    {new Date(training.created_at).toLocaleDateString()}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Modal */}
        {showModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md">
              <h2 className="text-xl font-bold mb-4">
                {selectedTraining ? 'Editar Treino' : 'Novo Treino'}
              </h2>

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nome *
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Descrição
                  </label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows={3}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Categoria
                  </label>
                  <select
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="STRENGTH">Força</option>
                    <option value="CARDIO">Cardio</option>
                    <option value="FLEXIBILITY">Flexibilidade</option>
                    <option value="MIXED">Misto</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Duração Estimada (minutos)
                  </label>
                  <input
                    type="number"
                    value={formData.estimated_duration_min}
                    onChange={(e) => setFormData({ ...formData, estimated_duration_min: parseInt(e.target.value) })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    min="1"
                    required
                  />
                </div>

                <div className="flex gap-3 pt-4">
                  <button
                    type="submit"
                    className="flex-1 bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700"
                  >
                    {selectedTraining ? 'Atualizar' : 'Criar'}
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowModal(false)}
                    className="flex-1 bg-gray-300 text-gray-700 py-2 rounded-md hover:bg-gray-400"
                  >
                    Cancelar
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </Layout>
  )
} 