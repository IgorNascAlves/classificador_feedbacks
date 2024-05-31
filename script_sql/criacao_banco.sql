-- Cria o banco de dados 'feedbacks_db' se ele não existir
CREATE DATABASE IF NOT EXISTS feedbacks_db;

-- Seleciona o banco de dados 'feedbacks_db' para uso
USE feedbacks_db;

-- Remove a tabela 'Feedback' se ela já existir (usado para fins de limpeza)
DROP TABLE IF EXISTS Feedback;

-- Cria a tabela 'Feedback' se ela não existir
CREATE TABLE IF NOT EXISTS Feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Identificador único para cada feedback
    feedback_id VARCHAR(50) UNIQUE NOT NULL,  -- Identificador único do feedback
    feedback_text TEXT NOT NULL,  -- Texto do feedback
    sentiment VARCHAR(20) NOT NULL,  -- Sentimento associado ao feedback (ex: positivo, negativo, neutro)
    code VARCHAR(50),  -- Código opcional associado ao feedback
    reason TEXT,  -- Razão opcional fornecida no feedback
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Data e hora em que o feedback foi criado
);
