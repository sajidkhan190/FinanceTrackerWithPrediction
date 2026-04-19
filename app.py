from flask import Flask, session, redirect, url_for, render_template, jsonify
from models.database import close_connection, init_db, get_db 
from routes.auth import auth 
from routes.transactions import transactions
from routes.dashboard import dashboard_bp
from routes.reports import reports

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(transactions)
app.register_blueprint(dashboard_bp)
app.register_blueprint(reports)
app.secret_key = 's4l143@@'

init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    close_connection(exception)
    
@app.route('/')
def index():
    return redirect(url_for('auth.login'))


if __name__ == '__main__':
    app.run(debug=True)
    

