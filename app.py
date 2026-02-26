from flask import Flask, session, redirect, url_for, render_template, jsonify
from models.database import close_connection, init_db, get_db 
from routes.auth import auth 
from routes.transactions import transactions


app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(transactions)
app.secret_key = 's4l143@@'

init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    close_connection(exception)
    
@app.route('/')
def index():
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    db = get_db()

    # Total Expense
    expense = db.execute("""
        SELECT SUM(amount) FROM transactions
        WHERE user_id = ? AND type = 'expense'
    """, (session['user_id'],)).fetchone()[0]

    expense = expense if expense else 0

    # Category-wise expense distribution (for pie chart)
    category_data = db.execute("""
        SELECT category, SUM(amount) as total
        FROM transactions
        WHERE user_id = ? AND type = 'expense'
        GROUP BY category
        ORDER BY total DESC
    """, (session['user_id'],)).fetchall()

    categories = [row['category'] for row in category_data]
    category_amounts = [row['total'] for row in category_data]

    # Monthly expense summary (for bar chart)
    monthly_data = db.execute("""
        SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
        FROM transactions
        WHERE user_id = ? AND type = 'expense'
        GROUP BY month
        ORDER BY month
    """, (session['user_id'],)).fetchall()

    months = [row['month'] for row in monthly_data]
    monthly_amounts = [row['total'] for row in monthly_data]

    # Recent 5 expenses
    recent_expenses = db.execute("""
        SELECT category, amount, date, description
        FROM transactions
        WHERE user_id = ? AND type = 'expense'
        ORDER BY date DESC
        LIMIT 5
    """, (session['user_id'],)).fetchall()

    return render_template(
        "dashboard.html",
        name=session['user_name'],
        expense=expense,
        categories=categories,
        category_amounts=category_amounts,
        months=months,
        monthly_amounts=monthly_amounts,
        recent_expenses=recent_expenses
    )

if __name__ == '__main__':
    app.run(debug=True)
    

