'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { userAPI, treinoAPI, User, Treino } from '@/lib/api';

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null);
  const [treinos, setTreinos] = useState<Treino[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const loadData = async () => {
      try {
        const [userResponse, treinosResponse] = await Promise.all([
          userAPI.getProfile(),
          treinoAPI.getAll()
        ]);

        setUser(userResponse.data);
        setTreinos(treinosResponse.data);
      } catch (error) {
        console.error('Erro ao carregar dados:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <div className="relative w-16 h-16">
            <div className="absolute inset-0 border-4 border-primary-200 rounded-full"></div>
            <div className="absolute inset-0 border-4 border-primary-600 rounded-full border-t-transparent animate-spin"></div>
          </div>
          <p className="text-gray-600 font-medium">Carregando dashboard...</p>
        </div>
      </div>
    );
  }

  const firstName = user?.nome.split(' ')[0] || 'Usuário';

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header Section */}
      <div className="bg-white border-b border-gray-200 mb-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Olá, {firstName}! 👋
              </h1>
              <p className="text-gray-600 mt-1 text-lg">
                Bem-vindo de volta ao seu painel de treinos
              </p>
            </div>
            <div className="hidden md:flex items-center space-x-4">
              <div className="bg-primary-50 p-3 rounded-lg">
                <div className="w-8 h-8 text-primary-600">
                  <svg fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-8">
        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <StatsCard
            title="Treinos Criados"
            value={treinos.length.toString()}
            subtitle={treinos.length === 1 ? 'treino ativo' : 'treinos ativos'}
            icon="💪"
            color="blue"
            trend="+12% este mês"
          />
          <StatsCard
            title="Meta Semanal"
            value="4/7"
            subtitle="dias concluídos"
            icon="🎯"
            color="green"
            trend="57% da meta"
          />
          <StatsCard
            title="Streak Atual"
            value="7"
            subtitle="dias consecutivos"
            icon="🔥"
            color="orange"
            trend="Melhor: 12 dias"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Recent Workouts */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-xl font-semibold text-gray-900">Seus Treinos</h2>
                <p className="text-gray-500 text-sm mt-1">Gerencie e visualize seus treinos</p>
              </div>
              <button
                onClick={() => router.push('/treinos')}
                className="text-primary-600 hover:text-primary-700 text-sm font-medium hover:underline transition-colors"
              >
                Ver todos
              </button>
            </div>

            {treinos.length === 0 ? (
              <EmptyState
                title="Nenhum treino criado"
                description="Crie seu primeiro treino para começar a organizar seus exercícios"
                actionText="Criar Primeiro Treino"
                actionHandler={() => router.push('/treinos/new')}
                icon="📝"
              />
            ) : (
              <div className="space-y-3">
                {treinos.slice(0, 4).map((treino, index) => (
                  <WorkoutCard
                    key={treino.id}
                    treino={treino}
                    onClick={() => router.push(`/treinos/${treino.id}`)}
                    delay={index * 50}
                  />
                ))}
                {treinos.length > 4 && (
                  <button
                    onClick={() => router.push('/treinos')}
                    className="w-full p-3 text-center text-primary-600 hover:text-primary-700 hover:bg-primary-50 rounded-lg transition-colors text-sm font-medium"
                  >
                    Ver mais {treinos.length - 4} treinos
                  </button>
                )}
              </div>
            )}
          </div>

          {/* Quick Actions */}
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="mb-6">
                <h2 className="text-xl font-semibold text-gray-900">Ações Rápidas</h2>
                <p className="text-gray-500 text-sm mt-1">Acesse funcionalidades principais</p>
              </div>

              <div className="space-y-4">
                <ActionButton
                  title="Criar Novo Treino"
                  description="Monte um treino personalizado"
                  icon="✨"
                  color="primary"
                  onClick={() => router.push('/treinos/new')}
                />
                <ActionButton
                  title="Meus Treinos"
                  description="Visualizar e gerenciar treinos"
                  icon="📋"
                  color="blue"
                  onClick={() => router.push('/treinos')}
                />
                <ActionButton
                  title="Perfil"
                  description="Configurações da conta"
                  icon="👤"
                  color="gray"
                  onClick={() => router.push('/profile')}
                />
              </div>
            </div>

            {/* Motivation Card */}
            <div className="bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl shadow-sm p-6 text-white">
              <div className="flex items-start space-x-3">
                <div className="bg-white/20 p-2 rounded-lg">
                  <span className="text-xl">💡</span>
                </div>
                <div>
                  <h3 className="font-semibold text-lg">Dica do Dia</h3>
                  <p className="text-primary-100 text-sm mt-1 leading-relaxed">
                    A consistência é mais importante que a intensidade. Pequenos progressos diários levam a grandes resultados!
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Components
interface StatsCardProps {
  title: string;
  value: string;
  subtitle: string;
  icon: string;
  color: 'blue' | 'green' | 'orange';
  trend: string;
}

function StatsCard({ title, value, subtitle, icon, color, trend }: StatsCardProps) {
  const colorClasses = {
    blue: 'bg-blue-500 text-blue-600 bg-blue-50',
    green: 'bg-green-500 text-green-600 bg-green-50',
    orange: 'bg-orange-500 text-orange-600 bg-orange-50'
  };

  const iconBg = `bg-${color}-50`;
  const iconColor = `text-${color}-600`;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-4">
        <div className={`p-2 rounded-lg ${iconBg}`}>
          <span className="text-xl">{icon}</span>
        </div>
        <span className="text-xs text-gray-500 font-medium">{trend}</span>
      </div>
      <div>
        <h3 className="text-2xl font-bold text-gray-900 mb-1">{value}</h3>
        <p className="text-gray-600 text-sm font-medium">{title}</p>
        <p className="text-gray-400 text-xs mt-1">{subtitle}</p>
      </div>
    </div>
  );
}

