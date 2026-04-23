import json
from flask import Blueprint, render_template, request, session, redirect, url_for, Response, flash
from models.database import get_db

backup = Blueprint('backup', __name__)

@backup.route('/backup')
def backup_page():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('backup.html')

@backup.route('/backup/download')
def download_backup():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    db = get_db()
    # Sirf login user ka data nikalna hai (Secure Approach)
    transactions = db.execute("""
        SELECT type, category, amount, description, date 
        FROM transactions 
        WHERE user_id = ?
    """, (session['user_id'],)).fetchall()
    
    # Data ko dictionary mein convert karna
    data = [dict(row) for row in transactions]
    
    # JSON file create karna
    json_data = json.dumps(data, indent=4)
    return Response(json_data, mimetype='application/json', headers={"Content-Disposition": "attachment; filename=My_Finance_Backup.json"})

@backup.route('/backup/restore', methods=['POST'])
def restore_backup():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if 'backup_file' not in request.files:
        flash('No file uploaded!', 'error')
        return redirect(url_for('backup.backup_page'))
        
    file = request.files['backup_file']
    if file.filename == '':
        flash('No file selected!', 'error')
        return redirect(url_for('backup.backup_page'))
        
    if file and file.filename.endswith('.json'):
        try:
            data = json.load(file)
            db = get_db()
            user_id = session['user_id']
            
            count = 0
            for item in data:
                # User ka apna ID use kar ke data wapis insert karna
                db.execute("""
                    INSERT INTO transactions (user_id, type, category, amount, description, date)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, item['type'], item['category'], item['amount'], item.get('description', ''), item['date']))
                count += 1
                
            db.commit()
            flash(f'Backup Restored: {count} records added successfully!', 'success')
        except Exception as e:
            flash('Invalid backup file. Please upload a correct JSON backup.', 'error')
    else:
        flash('Please upload a valid .json file.', 'error')
        
    return redirect(url_for('backup.backup_page'))