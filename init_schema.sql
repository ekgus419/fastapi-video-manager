-- 수동 DB 초기화용 스크립트 (PostgreSQL)
-- psql -U postgres -d lumanlab_db -f init_schema.sql

-- Drop existing tables (optional, for clean start)
DROP TABLE IF EXISTS refresh_token CASCADE;
DROP TABLE IF EXISTS video_view_log CASCADE;
DROP TABLE IF EXISTS video CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS corporation CASCADE;

-- 1. corporation
CREATE TABLE corporation (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    plan VARCHAR(20) NOT NULL DEFAULT 'FREE',
    plan_expire_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE
);

-- 2. user
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    name VARCHAR(100),
    role VARCHAR(20) NOT NULL DEFAULT 'guest',
    point INTEGER NOT NULL DEFAULT 0,
    corporation_id INTEGER REFERENCES corporation(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE
);

-- 3. video
CREATE TABLE video (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    corporation_id INTEGER REFERENCES corporation(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE
);

-- 4. video_view_log
CREATE TABLE video_view_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id),
    video_id INTEGER REFERENCES video(id),
    viewed_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    UNIQUE (user_id, video_id)
);

-- 5. refresh_token
CREATE TABLE refresh_token (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id),
    token TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE
);
