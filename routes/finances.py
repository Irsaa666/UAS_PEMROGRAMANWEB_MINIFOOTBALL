from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash)
from models.club_model import get_club_by_user
from models.finance_model import (get_finances, get_finance_by_id,
                                   create_finance, delete_finance,
                                   get_finance_summary, get_monthly_summary)
from routes.dashboard import login_required
import json

finances_bp = Blueprint('finances', __name__, url_prefix='/finances')


@finances_bp.route('/', methods=['GET'])
@login_required
def index():
    """Display the financial ledger with summary cards and monthly chart."""
    user_id = session['user_id']
    club    = get_club_by_user(user_id)
    tx_type = request.args.get('type', 'All')
    search  = request.args.get('search', '').strip()

    records  = get_finances(club['id'],
                            transaction_type=tx_type if tx_type != 'All' else None,
                            search=search or None)
    summary  = get_finance_summary(club['id'])
    monthly  = get_monthly_summary(club['id'])

    # Build chart data for Chart.js
    months_set     = sorted(set(r['month'] for r in monthly))
    income_data    = {r['month']: float(r['total']) for r in monthly if r['transaction_type'] == 'Income'}
    expense_data   = {r['month']: float(r['total']) for r in monthly if r['transaction_type'] == 'Expense'}
    chart_labels   = months_set
    chart_income   = [income_data.get(m, 0)  for m in months_set]
    chart_expenses = [expense_data.get(m, 0) for m in months_set]

    return render_template('pages/finances.html',
                           club=club,
                           records=records,
                           summary=summary,
                           type_filter=tx_type,
                           search=search,
                           chart_labels=json.dumps(chart_labels),
                           chart_income=json.dumps(chart_income),
                           chart_expenses=json.dumps(chart_expenses))


@finances_bp.route('/add', methods=['POST'])
@login_required
def add():
    """Add a new income or expense record."""
    user_id          = session['user_id']
    club             = get_club_by_user(user_id)
    transaction_date = request.form.get('transaction_date', '').strip()
    transaction_type = request.form.get('transaction_type', '').strip()
    amount           = request.form.get('amount', '').strip()
    description      = request.form.get('description', '').strip()

    errors = []
    if not transaction_date:
        errors.append('Transaction date is required.')
    if transaction_type not in ['Income', 'Expense']:
        errors.append('Transaction type must be Income or Expense.')
    try:
        amt = float(amount)
        if amt <= 0:
            raise ValueError
    except (ValueError, TypeError):
        errors.append('Amount must be a positive number.')
        amt = 0
    if not description or len(description) > 255:
        errors.append('Description is required and must be under 255 characters.')

    if errors:
        for err in errors:
            flash(err, 'danger')
        return redirect(url_for('finances.index'))

    create_finance(club['id'], transaction_date, transaction_type, amt, description)
    flash('Financial record added!', 'success')
    return redirect(url_for('finances.index'))


@finances_bp.route('/delete/<int:finance_id>', methods=['POST'])
@login_required
def delete(finance_id):
    """Delete a financial record and reverse the budget impact."""
    user_id = session['user_id']
    club    = get_club_by_user(user_id)
    record  = get_finance_by_id(finance_id)

    if not record or record['club_id'] != club['id']:
        flash('Record not found.', 'danger')
        return redirect(url_for('finances.index'))

    delete_finance(finance_id, club['id'], record['transaction_type'], float(record['amount']))
    flash('Financial record deleted and budget adjusted.', 'info')
    return redirect(url_for('finances.index'))
