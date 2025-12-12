#!/bin/bash
set -e

echo "=========================================="
echo "Initializing databases and users..."
echo "=========================================="

# Create databases and users
mysql -u root -p"$MYSQL_ROOT_PASSWORD" <<-EOSQL
    
    CREATE DATABASE IF NOT EXISTS meeting_notes_bot
        CHARACTER SET utf8mb4
        COLLATE utf8mb4_unicode_ci;

    CREATE USER IF NOT EXISTS 'meeting_notes_bot'@'%' IDENTIFIED BY '$MEETING_NOTES_BOT_DB_PASS';
    GRANT ALL PRIVILEGES ON meeting_notes_bot.* TO 'meeting_notes_bot'@'%';
    
    -- Apply changes
    FLUSH PRIVILEGES;
    
EOSQL

echo "✅ Databases and users initialized successfully!"
echo "=========================================="