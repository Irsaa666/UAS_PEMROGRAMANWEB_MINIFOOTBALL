from config.database import get_db


def create_club(user_id, name, stadium_name, founded_year):
    """Create a new club for a user. Returns the new club's ID."""
    db = get_db()
    with db.cursor() as cursor:
        sql = """INSERT INTO clubs (user_id, name, stadium_name, founded_year)
                 VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql, (user_id, name, stadium_name, founded_year))
    db.commit()
    return cursor.lastrowid


def get_club_by_user(user_id):
    """Fetch the club record associated with a specific user."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM clubs WHERE user_id = %s", (user_id,))
        return cursor.fetchone()


def get_club_by_id(club_id):
    """Fetch a club by its primary key."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM clubs WHERE id = %s", (club_id,))
        return cursor.fetchone()


def update_club(club_id, name, stadium_name, founded_year, logo_path=None):
    """Update club profile details."""
    db = get_db()
    with db.cursor() as cursor:
        if logo_path:
            sql = """UPDATE clubs SET name=%s, stadium_name=%s, founded_year=%s, logo_path=%s
                     WHERE id=%s"""
            cursor.execute(sql, (name, stadium_name, founded_year, logo_path, club_id))
        else:
            sql = """UPDATE clubs SET name=%s, stadium_name=%s, founded_year=%s
                     WHERE id=%s"""
            cursor.execute(sql, (name, stadium_name, founded_year, club_id))
    db.commit()


def update_club_budget(club_id, new_budget):
    """Directly set the club's budget value."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("UPDATE clubs SET budget=%s WHERE id=%s", (new_budget, club_id))
    db.commit()
