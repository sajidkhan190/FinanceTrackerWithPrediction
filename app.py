from flask import Flask, session, redirect, url_for, render_template
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
    
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    db = get_db()


    # Total Income
    income = db.execute("""
        SELECT SUM(amount) FROM transactions
        WHERE user_id = ? AND type = 'income'
    """, (session['user_id'],)).fetchone()[0]

    # Total Expense
    expense = db.execute("""
        SELECT SUM(amount) FROM transactions
        WHERE user_id = ? AND type = 'expense'
    """, (session['user_id'],)).fetchone()[0]

    income = income if income else 0
    expense = expense if expense else 0

    balance = income - expense

    return render_template(
        "dashboard.html",
        name=session['user_name'],
        income = income,
        expense = expense,
        balance = balance
        
    )

if __name__ == '__main__':
    app.run(debug=True)
    

