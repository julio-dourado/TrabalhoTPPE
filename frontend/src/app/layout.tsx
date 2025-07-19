import type { Metadata } from "next";
import { Inter, Poppins } from "next/font/google";
import "./globals.css";
import Layout from '@/components/Layout';

const inter = Inter({
  subsets: ["latin"],
  variable: '--font-inter'
});

const poppins = Poppins({
  subsets: ["latin"],
  weight: ['300', '400', '500', '600', '700', '800'],
  variable: '--font-poppins'
});

export const metadata: Metadata = {
  title: "Crie Seu Treino - Seu Parceiro Fitness 🏋️‍♀️",
  description: "Crie, gerencie e acompanhe seus treinos de forma simples e eficiente. Transforme sua rotina fitness hoje mesmo!",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
      </head>
      <body className={`${inter.variable} ${poppins.variable} font-sans antialiased bg-gray-50`}>
        <Layout>{children}</Layout>
      </body>
    </html>
  );
}
