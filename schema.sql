-- =============================================================
-- Mini Football Manager - MySQL Database Schema
-- Compatible with filess.io MySQL
-- =============================================================

-- Create and select database
CREATE DATABASE IF NOT EXISTS football_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE football_manager;

-- =============================================================
-- TABLE: users
-- Stores login credentials for application users
-- =============================================================
CREATE TABLE IF NOT EXISTS users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(50)  NOT NULL UNIQUE,
    email         VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================================
-- TABLE: clubs
-- Each user manages exactly one club (1-to-1 with users)
-- =============================================================
CREATE TABLE IF NOT EXISTS clubs (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    user_id       INT          NOT NULL UNIQUE,
    name          VARCHAR(100) NOT NULL,
    stadium_name  VARCHAR(100) NOT NULL,
    founded_year  INT          NOT NULL,
    budget        DECIMAL(15,2) DEFAULT 10000000.00,
    logo_path     VARCHAR(255) DEFAULT NULL,
    CONSTRAINT fk_club_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================================
-- TABLE: players
-- Players belonging to a club
-- =============================================================
CREATE TABLE IF NOT EXISTS players (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    club_id        INT          NOT NULL,
    name           VARCHAR(100) NOT NULL,
    age            INT          NOT NULL,
    position       ENUM('GK','DEF','MID','FWD') NOT NULL,
    overall_rating INT          NOT NULL DEFAULT 50,
    salary         DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    CONSTRAINT fk_player_club FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================================
-- TABLE: squads
-- Links players to a club role for squad selection
-- =============================================================
CREATE TABLE IF NOT EXISTS squads (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    club_id   INT NOT NULL,
    player_id INT NOT NULL UNIQUE,
    role      ENUM('Starting XI','Substitute','Reserve','Injured') NOT NULL DEFAULT 'Reserve',
    CONSTRAINT fk_squad_club   FOREIGN KEY (club_id)   REFERENCES clubs(id)   ON DELETE CASCADE,
    CONSTRAINT fk_squad_player FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================================
-- TABLE: trainings
-- Scheduled training sessions for a club
-- =============================================================
CREATE TABLE IF NOT EXISTS trainings (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    club_id          INT         NOT NULL,
    session_date     DATE        NOT NULL,
    focus_area       VARCHAR(50) NOT NULL,
    duration_minutes INT         NOT NULL DEFAULT 60,
    CONSTRAINT fk_training_club FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================================
-- TABLE: matches
-- Upcoming and past match fixtures
-- =============================================================
CREATE TABLE IF NOT EXISTS matches (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    club_id        INT          NOT NULL,
    opponent_name  VARCHAR(100) NOT NULL,
    match_date     DATETIME     NOT NULL,
    status         ENUM('Scheduled','Played') NOT NULL DEFAULT 'Scheduled',
    goals_for      INT          DEFAULT NULL,
    goals_against  INT          DEFAULT NULL,
    CONSTRAINT fk_match_club FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================================
-- TABLE: finances
-- Income and expense ledger for a club
-- =============================================================
CREATE TABLE IF NOT EXISTS finances (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    club_id          INT          NOT NULL,
    transaction_date DATE         NOT NULL,
    transaction_type ENUM('Income','Expense') NOT NULL,
    amount           DECIMAL(12,2) NOT NULL,
    description      VARCHAR(255) NOT NULL,
    CONSTRAINT fk_finance_club FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
