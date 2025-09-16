-- TaskMaster Database Initialization Script
-- This script runs when the PostgreSQL container starts for the first time

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create database (already created by POSTGRES_DB env var, but keeping for reference)
-- CREATE DATABASE taskmaster;

-- Connect to the taskmaster database
\c taskmaster;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT FALSE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create todos table
CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(250),
    completed BOOLEAN DEFAULT FALSE,
    owner_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_todos_owner ON todos(owner_id);
CREATE INDEX IF NOT EXISTS idx_todos_completed ON todos(completed);
CREATE INDEX IF NOT EXISTS idx_todos_created ON todos(created_at);

-- Insert a default admin user (password: admin123)
-- Note: In production, change this password immediately
INSERT INTO users (username, email, hashed_password, is_active, is_admin) 
VALUES (
    'admin',
    'admin@taskmaster.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3L3jzjvG4W', -- admin123
    TRUE,
    TRUE
) ON CONFLICT (username) DO NOTHING;

-- Insert some sample todos for the admin user
INSERT INTO todos (title, description, owner_id, completed)
SELECT 
    'Welcome to TaskMaster!',
    'This is your first task. You can edit or delete it anytime.',
    u.id,
    FALSE
FROM users u 
WHERE u.username = 'admin'
ON CONFLICT DO NOTHING;

INSERT INTO todos (title, description, owner_id, completed)
SELECT 
    'Set up your team',
    'Invite team members to collaborate on tasks.',
    u.id,
    FALSE
FROM users u 
WHERE u.username = 'admin'
ON CONFLICT DO NOTHING;

INSERT INTO todos (title, description, owner_id, completed)
SELECT 
    'Explore features',
    'Try creating, editing, and completing tasks.',
    u.id,
    TRUE
FROM users u 
WHERE u.username = 'admin'
ON CONFLICT DO NOTHING;

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO taskmaster_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO taskmaster_user;
