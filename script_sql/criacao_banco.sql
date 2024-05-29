-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS feedbacks_db;

drop table Feedback;
-- Use the newly created or existing database
USE feedbacks_db;

-- Create the Feedback table if it doesn't exist
CREATE TABLE IF NOT EXISTS Feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    feedback_id VARCHAR(50) UNIQUE NOT NULL,
    feedback_text TEXT NOT NULL,
    sentiment VARCHAR(20) NOT NULL,
    code VARCHAR(50),
    reason TEXT
);
