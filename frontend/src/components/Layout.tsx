'use client';

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import Cookies from 'js-cookie';
import { userAPI } from '@/lib/api';

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  const isAuthPage = pathname === '/login' || pathname === '/register';

  useEffect(() => {
    const checkAuth = async () => {
      const token = Cookies.get('token');

      if (!token) {
        if (!isAuthPage) {
          router.push('/login');
        }
        setLoading(false);
        return;
      }

      try {
        await userAPI.getProfile();

        if (isAuthPage) {
          router.push('/dashboard');
        }
      } catch (error) {
        console.error('Erro ao verificar autenticação:', error);
        Cookies.remove('token');
        if (!isAuthPage) {
          router.push('/login');
        }
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, [isAuthPage, router]);

  const logout = () => {
    Cookies.remove('token');
    router.push('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="flex flex-col items-center space-y-4">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-primary-200 border-t-primary-600"></div>
          <p className="text-black font-medium">Carregando aplicação...</p>
        </div>
      </div>
    );
  }

  if (isAuthPage) {
    return <div className="min-h-screen">{children}</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="flex items-center cursor-pointer" onClick={() => router.push('/dashboard')}>
                <span className="text-2xl mr-2">💪</span>
                <h1 className="text-xl font-bold text-black">Crie Seu Treino</h1>
              </div>
            </div>

            <nav className="flex items-center space-x-4">
              <button
                onClick={() => router.push('/dashboard')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${pathname === '/dashboard'
                    ? 'bg-primary-500 text-black font-bold'
                    : 'text-black hover:bg-primary-50 hover:text-black'
                  }`}
              >
                Dashboard
              </button>
              <button
                onClick={() => router.push('/treinos')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${pathname.startsWith('/treinos')
                    ? 'bg-primary-500 text-black font-bold'
                    : 'text-black hover:bg-primary-50 hover:text-black'
                  }`}
              >
                Treinos
              </button>
              <button
                onClick={() => router.push('/profile')}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${pathname === '/profile'
                    ? 'bg-primary-500 text-black font-bold'
                    : 'text-black hover:bg-primary-50 hover:text-black'
                  }`}
              >
                Perfil
              </button>
              <button
                onClick={logout}
                className="bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-black font-bold px-6 py-2 rounded-xl transition-all duration-300 transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-xl hover:shadow-red-500/25 border-0"
              >
                <div className="flex items-center">
                  <span className="mr-2">🚪</span>
                  <span>Sair</span>
                </div>
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  );
} 