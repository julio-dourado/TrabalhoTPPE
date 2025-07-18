import { useState, useEffect } from 'react'
import Layout from '@/components/Layout'
import { Plus, Edit2, Trash2, Dumbbell, Weight, Timer, Search } from 'lucide-react'

interface Exercise {
  id: number
  name: string
  muscle_group?: string
  difficulty: string
  sets: number
  reps: number
  comment?: string
  instructions?: string
  rest_time_sec: number
  exercise_type: 'WITH_WEIGHT' | 'WITHOUT_WEIGHT'
  with_weight?: {
    weight_kg: number
  }
  without_weight?: {
    time_sec?: number
    distance_m?: number
    intensity?: string
  }
  created_at: string
}

export default function Exercises() {
  const [exercises, setExercises] = useState<Exercise[]>([])
  const [filteredExercises, setFilteredExercises] = useState<Exercise[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [selectedExercise, setSelectedExercise] = useState<Exercise | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterType, setFilterType] = useState<string>('ALL')
  const [filterMuscle, setFilterMuscle] = useState<string>('ALL')
  const [formData, setFormData] = useState({
    name: '',
    muscle_group: 'CHEST',
    difficulty: 'BEGINNER',
    sets: 3,
    reps: 10,
    comment: '',
    instructions: '',
    rest_time_sec: 60,
    exercise_type: 'WITH_WEIGHT' as 'WITH_WEIGHT' | 'WITHOUT_WEIGHT',
    weight_kg: 0,
    time_sec: 0,
    distance_m: 0,
    intensity: 'moderate'
  })

  useEffect(() => {
    fetchExercises()
  }, [])

  useEffect(() => {
    filterExercises()
  }, [exercises, searchTerm, filterType, filterMuscle])

  const fetchExercises = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('http://localhost:8000/api/v1/exercises/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        setExercises(data)
      }
    } catch (error) {
      console.error('Erro ao buscar exercícios:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const filterExercises = () => {
    let filtered = exercises.filter(exercise =>
      exercise.name.toLowerCase().includes(searchTerm.toLowerCase())
    )

    if (filterType !== 'ALL') {
      filtered = filtered.filter(exercise => exercise.exercise_type === filterType)
    }

    if (filterMuscle !== 'ALL') {
      filtered = filtered.filter(exercise => exercise.muscle_group === filterMuscle)
    }

    setFilteredExercises(filtered)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const token = localStorage.getItem('token')

      // Preparar dados do exercício
      const exerciseData: any = {
        name: formData.name,
        muscle_group: formData.muscle_group,
        difficulty: formData.difficulty,
        sets: formData.sets,
        reps: formData.reps,
        comment: formData.comment,
        instructions: formData.instructions,
        rest_time_sec: formData.rest_time_sec,
        exercise_type: formData.exercise_type
      }

      // Adicionar dados específicos do tipo
      if (formData.exercise_type === 'WITH_WEIGHT') {
        exerciseData.with_weight = {
          weight_kg: formData.weight_kg
        }
      } else {
        exerciseData.without_weight = {
          time_sec: formData.time_sec,
          distance_m: formData.distance_m,
          intensity: formData.intensity
        }
      }

      const url = selectedExercise
        ? `http://localhost:8000/api/v1/exercises/${selectedExercise.id}`
        : 'http://localhost:8000/api/v1/exercises/'

      const response = await fetch(url, {
        method: selectedExercise ? 'PUT' : 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(exerciseData)
      })

      if (response.ok) {
        fetchExercises()
        setShowModal(false)
        resetForm()
      }
    } catch (error) {
      console.error('Erro ao salvar exercício:', error)
    }
  }

  const handleDelete = async (id: number) => {
    if (confirm('Tem certeza que deseja excluir este exercício?')) {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`http://localhost:8000/api/v1/exercises/${id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (response.ok) {
          fetchExercises()
        }
      } catch (error) {
        console.error('Erro ao deletar exercício:', error)
      }
    }
  }

  const resetForm = () => {
    setFormData({
      name: '',
      muscle_group: 'CHEST',
      difficulty: 'BEGINNER',
      sets: 3,
      reps: 10,
      comment: '',
      instructions: '',
      rest_time_sec: 60,
      exercise_type: 'WITH_WEIGHT',
      weight_kg: 0,
      time_sec: 0,
      distance_m: 0,
      intensity: 'moderate'
    })
    setSelectedExercise(null)
  }

  const openModal = (exercise?: Exercise) => {
    if (exercise) {
      setSelectedExercise(exercise)
      setFormData({
        name: exercise.name,
        muscle_group: exercise.muscle_group || 'CHEST',
        difficulty: exercise.difficulty,
        sets: exercise.sets,
        reps: exercise.reps,
        comment: exercise.comment || '',
        instructions: exercise.instructions || '',
        rest_time_sec: exercise.rest_time_sec,
        exercise_type: exercise.exercise_type,
        weight_kg: exercise.with_weight?.weight_kg || 0,
        time_sec: exercise.without_weight?.time_sec || 0,
        distance_m: exercise.without_weight?.distance_m || 0,
        intensity: exercise.without_weight?.intensity || 'moderate'
      })
    } else {
      resetForm()
    }
    setShowModal(true)
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'BEGINNER': return 'bg-green-100 text-green-800'
      case 'INTERMEDIATE': return 'bg-yellow-100 text-yellow-800'
      case 'ADVANCED': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const muscleGroups = [
    'CHEST', 'BACK', 'SHOULDERS', 'BICEPS', 'TRICEPS', 'LEGS', 'CORE', 'CARDIO', 'OTHER'
  ]

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
            <h1 className="text-3xl font-bold text-gray-900">Exercícios</h1>
            <p className="text-gray-600">Gerencie seu catálogo de exercícios</p>
          </div>
          <button
            onClick={() => openModal()}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
          >
            <Plus className="h-5 w-5" />
            Novo Exercício
          </button>
        </div>

        {/* Filtros */}
        <div className="bg-white rounded-lg shadow p-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Buscar exercícios..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="ALL">Todos os tipos</option>
              <option value="WITH_WEIGHT">Com peso</option>
              <option value="WITHOUT_WEIGHT">Sem peso</option>
            </select>

            <select
              value={filterMuscle}
              onChange={(e) => setFilterMuscle(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="ALL">Todos os grupos</option>
              {muscleGroups.map(muscle => (
                <option key={muscle} value={muscle}>{muscle}</option>
              ))}
            </select>

            <div className="text-sm text-gray-600 flex items-center">
              {filteredExercises.length} exercício(s) encontrado(s)
            </div>
          </div>
        </div>

        {/* Lista de Exercícios */}
        {filteredExercises.length === 0 ? (
          <div className="text-center py-12">
            <Dumbbell className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {exercises.length === 0 ? 'Nenhum exercício cadastrado' : 'Nenhum exercício encontrado'}
            </h3>
            <p className="text-gray-500 mb-4">
              {exercises.length === 0
                ? 'Crie seu primeiro exercício para começar'
                : 'Tente ajustar os filtros de busca'
              }
            </p>
            {exercises.length === 0 && (
              <button
                onClick={() => openModal()}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
              >
                Criar Exercício
              </button>
            )}
          </div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {filteredExercises.map((exercise) => (
              <div key={exercise.id} className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">{exercise.name}</h3>
                  <div className="flex gap-2">
                    <button
                      onClick={() => openModal(exercise)}
                      className="text-gray-600 hover:text-gray-800"
                      title="Editar"
                    >
                      <Edit2 className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDelete(exercise.id)}
                      className="text-red-600 hover:text-red-800"
                      title="Excluir"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>

                <div className="space-y-3">
                  <div className="flex gap-2">
                    <span className="px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {exercise.muscle_group}
                    </span>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(exercise.difficulty)}`}>
                      {exercise.difficulty}
                    </span>
                  </div>

                  <div className="grid grid-cols-2 gap-4 text-sm text-gray-600">
                    <div className="flex items-center gap-1">
                      <Dumbbell className="h-4 w-4" />
                      {exercise.sets}x{exercise.reps}
                    </div>
                    <div className="flex items-center gap-1">
                      <Timer className="h-4 w-4" />
                      {exercise.rest_time_sec}s
                    </div>
                  </div>

                  {exercise.exercise_type === 'WITH_WEIGHT' && exercise.with_weight && (
                    <div className="flex items-center gap-1 text-sm text-blue-600">
                      <Weight className="h-4 w-4" />
                      {exercise.with_weight.weight_kg} kg
                    </div>
                  )}

                  {exercise.exercise_type === 'WITHOUT_WEIGHT' && exercise.without_weight && (
                    <div className="text-sm text-green-600">
                      {exercise.without_weight.time_sec && (
                        <div>{exercise.without_weight.time_sec}s</div>
                      )}
                      {exercise.without_weight.distance_m && (
                        <div>{exercise.without_weight.distance_m}m</div>
                      )}
                    </div>
                  )}

                  {exercise.comment && (
                    <p className="text-sm text-gray-500 italic">"{exercise.comment}"</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Modal */}
        {showModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
              <h2 className="text-xl font-bold mb-4">
                {selectedExercise ? 'Editar Exercício' : 'Novo Exercício'}
              </h2>

              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
                      Grupo Muscular
                    </label>
                    <select
                      value={formData.muscle_group}
                      onChange={(e) => setFormData({ ...formData, muscle_group: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      {muscleGroups.map(muscle => (
                        <option key={muscle} value={muscle}>{muscle}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Dificuldade
                    </label>
                    <select
                      value={formData.difficulty}
                      onChange={(e) => setFormData({ ...formData, difficulty: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="BEGINNER">Iniciante</option>
                      <option value="INTERMEDIATE">Intermediário</option>
                      <option value="ADVANCED">Avançado</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Tipo de Exercício
                    </label>
                    <select
                      value={formData.exercise_type}
                      onChange={(e) => setFormData({ ...formData, exercise_type: e.target.value as 'WITH_WEIGHT' | 'WITHOUT_WEIGHT' })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="WITH_WEIGHT">Com Peso</option>
                      <option value="WITHOUT_WEIGHT">Sem Peso</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Séries
                    </label>
                    <input
                      type="number"
                      value={formData.sets}
                      onChange={(e) => setFormData({ ...formData, sets: parseInt(e.target.value) })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      min="1"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Repetições
                    </label>
                    <input
                      type="number"
                      value={formData.reps}
                      onChange={(e) => setFormData({ ...formData, reps: parseInt(e.target.value) })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      min="1"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Descanso (segundos)
                    </label>
                    <input
                      type="number"
                      value={formData.rest_time_sec}
                      onChange={(e) => setFormData({ ...formData, rest_time_sec: parseInt(e.target.value) })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      min="0"
                    />
                  </div>

                  {formData.exercise_type === 'WITH_WEIGHT' && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Peso (kg)
                      </label>
                      <input
                        type="number"
                        value={formData.weight_kg}
                        onChange={(e) => setFormData({ ...formData, weight_kg: parseFloat(e.target.value) })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        min="0"
                        step="0.5"
                      />
                    </div>
                  )}

                  {formData.exercise_type === 'WITHOUT_WEIGHT' && (
                    <>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Tempo (segundos)
                        </label>
                        <input
                          type="number"
                          value={formData.time_sec}
                          onChange={(e) => setFormData({ ...formData, time_sec: parseInt(e.target.value) })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                          min="0"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Distância (metros)
                        </label>
                        <input
                          type="number"
                          value={formData.distance_m}
                          onChange={(e) => setFormData({ ...formData, distance_m: parseFloat(e.target.value) })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                          min="0"
                          step="0.1"
                        />
                      </div>
                    </>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Comentário
                  </label>
                  <input
                    type="text"
                    value={formData.comment}
                    onChange={(e) => setFormData({ ...formData, comment: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Instruções
                  </label>
                  <textarea
                    value={formData.instructions}
                    onChange={(e) => setFormData({ ...formData, instructions: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows={3}
                  />
                </div>

                <div className="flex gap-3 pt-4">
                  <button
                    type="submit"
                    className="flex-1 bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700"
                  >
                    {selectedExercise ? 'Atualizar' : 'Criar'}
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