interface WorkoutCardProps {
  treino: Treino;
  onClick: () => void;
  delay: number;
}

function WorkoutCard({ treino, onClick, delay }: WorkoutCardProps) {
  return (
    <div
      className="flex items-center justify-between p-4 bg-gray-50 hover:bg-gray-100 rounded-lg transition-all duration-200 cursor-pointer group border border-gray-100 hover:border-gray-200"
      onClick={onClick}
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="flex items-center space-x-3">
        <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center group-hover:bg-primary-200 transition-colors">
          <span className="text-primary-700 font-semibold text-sm">
            {treino.nome.charAt(0).toUpperCase()}
          </span>
        </div>
        <div>
          <h4 className="font-semibold text-gray-900 group-hover:text-primary-700 transition-colors">
            {treino.nome}
          </h4>
          <p className="text-gray-500 text-sm">
            {treino.descricao || 'Sem descrição'}
          </p>
        </div>
      </div>
      <div className="flex items-center space-x-2">
        <span className="text-xs bg-primary-100 text-primary-700 px-2 py-1 rounded font-medium">
          Treino
        </span>
        <svg className="w-5 h-5 text-gray-400 group-hover:text-primary-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
        </svg>
      </div>
    </div>
  );
}

interface ActionButtonProps {
  title: string;
  description: string;
  icon: string;
  color: 'primary' | 'blue' | 'gray';
  onClick: () => void;
}

function ActionButton({ title, description, icon, color, onClick }: ActionButtonProps) {
  const colorClasses = {
    primary: 'bg-primary-500 hover:bg-primary-600 text-white',
    blue: 'bg-blue-500 hover:bg-blue-600 text-white',
    gray: 'bg-gray-500 hover:bg-gray-600 text-white'
  };

  return (
    <button
      onClick={onClick}
      className={`w-full p-4 rounded-lg transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98] ${colorClasses[color]} shadow-sm hover:shadow-md`}
    >
      <div className="flex items-center space-x-3">
        <span className="text-xl">{icon}</span>
        <div className="text-left">
          <h3 className="font-semibold">{title}</h3>
          <p className="text-sm opacity-90">{description}</p>
        </div>
      </div>
    </button>
  );
}

interface EmptyStateProps {
  title: string;
  description: string;
  actionText: string;
  actionHandler: () => void;
  icon: string;
}

function EmptyState({ title, description, actionText, actionHandler, icon }: EmptyStateProps) {
  return (
    <div className="text-center py-8">
      <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <span className="text-2xl">{icon}</span>
      </div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600 mb-6 max-w-sm mx-auto">{description}</p>
      <button
        onClick={actionHandler}
        className="bg-primary-500 hover:bg-primary-600 text-white px-6 py-3 rounded-lg font-medium transition-colors shadow-sm hover:shadow-md"
      >
        {actionText}
      </button>
    </div>
  );
} 