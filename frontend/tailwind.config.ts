import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f1ff',
          100: '#e4e6ff',
          200: '#cdd0ff',
          300: '#a6abff',
          400: '#7c82ff',
          500: '#8F93FF',  // Cor principal
          600: '#7c80ff',
          700: '#6b6eff',
          800: '#5a5eff',
          900: '#4d51ff',
        },
        gray: {
          50: '#f9fafb',
          100: '#f3f4f6',
          200: '#e5e7eb',
          300: '#d1d5db',
          400: '#9ca3af',
          500: '#6b7280',
          600: '#4b5563',
          700: '#374151',
          800: '#1f2937',
          900: '#111827',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Poppins', 'system-ui', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'slide-down': 'slideDown 0.4s ease-out',
        'scale-in': 'scaleIn 0.3s ease-out',
        'bounce-gentle': 'bounceGentle 2s infinite',
        'pulse-glow': 'pulseGlow 2s infinite',
        'gradient': 'gradient 6s ease infinite',
        'button-pulse': 'buttonPulse 2s infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideDown: {
          '0%': { opacity: '0', transform: 'translateY(-20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        bounceGentle: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-5px)' },
        },
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(143, 147, 255, 0.4)' },
          '50%': { boxShadow: '0 0 30px rgba(143, 147, 255, 0.8)' },
        },
        gradient: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
        buttonPulse: {
          '0%, 100%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.02)' },
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'gradient-primary': 'linear-gradient(135deg, #8F93FF 0%, #6366f1 100%)',
        'gradient-secondary': 'linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%)',
        'gradient-dark': 'linear-gradient(135deg, #1f2937 0%, #111827 100%)',
        'gradient-animated': 'linear-gradient(-45deg, #8F93FF, #6366f1, #4f46e5, #4338ca)',
      },
      boxShadow: {
        'glow': '0 0 30px rgba(143, 147, 255, 0.3)',
        'glow-lg': '0 0 50px rgba(143, 147, 255, 0.4)',
        'card': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'card-hover': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'button': '0 4px 14px 0 rgba(0, 0, 0, 0.1)',
        'button-hover': '0 6px 20px rgba(143, 147, 255, 0.4)',
      },
      backdropBlur: {
        xs: '2px',
      },
      borderWidth: {
        '3': '3px',
      }
    },
  },
  plugins: [],
};

export default config; 