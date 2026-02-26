from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.database import get_db

transactions = Blueprint('transactions', __name__)

@transactions.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        t_type = request.form['type']
        category = request.form['category']
        amount = request.form['amount']
        description = request.form.get('description', '')
        date = request.form['date']

        if float(amount) <= 0:
            flash('Amount must be greater than zero', 'error')
            return redirect(url_for('transactions.add_transaction'))

        db = get_db()
        db.execute("""
                   INSERT INTO transactions
                   (user_id, type, category, amount, description, date)
                     VALUES (?, ?, ?, ?, ?, ?)
                     """, (session['user_id'], t_type, category, amount, description, date))
        
        db.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_transaction.html')


@transactions.route('/expenses')
def view_expenses():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    db = get_db()
    expenses = db.execute("""
        SELECT id, category, amount, description, date 
        FROM transactions
        WHERE user_id = ? AND type = 'expense'
        ORDER BY date DESC
    """, (session['user_id'],)).fetchall()

    return render_template('expenses.html', expenses=expenses)
