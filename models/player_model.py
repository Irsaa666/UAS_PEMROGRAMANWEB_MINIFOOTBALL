from config.database import get_db


def get_players(club_id, search=None, position=None):
    """Fetch all players for a club, with optional search and position filter."""
    db = get_db()
    with db.cursor() as cursor:
        sql = "SELECT * FROM players WHERE club_id = %s"
        params = [club_id]

        if search:
            sql += " AND name LIKE %s"
            params.append(f"%{search}%")

        if position and position != 'All':
            sql += " AND position = %s"
            params.append(position)

        sql += " ORDER BY position, name"
        cursor.execute(sql, params)
        return cursor.fetchall()


def get_player_by_id(player_id):
    """Fetch a single player by primary key."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM players WHERE id = %s", (player_id,))
        return cursor.fetchone()


def create_player(club_id, name, age, position, overall_rating, salary):
    """Insert a new player into the database."""
    db = get_db()
    with db.cursor() as cursor:
        sql = """INSERT INTO players (club_id, name, age, position, overall_rating, salary)
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (club_id, name, age, position, overall_rating, salary))
    db.commit()
    return cursor.lastrowid


def update_player(player_id, name, age, position, overall_rating, salary):
    """Update an existing player's details."""
    db = get_db()
    with db.cursor() as cursor:
        sql = """UPDATE players SET name=%s, age=%s, position=%s, overall_rating=%s, salary=%s
                 WHERE id=%s"""
        cursor.execute(sql, (name, age, position, overall_rating, salary, player_id))
    db.commit()


def delete_player(player_id):
    """Delete a player (also cascades to squads)."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM players WHERE id = %s", (player_id,))
    db.commit()


def count_players(club_id):
    """Return the total number of players in the club."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM players WHERE club_id = %s", (club_id,))
        row = cursor.fetchone()
        return row['total'] if row else 0
