from flask import Flask
from models.database import close_connection
from models.database import init_db 
from routes.auth import auth 

app = Flask(__name__)
app.register_blueprint(auth)
app.secret_key = 's4l143@@'

init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    close_connection(exception)


if __name__ == "__main__":
    app.run(debug=True)
    
@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard!"

