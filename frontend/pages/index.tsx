import { useEffect } from 'react'
import { useRouter } from 'next/router'
import Link from 'next/link'
import { Activity, LogIn, UserPlus } from 'lucide-react'

export default function Home() {
  const router = useRouter()

  useEffect(() => {
    // Se já estiver logado, redireciona para dashboard
    const token = localStorage.getItem('token')
    if (token) {
      router.push('/dashboard')
    }
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          {/* Logo e Título */}
          <div className="text-center">
            <div className="flex justify-center items-center gap-3 mb-6">
              <Activity className="w-12 h-12 text-blue-600" />
              <h1 className="text-4xl font-bold text-gray-900">Training App</h1>
            </div>
            <h2 className="text-xl text-gray-600 mb-8">
              Sistema de gerenciamento de treinos e exercícios
            </h2>
          </div>

          {/* Botões de Ação */}
          <div className="space-y-4">
            <Link href="/login">
              <button className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
                <LogIn className="h-5 w-5 mr-2" />
                Fazer Login
              </button>
            </Link>
            
            <Link href="/register">
              <button className="group relative w-full flex justify-center py-3 px-4 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
                <UserPlus className="h-5 w-5 mr-2" />
                Criar Conta
              </button>
            </Link>
          </div>

          {/* Features */}
          <div className="mt-12 grid grid-cols-1 gap-4 text-center">
            <div className="bg-white/50 rounded-lg p-4">
              <Activity className="w-8 h-8 text-blue-600 mx-auto mb-2" />
              <h3 className="font-semibold text-gray-900">Gerencie seus Treinos</h3>
              <p className="text-sm text-gray-600">Crie e organize suas rotinas de exercícios</p>
            </div>
            
            <div className="bg-white/50 rounded-lg p-4">
              <Activity className="w-8 h-8 text-green-600 mx-auto mb-2" />
              <h3 className="font-semibold text-gray-900">Acompanhe seu Progresso</h3>
              <p className="text-sm text-gray-600">Visualize estatísticas e evolução</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 