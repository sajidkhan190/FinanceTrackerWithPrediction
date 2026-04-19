from flask import Blueprint, render_template, request, session, redirect, url_for, Response
from models.database import get_db

reports = Blueprint('reports', __name__)

@reports.route('/reports', methods=['GET', 'POST'])
def view_reports():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    db = get_db()
    user_id = session['user_id']
    
    # By default, saari transactions show hongi
    query = "SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC"
    params = [user_id]

    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        category = request.form.get('category')
        t_type = request.form.get('type')

        # Filters ke hisaab se query build karna
        query = "SELECT * FROM transactions WHERE user_id = ?"
        params = [user_id]
        
        if start_date and end_date:
            query += " AND date BETWEEN ? AND ?"
            params.extend([start_date, end_date])
        
        if category and category != 'all':
            query += " AND category = ?"
            params.append(category)
            
        if t_type and t_type != 'all':
            query += " AND type = ?"
            params.append(t_type)
            
        query += " ORDER BY date DESC"

    transactions = db.execute(query, params).fetchall()

    # Dropdown mein dikhane ke liye user ki use ki gayi categories nikalna
    categories_data = db.execute("SELECT DISTINCT category FROM transactions WHERE user_id = ?", (user_id,)).fetchall()
    categories = [row['category'] for row in categories_data]

    return render_template('reports.html', transactions=transactions, categories=categories)

@reports.route('/export')
def export_data():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    db = get_db()
    transactions = db.execute("""
        SELECT type, category, amount, description, date 
        FROM transactions 
        WHERE user_id = ? 
        ORDER BY date DESC
    """, (session['user_id'],)).fetchall()
    
    # CSV Data generate karna
    def generate():
        # CSV header
        yield 'Type,Category,Amount,Description,Date\n'
        for row in transactions:
            # Har row ka data comma separated
            yield f"{row['type'].capitalize()},{row['category']},{row['amount']},{row['description']},{row['date']}\n"
            
    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment; filename=Financial_Report.csv"})