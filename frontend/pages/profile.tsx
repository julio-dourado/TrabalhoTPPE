import { useState, useEffect } from 'react'
import Layout from '@/components/Layout'
import { User, Mail, Calendar, Ruler, Weight, Target, Trophy, Save, Lock } from 'lucide-react'

interface UserProfile {
  id: number
  name: string
  email: string
  birth_date?: string
  gender: string
  height_cm?: number
  weight_kg?: number
  activity_level: string
  main_goal: string
  training_experience_years?: number
  bio?: string
  target_weight_kg?: number
  is_active: boolean
  is_premium: boolean
  created_at: string
}

export default function Profile() {
  const [user, setUser] = useState<UserProfile | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isEditing, setIsEditing] = useState(false)
  const [showPasswordModal, setShowPasswordModal] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    birth_date: '',
    gender: 'not_informed',
    height_cm: '',
    weight_kg: '',
    activity_level: 'sedentary',
    main_goal: 'general_health',
    training_experience_years: '',
    bio: '',
    target_weight_kg: ''
  })
  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  })

  useEffect(() => {
    fetchUserProfile()
  }, [])

  const fetchUserProfile = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('http://localhost:8000/api/v1/users/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      if (response.ok) {
        const userData = await response.json()
        setUser(userData)
        setFormData({
          name: userData.name || '',
          email: userData.email || '',
          birth_date: userData.birth_date ? userData.birth_date.split('T')[0] : '',
          gender: userData.gender || 'not_informed',
          height_cm: userData.height_cm?.toString() || '',
          weight_kg: userData.weight_kg?.toString() || '',
          activity_level: userData.activity_level || 'sedentary',
          main_goal: userData.main_goal || 'general_health',
          training_experience_years: userData.training_experience_years?.toString() || '',
          bio: userData.bio || '',
          target_weight_kg: userData.target_weight_kg?.toString() || ''
        })
      }
    } catch (error) {
      console.error('Erro ao buscar perfil:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const token = localStorage.getItem('token')
      
      const profileData = {
        ...formData,
        height_cm: formData.height_cm ? parseInt(formData.height_cm) : null,
        weight_kg: formData.weight_kg ? parseFloat(formData.weight_kg) : null,
        target_weight_kg: formData.target_weight_kg ? parseFloat(formData.target_weight_kg) : null,
        training_experience_years: formData.training_experience_years ? parseInt(formData.training_experience_years) : null
      }

      const response = await fetch('http://localhost:8000/api/v1/users/me', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(profileData)
      })

      if (response.ok) {
        setIsEditing(false)
        fetchUserProfile()
        alert('Perfil atualizado com sucesso!')
      } else {
        alert('Erro ao atualizar perfil')
      }
    } catch (error) {
      console.error('Erro ao salvar perfil:', error)
      alert('Erro ao salvar perfil')
    }
  }

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (passwordData.new_password !== passwordData.confirm_password) {
      alert('As senhas não coincidem')
      return
    }

    try {
      const token = localStorage.getItem('token')
      const response = await fetch('http://localhost:8000/api/v1/users/change-password', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          current_password: passwordData.current_password,
          new_password: passwordData.new_password
        })
      })

      if (response.ok) {
        setShowPasswordModal(false)
        setPasswordData({ current_password: '', new_password: '', confirm_password: '' })
        alert('Senha alterada com sucesso!')
      } else {
        alert('Erro ao alterar senha. Verifique a senha atual.')
      }
    } catch (error) {
      console.error('Erro ao alterar senha:', error)
      alert('Erro ao alterar senha')
    }
  }

  const calculateAge = (birthDate: string) => {
    const today = new Date()
    const birth = new Date(birthDate)
    let age = today.getFullYear() - birth.getFullYear()
    const monthDiff = today.getMonth() - birth.getMonth()
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--
    }
    
    return age
  }

  const calculateBMI = (weight: number, height: number) => {
    const heightInMeters = height / 100
    return (weight / (heightInMeters * heightInMeters)).toFixed(1)
  }

  const getBMICategory = (bmi: number) => {
    if (bmi < 18.5) return { category: 'Abaixo do peso', color: 'text-blue-600' }
    if (bmi < 25) return { category: 'Peso normal', color: 'text-green-600' }
    if (bmi < 30) return { category: 'Sobrepeso', color: 'text-yellow-600' }
    return { category: 'Obeso', color: 'text-red-600' }
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

  if (!user) {
    return (
      <Layout>
        <div className="text-center py-12">
          <p className="text-gray-500">Erro ao carregar perfil</p>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Meu Perfil</h1>
            <p className="text-gray-600">Gerencie suas informações pessoais</p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setShowPasswordModal(true)}
              className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 flex items-center gap-2"
            >
              <Lock className="h-4 w-4" />
              Alterar Senha
            </button>
            {!isEditing ? (
              <button
                onClick={() => setIsEditing(true)}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
              >
                Editar Perfil
              </button>
            ) : (
              <div className="flex gap-2">
                <button
                  onClick={handleSaveProfile}
                  className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center gap-2"
                >
                  <Save className="h-4 w-4" />
                  Salvar
                </button>
                <button
                  onClick={() => {
                    setIsEditing(false)
                    fetchUserProfile()
                  }}
                  className="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400"
                >
                  Cancelar
                </button>
              </div>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Informações Básicas */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <User className="h-5 w-5 text-blue-600" />
                Informações Básicas
              </h2>

              <form onSubmit={handleSaveProfile} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Nome Completo
                    </label>
                    {isEditing ? (
                      <input
                        type="text"
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    ) : (
                      <p className="py-2 text-gray-900">{user.name}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Email
                    </label>
                    {isEditing ? (
                      <input
                        type="email"
                        value={formData.email}
                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    ) : (
                      <p className="py-2 text-gray-900">{user.email}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Data de Nascimento
                    </label>
                    {isEditing ? (
                      <input
                        type="date"
                        value={formData.birth_date}
                        onChange={(e) => setFormData({ ...formData, birth_date: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    ) : (
                      <p className="py-2 text-gray-900">
                        {user.birth_date 
                          ? `${new Date(user.birth_date).toLocaleDateString()} (${calculateAge(user.birth_date)} anos)`
                          : 'Não informado'
                        }
                      </p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Gênero
                    </label>
                    {isEditing ? (
                      <select
                        value={formData.gender}
                        onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="not_informed">Não informado</option>
                        <option value="male">Masculino</option>
                        <option value="female">Feminino</option>
                        <option value="other">Outro</option>
                      </select>
                    ) : (
                      <p className="py-2 text-gray-900">
                        {user.gender === 'male' ? 'Masculino' : 
                         user.gender === 'female' ? 'Feminino' :
                         user.gender === 'other' ? 'Outro' : 'Não informado'}
                      </p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Altura (cm)
                    </label>
                    {isEditing ? (
                      <input
                        type="number"
                        value={formData.height_cm}
                        onChange={(e) => setFormData({ ...formData, height_cm: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        min="100"
                        max="250"
                      />
                    ) : (
                      <p className="py-2 text-gray-900">
                        {user.height_cm ? `${user.height_cm} cm` : 'Não informado'}
                      </p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Peso Atual (kg)
                    </label>
                    {isEditing ? (
                      <input
                        type="number"
                        value={formData.weight_kg}
                        onChange={(e) => setFormData({ ...formData, weight_kg: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        min="30"
                        max="300"
                        step="0.1"
                      />
                    ) : (
                      <p className="py-2 text-gray-900">
                        {user.weight_kg ? `${user.weight_kg} kg` : 'Não informado'}
                      </p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Peso Meta (kg)
                    </label>
                    {isEditing ? (
                      <input
                        type="number"
                        value={formData.target_weight_kg}
                        onChange={(e) => setFormData({ ...formData, target_weight_kg: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        min="30"
                        max="300"
                        step="0.1"
                      />
                    ) : (
                      <p className="py-2 text-gray-900">
                        {user.target_weight_kg ? `${user.target_weight_kg} kg` : 'Não informado'}
                      </p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Experiência (anos)
                    </label>
                    {isEditing ? (
                      <input
                        type="number"
                        value={formData.training_experience_years}
                        onChange={(e) => setFormData({ ...formData, training_experience_years: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        min="0"
                        max="50"
                      />
                    ) : (
                      <p className="py-2 text-gray-900">
                        {user.training_experience_years ? `${user.training_experience_years} anos` : 'Não informado'}
                      </p>
                    )}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nível de Atividade
                  </label>
                  {isEditing ? (
                    <select
                      value={formData.activity_level}
                      onChange={(e) => setFormData({ ...formData, activity_level: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="sedentary">Sedentário</option>
                      <option value="lightly_active">Levemente ativo</option>
                      <option value="moderately_active">Moderadamente ativo</option>
                      <option value="very_active">Muito ativo</option>
                      <option value="extremely_active">Extremamente ativo</option>
                    </select>
                  ) : (
                    <p className="py-2 text-gray-900">
                      {user.activity_level === 'sedentary' ? 'Sedentário' :
                       user.activity_level === 'lightly_active' ? 'Levemente ativo' :
                       user.activity_level === 'moderately_active' ? 'Moderadamente ativo' :
                       user.activity_level === 'very_active' ? 'Muito ativo' :
                       user.activity_level === 'extremely_active' ? 'Extremamente ativo' : 'Não informado'}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Objetivo Principal
                  </label>
                  {isEditing ? (
                    <select
                      value={formData.main_goal}
                      onChange={(e) => setFormData({ ...formData, main_goal: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="general_health">Saúde geral</option>
                      <option value="weight_loss">Perda de peso</option>
                      <option value="weight_gain">Ganho de peso</option>
                      <option value="muscle_gain">Ganho de massa muscular</option>
                      <option value="strength">Aumento de força</option>
                      <option value="endurance">Resistência</option>
                      <option value="flexibility">Flexibilidade</option>
                    </select>
                  ) : (
                    <p className="py-2 text-gray-900">
                      {user.main_goal === 'general_health' ? 'Saúde geral' :
                       user.main_goal === 'weight_loss' ? 'Perda de peso' :
                       user.main_goal === 'weight_gain' ? 'Ganho de peso' :
                       user.main_goal === 'muscle_gain' ? 'Ganho de massa muscular' :
                       user.main_goal === 'strength' ? 'Aumento de força' :
                       user.main_goal === 'endurance' ? 'Resistência' :
                       user.main_goal === 'flexibility' ? 'Flexibilidade' : 'Não informado'}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Bio
                  </label>
                  {isEditing ? (
                    <textarea
                      value={formData.bio}
                      onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      rows={3}
                      placeholder="Conte um pouco sobre você..."
                    />
                  ) : (
                    <p className="py-2 text-gray-900">{user.bio || 'Nenhuma informação adicionada'}</p>
                  )}
                </div>
              </form>
            </div>
          </div>

          {/* Estatísticas */}
          <div className="space-y-6">
            {/* IMC */}
            {user.weight_kg && user.height_cm && (
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                  <Weight className="h-5 w-5 text-green-600" />
                  Índice de Massa Corporal
                </h3>
                <div className="text-center">
                  <div className="text-3xl font-bold text-gray-900 mb-1">
                    {calculateBMI(user.weight_kg, user.height_cm)}
                  </div>
                  <div className={`text-sm font-medium ${getBMICategory(parseFloat(calculateBMI(user.weight_kg, user.height_cm))).color}`}>
                    {getBMICategory(parseFloat(calculateBMI(user.weight_kg, user.height_cm))).category}
                  </div>
                </div>
              </div>
            )}

            {/* Status da Conta */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                <Trophy className="h-5 w-5 text-yellow-600" />
                Status da Conta
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Status:</span>
                  <span className={`font-medium ${user.is_active ? 'text-green-600' : 'text-red-600'}`}>
                    {user.is_active ? 'Ativo' : 'Inativo'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Plano:</span>
                  <span className={`font-medium ${user.is_premium ? 'text-purple-600' : 'text-gray-600'}`}>
                    {user.is_premium ? 'Premium' : 'Gratuito'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Membro desde:</span>
                  <span className="font-medium text-gray-900">
                    {new Date(user.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Modal de Alteração de Senha */}
        {showPasswordModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md">
              <h2 className="text-xl font-bold mb-4">Alterar Senha</h2>
              
              <form onSubmit={handleChangePassword} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Senha Atual
                  </label>
                  <input
                    type="password"
                    value={passwordData.current_password}
                    onChange={(e) => setPasswordData({ ...passwordData, current_password: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nova Senha
                  </label>
                  <input
                    type="password"
                    value={passwordData.new_password}
                    onChange={(e) => setPasswordData({ ...passwordData, new_password: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                    minLength={6}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Confirmar Nova Senha
                  </label>
                  <input
                    type="password"
                    value={passwordData.confirm_password}
                    onChange={(e) => setPasswordData({ ...passwordData, confirm_password: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                    minLength={6}
                  />
                </div>

                <div className="flex gap-3 pt-4">
                  <button
                    type="submit"
                    className="flex-1 bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700"
                  >
                    Alterar Senha
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setShowPasswordModal(false)
                      setPasswordData({ current_password: '', new_password: '', confirm_password: '' })
                    }}
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