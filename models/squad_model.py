from config.database import get_db


def get_squad(club_id):
    """Fetch all squad entries joined with player data for a club."""
    db = get_db()
    with db.cursor() as cursor:
        sql = """
            SELECT s.id AS squad_id, s.role, p.id AS player_id, p.name,
                   p.position, p.age, p.overall_rating
            FROM squads s
            JOIN players p ON s.player_id = p.id
            WHERE s.club_id = %s
            ORDER BY FIELD(s.role, 'Starting XI', 'Substitute', 'Reserve', 'Injured'), p.position
        """
        cursor.execute(sql, (club_id,))
        return cursor.fetchall()


def get_unassigned_players(club_id):
    """Fetch players who are NOT yet in any squad entry for this club."""
    db = get_db()
    with db.cursor() as cursor:
        sql = """
            SELECT p.id, p.name, p.position, p.overall_rating
            FROM players p
            WHERE p.club_id = %s
              AND p.id NOT IN (SELECT player_id FROM squads WHERE club_id = %s)
            ORDER BY p.position, p.name
        """
        cursor.execute(sql, (club_id, club_id))
        return cursor.fetchall()


def assign_player_to_squad(club_id, player_id, role):
    """Add a player to the squad (INSERT OR UPDATE if already assigned)."""
    db = get_db()
    with db.cursor() as cursor:
        sql = """INSERT INTO squads (club_id, player_id, role) VALUES (%s, %s, %s)
                 ON DUPLICATE KEY UPDATE role = VALUES(role)"""
        cursor.execute(sql, (club_id, player_id, role))
    db.commit()


def update_squad_role(squad_id, role):
    """Update the role of an existing squad entry."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("UPDATE squads SET role=%s WHERE id=%s", (role, squad_id))
    db.commit()


def remove_from_squad(squad_id):
    """Remove a player from the squad list."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM squads WHERE id=%s", (squad_id,))
    db.commit()
