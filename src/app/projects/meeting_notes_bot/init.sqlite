-- SQLite schema for meeting_notes_bot
-- Database is created automatically when connecting to the file
-- This script is idempotent (safe to run multiple times)

-- Users table
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  password_hash BLOB NOT NULL,
  default_prompt TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
) STRICT;

CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Meetings table
CREATE TABLE IF NOT EXISTS meetings (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  timestamp TEXT NOT NULL,
  transcript TEXT NOT NULL,
  user_id INTEGER NOT NULL,
  UNIQUE(title, user_id),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE RESTRICT
) STRICT;

CREATE INDEX IF NOT EXISTS idx_meetings_user ON meetings(user_id);

-- Notes table
CREATE TABLE IF NOT EXISTS notes (
  meeting_id INTEGER NOT NULL,
  version INTEGER NOT NULL DEFAULT 1,
  notes TEXT NOT NULL,
  PRIMARY KEY (meeting_id, version),
  FOREIGN KEY (meeting_id) REFERENCES meetings(id) ON DELETE CASCADE
) STRICT;

CREATE INDEX IF NOT EXISTS idx_notes_meeting_version ON notes(meeting_id, version);

-- Chat history table
CREATE TABLE IF NOT EXISTS chat_history (
  id INTEGER PRIMARY KEY,
  meeting_id INTEGER NOT NULL,
  role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
  content TEXT NOT NULL,
  timestamp TEXT NOT NULL DEFAULT (datetime('now')),
  notes_version INTEGER NOT NULL,
  FOREIGN KEY (meeting_id) REFERENCES meetings(id) ON DELETE CASCADE ON UPDATE RESTRICT,
  FOREIGN KEY (meeting_id, notes_version) REFERENCES notes(meeting_id, version) ON DELETE RESTRICT ON UPDATE RESTRICT
) STRICT;

CREATE INDEX IF NOT EXISTS idx_chat_history_meeting ON chat_history(meeting_id);