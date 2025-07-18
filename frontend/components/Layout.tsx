import React, { ReactNode, useState, useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/router'
import { User, LogOut, Home, Dumbbell, Activity, UserCircle, Menu, X } from 'lucide-react'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState<any>(null)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      setIsAuthenticated(true)
      // Buscar dados do usuário se necessário
    } else if (!['/login', '/register', '/'].includes(router.pathname)) {
      router.push('/login')
    }
  }, [router.pathname])

  const handleLogout = () => {
    localStorage.removeItem('token')
    setIsAuthenticated(false)
    setUser(null)
    router.push('/login')
  }

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: Home },
    { name: 'Treinos', href: '/trainings', icon: Activity },
    { name: 'Exercícios', href: '/exercises', icon: Dumbbell },
    { name: 'Perfil', href: '/profile', icon: UserCircle },
  ]

  if (!isAuthenticated && !['/login', '/register', '/'].includes(router.pathname)) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Verificando autenticação...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navegação */}
      {isAuthenticated && (
        <nav className="bg-white shadow-lg">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex">
                <div className="flex-shrink-0 flex items-center">
                  <Activity className="h-8 w-8 text-blue-600" />
                  <span className="ml-2 text-xl font-bold text-gray-900">Training App</span>
                </div>
                <div className="hidden md:ml-6 md:flex md:space-x-8">
                  {navigation.map((item) => {
                    const Icon = item.icon
                    return (
                      <Link
                        key={item.name}
                        href={item.href}
                        className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${router.pathname === item.href
                          ? 'border-blue-500 text-gray-900'
                          : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                          }`}
                      >
                        <Icon className="h-4 w-4 mr-1" />
                        {item.name}
                      </Link>
                    )
                  })}
                </div>
              </div>
              <div className="hidden md:ml-6 md:flex md:items-center">
                <button
                  onClick={handleLogout}
                  className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-gray-500 hover:text-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  <LogOut className="h-4 w-4 mr-1" />
                  Sair
                </button>
              </div>
              <div className="md:hidden flex items-center">
                <button
                  onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                  className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
                >
                  {isMobileMenuOpen ? (
                    <X className="h-6 w-6" />
                  ) : (
                    <Menu className="h-6 w-6" />
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Menu Mobile */}
          {isMobileMenuOpen && (
            <div className="md:hidden">
              <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
                {navigation.map((item) => {
                  const Icon = item.icon
                  return (
                    <Link
                      key={item.name}
                      href={item.href}
                      className={`block px-3 py-2 rounded-md text-base font-medium ${router.pathname === item.href
                        ? 'text-blue-700 bg-blue-50'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                        }`}
                      onClick={() => setIsMobileMenuOpen(false)}
                    >
                      <Icon className="h-4 w-4 inline mr-2" />
                      {item.name}
                    </Link>
                  )
                })}
                <button
                  onClick={handleLogout}
                  className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50"
                >
                  <LogOut className="h-4 w-4 inline mr-2" />
                  Sair
                </button>
              </div>
            </div>
          )}
        </nav>
      )}

      {/* Conteúdo principal */}
      <main className={isAuthenticated ? 'max-w-7xl mx-auto py-6 sm:px-6 lg:px-8' : ''}>
        {children}
      </main>
    </div>
  )
} 