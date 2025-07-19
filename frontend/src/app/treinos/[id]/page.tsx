'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { treinoAPI, exercicioAPI, Exercicio, TreinoWithExercicios } from '@/lib/api';

export default function TreinoDetailsPage() {
  const [treino, setTreino] = useState<TreinoWithExercicios | null>(null);
  const [loading, setLoading] = useState(true);
  const [showExercicioForm, setShowExercicioForm] = useState(false);
  const router = useRouter();
  const params = useParams();
  const treinoId = parseInt(params.id as string);

  const loadTreino = useCallback(async () => {
    try {
      const response = await treinoAPI.getByIdWithExercicios(treinoId);
      setTreino(response.data);
    } catch (error) {
      console.error('Erro ao carregar treino:', error);
      router.push('/treinos');
    } finally {
      setLoading(false);
    }
  }, [treinoId, router]);

  useEffect(() => {
    loadTreino();
  }, [loadTreino]);

  const handleDeleteExercicio = async (exercicioId: number) => {
    if (confirm('Tem certeza que deseja excluir este exercício?')) {
      try {
        await exercicioAPI.delete(exercicioId);
        await loadTreino();
      } catch (error) {
        console.error('Erro ao excluir exercício:', error);
        alert('Erro ao excluir exercício');
      }
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
          <p className="text-gray-600 font-medium">Carregando treino...</p>
        </div>
      </div>
    );
  }

  if (!treino) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">😕</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Treino não encontrado</h2>
          <p className="text-gray-600 mb-6">O treino que você procura não existe ou foi removido</p>
          <button
            onClick={() => router.push('/treinos')}
            className="bg-primary-500 hover:bg-primary-600 text-white px-6 py-3 rounded-lg font-medium transition-colors"
          >
            Voltar aos Treinos
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
            <div className="flex items-center space-x-4">
              <button
                onClick={() => router.push('/treinos')}
                className="text-gray-500 hover:text-gray-700 flex items-center space-x-2 transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                <span>Voltar aos Treinos</span>
              </button>
            </div>
            <div className="flex items-center space-x-3">
              <button
                onClick={() => setShowExercicioForm(true)}
                className="bg-primary-500 hover:bg-primary-600 text-white px-4 py-2 rounded-lg font-medium transition-colors shadow-sm hover:shadow-md"
              >
                + Adicionar Exercício
              </button>
            </div>
          </div>

          <div className="mt-6">
            <div className="flex items-center space-x-3 mb-2">
              <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                <span className="text-primary-700 font-semibold">
                  {treino.nome.charAt(0).toUpperCase()}
                </span>
              </div>
              <h1 className="text-3xl font-bold text-gray-900">{treino.nome}</h1>
            </div>
            {treino.descricao && (
              <p className="text-gray-600 text-lg ml-13">{treino.descricao}</p>
            )}
            <div className="flex items-center space-x-4 mt-4 ml-13">
              <div className="flex items-center space-x-2 text-sm text-gray-500">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>Criado em {new Date(treino.created_at).toLocaleDateString('pt-BR')}</span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-gray-500">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                <span>{treino.exercicios.length} {treino.exercicios.length === 1 ? 'exercício' : 'exercícios'}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Exercises Section */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-2xl font-semibold text-gray-900">Exercícios</h2>
              <p className="text-gray-600 text-sm mt-1">Configure os exercícios do seu treino</p>
            </div>
          </div>

          {treino.exercicios.length === 0 ? (
            <EmptyExerciseState
              onAddExercise={() => setShowExercicioForm(true)}
            />
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {treino.exercicios.map((exercicio, index) => (
                <ExerciseCard
                  key={exercicio.id}
                  exercicio={exercicio}
                  onDelete={() => handleDeleteExercicio(exercicio.id)}
                  delay={index * 100}
                />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Modal para adicionar exercício */}
      {showExercicioForm && (
        <ExercicioForm
          treinoId={treinoId}
          onClose={() => setShowExercicioForm(false)}
          onSave={() => {
            setShowExercicioForm(false);
            loadTreino();
          }}
        />
      )}
    </div>
  );
}

// Components
interface EmptyExerciseStateProps {
  onAddExercise: () => void;
}

function EmptyExerciseState({ onAddExercise }: EmptyExerciseStateProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12">
      <div className="text-center">
        <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg className="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        </div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">
          Nenhum exercício adicionado
        </h3>
        <p className="text-gray-600 mb-8 max-w-md mx-auto">
          Comece a montar seu treino adicionando exercícios personalizados
        </p>
        <button
          onClick={onAddExercise}
          className="bg-primary-500 hover:bg-primary-600 text-white px-8 py-4 rounded-lg font-semibold transition-colors shadow-sm hover:shadow-md"
        >
          Adicionar Primeiro Exercício
        </button>
      </div>
    </div>
  );
}

interface ExerciseCardProps {
  exercicio: Exercicio;
  onDelete: () => void;
  delay: number;
}

function ExerciseCard({ exercicio, onDelete, delay }: ExerciseCardProps) {
  return (
    <div
      className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-all duration-200 group"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-3">
            <span className={`px-3 py-1 rounded-full text-xs font-semibold ${exercicio.tipo === 'com_peso'
                ? 'bg-blue-100 text-blue-700'
                : 'bg-green-100 text-green-700'
              }`}>
              {exercicio.tipo === 'com_peso' ? 'Com Peso' : 'Cardio'}
            </span>
          </div>
          <h3 className="font-semibold text-lg text-gray-900 group-hover:text-primary-700 transition-colors">
            {exercicio.nome}
          </h3>
          {exercicio.musculo && (
            <p className="text-gray-600 text-sm mt-1">
              <span className="font-medium">Foco:</span> {exercicio.musculo}
            </p>
          )}
        </div>
        <button
          onClick={onDelete}
          className="text-gray-400 hover:text-red-500 bg-gray-100 hover:bg-red-50 w-8 h-8 rounded-full flex items-center justify-center text-sm transition-all duration-200 opacity-0 group-hover:opacity-100"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>

      <div className="space-y-3">
        {exercicio.tipo === 'com_peso' ? (
          <>
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-gray-50 p-3 rounded-lg">
                <p className="text-xs text-gray-500 font-medium mb-1">REPETIÇÕES</p>
                <p className="font-bold text-lg text-gray-900">{exercicio.repeticoes}</p>
              </div>
              <div className="bg-gray-50 p-3 rounded-lg">
                <p className="text-xs text-gray-500 font-medium mb-1">SETS</p>
                <p className="font-bold text-lg text-gray-900">{exercicio.sets}</p>
              </div>
            </div>
            <div className="bg-primary-50 p-3 rounded-lg">
              <p className="text-xs text-primary-600 font-medium mb-1">CARGA</p>
              <p className="font-bold text-xl text-primary-700">{exercicio.carga} kg</p>
            </div>
          </>
        ) : (
          <>
            {exercicio.tempo && (
              <div className="bg-green-50 p-3 rounded-lg">
                <p className="text-xs text-green-600 font-medium mb-1">TEMPO</p>
                <p className="font-bold text-lg text-green-700">{Math.floor(exercicio.tempo / 60)}:{(exercicio.tempo % 60).toString().padStart(2, '0')} min</p>
              </div>
            )}
            {exercicio.distancia && (
              <div className="bg-blue-50 p-3 rounded-lg">
                <p className="text-xs text-blue-600 font-medium mb-1">DISTÂNCIA</p>
                <p className="font-bold text-lg text-blue-700">
                  {exercicio.distancia >= 1000
                    ? `${(exercicio.distancia / 1000).toFixed(1)} km`
                    : `${exercicio.distancia} m`
                  }
                </p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

// O componente ExercicioForm permanece o mesmo...
interface ExercicioFormProps {
  treinoId: number;
  onClose: () => void;
  onSave: () => void;
}

function ExercicioForm({ treinoId, onClose, onSave }: ExercicioFormProps) {
  const [formData, setFormData] = useState({
    nome: '',
    tipo: 'com_peso' as 'com_peso' | 'sem_peso',
    musculo: '',
    repeticoes: '',
    sets: '',
    carga: '',
    tempo: '',
    distancia: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const data: Record<string, unknown> = {
        nome: formData.nome,
        tipo: formData.tipo,
      };

      if (formData.musculo) data.musculo = formData.musculo;

      if (formData.tipo === 'com_peso') {
        if (!formData.repeticoes || !formData.sets || !formData.carga) {
          setError('Para exercícios com peso, informe repetições, sets e carga.');
          return;
        }
        data.repeticoes = parseInt(formData.repeticoes);
        data.sets = parseInt(formData.sets);
        data.carga = parseFloat(formData.carga);
      } else {
        if (!formData.tempo && !formData.distancia) {
          setError('Para exercícios sem peso, informe tempo ou distância.');
          return;
        }
        if (formData.tempo) data.tempo = parseInt(formData.tempo);
        if (formData.distancia) data.distancia = parseFloat(formData.distancia);
      }

      await exercicioAPI.create(treinoId, data as Omit<Exercicio, 'id' | 'treino_id' | 'created_at'>);
      onSave();
    } catch (error) {
      console.error('Erro ao criar exercício:', error);
      setError('Erro ao criar exercício. Verifique os dados e tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-gray-900">Adicionar Exercício</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-semibold text-gray-800 mb-2">Nome do exercício *</label>
              <input
                type="text"
                name="nome"
                required
                value={formData.nome}
                onChange={handleChange}
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary-500 text-gray-900"
                placeholder="Ex: Supino Reto, Corrida..."
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-800 mb-3">Tipo de exercício *</label>
              <div className="grid grid-cols-2 gap-3">
                <label className={`flex items-center justify-center p-4 border-2 rounded-lg cursor-pointer transition-all ${formData.tipo === 'com_peso'
                    ? 'border-primary-500 bg-primary-50 text-primary-700'
                    : 'border-gray-300 hover:border-gray-400'
                  }`}>
                  <input
                    type="radio"
                    name="tipo"
                    value="com_peso"
                    checked={formData.tipo === 'com_peso'}
                    onChange={handleChange}
                    className="sr-only"
                  />
                  <div className="text-center">
                    <div className="text-2xl mb-1">🏋️</div>
                    <span className="font-medium">Com Peso</span>
                  </div>
                </label>
                <label className={`flex items-center justify-center p-4 border-2 rounded-lg cursor-pointer transition-all ${formData.tipo === 'sem_peso'
                    ? 'border-primary-500 bg-primary-50 text-primary-700'
                    : 'border-gray-300 hover:border-gray-400'
                  }`}>
                  <input
                    type="radio"
                    name="tipo"
                    value="sem_peso"
                    checked={formData.tipo === 'sem_peso'}
                    onChange={handleChange}
                    className="sr-only"
                  />
                  <div className="text-center">
                    <div className="text-2xl mb-1">🏃</div>
                    <span className="font-medium">Cardio</span>
                  </div>
                </label>
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-800 mb-2">Músculo/Foco</label>
              <input
                type="text"
                name="musculo"
                value={formData.musculo}
                onChange={handleChange}
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary-500 text-gray-900"
                placeholder="Ex: Peito, Costas, Pernas, Resistência..."
              />
            </div>

            {formData.tipo === 'com_peso' ? (
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-gray-800 mb-2">Repetições *</label>
                    <input
                      type="number"
                      name="repeticoes"
                      required
                      value={formData.repeticoes}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary-500 text-gray-900"
                      placeholder="12"
                      min="1"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-800 mb-2">Sets *</label>
                    <input
                      type="number"
                      name="sets"
                      required
                      value={formData.sets}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary-500 text-gray-900"
                      placeholder="3"
                      min="1"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-800 mb-2">Carga (kg) *</label>
                  <input
                    type="number"
                    step="0.5"
                    name="carga"
                    required
                    value={formData.carga}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary-500 text-gray-900"
                    placeholder="20.0"
                    min="0"
                  />
                </div>
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-800 mb-2">Tempo (segundos)</label>
                  <input
                    type="number"
                    name="tempo"
                    value={formData.tempo}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary-500 text-gray-900"
                    placeholder="1800"
                    min="0"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-800 mb-2">Distância (metros)</label>
                  <input
                    type="number"
                    step="0.1"
                    name="distancia"
                    value={formData.distancia}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary-500 text-gray-900"
                    placeholder="5000"
                    min="0"
                  />
                </div>
              </div>
            )}

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
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
                    <span>Salvando...</span>
                  </div>
                ) : (
                  'Adicionar Exercício'
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
} 