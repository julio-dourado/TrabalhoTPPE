'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { treinoAPI, Treino } from '@/lib/api';

export default function TreinosPage() {
  const [treinos, setTreinos] = useState<Treino[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    loadTreinos();
  }, []);

  const loadTreinos = async () => {
    try {
      const response = await treinoAPI.getAll();
      setTreinos(response.data);
    } catch (error) {
      console.error('Erro ao carregar treinos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number, e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent card click
    if (confirm('Tem certeza que deseja excluir este treino?')) {
      try {
        await treinoAPI.delete(id);
        setTreinos(treinos.filter(t => t.id !== id));
      } catch (error) {
        console.error('Erro ao excluir treino:', error);
        alert('Erro ao excluir treino');
      }
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="flex flex-col items-center space-y-4">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-primary-200 border-t-primary-600"></div>
          <p className="text-black font-medium">Carregando treinos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="animate-fade-in">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-black">Meus Treinos</h1>
          <p className="text-black mt-2">Gerencie todos os seus treinos</p>
        </div>
        <button
          onClick={() => router.push('/treinos/new')}
          className="bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-black font-bold px-8 py-4 rounded-2xl transition-all duration-300 transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-xl hover:shadow-primary-500/25 border-0"
        >
          <div className="flex items-center justify-center">
            <span className="text-xl mr-2">✨</span>
            <span>Criar Treino</span>
          </div>
        </button>
      </div>

      {treinos.length === 0 ? (
        <div className="text-center py-16">
          <div className="w-24 h-24 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <span className="text-4xl">💪</span>
          </div>
          <h3 className="text-lg font-semibold text-black mb-2">
            Você não possui nenhum treino ainda.
          </h3>
          <p className="text-black mb-6">
            Crie seu primeiro treino!
          </p>
          <button
            onClick={() => router.push('/treinos/new')}
            className="bg-gradient-to-r from-green-500 to-primary-500 hover:from-green-600 hover:to-primary-600 text-black font-bold px-8 py-4 rounded-2xl transition-all duration-300 transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-xl hover:shadow-green-500/25 border-0"
          >
            <div className="flex items-center justify-center">
              <span className="text-xl mr-2">🚀</span>
              <span>Criar Primeiro Treino</span>
            </div>
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {treinos.map((treino) => (
            <div
              key={treino.id}
              className="bg-white rounded-2xl shadow-card hover:shadow-card-hover transition-all duration-300 cursor-pointer animate-slide-up transform hover:scale-105 border border-gray-100"
              onClick={() => router.push(`/treinos/${treino.id}`)}
            >
              <div className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <div className="flex-1">
                    <h3 className="font-bold text-xl text-black mb-2">
                      {treino.nome}
                    </h3>
                    {treino.descricao && (
                      <p className="text-black text-sm">{treino.descricao}</p>
                    )}
                  </div>
                  <button
                    onClick={(e) => handleDelete(treino.id, e)}
                    className="bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-black p-2 rounded-xl font-bold transition-all duration-300 transform hover:scale-110 active:scale-95 shadow-lg hover:shadow-xl hover:shadow-red-500/25 border-0 ml-4"
                    title="Excluir treino"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>

                <div className="border-t border-gray-100 pt-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center text-black text-sm">
                      <span className="mr-2">📅</span>
                      <span>Criado em {new Date(treino.created_at).toLocaleDateString('pt-BR')}</span>
                    </div>
                    <div className="flex items-center text-black text-sm">
                      <span className="mr-2">🎯</span>
                      <span>Ver detalhes</span>
                      <svg className="w-4 h-4 ml-1 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
} 