from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.database import get_db

transactions = Blueprint('transactions', __name__)

@transactions.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        t_type = request.form['type']
        catergory = request.form['category']
        amount = request.form['amount']
        description = request.form['description']
        date = request.form['date']

        if float (amount) <= 0:
            flash('Amount must be greater than zero', 'danger')
            return redirect(url_for('transactions.add_trasaction'))
        

        db = get_db()
        db.execute("""
                   INSERT INTO transactions
                   (user_id, type, category, amount, description, date)
                     VALUES (?, ?, ?, ?, ?, ?)
                     """, (session['user_id'], t_type, catergory, amount, description, date))
        
        db.commit()
        flash('Transaction added successfully', 'success')
        return redirect(url_for('auth.dashboard'))

    return render_template('add_transaction.html')
