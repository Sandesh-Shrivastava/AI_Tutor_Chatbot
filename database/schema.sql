-- ============================================================
--  AI Tutor Chatbot — MySQL Schema
--  Run:  mysql -u root -p ai_tutor < database/schema.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS ai_tutor
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE ai_tutor;

-- ── Users ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id         INT PRIMARY KEY AUTO_INCREMENT,
    username   VARCHAR(100) UNIQUE NOT NULL,
    level      ENUM('beginner', 'intermediate', 'advanced') DEFAULT 'beginner',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ── Sessions ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS sessions (
    id         INT PRIMARY KEY AUTO_INCREMENT,
    user_id    INT NOT NULL,
    subject    VARCHAR(100),
    level      ENUM('beginner', 'intermediate', 'advanced'),
    mode       ENUM('normal', 'socratic') DEFAULT 'normal',
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at   TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ── Messages ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS messages (
    id         INT PRIMARY KEY AUTO_INCREMENT,
    session_id INT NOT NULL,
    role       ENUM('user', 'assistant') NOT NULL,
    content    TEXT NOT NULL,
    timestamp  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);

-- ── Topic Performance ─────────────────────────────────────────
-- Tracks how many times a user asks about a topic (high count = weak topic)
CREATE TABLE IF NOT EXISTS topic_performance (
    id           INT PRIMARY KEY AUTO_INCREMENT,
    user_id      INT NOT NULL,
    subject      VARCHAR(100),
    topic        VARCHAR(200),
    query_count  INT DEFAULT 1,
    last_queried TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_topic (user_id, topic)
);

-- ── Indexes ───────────────────────────────────────────────────
CREATE INDEX idx_sessions_user     ON sessions(user_id);
CREATE INDEX idx_messages_session  ON messages(session_id);
CREATE INDEX idx_topic_user        ON topic_performance(user_id);
