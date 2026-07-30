from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user_model import (create_user, get_user_by_email, email_exists,
                                username_exists, verify_password)
from models.club_model import create_club, get_club_by_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        # Basic presence validation
        if not email or not password:
            flash('Email and password are required.', 'danger')
            return render_template('pages/login.html')

        user = get_user_by_email(email)
        if not user or not verify_password(user, password):
            flash('Invalid email or password. Please try again.', 'danger')
            return render_template('pages/login.html')

        # Store user info in session
        session['user_id']  = user['id']
        session['username'] = user['username']
        flash(f"Welcome back, {user['username']}!", 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('pages/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle new user registration with club setup."""
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username     = request.form.get('username', '').strip()
        email        = request.form.get('email', '').strip()
        password     = request.form.get('password', '')
        confirm_pass = request.form.get('confirm_password', '')
        club_name    = request.form.get('club_name', '').strip()
        stadium_name = request.form.get('stadium_name', '').strip()
        founded_year = request.form.get('founded_year', '').strip()

        # --- Validation ---
        errors = []
        if not username or len(username) < 2:
            errors.append('Username must be at least 2 characters.')
        if not email or '@' not in email:
            errors.append('Please enter a valid email address.')
        if len(password) < 8:
            errors.append('Password must be at least 8 characters.')
        if password != confirm_pass:
            errors.append('Passwords do not match.')
        if not club_name or len(club_name) < 2:
            errors.append('Club name must be at least 2 characters.')
        if not stadium_name or len(stadium_name) < 2:
            errors.append('Stadium name must be at least 2 characters.')
        if not founded_year or not founded_year.isdigit() or not (1800 <= int(founded_year) <= 2026):
            errors.append('Founded year must be a valid year between 1800 and 2026.')
        if username_exists(username):
            errors.append('That username is already taken.')
        if email_exists(email):
            errors.append('That email address is already registered.')

        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template('pages/register.html',
                                   form_data=request.form)

        # --- Create user and club ---
        user_id = create_user(username, email, password)
        create_club(user_id, club_name, stadium_name, int(founded_year))

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('pages/register.html', form_data={})


@auth_bp.route('/logout')
def logout():
    """Clear the session and redirect to login."""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
