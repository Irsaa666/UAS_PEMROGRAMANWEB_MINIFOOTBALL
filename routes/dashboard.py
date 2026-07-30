from flask import Blueprint, render_template, session, redirect, url_for
from models.club_model import get_club_by_user
from models.player_model import count_players
from models.match_model import get_match_stats, get_next_match, get_recent_matches

dashboard_bp = Blueprint('dashboard', __name__)


def login_required(f):
    """Decorator to protect routes that require authentication."""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@dashboard_bp.route('/')
@login_required
def index():
    """Render the main dashboard with club summary data."""
    user_id = session['user_id']
    club    = get_club_by_user(user_id)

    if not club:
        return redirect(url_for('auth.logout'))

    club_id      = club['id']
    total_players = count_players(club_id)
    match_stats   = get_match_stats(club_id)
    next_match    = get_next_match(club_id)
    recent        = get_recent_matches(club_id, limit=5)

    # Prepare recent match data for Chart.js
    chart_labels = []
    chart_gf     = []
    chart_ga     = []
    for m in reversed(recent):
        chart_labels.append(f"vs {m['opponent_name']}")
        chart_gf.append(m['goals_for'])
        chart_ga.append(m['goals_against'])

    return render_template(
        'pages/dashboard.html',
        club          = club,
        total_players = total_players,
        match_stats   = match_stats,
        next_match    = next_match,
        recent_matches= recent,
        chart_labels  = chart_labels,
        chart_gf      = chart_gf,
        chart_ga      = chart_ga,
    )
