-- Criação do banco de dados para Sistema Crie Seu Treino
-- PostgreSQL Script

-- Criar banco de dados (execute como superuser)
-- CREATE DATABASE treino_db;
-- \c treino_db;

-- Criar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabela de usuários
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Tabela de treinos
CREATE TABLE treinos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Tipo enum para exercícios
CREATE TYPE tipo_exercicio AS ENUM ('com_peso', 'sem_peso');

-- Tabela de exercícios
CREATE TABLE exercicios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    tipo tipo_exercicio NOT NULL,
    musculo VARCHAR(255),
    
    -- Campos para exercícios com peso
    repeticoes INTEGER,
    sets INTEGER,
    carga DECIMAL(10,2),
    
    -- Campos para exercícios sem peso
    tempo INTEGER, -- em segundos
    distancia DECIMAL(10,2), -- em metros
    
    treino_id INTEGER NOT NULL REFERENCES treinos(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Índices para performance
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_treinos_usuario_id ON treinos(usuario_id);
CREATE INDEX idx_exercicios_treino_id ON exercicios(treino_id);
CREATE INDEX idx_exercicios_tipo ON exercicios(tipo);

-- Trigger para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_usuarios_updated_at BEFORE UPDATE ON usuarios
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_treinos_updated_at BEFORE UPDATE ON treinos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_exercicios_updated_at BEFORE UPDATE ON exercicios
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Inserir dados de exemplo (opcional)
INSERT INTO usuarios (nome, email, hashed_password) VALUES
('Admin Test', 'admin@test.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'); -- senha: 123456

INSERT INTO treinos (nome, descricao, usuario_id) VALUES
('Treino Push', 'Treino de empurrar - peito, ombro e tríceps', 1),
('Treino Pull', 'Treino de puxar - costas e bíceps', 1),
('Treino Cardio', 'Treino cardiovascular', 1);

INSERT INTO exercicios (nome, tipo, musculo, repeticoes, sets, carga, treino_id) VALUES
('Supino Reto', 'com_peso', 'Peitoral', 12, 3, 80.5, 1),
('Desenvolvimento', 'com_peso', 'Ombro', 10, 3, 40.0, 1);

INSERT INTO exercicios (nome, tipo, tempo, distancia, treino_id) VALUES
('Corrida', 'sem_peso', 1800, 5000, 3),
('Caminhada', 'sem_peso', 2400, 3000, 3); 