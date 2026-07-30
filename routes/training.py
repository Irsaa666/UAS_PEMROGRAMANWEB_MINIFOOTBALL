from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, jsonify)
from models.club_model import get_club_by_user
from models.training_model import (get_trainings, get_training_by_id,
                                    create_training, update_training,
                                    delete_training)
from routes.dashboard import login_required

training_bp = Blueprint('training', __name__, url_prefix='/training')

FOCUS_AREAS = ['Attack', 'Defense', 'Fitness', 'Set Pieces', 'Tactics', 'Recovery', 'Goalkeeping']


@training_bp.route('/', methods=['GET'])
@login_required
def index():
    """List all training sessions with search and focus filter."""
    user_id = session['user_id']
    club    = get_club_by_user(user_id)
    search  = request.args.get('search', '').strip()
    focus   = request.args.get('focus', 'All')

    sessions = get_trainings(club['id'], search=search or None,
                             focus=focus if focus != 'All' else None)
    return render_template('pages/training.html',
                           club=club,
                           sessions=sessions,
                           search=search,
                           focus_filter=focus,
                           focus_areas=FOCUS_AREAS)


@training_bp.route('/add', methods=['POST'])
@login_required
def add():
    """Add a new training session."""
    user_id      = session['user_id']
    club         = get_club_by_user(user_id)
    session_date = request.form.get('session_date', '').strip()
    focus_area   = request.form.get('focus_area', '').strip()
    duration     = request.form.get('duration_minutes', '').strip()

    errors = []
    if not session_date:
        errors.append('Session date is required.')
    if not focus_area:
        errors.append('Focus area is required.')
    if not duration or not duration.isdigit() or int(duration) <= 0:
        errors.append('Duration must be a positive integer (minutes).')

    if errors:
        for err in errors:
            flash(err, 'danger')
        return redirect(url_for('training.index'))

    create_training(club['id'], session_date, focus_area, int(duration))
    flash('Training session scheduled!', 'success')
    return redirect(url_for('training.index'))


@training_bp.route('/edit/<int:training_id>', methods=['POST'])
@login_required
def edit(training_id):
    """Update an existing training session."""
    user_id      = session['user_id']
    club         = get_club_by_user(user_id)
    t            = get_training_by_id(training_id)

    if not t or t['club_id'] != club['id']:
        flash('Training session not found.', 'danger')
        return redirect(url_for('training.index'))

    session_date = request.form.get('session_date', '').strip()
    focus_area   = request.form.get('focus_area', '').strip()
    duration     = request.form.get('duration_minutes', '').strip()

    errors = []
    if not session_date:
        errors.append('Session date is required.')
    if not focus_area:
        errors.append('Focus area is required.')
    if not duration or not duration.isdigit() or int(duration) <= 0:
        errors.append('Duration must be a positive integer.')

    if errors:
        for err in errors:
            flash(err, 'danger')
        return redirect(url_for('training.index'))

    update_training(training_id, session_date, focus_area, int(duration))
    flash('Training session updated!', 'success')
    return redirect(url_for('training.index'))


@training_bp.route('/delete/<int:training_id>', methods=['POST'])
@login_required
def delete(training_id):
    """Delete a training session."""
    user_id = session['user_id']
    club    = get_club_by_user(user_id)
    t       = get_training_by_id(training_id)

    if not t or t['club_id'] != club['id']:
        flash('Training session not found.', 'danger')
        return redirect(url_for('training.index'))

    delete_training(training_id)
    flash('Training session removed.', 'info')
    return redirect(url_for('training.index'))


@training_bp.route('/get/<int:training_id>', methods=['GET'])
@login_required
def get_session(training_id):
    """Return training JSON for edit modal."""
    user_id = session['user_id']
    club    = get_club_by_user(user_id)
    t       = get_training_by_id(training_id)

    if not t or t['club_id'] != club['id']:
        return jsonify({'error': 'Not found'}), 404

    return jsonify({
        'id':               t['id'],
        'session_date':     str(t['session_date']),
        'focus_area':       t['focus_area'],
        'duration_minutes': t['duration_minutes'],
    })
