'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { treinoAPI } from '@/lib/api';

export default function NewTreinoPage() {
  const [formData, setFormData] = useState({
    nome: '',
    descricao: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await treinoAPI.create(formData);
      router.push('/treinos');
    } catch (error) {
      console.error('Erro ao criar treino:', error);
      setError('Erro ao criar treino. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="animate-fade-in">
      <div className="mb-8">
        <button
          onClick={() => router.push('/treinos')}
          className="text-gray-600 hover:text-gray-900 mb-4 flex items-center font-medium hover:underline transition-all duration-200"
        >
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Voltar para treinos
        </button>
        <h1 className="text-3xl font-bold text-gray-900">Criar Novo Treino</h1>
        <p className="text-gray-600 mt-2">Defina nome e descrição do seu treino</p>
      </div>

      <div className="bg-white rounded-3xl shadow-lg border border-gray-100 p-8 max-w-2xl mx-auto">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label htmlFor="nome" className="block text-sm font-semibold text-gray-800">
              🏋️ Nome do Treino
            </label>
            <input
              type="text"
              id="nome"
              value={formData.nome}
              onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
              className="w-full px-4 py-3 bg-white border-2 border-gray-200 rounded-xl focus:border-primary-400 focus:ring-0 outline-none transition-all duration-200 font-medium placeholder-gray-400 hover:border-gray-300 text-gray-900"
              placeholder="Ex: Treino de Peito e Tríceps"
              required
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="descricao" className="block text-sm font-semibold text-gray-800">
              📝 Descrição (Opcional)
            </label>
            <textarea
              id="descricao"
              rows={4}
              value={formData.descricao}
              onChange={(e) => setFormData({ ...formData, descricao: e.target.value })}
              className="w-full px-4 py-3 bg-white border-2 border-gray-200 rounded-xl focus:border-primary-400 focus:ring-0 outline-none transition-all duration-200 font-medium placeholder-gray-400 hover:border-gray-300 text-gray-900 resize-none"
              placeholder="Descreva os músculos trabalhados, intensidade, etc..."
            />
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-xl p-4">
              <p className="text-red-700 text-sm font-medium flex items-center">
                <span className="mr-2">❌</span>
                {error}
              </p>
            </div>
          )}

          <div className="flex gap-3 pt-6">
            <button
              type="button"
              onClick={() => router.push('/treinos')}
              className="flex-1 bg-white hover:bg-gray-50 text-gray-700 font-semibold py-3 px-6 rounded-xl transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98] shadow-sm hover:shadow-md border border-gray-300 hover:border-gray-400"
            >
              <div className="flex items-center justify-center">
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
                <span>Cancelar</span>
              </div>
            </button>

            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-60 disabled:transform-none disabled:cursor-not-allowed shadow-md hover:shadow-lg hover:shadow-primary-500/25"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-3"></div>
                  <span>Criando...</span>
                </div>
              ) : (
                <div className="flex items-center justify-center">
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  <span>Criar Treino</span>
                </div>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
} 