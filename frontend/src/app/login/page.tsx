'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Cookies from 'js-cookie';
import { authAPI } from '@/lib/api';

export default function LoginPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const loginData = new URLSearchParams();
      loginData.append('username', formData.email);
      loginData.append('password', formData.password);

      const response = await authAPI.login({
        username: formData.email,
        password: formData.password
      });

      Cookies.set('token', response.data.access_token, { expires: 7 });
      router.push('/dashboard');
    } catch (error: unknown) {
      console.error('Erro no login:', error);
      setError('Email ou senha inválidos. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background decorativo */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-r from-primary-300 to-primary-400 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-r from-primary-400 to-primary-500 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-r from-primary-200 to-primary-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-bounce-gentle"></div>
      </div>

      <div className="w-full max-w-md relative z-10">
        {/* Card principal */}
        <div className="bg-white/70 backdrop-blur-xl rounded-3xl shadow-card-hover border border-white/20 p-8 animate-fade-in">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-primary-500 to-primary-600 rounded-2xl shadow-glow mb-4 animate-pulse-glow">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h1 className="text-3xl font-display font-bold text-black mb-2">
              Bem-vindo de volta! 👋
            </h1>
            <p className="text-black font-medium">
              Entre na sua conta para continuar treinando
            </p>
          </div>

          {/* Formulário */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Email */}
            <div className="space-y-2 animate-slide-up">
              <label htmlFor="email" className="block text-sm font-semibold text-black">
                📧 Email
              </label>
              <div className="relative">
                <input
                  type="email"
                  id="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-4 py-3 bg-white/50 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:ring-0 outline-none transition-all duration-200 font-medium placeholder-gray-400 hover:border-gray-300 text-black"
                  placeholder="seu@email.com"
                  required
                />
                <div className="absolute inset-0 rounded-xl bg-gradient-primary opacity-0 group-focus:opacity-10 transition-opacity pointer-events-none"></div>
              </div>
            </div>

            {/* Senha */}
            <div className="space-y-2 animate-slide-up" style={{ animationDelay: '100ms' }}>
              <label htmlFor="password" className="block text-sm font-semibold text-black">
                🔐 Senha
              </label>
              <input
                type="password"
                id="password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="w-full px-4 py-3 bg-white/50 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:ring-0 outline-none transition-all duration-200 font-medium placeholder-gray-400 hover:border-gray-300 text-black"
                placeholder="••••••••"
                required
              />
            </div>

            {/* Error */}
            {error && (
              <div className="bg-red-50 border-2 border-red-200 rounded-xl p-3 animate-scale-in">
                <p className="text-black text-sm font-medium">❌ {error}</p>
              </div>
            )}

            {/* Botão de login */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-black font-bold py-4 px-6 rounded-2xl transition-all duration-300 transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:transform-none animate-slide-up shadow-lg hover:shadow-xl hover:shadow-primary-500/25 border-0"
              style={{ animationDelay: '200ms' }}
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="w-6 h-6 border-3 border-black/30 border-t-black rounded-full animate-spin mr-3"></div>
                  <span className="text-lg text-black">Entrando...</span>
                </div>
              ) : (
                <div className="flex items-center justify-center">
                  <span className="text-xl mr-2">🚀</span>
                  <span className="text-lg font-bold text-black">Entrar na Conta</span>
                </div>
              )}
            </button>

            {/* Link para registro */}
            <div className="text-center animate-fade-in" style={{ animationDelay: '300ms' }}>
              <p className="text-black font-medium">
                Não tem uma conta ainda?{' '}
                <Link
                  href="/register"
                  className="text-black hover:text-black font-semibold hover:underline transition-all duration-200"
                >
                  Criar conta grátis ✨
                </Link>
              </p>
            </div>

            {/* Demo credentials */}
            <div className="bg-primary-50 border-2 border-primary-200 rounded-xl p-4 animate-fade-in" style={{ animationDelay: '400ms' }}>
              <p className="text-black text-sm font-medium mb-2">💡 Credenciais de teste:</p>
              <div className="space-y-1 text-xs font-mono">
                <p className="text-black">Email: admin@test.com</p>
                <p className="text-black">Senha: 123456</p>
              </div>
            </div>
          </form>
        </div>

        {/* Footer */}
        <div className="text-center mt-8 animate-fade-in" style={{ animationDelay: '500ms' }}>
          <p className="text-black font-medium">
            🏋️‍♀️ Crie Seu Treino - Seu parceiro fitness
          </p>
        </div>
      </div>
    </div>
  );
} 