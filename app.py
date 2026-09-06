from flask import Flask, render_template, request, redirect, url_for, session, g
from sqlalchemy import create_engine, text
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Ensure the instance folder exists
os.makedirs(app.instance_path, exist_ok=True)
DATABASE_URI = f"sqlite:///{os.path.join(app.instance_path, 'data.db')}"
engine = create_engine(DATABASE_URI)

def get_db():
    """Wrapper function for database session access"""
    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = engine.connect()
    return conn

@app.teardown_appcontext
def close_connection(exception):
    conn = getattr(g, '_database', None)
    if conn is not None:
        conn.close()

def login_required(f):
    """Wrapper function for user session access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login.html', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Simple dummy authentication, replace with real DB check using text()
        # conn = get_db()
        # result = conn.execute(text("SELECT * FROM users WHERE username = :user"), {"user": "admin"})
        
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/dashboard.html')
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/question.html')
@app.route('/questions')
@login_required
def questions():
    return render_template('question.html')

@app.route('/team.html')
@app.route('/teams')
@login_required
def teams():
    return render_template('team.html')

@app.route('/submission.html')
@app.route('/submissions')
@login_required
def submissions():
    return render_template('submission.html')

# Initialize DB schema using text() and commit()
def init_db():
    with app.app_context():
        conn = get_db()
        # Create tables here using normal string queries
        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY, 
                username TEXT, 
                password TEXT
            )
        '''))
        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                question_text TEXT,
                option_a TEXT,
                option_b TEXT,
                option_c TEXT,
                option_d TEXT,
                correct_option TEXT
            )
        '''))
        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY,
                team_name TEXT,
                score INTEGER DEFAULT 0
            )
        '''))
        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY,
                team_id INTEGER,
                question_id INTEGER,
                submitted_option TEXT,
                is_correct BOOLEAN,
                FOREIGN KEY(team_id) REFERENCES teams(id),
                FOREIGN KEY(question_id) REFERENCES questions(id)
            )
        '''))
        conn.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)

