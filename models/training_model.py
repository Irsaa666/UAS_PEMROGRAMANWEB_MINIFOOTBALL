from config.database import get_db


def get_trainings(club_id, search=None, focus=None):
    """Fetch all training sessions for a club with optional filters."""
    db = get_db()
    with db.cursor() as cursor:
        sql = "SELECT * FROM trainings WHERE club_id = %s"
        params = [club_id]

        if search:
            sql += " AND focus_area LIKE %s"
            params.append(f"%{search}%")

        if focus and focus != 'All':
            sql += " AND focus_area = %s"
            params.append(focus)

        sql += " ORDER BY session_date DESC"
        cursor.execute(sql, params)
        return cursor.fetchall()


def get_training_by_id(training_id):
    """Fetch a single training session by primary key."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM trainings WHERE id=%s", (training_id,))
        return cursor.fetchone()


def create_training(club_id, session_date, focus_area, duration_minutes):
    """Insert a new training session."""
    db = get_db()
    with db.cursor() as cursor:
        sql = """INSERT INTO trainings (club_id, session_date, focus_area, duration_minutes)
                 VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql, (club_id, session_date, focus_area, duration_minutes))
    db.commit()
    return cursor.lastrowid


def update_training(training_id, session_date, focus_area, duration_minutes):
    """Update an existing training session."""
    db = get_db()
    with db.cursor() as cursor:
        sql = """UPDATE trainings SET session_date=%s, focus_area=%s, duration_minutes=%s
                 WHERE id=%s"""
        cursor.execute(sql, (session_date, focus_area, duration_minutes, training_id))
    db.commit()


def delete_training(training_id):
    """Delete a training session."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM trainings WHERE id=%s", (training_id,))
    db.commit()
