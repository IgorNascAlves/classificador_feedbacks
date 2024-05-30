-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS feedbacks_db;

USE feedbacks_db;
drop table Feedback;
-- Use the newly created or existing database

-- Create the Feedback table if it doesn't exist
CREATE TABLE IF NOT EXISTS Feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    feedback_id VARCHAR(50) UNIQUE NOT NULL,
    feedback_text TEXT NOT NULL,
    sentiment VARCHAR(20) NOT NULL,
    code VARCHAR(50),
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM feedbacks_db.feedback;

-- Create a feedback

INSERT INTO Feedback (feedback_id, feedback_text, sentiment, code, reason) VALUES ('1', 'I loved the product', 'positive', '1', 'good product');

