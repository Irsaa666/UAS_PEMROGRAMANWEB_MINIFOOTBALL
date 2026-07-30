from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash)
from models.club_model import get_club_by_user
from models.squad_model import (get_squad, get_unassigned_players,
                                  assign_player_to_squad, update_squad_role,
                                  remove_from_squad)
from routes.dashboard import login_required

squad_bp = Blueprint('squad', __name__, url_prefix='/squad')

VALID_ROLES = ['Starting XI', 'Substitute', 'Reserve', 'Injured']


@squad_bp.route('/', methods=['GET'])
@login_required
def index():
    """Display the current squad configuration."""
    user_id    = session['user_id']
    club       = get_club_by_user(user_id)
    squad      = get_squad(club['id'])
    unassigned = get_unassigned_players(club['id'])

    # Group squad members by role for display
    grouped = {role: [] for role in VALID_ROLES}
    for member in squad:
        grouped[member['role']].append(member)

    return render_template('pages/squad.html',
                           club=club,
                           grouped_squad=grouped,
                           unassigned=unassigned,
                           roles=VALID_ROLES)


@squad_bp.route('/assign', methods=['POST'])
@login_required
def assign():
    """Assign or move a player to a squad role."""
    user_id   = session['user_id']
    club      = get_club_by_user(user_id)
    player_id = request.form.get('player_id', type=int)
    role      = request.form.get('role', '').strip()

    if not player_id or role not in VALID_ROLES:
        flash('Invalid assignment data.', 'danger')
        return redirect(url_for('squad.index'))

    assign_player_to_squad(club['id'], player_id, role)
    flash('Player assigned to squad successfully!', 'success')
    return redirect(url_for('squad.index'))


@squad_bp.route('/update-role', methods=['POST'])
@login_required
def update_role():
    """Update the role of a player already in the squad."""
    squad_id = request.form.get('squad_id', type=int)
    role     = request.form.get('role', '').strip()

    if not squad_id or role not in VALID_ROLES:
        flash('Invalid role update data.', 'danger')
        return redirect(url_for('squad.index'))

    update_squad_role(squad_id, role)
    flash('Squad role updated!', 'success')
    return redirect(url_for('squad.index'))


@squad_bp.route('/remove/<int:squad_id>', methods=['POST'])
@login_required
def remove(squad_id):
    """Remove a player from the squad list."""
    remove_from_squad(squad_id)
    flash('Player removed from squad.', 'info')
    return redirect(url_for('squad.index'))
