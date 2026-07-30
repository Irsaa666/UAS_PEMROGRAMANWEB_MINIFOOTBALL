from config.database import get_db
from werkzeug.security import generate_password_hash, check_password_hash


def create_user(username, email, password):
    """Insert a new user and return the new user's ID."""
    db = get_db()
    with db.cursor() as cursor:
        password_hash = generate_password_hash(password)
        sql = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
        cursor.execute(sql, (username, email, password_hash))
    db.commit()
    return cursor.lastrowid


def get_user_by_email(email):
    """Fetch a user by email address."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        return cursor.fetchone()


def get_user_by_id(user_id):
    """Fetch a user by their primary key."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return cursor.fetchone()


def email_exists(email):
    """Return True if the email is already registered."""
    return get_user_by_email(email) is not None


def username_exists(username):
    """Return True if the username is already taken."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        return cursor.fetchone() is not None


def verify_password(user, password):
    """Check a plain-text password against the stored hash."""
    return check_password_hash(user['password_hash'], password)


def update_password(user_id, new_password):
    """Update a user's password hash."""
    db = get_db()
    with db.cursor() as cursor:
        password_hash = generate_password_hash(new_password)
        cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s", (password_hash, user_id))
    db.commit()
