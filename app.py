from flask import Flask
from models.database import close_connection
from models.database import init_db 

app = Flask(__name__)
app.secret_key = 's4l143@@'

init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    close_connection(exception)


if __name__ == "__main__":
    app.run(debug=True)
    