-- Criação completa do banco de dados com todos os novos campos

-- Tabela de usuários
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    data_nascimento DATE,
    genero VARCHAR(20),
    altura_cm INTEGER,
    peso_kg FLOAT,
    nivel_atividade VARCHAR(20),
    objetivo_principal VARCHAR(30),
    experiencia_treino_anos INTEGER,
    bio TEXT,
    meta_peso_kg FLOAT,
    is_active BOOLEAN DEFAULT TRUE,
    is_premium BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Tabela de treinos
CREATE TABLE treinos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    categoria VARCHAR(20) DEFAULT 'FORCA',
    status VARCHAR(20) DEFAULT 'PLANEJADO',
    duracao_estimada_min INTEGER DEFAULT 60,
    duracao_real_min INTEGER,
    calorias_queimadas FLOAT,
    volume_total_kg FLOAT,
    dificuldade_percebida INTEGER,
    satisfacao INTEGER,
    observacoes TEXT,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    iniciado_em TIMESTAMP,
    finalizado_em TIMESTAMP
);

-- Tabela de exercícios
CREATE TABLE exercicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(255) NOT NULL,
    grupo_muscular VARCHAR(20),
    dificuldade VARCHAR(20) DEFAULT 'INICIANTE',
    serie INTEGER NOT NULL,
    repeticoes INTEGER NOT NULL,
    comentario TEXT,
    instrucoes TEXT,
    tempo_descanso_seg INTEGER DEFAULT 60,
    is_composto BOOLEAN DEFAULT FALSE,
    equipamento VARCHAR(100),
    tipo_exercicio VARCHAR(20) CHECK (tipo_exercicio IN ('COM_PESO', 'SEM_PESO')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Tabela de exercícios com peso
CREATE TABLE com_peso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exercicio_id INTEGER NOT NULL REFERENCES exercicios(id) ON DELETE CASCADE,
    peso_kg FLOAT NOT NULL,
    peso_maximo_kg FLOAT,
    incremento_sugerido_kg FLOAT DEFAULT 2.5
);

-- Tabela de exercícios sem peso
CREATE TABLE sem_peso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exercicio_id INTEGER NOT NULL REFERENCES exercicios(id) ON DELETE CASCADE,
    tempo_seg FLOAT,
    distancia_m FLOAT,
    calorias_estimadas FLOAT,
    intensidade VARCHAR(20) DEFAULT 'moderada'
);

-- Tabela de relacionamento treino-exercício
CREATE TABLE treino_exercicio (
    treino_id INTEGER REFERENCES treinos(id) ON DELETE CASCADE,
    exercicio_id INTEGER REFERENCES exercicios(id) ON DELETE CASCADE,
    PRIMARY KEY (treino_id, exercicio_id)
);

-- Tabela de histórico de execução
CREATE TABLE historico_execucao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    exercicio_id INTEGER NOT NULL REFERENCES exercicios(id) ON DELETE CASCADE,
    treino_id INTEGER REFERENCES treinos(id) ON DELETE SET NULL,
    series_realizadas INTEGER NOT NULL,
    repeticoes_realizadas INTEGER NOT NULL,
    peso_utilizado_kg FLOAT,
    tempo_execucao_seg FLOAT,
    distancia_realizada_m FLOAT,
    dificuldade_percebida INTEGER,
    observacoes TEXT,
    executado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de templates de treino
CREATE TABLE template_treino (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    categoria VARCHAR(20) DEFAULT 'FORCA',
    nivel_dificuldade VARCHAR(20) DEFAULT 'iniciante',
    duracao_estimada_min INTEGER DEFAULT 60,
    is_publico BOOLEAN DEFAULT FALSE,
    criador_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    vezes_usado INTEGER DEFAULT 0,
    avaliacao_media FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Tabela de exercícios do template
CREATE TABLE exercicio_template (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_id INTEGER NOT NULL REFERENCES template_treino(id) ON DELETE CASCADE,
    exercicio_id INTEGER NOT NULL REFERENCES exercicios(id) ON DELETE CASCADE,
    ordem INTEGER NOT NULL,
    series_sugeridas INTEGER NOT NULL,
    repeticoes_sugeridas INTEGER NOT NULL,
    peso_sugerido_kg FLOAT,
    tempo_descanso_seg INTEGER DEFAULT 60,
    observacoes TEXT
);

-- Índices para melhor performance
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_treinos_usuario_id ON treinos(usuario_id);
CREATE INDEX idx_exercicios_tipo ON exercicios(tipo_exercicio);
CREATE INDEX idx_historico_usuario_id ON historico_execucao(usuario_id);
CREATE INDEX idx_historico_exercicio_id ON historico_execucao(exercicio_id);
CREATE INDEX idx_template_criador_id ON template_treino(criador_id);
CREATE INDEX idx_template_publico ON template_treino(is_publico); 