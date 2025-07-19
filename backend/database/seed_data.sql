-- Dados iniciais para teste do sistema

-- Usuário de teste
INSERT INTO usuarios (nome, email, hashed_password) VALUES
('João Silva', 'joao@exemplo.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'), -- senha: 123456
('Maria Santos', 'maria@exemplo.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'), -- senha: 123456
('Carlos Oliveira', 'carlos@exemplo.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'); -- senha: 123456

-- Treinos de exemplo
INSERT INTO treinos (nome, descricao, usuario_id) VALUES
-- João Silva (id=1)
('Treino A - Push', 'Peitoral, Ombros e Tríceps', 1),
('Treino B - Pull', 'Costas e Bíceps', 1),
('Treino C - Legs', 'Pernas completo', 1),
('Cardio Manhã', 'Treino cardiovascular matinal', 1),

-- Maria Santos (id=2)
('Upper Body', 'Parte superior do corpo', 2),
('Lower Body', 'Parte inferior do corpo', 2),
('HIIT Workout', 'Treino intervalado de alta intensidade', 2),

-- Carlos Oliveira (id=3)
('Força Básica', 'Treino básico de força', 3),
('Resistência', 'Treino de resistência muscular', 3);

-- Exercícios com peso
INSERT INTO exercicios (nome, tipo, musculo, repeticoes, sets, carga, treino_id) VALUES
-- Treino A - Push (João)
('Supino Reto', 'com_peso', 'Peitoral', 12, 3, 80.0, 1),
('Supino Inclinado', 'com_peso', 'Peitoral', 10, 3, 70.0, 1),
('Desenvolvimento Militar', 'com_peso', 'Ombros', 10, 3, 50.0, 1),
('Elevação Lateral', 'com_peso', 'Ombros', 15, 3, 15.0, 1),
('Tríceps Pulley', 'com_peso', 'Tríceps', 12, 3, 40.0, 1),

-- Treino B - Pull (João)
('Barra Fixa', 'com_peso', 'Costas', 8, 3, 0.0, 2),
('Remada Curvada', 'com_peso', 'Costas', 12, 3, 60.0, 2),
('Puxada Frontal', 'com_peso', 'Costas', 10, 3, 50.0, 2),
('Rosca Direta', 'com_peso', 'Bíceps', 12, 3, 25.0, 2),
('Rosca Martelo', 'com_peso', 'Bíceps', 10, 3, 20.0, 2),

-- Treino C - Legs (João)
('Agachamento', 'com_peso', 'Quadríceps', 15, 4, 100.0, 3),
('Leg Press', 'com_peso', 'Quadríceps', 20, 3, 200.0, 3),
('Stiff', 'com_peso', 'Posterior', 12, 3, 80.0, 3),
('Panturrilha', 'com_peso', 'Panturrilha', 20, 4, 100.0, 3),

-- Upper Body (Maria)
('Supino com Halteres', 'com_peso', 'Peitoral', 12, 3, 30.0, 5),
('Voador', 'com_peso', 'Peitoral', 15, 3, 40.0, 5),
('Remada Sentada', 'com_peso', 'Costas', 12, 3, 45.0, 5),
('Desenvolvimento com Halteres', 'com_peso', 'Ombros', 10, 3, 25.0, 5),

-- Lower Body (Maria)
('Agachamento Goblet', 'com_peso', 'Quadríceps', 15, 3, 25.0, 6),
('Afundo', 'com_peso', 'Quadríceps', 12, 3, 20.0, 6),
('Hip Thrust', 'com_peso', 'Glúteos', 15, 3, 60.0, 6),

-- Força Básica (Carlos)
('Supino Básico', 'com_peso', 'Peitoral', 8, 3, 60.0, 8),
('Agachamento Básico', 'com_peso', 'Quadríceps', 10, 3, 80.0, 8),
('Remada Básica', 'com_peso', 'Costas', 10, 3, 50.0, 8);

-- Exercícios sem peso (cardio/tempo)
INSERT INTO exercicios (nome, tipo, tempo, distancia, treino_id) VALUES
-- Cardio Manhã (João)
('Corrida Leve', 'sem_peso', 1800, 5000, 4), -- 30min, 5km
('Caminhada Rápida', 'sem_peso', 1200, 2000, 4), -- 20min, 2km

-- HIIT Workout (Maria)
('Burpees', 'sem_peso', 300, NULL, 7), -- 5 minutos
('Mountain Climbers', 'sem_peso', 240, NULL, 7), -- 4 minutos
('Jumping Jacks', 'sem_peso', 180, NULL, 7), -- 3 minutos
('High Knees', 'sem_peso', 120, NULL, 7), -- 2 minutos

-- Resistência (Carlos)
('Flexão', 'sem_peso', 600, NULL, 9), -- 10 minutos
('Prancha', 'sem_peso', 180, NULL, 9), -- 3 minutos
('Polichinelo', 'sem_peso', 300, NULL, 9); -- 5 minutos 