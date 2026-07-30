from config.database import get_db


def get_finances(club_id, transaction_type=None, search=None):
    """Fetch all financial records for a club with optional filters."""
    db = get_db()
    with db.cursor() as cursor:
        sql = "SELECT * FROM finances WHERE club_id = %s"
        params = [club_id]

        if transaction_type and transaction_type != 'All':
            sql += " AND transaction_type = %s"
            params.append(transaction_type)

        if search:
            sql += " AND description LIKE %s"
            params.append(f"%{search}%")

        sql += " ORDER BY transaction_date DESC"
        cursor.execute(sql, params)
        return cursor.fetchall()


def get_finance_by_id(finance_id):
    """Fetch a single finance record by primary key."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM finances WHERE id=%s", (finance_id,))
        return cursor.fetchone()


def create_finance(club_id, transaction_date, transaction_type, amount, description):
    """Insert a new financial record and adjust club budget."""
    db = get_db()
    with db.cursor() as cursor:
        sql = """INSERT INTO finances (club_id, transaction_date, transaction_type, amount, description)
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (club_id, transaction_date, transaction_type, amount, description))

        # Adjust club budget based on transaction type
        if transaction_type == 'Income':
            cursor.execute("UPDATE clubs SET budget = budget + %s WHERE id = %s", (amount, club_id))
        else:
            cursor.execute("UPDATE clubs SET budget = budget - %s WHERE id = %s", (amount, club_id))
    db.commit()
    return cursor.lastrowid


def delete_finance(finance_id, club_id, transaction_type, amount):
    """Delete a finance record and reverse the budget adjustment."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM finances WHERE id=%s", (finance_id,))
        # Reverse the budget effect
        if transaction_type == 'Income':
            cursor.execute("UPDATE clubs SET budget = budget - %s WHERE id = %s", (amount, club_id))
        else:
            cursor.execute("UPDATE clubs SET budget = budget + %s WHERE id = %s", (amount, club_id))
    db.commit()


def update_finance(finance_id, club_id, new_date, new_type, new_amount, new_description, old_type, old_amount):
    """Update a finance record and adjust the budget difference."""
    db = get_db()
    with db.cursor() as cursor:
        sql = """UPDATE finances SET transaction_date=%s, transaction_type=%s, amount=%s, description=%s
                 WHERE id=%s"""
        cursor.execute(sql, (new_date, new_type, new_amount, new_description, finance_id))

        # Revert old budget effect
        if old_type == 'Income':
            cursor.execute("UPDATE clubs SET budget = budget - %s WHERE id = %s", (old_amount, club_id))
        else:
            cursor.execute("UPDATE clubs SET budget = budget + %s WHERE id = %s", (old_amount, club_id))

        # Apply new budget effect
        if new_type == 'Income':
            cursor.execute("UPDATE clubs SET budget = budget + %s WHERE id = %s", (new_amount, club_id))
        else:
            cursor.execute("UPDATE clubs SET budget = budget - %s WHERE id = %s", (new_amount, club_id))
            
    db.commit()


def get_finance_summary(club_id):
    """Return total income and total expense for the club."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT transaction_type, SUM(amount) AS total
            FROM finances WHERE club_id = %s
            GROUP BY transaction_type
        """, (club_id,))
        rows = cursor.fetchall()
        summary = {'Income': 0, 'Expense': 0}
        for row in rows:
            summary[row['transaction_type']] = float(row['total'])
        return summary


def get_monthly_summary(club_id):
    """Return monthly income/expense data for chart rendering (last 6 months)."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT
                DATE_FORMAT(transaction_date, '%%Y-%%m') AS month,
                transaction_type,
                SUM(amount) AS total
            FROM finances
            WHERE club_id = %s
              AND transaction_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
            GROUP BY month, transaction_type
            ORDER BY month ASC
        """, (club_id,))
        return cursor.fetchall()
