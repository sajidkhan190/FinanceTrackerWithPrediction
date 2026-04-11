from flask import Blueprint, render_template, session, redirect, url_for
from models.database import get_db

# Blueprint banaya
dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    db = get_db()
    user_id = session['user_id']

    # 1. Total Expense
    expense = db.execute("""
        SELECT SUM(amount) FROM transactions
        WHERE user_id = ? AND type = 'expense'
    """, (user_id,)).fetchone()[0]
    expense = expense if expense else 0

    # 2. Total Income (Naya Hissa)
    income = db.execute("""
        SELECT SUM(amount) FROM transactions
        WHERE user_id = ? AND type = 'income'
    """, (user_id,)).fetchone()[0]
    income = income if income else 0

    # 3. Current Balance
    balance = income - expense

    # 4. Category-wise expense (Pie Chart ke liye)
    category_data = db.execute("""
        SELECT category, SUM(amount) as total
        FROM transactions
        WHERE user_id = ? AND type = 'expense'
        GROUP BY category
        ORDER BY total DESC
    """, (user_id,)).fetchall()
    categories = [row['category'] for row in category_data]
    category_amounts = [row['total'] for row in category_data]

    # 5. Monthly expense summary (Bar Chart ke liye)
    monthly_data = db.execute("""
        SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
        FROM transactions
        WHERE user_id = ? AND type = 'expense'
        GROUP BY month
        ORDER BY month
    """, (user_id,)).fetchall()
    months = [row['month'] for row in monthly_data]
    monthly_amounts = [row['total'] for row in monthly_data]

    # 6. Recent 5 Transactions (Income + Expense dono aayenge)
    recent_transactions = db.execute("""
        SELECT type, category, amount, date, description
        FROM transactions
        WHERE user_id = ?
        ORDER BY date DESC
        LIMIT 5
    """, (user_id,)).fetchall()

    return render_template(
        "dashboard.html",
        name=session['user_name'],
        expense=expense,
        income=income,
        balance=balance,
        categories=categories,
        category_amounts=category_amounts,
        months=months,
        monthly_amounts=monthly_amounts,
        recent_transactions=recent_transactions
    )