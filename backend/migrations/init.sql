-- Migração principal do banco de dados
-- Criação das tabelas em inglês compatíveis com o código do backend

-- Remover tabelas se existirem
DROP TABLE IF EXISTS training_exercise CASCADE;
DROP TABLE IF EXISTS execution_history CASCADE;
DROP TABLE IF EXISTS with_weight CASCADE;
DROP TABLE IF EXISTS without_weight CASCADE;
DROP TABLE IF EXISTS exercises CASCADE;
DROP TABLE IF EXISTS trainings CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Tabela de usuários
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    birth_date DATE,
    gender VARCHAR(20) DEFAULT 'not_informed',
    height_cm INTEGER,
    weight_kg FLOAT,
    activity_level VARCHAR(20) DEFAULT 'sedentary',
    main_goal VARCHAR(30) DEFAULT 'general_health',
    training_experience_years INTEGER DEFAULT 0,
    bio TEXT,
    target_weight_kg FLOAT,
    is_active BOOLEAN DEFAULT TRUE,
    is_premium BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de treinos
CREATE TABLE trainings (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(20) DEFAULT 'STRENGTH',
    status VARCHAR(20) DEFAULT 'PLANNED',
    estimated_duration_min INTEGER DEFAULT 60,
    actual_duration_min INTEGER,
    calories_burned FLOAT,
    total_volume_kg FLOAT,
    perceived_difficulty INTEGER,
    satisfaction INTEGER,
    notes TEXT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    finished_at TIMESTAMP
);

-- Tabela de exercícios
CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    muscle_group VARCHAR(20) DEFAULT 'general',
    difficulty VARCHAR(20) DEFAULT 'BEGINNER',
    sets INTEGER NOT NULL,
    reps INTEGER NOT NULL,
    comment TEXT,
    instructions TEXT,
    rest_time_sec INTEGER DEFAULT 60,
    is_compound BOOLEAN DEFAULT FALSE,
    equipment VARCHAR(100),
    exercise_type VARCHAR(20) CHECK (exercise_type IN ('WITH_WEIGHT', 'WITHOUT_WEIGHT')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de exercícios com peso
CREATE TABLE with_weight (
    id SERIAL PRIMARY KEY,
    exercise_id INTEGER NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    weight_kg FLOAT NOT NULL,
    max_weight_kg FLOAT,
    suggested_increment_kg FLOAT DEFAULT 2.5
);

-- Tabela de exercícios sem peso
CREATE TABLE without_weight (
    id SERIAL PRIMARY KEY,
    exercise_id INTEGER NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    time_sec FLOAT,
    distance_m FLOAT,
    estimated_calories FLOAT,
    intensity VARCHAR(20) DEFAULT 'moderate'
);

-- Tabela de relacionamento treino-exercício
CREATE TABLE training_exercise (
    training_id INTEGER REFERENCES trainings(id) ON DELETE CASCADE,
    exercise_id INTEGER REFERENCES exercises(id) ON DELETE CASCADE,
    PRIMARY KEY (training_id, exercise_id)
);

-- Tabela de histórico de execução
CREATE TABLE execution_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    exercise_id INTEGER NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    training_id INTEGER REFERENCES trainings(id) ON DELETE SET NULL,
    completed_sets INTEGER NOT NULL,
    completed_reps INTEGER NOT NULL,
    weight_used_kg FLOAT,
    execution_time_sec FLOAT,
    distance_completed_m FLOAT,
    perceived_difficulty INTEGER,
    observations TEXT,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar índices para melhor performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_trainings_user_id ON trainings(user_id);
CREATE INDEX idx_exercises_type ON exercises(exercise_type);
CREATE INDEX idx_history_user_id ON execution_history(user_id);
CREATE INDEX idx_history_exercise_id ON execution_history(exercise_id);

-- Inserir dados iniciais de teste
INSERT INTO users (name, email, password_hash, is_active) VALUES 
('Admin', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeZMiJYzPJEKHOxZy', TRUE); 