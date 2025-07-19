'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Cookies from 'js-cookie';
import { authAPI } from '@/lib/api';

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    nome: '',
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
      const registerResponse = await authAPI.register(formData);

      const loginResponse = await authAPI.login({
        username: formData.email,
        password: formData.password
      });

      Cookies.set('token', loginResponse.data.access_token, { expires: 7 });
      router.push('/dashboard');
    } catch (error: unknown) {
      console.error('Erro no registro:', error);
      if (error && typeof error === 'object' && 'response' in error &&
        typeof error.response === 'object' && error.response && 'status' in error.response &&
        error.response.status === 400) {
        setError('Email já está em uso. Tente com outro email.');
      } else {
        setError('Erro ao criar conta. Tente novamente.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background decorativo */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -left-40 w-80 h-80 bg-gradient-to-r from-green-300 to-primary-300 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse delay-500"></div>
        <div className="absolute -bottom-40 -right-40 w-80 h-80 bg-gradient-to-r from-primary-400 to-blue-400 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse"></div>
        <div className="absolute top-1/3 left-1/3 w-96 h-96 bg-gradient-to-r from-purple-200 to-primary-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-bounce-gentle"></div>
      </div>

      <div className="w-full max-w-md relative z-10">
        {/* Card principal */}
        <div className="bg-white/70 backdrop-blur-xl rounded-3xl shadow-card-hover border border-white/20 p-8 animate-fade-in">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-green-500 to-primary-500 rounded-2xl shadow-glow mb-4 animate-pulse-glow">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <h1 className="text-3xl font-display font-bold text-black mb-2">
              Crie sua conta! 🎯
            </h1>
            <p className="text-black font-medium">
              Junte-se a nós e comece sua jornada fitness
            </p>
          </div>

          {/* Formulário */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Nome */}
            <div className="space-y-2 animate-slide-up">
              <label htmlFor="nome" className="block text-sm font-semibold text-black">
                👤 Nome Completo
              </label>
              <input
                type="text"
                id="nome"
                value={formData.nome}
                onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                className="w-full px-4 py-3 bg-white/50 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:ring-0 outline-none transition-all duration-200 font-medium placeholder-gray-400 hover:border-gray-300 text-black"
                placeholder="Seu nome completo"
                required
              />
            </div>

            {/* Email */}
            <div className="space-y-2 animate-slide-up" style={{ animationDelay: '100ms' }}>
              <label htmlFor="email" className="block text-sm font-semibold text-black">
                📧 Email
              </label>
              <input
                type="email"
                id="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-4 py-3 bg-white/50 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:ring-0 outline-none transition-all duration-200 font-medium placeholder-gray-400 hover:border-gray-300 text-black"
                placeholder="seu@email.com"
                required
              />
            </div>

            {/* Senha */}
            <div className="space-y-2 animate-slide-up" style={{ animationDelay: '200ms' }}>
              <label htmlFor="password" className="block text-sm font-semibold text-black">
                🔐 Senha
              </label>
              <input
                type="password"
                id="password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="w-full px-4 py-3 bg-white/50 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:ring-0 outline-none transition-all duration-200 font-medium placeholder-gray-400 hover:border-gray-300 text-black"
                placeholder="Mínimo 6 caracteres"
                minLength={6}
                required
              />
              <p className="text-xs text-black font-medium">
                💡 Use no mínimo 6 caracteres para maior segurança
              </p>
            </div>

            {/* Error */}
            {error && (
              <div className="bg-red-50 border-2 border-red-200 rounded-xl p-3 animate-scale-in">
                <p className="text-black text-sm font-medium">❌ {error}</p>
              </div>
            )}

            {/* Botão de registro */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-green-500 to-primary-500 hover:from-green-600 hover:to-primary-600 text-black font-bold py-4 px-6 rounded-2xl transition-all duration-300 transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:transform-none animate-slide-up shadow-lg hover:shadow-xl hover:shadow-green-500/25 border-0"
              style={{ animationDelay: '300ms' }}
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="w-6 h-6 border-3 border-black/30 border-t-black rounded-full animate-spin mr-3"></div>
                  <span className="text-lg text-black">Criando conta...</span>
                </div>
              ) : (
                <div className="flex items-center justify-center">
                  <span className="text-xl mr-2">✨</span>
                  <span className="text-lg font-bold text-black">Criar Minha Conta</span>
                </div>
              )}
            </button>

            {/* Link para login */}
            <div className="text-center animate-fade-in" style={{ animationDelay: '400ms' }}>
              <p className="text-black font-medium">
                Já tem uma conta?{' '}
                <Link
                  href="/login"
                  className="text-black hover:text-black font-semibold hover:underline transition-all duration-200"
                >
                  Fazer login 🚀
                </Link>
              </p>
            </div>
          </form>
        </div>

        {/* Footer */}
        <div className="text-center mt-8 animate-fade-in" style={{ animationDelay: '500ms' }}>
          <p className="text-black font-medium">
            🏋️‍♀️ Crie Seu Treino - Transforme sua rotina
          </p>
        </div>
      </div>
    </div>
  );
} 