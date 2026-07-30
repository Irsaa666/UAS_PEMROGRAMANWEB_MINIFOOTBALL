from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, jsonify)
from models.club_model import get_club_by_user
from models.player_model import (get_players, get_player_by_id, create_player,
                                  update_player, delete_player)
from routes.dashboard import login_required

players_bp = Blueprint('players', __name__, url_prefix='/players')

VALID_POSITIONS = ['GK', 'DEF', 'MID', 'FWD']


def _validate_player_form(form):
    """Validate player form data. Returns a list of error strings."""
    errors = []
    name   = form.get('name', '').strip()
    age    = form.get('age', '')
    pos    = form.get('position', '')
    rating = form.get('overall_rating', '')
    salary = form.get('salary', '')

    if not name or len(name) < 2:
        errors.append('Player name must be at least 2 characters.')
    if not age or not age.isdigit() or not (15 <= int(age) <= 45):
        errors.append('Age must be an integer between 15 and 45.')
    if pos not in VALID_POSITIONS:
        errors.append('Position must be one of: GK, DEF, MID, FWD.')
    if not rating or not rating.isdigit() or not (1 <= int(rating) <= 100):
        errors.append('Overall rating must be an integer between 1 and 100.')
    try:
        s = float(salary)
        if s < 0:
            raise ValueError
    except (ValueError, TypeError):
        errors.append('Salary must be a positive number.')
    return errors


@players_bp.route('/', methods=['GET'])
@login_required
def index():
    """List players with optional search and position filter."""
    user_id  = session['user_id']
    club     = get_club_by_user(user_id)
    search   = request.args.get('search', '').strip()
    position = request.args.get('position', 'All')

    players = get_players(club['id'], search=search or None, position=position)
    return render_template('pages/players.html',
                           club=club,
                           players=players,
                           search=search,
                           position_filter=position,
                           positions=VALID_POSITIONS)


@players_bp.route('/add', methods=['POST'])
@login_required
def add():
    """Create a new player via modal form submission."""
    user_id = session['user_id']
    club    = get_club_by_user(user_id)
    errors  = _validate_player_form(request.form)

    if errors:
        for err in errors:
            flash(err, 'danger')
        return redirect(url_for('players.index'))

    create_player(
        club_id        = club['id'],
        name           = request.form['name'].strip(),
        age            = int(request.form['age']),
        position       = request.form['position'],
        overall_rating = int(request.form['overall_rating']),
        salary         = float(request.form['salary']),
    )
    flash('Player added successfully!', 'success')
    return redirect(url_for('players.index'))


@players_bp.route('/edit/<int:player_id>', methods=['POST'])
@login_required
def edit(player_id):
    """Update an existing player's details."""
    user_id = session['user_id']
    club    = get_club_by_user(user_id)
    player  = get_player_by_id(player_id)

    # Security: ensure the player belongs to this user's club
    if not player or player['club_id'] != club['id']:
        flash('Player not found.', 'danger')
        return redirect(url_for('players.index'))

    errors = _validate_player_form(request.form)
    if errors:
        for err in errors:
            flash(err, 'danger')
        return redirect(url_for('players.index'))

    update_player(
        player_id      = player_id,
        name           = request.form['name'].strip(),
        age            = int(request.form['age']),
        position       = request.form['position'],
        overall_rating = int(request.form['overall_rating']),
        salary         = float(request.form['salary']),
    )
    flash('Player updated successfully!', 'success')
    return redirect(url_for('players.index'))


@players_bp.route('/delete/<int:player_id>', methods=['POST'])
@login_required
def delete(player_id):
    """Release (delete) a player from the club."""
    user_id = session['user_id']
    club    = get_club_by_user(user_id)
    player  = get_player_by_id(player_id)

    if not player or player['club_id'] != club['id']:
        flash('Player not found.', 'danger')
        return redirect(url_for('players.index'))

    delete_player(player_id)
    flash('Player released from the club.', 'info')
    return redirect(url_for('players.index'))


@players_bp.route('/get/<int:player_id>', methods=['GET'])
@login_required
def get_player(player_id):
    """Return player JSON data for edit modal population."""
    user_id = session['user_id']
    club    = get_club_by_user(user_id)
    player  = get_player_by_id(player_id)

    if not player or player['club_id'] != club['id']:
        return jsonify({'error': 'Not found'}), 404

    return jsonify({
        'id':             player['id'],
        'name':           player['name'],
        'age':            player['age'],
        'position':       player['position'],
        'overall_rating': player['overall_rating'],
        'salary':         float(player['salary']),
    })
