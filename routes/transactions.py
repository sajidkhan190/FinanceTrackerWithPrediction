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
        return redirect(url_for('dashboard_bp.dashboard'))

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


@transactions.route('/expenses/<int:transaction_id>/delete', methods=['POST'])
def delete_expense(transaction_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    db = get_db()
    result = db.execute("""
        DELETE FROM transactions
        WHERE id = ? AND user_id = ? AND type = 'expense'
    """, (transaction_id, session['user_id']))
    db.commit()

    if result.rowcount:
        flash('Expense deleted successfully!', 'success')
    else:
        flash('Expense not found or permission denied.', 'error')

    return redirect(url_for('transactions.view_expenses'))


@transactions.route('/expenses/<int:transaction_id>/edit', methods=['POST'])
def edit_expense(transaction_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    category = request.form.get('category', '').strip()
    description = request.form.get('description', '').strip()
    date = request.form.get('date', '').strip()
    amount_raw = request.form.get('amount', '').strip()

    try:
        amount = float(amount_raw)
    except ValueError:
        flash('Invalid amount value.', 'error')
        return redirect(url_for('transactions.view_expenses'))

    if not category or not date:
        flash('Category and date are required.', 'error')
        return redirect(url_for('transactions.view_expenses'))

    if amount <= 0:
        flash('Amount must be greater than zero.', 'error')
        return redirect(url_for('transactions.view_expenses'))

    db = get_db()
    result = db.execute("""
        UPDATE transactions
        SET category = ?, amount = ?, description = ?, date = ?
        WHERE id = ? AND user_id = ? AND type = 'expense'
    """, (category, amount, description, date, transaction_id, session['user_id']))
    db.commit()

    if result.rowcount:
        flash('Expense updated successfully!', 'success')
    else:
        flash('Expense not found or permission denied.', 'error')

    return redirect(url_for('transactions.view_expenses'))

@transactions.route('/add_income', methods=['GET', 'POST'])
def add_income():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        t_type = 'income'  # Yahan hum type automatically 'income' set kar rahe hain
        category = request.form['category']
        amount = request.form['amount']
        description = request.form.get('description', '')
        date = request.form['date']

        if float(amount) <= 0:
            flash('Amount must be greater than zero', 'error')
            return redirect(url_for('transactions.add_income'))

        db = get_db()
        db.execute("""
                   INSERT INTO transactions
                   (user_id, type, category, amount, description, date)
                     VALUES (?, ?, ?, ?, ?, ?)
                     """, (session['user_id'], t_type, category, amount, description, date))
        
        db.commit()
        flash('Income added successfully!', 'success')
        return redirect(url_for('dashboard_bp.dashboard'))
    
    # Hum aapki khali add_entry.html file ko Add Income ke liye use karenge
    return render_template('add_entry.html') 

@transactions.route('/incomes')
def view_incomes():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    db = get_db()
    incomes = db.execute("""
        SELECT id, category, amount, description, date 
        FROM transactions
        WHERE user_id = ? AND type = 'income'
        ORDER BY date DESC
    """, (session['user_id'],)).fetchall()

    return render_template('incomes.html', incomes=incomes)


@transactions.route('/incomes/<int:transaction_id>/delete', methods=['POST'])
def delete_income(transaction_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    db = get_db()
    result = db.execute("""
        DELETE FROM transactions
        WHERE id = ? AND user_id = ? AND type = 'income'
    """, (transaction_id, session['user_id']))
    db.commit()

    if result.rowcount:
        flash('Income deleted successfully!', 'success')
    else:
        flash('Income not found or permission denied.', 'error')

    return redirect(url_for('transactions.view_incomes'))


@transactions.route('/incomes/<int:transaction_id>/edit', methods=['POST'])
def edit_income(transaction_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    category = request.form.get('category', '').strip()
    description = request.form.get('description', '').strip()
    date = request.form.get('date', '').strip()
    amount_raw = request.form.get('amount', '').strip()

    try:
        amount = float(amount_raw)
    except ValueError:
        flash('Invalid amount value.', 'error')
        return redirect(url_for('transactions.view_incomes'))

    if not category or not date:
        flash('Category and date are required.', 'error')
        return redirect(url_for('transactions.view_incomes'))

    if amount <= 0:
        flash('Amount must be greater than zero.', 'error')
        return redirect(url_for('transactions.view_incomes'))

    db = get_db()
    result = db.execute("""
        UPDATE transactions
        SET category = ?, amount = ?, description = ?, date = ?
        WHERE id = ? AND user_id = ? AND type = 'income'
    """, (category, amount, description, date, transaction_id, session['user_id']))
    db.commit()

    if result.rowcount:
        flash('Income updated successfully!', 'success')
    else:
        flash('Income not found or permission denied.', 'error')

    return redirect(url_for('transactions.view_incomes'))