from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, jsonify)
from models.club_model import get_club_by_user
from models.match_model import (get_matches, get_match_by_id, create_match,
                                  update_match_schedule, log_match_result,
                                  delete_match)
from routes.dashboard import login_required

matches_bp = Blueprint('matches', __name__, url_prefix='/matches')


@matches_bp.route('/', methods=['GET'])
@login_required
def index():
    """List all match fixtures with optional status filter."""
    user_id = session['user_id']
    club    = get_club_by_user(user_id)
    status  = request.args.get('status', 'All')

    fixtures = get_matches(club['id'], status=status if status != 'All' else None)
    return render_template('pages/matches.html',
                           club=club,
                           fixtures=fixtures,
                           status_filter=status)


@matches_bp.route('/add', methods=['POST'])
@login_required
def add():
    """Schedule a new match fixture."""
    user_id      = session['user_id']
    club         = get_club_by_user(user_id)
    opponent     = request.form.get('opponent_name', '').strip()
    match_date   = request.form.get('match_date', '').strip()

    errors = []
    if not opponent or len(opponent) < 2:
        errors.append('Opponent name must be at least 2 characters.')
    if not match_date:
        errors.append('Match date and time is required.')

    if errors:
        for err in errors:
            flash(err, 'danger')
        return redirect(url_for('matches.index'))

    create_match(club['id'], opponent, match_date)
    flash('Match fixture scheduled!', 'success')
    return redirect(url_for('matches.index'))


@matches_bp.route('/edit/<int:match_id>', methods=['POST'])
@login_required
def edit(match_id):
    """Update a scheduled match's details."""
    user_id    = session['user_id']
    club       = get_club_by_user(user_id)
    match      = get_match_by_id(match_id)

    if not match or match['club_id'] != club['id']:
        flash('Match not found.', 'danger')
        return redirect(url_for('matches.index'))

    opponent   = request.form.get('opponent_name', '').strip()
    match_date = request.form.get('match_date', '').strip()

    errors = []
    if not opponent or len(opponent) < 2:
        errors.append('Opponent name must be at least 2 characters.')
    if not match_date:
        errors.append('Match date is required.')

    if errors:
        for err in errors:
            flash(err, 'danger')
        return redirect(url_for('matches.index'))

    update_match_schedule(match_id, opponent, match_date)
    flash('Match updated successfully!', 'success')
    return redirect(url_for('matches.index'))


@matches_bp.route('/result/<int:match_id>', methods=['POST'])
@login_required
def result(match_id):
    """Log the result of a played match."""
    user_id = session['user_id']
    club    = get_club_by_user(user_id)
    match   = get_match_by_id(match_id)

    if not match or match['club_id'] != club['id']:
        flash('Match not found.', 'danger')
        return redirect(url_for('matches.index'))

    gf = request.form.get('goals_for', '')
    ga = request.form.get('goals_against', '')

    errors = []
    if not gf or not gf.isdigit() or int(gf) < 0:
        errors.append('Goals scored must be a positive integer or 0.')
    if not ga or not ga.isdigit() or int(ga) < 0:
        errors.append('Goals conceded must be a positive integer or 0.')

    if errors:
        for err in errors:
            flash(err, 'danger')
        return redirect(url_for('matches.index'))

    log_match_result(match_id, int(gf), int(ga))
    flash('Match result recorded!', 'success')
    return redirect(url_for('matches.index'))


@matches_bp.route('/delete/<int:match_id>', methods=['POST'])
@login_required
def delete(match_id):
    """Delete/cancel a match fixture."""
    user_id = session['user_id']
    club    = get_club_by_user(user_id)
    match   = get_match_by_id(match_id)

    if not match or match['club_id'] != club['id']:
        flash('Match not found.', 'danger')
        return redirect(url_for('matches.index'))

    delete_match(match_id)
    flash('Match fixture removed.', 'info')
    return redirect(url_for('matches.index'))


@matches_bp.route('/get/<int:match_id>', methods=['GET'])
@login_required
def get_match(match_id):
    """Return match JSON for modal population."""
    user_id = session['user_id']
    club    = get_club_by_user(user_id)
    match   = get_match_by_id(match_id)

    if not match or match['club_id'] != club['id']:
        return jsonify({'error': 'Not found'}), 404

    return jsonify({
        'id':            match['id'],
        'opponent_name': match['opponent_name'],
        'match_date':    str(match['match_date']).replace(' ', 'T')[:16],
        'status':        match['status'],
    })
