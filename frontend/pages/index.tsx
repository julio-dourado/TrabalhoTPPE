import { useState, useEffect } from 'react'
import { testService } from '@/services/api'
import { Activity, Heart, Dumbbell, User, CheckCircle } from 'lucide-react'

export default function Home() {
  const [apiMessage, setApiMessage] = useState<string>('')
  const [isLoading, setIsLoading] = useState(true)
  const [isConnected, setIsConnected] = useState(false)

  useEffect(() => {
    const testConnection = async () => {
      try {
        setIsLoading(true)
        const response = await testService.getRoot()
        setApiMessage(response.message)
        setIsConnected(true)
      } catch (error) {
        console.error('Erro ao conectar com a API:', error)
        setApiMessage('Erro ao conectar com o backend')
        setIsConnected(false)
      } finally {
        setIsLoading(false)
      }
    }

    testConnection()
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex justify-center items-center gap-2 mb-4">
            <Activity className="w-8 h-8 text-primary-600" />
            <h1 className="text-4xl font-bold text-gray-900">Training App</h1>
          </div>
          <p className="text-xl text-gray-600">
            Sistema de gerenciamento de treinos e exercícios
          </p>
        </div>

        {/* Status de Conexão */}
        <div className="max-w-md mx-auto mb-8">
          <div className="card">
            <div className="flex items-center justify-center gap-3 mb-4">
              {isLoading ? (
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600"></div>
              ) : isConnected ? (
                <CheckCircle className="w-6 h-6 text-green-600" />
              ) : (
                <div className="w-6 h-6 rounded-full bg-red-600"></div>
              )}
              <h2 className="text-lg font-semibold">Status da Conexão</h2>
            </div>

            {isLoading ? (
              <p className="text-center text-gray-600">Conectando com o backend...</p>
            ) : (
              <div className="text-center">
                <p className={`font-medium ${isConnected ? 'text-green-600' : 'text-red-600'}`}>
                  {isConnected ? 'Conectado com sucesso!' : 'Erro de conexão'}
                </p>
                <p className="text-sm text-gray-600 mt-2 p-3 bg-gray-100 rounded-lg">
                  {apiMessage}
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          <div className="card text-center">
            <div className="flex justify-center mb-4">
              <User className="w-12 h-12 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Usuários</h3>
            <p className="text-gray-600">
              Gerencie contas de usuários e perfis personalizados
            </p>
          </div>

          <div className="card text-center">
            <div className="flex justify-center mb-4">
              <Dumbbell className="w-12 h-12 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Exercícios</h3>
            <p className="text-gray-600">
              Catálogo completo de exercícios organizados por grupos musculares
            </p>
          </div>

          <div className="card text-center">
            <div className="flex justify-center mb-4">
              <Heart className="w-12 h-12 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Treinos</h3>
            <p className="text-gray-600">
              Crie e gerencie rotinas de treino personalizadas
            </p>
          </div>
        </div>

        {/* API Info */}
        <div className="max-w-2xl mx-auto mt-12">
          <div className="card">
            <h3 className="text-lg font-semibold mb-3 text-center">Informações da API</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Backend URL:</span>
                <span className="font-mono text-primary-600">
                  {process.env.API_URL || 'http://localhost:8000'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Status:</span>
                <span className={`font-medium ${isConnected ? 'text-green-600' : 'text-red-600'}`}>
                  {isConnected ? 'Online' : 'Offline'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Versão:</span>
                <span className="font-mono">v1.0.0</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 