import os
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, current_app)
from werkzeug.utils import secure_filename
from models.club_model import get_club_by_user, update_club
from routes.dashboard import login_required

club_bp = Blueprint('club', __name__, url_prefix='/club')




@club_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """View and edit the club profile."""
    user_id = session['user_id']
    club    = get_club_by_user(user_id)

    if request.method == 'POST':
        name         = request.form.get('name', '').strip()
        stadium_name = request.form.get('stadium_name', '').strip()
        founded_year = request.form.get('founded_year', '').strip()
        logo_path = request.form.get('logo_path', club.get('logo_path'))
        
        # Validation
        errors = []
        if not name or len(name) > 100:
            errors.append('Club name is required and must be under 100 characters.')
        if not stadium_name or len(stadium_name) > 100:
            errors.append('Stadium name is required and must be under 100 characters.')
        if not founded_year or not founded_year.isdigit() or not (1800 <= int(founded_year) <= 2026):
            errors.append('Founded year must be a valid number between 1800 and 2026.')

        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template('pages/club_profile.html', club=club)

        allowed_logos = ['barcelona.png', 'arsenal.png', 'real_madrid.png', 
                         'generic_blue.png', 'generic_red.png', 'eagle.png', 'phoenix.png']
        if logo_path not in allowed_logos:
            logo_path = 'generic_blue.png'

        update_club(club['id'], name, stadium_name, int(founded_year), logo_path)
        flash('Club profile updated successfully!', 'success')
        return redirect(url_for('club.profile'))

    return render_template('pages/club_profile.html', club=club)
