-- Migration: 001_initial_schema
-- Description: Initial database schema for PGA data sync service
-- Created: 2025-01-01

BEGIN;

-- ============================================
-- CORE PGA DATA TABLES
-- ============================================

-- Players
CREATE TABLE players (
    id VARCHAR(10) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    display_name VARCHAR(200) NOT NULL,
    country VARCHAR(100),
    country_flag VARCHAR(255),
    headshot_url VARCHAR(500),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_players_active ON players(is_active);
CREATE INDEX idx_players_name ON players(last_name, first_name);

-- Tournaments
CREATE TABLE tournaments (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    season_year INT NOT NULL,
    tour_code VARCHAR(5) DEFAULT 'R',
    start_date DATE,
    end_date DATE,
    timezone VARCHAR(50),
    course_name VARCHAR(255),
    course_id VARCHAR(50),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    purse DECIMAL(15,2),
    status VARCHAR(20) DEFAULT 'UPCOMING',
    format_type VARCHAR(50),
    picks_lock_time TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT valid_status CHECK (status IN ('UPCOMING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED'))
);

CREATE INDEX idx_tournaments_season ON tournaments(season_year);
CREATE INDEX idx_tournaments_status ON tournaments(status);
CREATE INDEX idx_tournaments_dates ON tournaments(start_date, end_date);

-- Tournament Field (who's playing in each tournament)
CREATE TABLE tournament_fields (
    tournament_id VARCHAR(20) REFERENCES tournaments(id) ON DELETE CASCADE,
    player_id VARCHAR(10) REFERENCES players(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (tournament_id, player_id),
    CONSTRAINT valid_field_status CHECK (status IN ('ACTIVE', 'CUT', 'WITHDRAWN', 'DISQUALIFIED'))
);

-- Tournament Results (CRITICAL - this is how we score)
CREATE TABLE tournament_results (
    tournament_id VARCHAR(20) REFERENCES tournaments(id) ON DELETE CASCADE,
    player_id VARCHAR(10) REFERENCES players(id) ON DELETE CASCADE,
    position VARCHAR(10),
    position_numeric INT,
    total_score VARCHAR(10),
    total_strokes INT,
    rounds JSONB,
    earnings DECIMAL(15,2) NOT NULL DEFAULT 0,
    fedex_points DECIMAL(10,2),
    status VARCHAR(20),
    is_official BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (tournament_id, player_id)
);

CREATE INDEX idx_results_earnings ON tournament_results(earnings DESC);
CREATE INDEX idx_results_position ON tournament_results(position_numeric);

-- Player Stats (for user research when making picks)
CREATE TABLE player_stats (
    player_id VARCHAR(10) REFERENCES players(id) ON DELETE CASCADE,
    stat_id VARCHAR(10) NOT NULL,
    stat_name VARCHAR(100),
    value VARCHAR(50),
    rank INT,
    season_year INT NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (player_id, stat_id, season_year)
);

CREATE INDEX idx_player_stats_season ON player_stats(season_year);

-- Player Season Summary
CREATE TABLE player_seasons (
    player_id VARCHAR(10) REFERENCES players(id) ON DELETE CASCADE,
    season_year INT NOT NULL,
    events INT DEFAULT 0,
    wins INT DEFAULT 0,
    top_5 INT DEFAULT 0,
    top_10 INT DEFAULT 0,
    top_25 INT DEFAULT 0,
    cuts_made INT DEFAULT 0,
    missed_cuts INT DEFAULT 0,
    earnings DECIMAL(15,2) DEFAULT 0,
    fedex_rank INT,
    fedex_points DECIMAL(10,2),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (player_id, season_year)
);

-- Leaderboard Snapshots (for live tracking during tournaments)
CREATE TABLE leaderboard_snapshots (
    id BIGSERIAL PRIMARY KEY,
    tournament_id VARCHAR(20) REFERENCES tournaments(id) ON DELETE CASCADE,
    player_id VARCHAR(10) REFERENCES players(id) ON DELETE CASCADE,
    position VARCHAR(10),
    total VARCHAR(10),
    today VARCHAR(10),
    thru VARCHAR(10),
    current_round INT,
    player_state VARCHAR(20),
    projected_earnings DECIMAL(15,2),
    snapshot_time TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_snapshots_tournament_time ON leaderboard_snapshots(tournament_id, snapshot_time DESC);
CREATE INDEX idx_snapshots_player ON leaderboard_snapshots(player_id, snapshot_time DESC);

-- ============================================
-- APP TABLES (One and Done game logic)
-- ============================================

-- Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Leagues/Competitions
CREATE TABLE leagues (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    season_year INT NOT NULL,
    is_public BOOLEAN DEFAULT false,
    invite_code VARCHAR(20) UNIQUE,
    created_by INT REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_leagues_season ON leagues(season_year);

-- League Members
CREATE TABLE league_members (
    league_id INT REFERENCES leagues(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'member',
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (league_id, user_id),
    CONSTRAINT valid_role CHECK (role IN ('owner', 'admin', 'member'))
);

-- User Picks (THE CORE GAME TABLE)
CREATE TABLE user_picks (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    league_id INT REFERENCES leagues(id) ON DELETE CASCADE,
    tournament_id VARCHAR(20) REFERENCES tournaments(id) ON DELETE CASCADE,
    player_id VARCHAR(10) REFERENCES players(id) ON DELETE CASCADE,
    picked_at TIMESTAMPTZ DEFAULT NOW(),
    earnings DECIMAL(15,2),
    is_locked BOOLEAN DEFAULT false,
    UNIQUE (user_id, league_id, tournament_id),
    UNIQUE (user_id, league_id, player_id)
);

CREATE INDEX idx_picks_user_league ON user_picks(user_id, league_id);
CREATE INDEX idx_picks_tournament ON user_picks(tournament_id);

-- User Season Scores (denormalized for performance)
CREATE TABLE user_scores (
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    league_id INT REFERENCES leagues(id) ON DELETE CASCADE,
    season_year INT NOT NULL,
    total_earnings DECIMAL(15,2) DEFAULT 0,
    tournaments_played INT DEFAULT 0,
    best_finish INT,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, league_id, season_year)
);

-- ============================================
-- SYNC TRACKING
-- ============================================

-- Track sync operations for debugging and monitoring
CREATE TABLE sync_log (
    id BIGSERIAL PRIMARY KEY,
    sync_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    records_processed INT DEFAULT 0,
    error_message TEXT,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    CONSTRAINT valid_sync_status CHECK (status IN ('running', 'completed', 'failed'))
);

CREATE INDEX idx_sync_log_type ON sync_log(sync_type, started_at DESC);

-- ============================================
-- HELPER FUNCTIONS
-- ============================================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to all tables with updated_at
CREATE TRIGGER update_players_updated_at BEFORE UPDATE ON players
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_tournaments_updated_at BEFORE UPDATE ON tournaments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_tournament_fields_updated_at BEFORE UPDATE ON tournament_fields
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_tournament_results_updated_at BEFORE UPDATE ON tournament_results
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_player_seasons_updated_at BEFORE UPDATE ON player_seasons
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_leagues_updated_at BEFORE UPDATE ON leagues
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_user_scores_updated_at BEFORE UPDATE ON user_scores
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

COMMIT;
