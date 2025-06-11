CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS treinos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    usuario_id INT REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS exercicios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    serie INT NOT NULL,
    repeticoes INT NOT NULL,
    comentario TEXT,
    tipo_exercicio VARCHAR(20) CHECK (tipo_exercicio IN ('ComPeso', 'SemPeso')) NOT NULL
);

CREATE TABLE IF NOT EXISTS com_peso (
    id SERIAL PRIMARY KEY,
    exercicio_id INT REFERENCES exercicios(id) ON DELETE CASCADE,
    peso FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS sem_peso (
    id SERIAL PRIMARY KEY,
    exercicio_id INT REFERENCES exercicios(id) ON DELETE CASCADE,
    tempo_seg FLOAT NOT NULL,
    distancia_m FLOAT NOT NULL,
    meta_velocidade FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS treino_exercicio (
    treino_id INT REFERENCES treinos(id) ON DELETE CASCADE,
    exercicio_id INT REFERENCES exercicios(id) ON DELETE CASCADE,
    PRIMARY KEY (treino_id, exercicio_id)
);