from .database import DatabaseService
import glob, os, sqlite3
from datetime import datetime, timezone


def apply_migrations(db: DatabaseService, migrations_dir):
    """Public entrypoint: apply any pending migrations in order."""
    conn = db.connection

    _ensure_migrations_table_exists(conn)
    applied = _get_applied_versions(conn)
    pending = _pending_migrations(migrations_dir, applied)

    for version, filepath in pending:
        _apply_migration(conn, version, filepath)

    if not pending:
        print("✓ All migrations up to date")


def _ensure_migrations_table_exists(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version INTEGER PRIMARY KEY,
            applied_at TEXT NOT NULL
        ) STRICT
        """
    )
    conn.commit()


def _get_applied_versions(conn):
    cursor = conn.execute("SELECT version FROM schema_migrations")
    return {row[0] for row in cursor.fetchall()}


def _pending_migrations(migrations_dir, applied_versions):

    migration_files = sorted(glob.glob(os.path.join(migrations_dir, "*.sql")))

    pending = []
    for filepath in migration_files:
        version = _parse_migration_file_version(filepath)
        if version is not None and version not in applied_versions:
            pending.append((version, filepath))

    pending.sort(key=lambda x: x[0])
    return pending

def _parse_migration_file_version(filepath):
    basename = os.path.basename(filepath)
    version_str = basename.split("-", 1)[0]
    return int(version_str) if version_str.isdigit() else None

def _apply_migration(conn, version, filepath):
    print(f"Applying migration {version}: {os.path.basename(filepath)}")

    with open(filepath, "r", encoding="utf-8") as f:
        migration_sql = f.read()

    try:
        conn.execute("BEGIN")
        conn.executescript(migration_sql)
        conn.execute(
            "INSERT INTO schema_migrations (version, applied_at) VALUES (?, ?)",
            (version, datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")),
        )
        conn.commit()
        print(f"✓ Migration {version} applied successfully")
    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"Failed to apply migration {version}: {str(e)}") from e
