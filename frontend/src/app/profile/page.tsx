'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { userAPI, User, treinoAPI, Treino } from '@/lib/api';

export default function ProfilePage() {
  const [user, setUser] = useState<User | null>(null);
  const [treinos, setTreinos] = useState<Treino[]>([]);
  const [showEditForm, setShowEditForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [userResponse, treinosResponse] = await Promise.all([
        userAPI.getProfile(),
        treinoAPI.getAll(),
      ]);

      setUser(userResponse.data);
      setTreinos(treinosResponse.data);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <div className="relative w-16 h-16">
            <div className="absolute inset-0 border-4 border-primary-200 rounded-full"></div>
            <div className="absolute inset-0 border-4 border-primary-600 rounded-full border-t-transparent animate-spin"></div>
          </div>
          <p className="text-gray-600 font-medium">Carregando perfil...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">😕</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Erro ao carregar perfil</h2>
          <p className="text-gray-600 mb-6">Não foi possível carregar suas informações</p>
          <button
            onClick={() => router.push('/dashboard')}
            className="bg-primary-500 hover:bg-primary-600 text-white px-6 py-3 rounded-lg font-medium transition-colors"
          >
            Voltar ao Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header Section */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Meu Perfil</h1>
              <p className="text-gray-600 mt-1">Gerencie suas informações pessoais e configurações</p>
            </div>
            <button
              onClick={() => router.push('/dashboard')}
              className="text-gray-500 hover:text-gray-700 flex items-center space-x-2 transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
              <span>Voltar ao Dashboard</span>
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Profile Card */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
              {/* Profile Header */}
              <div className="bg-gradient-to-br from-primary-500 to-primary-600 px-6 py-8">
                <div className="text-center">
                  <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg">
                    <span className="text-primary-600 font-bold text-2xl">
                      {user.nome.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <h2 className="text-xl font-bold text-white">{user.nome}</h2>
                  <p className="text-primary-100 mt-1">{user.email}</p>
                </div>
              </div>

              {/* Profile Details */}
              <div className="p-6 space-y-6">
                <button
                  onClick={() => setShowEditForm(true)}
                  className="w-full bg-primary-500 hover:bg-primary-600 text-white px-4 py-3 rounded-lg font-semibold transition-colors shadow-sm hover:shadow-md"
                >
                  Editar Perfil
                </button>

                <div className="space-y-4">
                  <div className="flex items-center justify-between py-3 border-b border-gray-100">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-blue-50 rounded-lg flex items-center justify-center">
                        <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3a1 1 0 011-1h6a1 1 0 011 1v4h3a2 2 0 012 2v1a2 2 0 01-2 2H4a2 2 0 01-2-2V9a2 2 0 012-2h4z" />
                        </svg>
                      </div>
                      <span className="text-gray-600 text-sm font-medium">Membro desde</span>
                    </div>
                    <span className="font-semibold text-gray-900 text-sm">
                      {new Date(user.created_at).toLocaleDateString('pt-BR', {
                        year: 'numeric',
                        month: 'long'
                      })}
                    </span>
                  </div>

                  <div className="flex items-center justify-between py-3">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-green-50 rounded-lg flex items-center justify-center">
                        <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                      <span className="text-gray-600 text-sm font-medium">Status da conta</span>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${user.is_active
                        ? 'bg-green-100 text-green-700'
                        : 'bg-red-100 text-red-700'
                      }`}>
                      {user.is_active ? 'Ativo' : 'Inativo'}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Stats Overview */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <StatCard
                title="Treinos"
                value={treinos.length.toString()}
                subtitle="criados"
                icon="💪"
                color="blue"
              />
              <StatCard
                title="Exercícios"
                value="42"
                subtitle="realizados"
                icon="🏋️"
                color="green"
              />
              <StatCard
                title="Streak"
                value="7"
                subtitle="dias"
                icon="🔥"
                color="orange"
              />
              <StatCard
                title="Meta"
                value="85%"
                subtitle="concluída"
                icon="🎯"
                color="purple"
              />
            </div>

            {/* Workouts Section */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h3 className="text-xl font-semibold text-gray-900">Meus Treinos</h3>
                  <p className="text-gray-500 text-sm mt-1">Gerencie e organize seus treinos</p>
                </div>
                <button
                  onClick={() => router.push('/treinos/new')}
                  className="bg-primary-500 hover:bg-primary-600 text-white px-4 py-2 rounded-lg font-medium transition-colors text-sm shadow-sm hover:shadow-md"
                >
                  + Novo Treino
                </button>
              </div>

              {treinos.length === 0 ? (
                <div className="text-center py-12">
                  <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-2xl">📝</span>
                  </div>
                  <h4 className="text-lg font-semibold text-gray-900 mb-2">Nenhum treino criado</h4>
                  <p className="text-gray-600 mb-6 max-w-sm mx-auto">
                    Crie seu primeiro treino para começar a organizar seus exercícios
                  </p>
                  <button
                    onClick={() => router.push('/treinos/new')}
                    className="bg-primary-500 hover:bg-primary-600 text-white px-6 py-3 rounded-lg font-medium transition-colors shadow-sm hover:shadow-md"
                  >
                    Criar Primeiro Treino
                  </button>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {treinos.map((treino) => (
                    <WorkoutCard
                      key={treino.id}
                      treino={treino}
                      onClick={() => router.push(`/treinos/${treino.id}`)}
                    />
                  ))}
                </div>
              )}

              {treinos.length > 0 && (
                <div className="mt-6 text-center">
                  <button
                    onClick={() => router.push('/treinos')}
                    className="text-primary-600 hover:text-primary-700 font-medium text-sm hover:underline transition-colors"
                  >
                    Ver todos os treinos →
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Edit Profile Modal */}
      {showEditForm && (
        <EditProfileModal
          user={user}
          onClose={() => setShowEditForm(false)}
          onSave={(updatedUser) => {
            setUser(updatedUser);
            setShowEditForm(false);
          }}
        />
      )}
    </div>
  );
}

// Components
interface StatCardProps {
  title: string;
  value: string;
  subtitle: string;
  icon: string;
  color: 'blue' | 'green' | 'orange' | 'purple';
}

function StatCard({ title, value, subtitle, icon, color }: StatCardProps) {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-green-50 text-green-600',
    orange: 'bg-orange-50 text-orange-600',
    purple: 'bg-purple-50 text-purple-600'
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-3">
        <div className={`p-2 rounded-lg ${colorClasses[color]}`}>
          <span className="text-lg">{icon}</span>
        </div>
      </div>
      <div>
        <h3 className="text-2xl font-bold text-gray-900">{value}</h3>
        <p className="text-gray-600 text-sm font-medium">{title}</p>
        <p className="text-gray-400 text-xs">{subtitle}</p>
      </div>
    </div>
  );
}

interface WorkoutCardProps {
  treino: Treino;
  onClick: () => void;
}

function WorkoutCard({ treino, onClick }: WorkoutCardProps) {
  return (
    <div
      className="bg-gray-50 hover:bg-gray-100 border border-gray-200 hover:border-primary-300 p-4 rounded-lg cursor-pointer transition-all duration-200 group"
      onClick={onClick}
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h4 className="font-semibold text-gray-900 group-hover:text-primary-700 transition-colors">
            {treino.nome}
          </h4>
          <p className="text-gray-600 text-sm mt-1">
            {treino.descricao || 'Sem descrição'}
          </p>
        </div>
        <svg className="w-5 h-5 text-gray-400 group-hover:text-primary-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
        </svg>
      </div>
      <div className="flex items-center justify-between">
        <span className="text-xs bg-primary-100 text-primary-700 px-2 py-1 rounded font-medium">
          Treino Ativo
        </span>
        <span className="text-xs text-gray-500">
          {new Date(treino.created_at).toLocaleDateString('pt-BR')}
        </span>
      </div>
    </div>
  );
}

interface EditProfileModalProps {
  user: User;
  onClose: () => void;
  onSave: (user: User) => void;
}

function EditProfileModal({ user, onClose, onSave }: EditProfileModalProps) {
  const [formData, setFormData] = useState({
    nome: user.nome,
    email: user.email,
    password: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const updateData: Record<string, unknown> = {
        nome: formData.nome,
        email: formData.email,
      };

      if (formData.password) {
        updateData.password = formData.password;
      }

      const response = await userAPI.updateProfile(updateData);
      onSave(response.data);
    } catch (error) {
      console.error('Erro ao atualizar perfil:', error);
      setError('Erro ao atualizar perfil. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-md max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-900">Editar Perfil</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-gray-800 mb-2">Nome completo</label>
              <input
                type="text"
                name="nome"
                required
                value={formData.nome}
                onChange={handleChange}
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary-500 text-gray-900 transition-colors"
                placeholder="Seu nome completo"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-800 mb-2">Email</label>
              <input
                type="email"
                name="email"
                required
                value={formData.email}
                onChange={handleChange}
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary-500 text-gray-900 transition-colors"
                placeholder="seu@email.com"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-800 mb-2">
                Nova senha (opcional)
              </label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary-500 text-gray-900 transition-colors"
                placeholder="Digite uma nova senha"
              />
              <p className="text-xs text-gray-500 mt-1">Deixe em branco para manter a senha atual</p>
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                <p className="text-red-700 text-sm font-medium flex items-center">
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {error}
                </p>
              </div>
            )}

            <div className="flex gap-3 pt-4">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold py-3 px-4 rounded-lg transition-colors"
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={loading}
                className="flex-1 bg-primary-500 hover:bg-primary-600 text-white font-semibold py-3 px-4 rounded-lg transition-colors disabled:opacity-60 disabled:cursor-not-allowed shadow-sm hover:shadow-md"
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"></div>
                    Salvando...
                  </div>
                ) : (
                  'Salvar Alterações'
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
} 