from config.database import get_db


def get_matches(club_id, status=None):
    """Fetch all matches for a club, optionally filtered by status."""
    db = get_db()
    with db.cursor() as cursor:
        sql = "SELECT * FROM matches WHERE club_id = %s"
        params = [club_id]

        if status and status != 'All':
            sql += " AND status = %s"
            params.append(status)

        sql += " ORDER BY match_date DESC"
        cursor.execute(sql, params)
        return cursor.fetchall()


def get_match_by_id(match_id):
    """Fetch a single match by primary key."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM matches WHERE id=%s", (match_id,))
        return cursor.fetchone()


def create_match(club_id, opponent_name, match_date):
    """Schedule a new match fixture."""
    db = get_db()
    with db.cursor() as cursor:
        sql = """INSERT INTO matches (club_id, opponent_name, match_date, status)
                 VALUES (%s, %s, %s, 'Scheduled')"""
        cursor.execute(sql, (club_id, opponent_name, match_date))
    db.commit()
    return cursor.lastrowid


def update_match_schedule(match_id, opponent_name, match_date):
    """Update a scheduled match's opponent or date."""
    db = get_db()
    with db.cursor() as cursor:
        sql = "UPDATE matches SET opponent_name=%s, match_date=%s WHERE id=%s"
        cursor.execute(sql, (opponent_name, match_date, match_id))
    db.commit()


def log_match_result(match_id, goals_for, goals_against):
    """Record the result of a played match."""
    db = get_db()
    with db.cursor() as cursor:
        sql = """UPDATE matches SET status='Played', goals_for=%s, goals_against=%s
                 WHERE id=%s"""
        cursor.execute(sql, (goals_for, goals_against, match_id))
    db.commit()


def delete_match(match_id):
    """Delete a match record."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM matches WHERE id=%s", (match_id,))
    db.commit()


def get_match_stats(club_id):
    """Return win/draw/loss counts for a club's played matches."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT
                SUM(CASE WHEN goals_for > goals_against THEN 1 ELSE 0 END) AS wins,
                SUM(CASE WHEN goals_for = goals_against THEN 1 ELSE 0 END) AS draws,
                SUM(CASE WHEN goals_for < goals_against THEN 1 ELSE 0 END) AS losses
            FROM matches
            WHERE club_id = %s AND status = 'Played'
        """, (club_id,))
        return cursor.fetchone()


def get_recent_matches(club_id, limit=5):
    """Get the N most recent played matches for chart/dashboard display."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT opponent_name, goals_for, goals_against, match_date
            FROM matches WHERE club_id=%s AND status='Played'
            ORDER BY match_date DESC LIMIT %s
        """, (club_id, limit))
        return cursor.fetchall()


def get_next_match(club_id):
    """Get the next upcoming scheduled match."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM matches WHERE club_id=%s AND status='Scheduled'
            ORDER BY match_date ASC LIMIT 1
        """, (club_id,))
        return cursor.fetchone()
