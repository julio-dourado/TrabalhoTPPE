-- Migração para atualizar o banco com os novos campos dos modelos

-- Atualizar tabela usuarios
ALTER TABLE usuarios ADD COLUMN data_nascimento DATE;
ALTER TABLE usuarios ADD COLUMN genero VARCHAR(20);
ALTER TABLE usuarios ADD COLUMN altura_cm INTEGER;
ALTER TABLE usuarios ADD COLUMN peso_kg FLOAT;
ALTER TABLE usuarios ADD COLUMN nivel_atividade VARCHAR(20);
ALTER TABLE usuarios ADD COLUMN objetivo_principal VARCHAR(30);
ALTER TABLE usuarios ADD COLUMN experiencia_treino_anos INTEGER;
ALTER TABLE usuarios ADD COLUMN bio TEXT;
ALTER TABLE usuarios ADD COLUMN meta_peso_kg FLOAT;
ALTER TABLE usuarios ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
ALTER TABLE usuarios ADD COLUMN is_premium BOOLEAN DEFAULT FALSE;
ALTER TABLE usuarios ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE usuarios ADD COLUMN updated_at TIMESTAMP;

-- Atualizar tabela treinos
ALTER TABLE treinos ADD COLUMN descricao TEXT;
ALTER TABLE treinos ADD COLUMN categoria VARCHAR(20) DEFAULT 'FORCA';
ALTER TABLE treinos ADD COLUMN status VARCHAR(20) DEFAULT 'PLANEJADO';
ALTER TABLE treinos ADD COLUMN duracao_estimada_min INTEGER DEFAULT 60;
ALTER TABLE treinos ADD COLUMN duracao_real_min INTEGER;
ALTER TABLE treinos ADD COLUMN calorias_queimadas FLOAT;
ALTER TABLE treinos ADD COLUMN volume_total_kg FLOAT;
ALTER TABLE treinos ADD COLUMN dificuldade_percebida INTEGER;
ALTER TABLE treinos ADD COLUMN satisfacao INTEGER;
ALTER TABLE treinos ADD COLUMN observacoes TEXT;
ALTER TABLE treinos ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE treinos ADD COLUMN updated_at TIMESTAMP;
ALTER TABLE treinos ADD COLUMN iniciado_em TIMESTAMP;
ALTER TABLE treinos ADD COLUMN finalizado_em TIMESTAMP;

-- Atualizar tabela exercicios
ALTER TABLE exercicios ADD COLUMN grupo_muscular VARCHAR(20);
ALTER TABLE exercicios ADD COLUMN dificuldade VARCHAR(20) DEFAULT 'INICIANTE';
ALTER TABLE exercicios ADD COLUMN instrucoes TEXT;
ALTER TABLE exercicios ADD COLUMN tempo_descanso_seg INTEGER DEFAULT 60;
ALTER TABLE exercicios ADD COLUMN is_composto BOOLEAN DEFAULT FALSE;
ALTER TABLE exercicios ADD COLUMN equipamento VARCHAR(100);
ALTER TABLE exercicios ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE exercicios ADD COLUMN updated_at TIMESTAMP;

-- Atualizar tabela com_peso
ALTER TABLE com_peso RENAME COLUMN peso TO peso_kg;
ALTER TABLE com_peso ADD COLUMN peso_maximo_kg FLOAT;
ALTER TABLE com_peso ADD COLUMN incremento_sugerido_kg FLOAT DEFAULT 2.5;

-- Atualizar tabela sem_peso
ALTER TABLE sem_peso ADD COLUMN calorias_estimadas FLOAT;
ALTER TABLE sem_peso ADD COLUMN intensidade VARCHAR(20) DEFAULT 'moderada';
-- Tornar campos opcionais
UPDATE sem_peso SET tempo_seg = NULL WHERE tempo_seg = 0;
UPDATE sem_peso SET distancia_m = NULL WHERE distancia_m = 0;

-- Criar tabela de histórico de execução
CREATE TABLE IF NOT EXISTS historico_execucao (
    id SERIAL PRIMARY KEY,
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

-- Criar tabela de templates de treino
CREATE TABLE IF NOT EXISTS template_treino (
    id SERIAL PRIMARY KEY,
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

-- Criar tabela de exercícios do template
CREATE TABLE IF NOT EXISTS exercicio_template (
    id SERIAL PRIMARY KEY,
    template_id INTEGER NOT NULL REFERENCES template_treino(id) ON DELETE CASCADE,
    exercicio_id INTEGER NOT NULL REFERENCES exercicios(id) ON DELETE CASCADE,
    ordem INTEGER NOT NULL,
    series_sugeridas INTEGER NOT NULL,
    repeticoes_sugeridas INTEGER NOT NULL,
    peso_sugerido_kg FLOAT,
    tempo_descanso_seg INTEGER DEFAULT 60,
    observacoes TEXT
);

-- Criar índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
CREATE INDEX IF NOT EXISTS idx_treinos_usuario_id ON treinos(usuario_id);
CREATE INDEX IF NOT EXISTS idx_exercicios_tipo ON exercicios(tipo_exercicio);
CREATE INDEX IF NOT EXISTS idx_historico_usuario_id ON historico_execucao(usuario_id);
CREATE INDEX IF NOT EXISTS idx_historico_exercicio_id ON historico_execucao(exercicio_id);
CREATE INDEX IF NOT EXISTS idx_template_criador_id ON template_treino(criador_id);
CREATE INDEX IF NOT EXISTS idx_template_publico ON template_treino(is_publico); 