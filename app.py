from flask import Flask
from models.database import close_connection
from models.database import init_db 
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


if __name__ == "__main__":
    app.run(debug=True)
    
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    return f"""
    <h2> Welcome {session['user_name']}</h2>
    <a href='/add'> Add Transaction </a><br>
    <a href='/logout'> Logout </a>
    """

