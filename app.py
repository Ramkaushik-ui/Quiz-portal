from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24).hex())

# Ensure the instance folder exists
os.makedirs(app.instance_path, exist_ok=True)
DATABASE_URI = f"sqlite:///{os.path.join(app.instance_path, 'data.db')}"
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="student")
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=True)
    
    team = relationship("Team", back_populates="members")

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String)
    option_a = Column(String)
    option_b = Column(String)
    option_c = Column(String)
    option_d = Column(String)
    correct_option = Column(String)
    points = Column(Integer, default=10)
    type = Column(String, default="MCQ")
    submissions = relationship("Submission", back_populates="question")

class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String)
    score = Column(Integer, default=0)
    is_disqualified = Column(Boolean, default=False)
    
    members = relationship("User", back_populates="team")
    submissions = relationship("Submission", back_populates="team")

class Submission(Base):
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    question_id = Column(Integer, ForeignKey('questions.id'))
    submitted_option = Column(String)
    is_correct = Column(Boolean, default=False)
    
    team = relationship("Team", back_populates="submissions")
    question = relationship("Question", back_populates="submissions")


def get_db():
    if 'db' not in g:
        g.db = SessionLocal()
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or session.get('role') != 'admin':
            flash("Admin access required")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'logged_in' in session:
        # Check if admin
        if session.get('role') == 'admin':
            return redirect(url_for('dashboard'))
        return redirect(url_for('student_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('loginEmail')
        password = request.form.get('loginPassword')
        
        db = get_db()
        user = db.query(User).filter(User.email == email, User.password == password).first()
        
        if user:
            session['logged_in'] = True
            session['user_id'] = user.id
            session['email'] = user.email
            session['fullname'] = user.fullname
            session['role'] = user.role
            
            if user.role == 'admin':
                return redirect(url_for('dashboard'))
            return redirect(url_for('student_dashboard'))
        else:
            flash("Invalid credentials")
            
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    fullname = request.form.get('signupName')
    email = request.form.get('signupEmail')
    password = request.form.get('signupPassword')
    confirm = request.form.get('signupConfirm')
    
    if password != confirm:
        flash("Passwords do not match")
        return redirect(url_for('login'))
        
    db = get_db()
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        flash("Email already registered")
        return redirect(url_for('login'))
        
    new_user = User(
        fullname=fullname,
        email=email,
        password=password,
        role="student"
    )
    db.add(new_user)
    db.commit()
    
    session['logged_in'] = True
    session['user_id'] = new_user.id
    session['email'] = new_user.email
    session['fullname'] = new_user.fullname
    session['role'] = new_user.role
    
    return redirect(url_for('student_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ----- ADMIN ROUTES -----
@app.route('/dashboard')
@admin_required
def dashboard():
    db = get_db()
    teams = db.query(Team).order_by(Team.score.desc()).all()
    questions = db.query(Question).all()
    submissions = db.query(Submission).order_by(Submission.id.desc()).limit(5).all()
    return render_template('dashboard.html', teams=teams, questions=questions, submissions=submissions)

@app.route('/questions')
@admin_required
def questions():
    db = get_db()
    questions_list = db.query(Question).all()
    return render_template('question.html', questions=questions_list)

@app.route('/teams')
@admin_required
def teams():
    db = get_db()
    teams_list = db.query(Team).order_by(Team.score.desc()).all()
    return render_template('team.html', teams=teams_list)

@app.route('/admin/team/<int:team_id>')
@admin_required
def team_detail(team_id):
    db = get_db()
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        flash("Team not found")
        return redirect(url_for('teams'))
    return render_template('team_detail.html', team=team)

@app.route('/admin/team/<int:team_id>/disqualify', methods=['POST'])
@admin_required
def disqualify_team(team_id):
    db = get_db()
    team = db.query(Team).filter(Team.id == team_id).first()
    if team:
        team.is_disqualified = True
        db.commit()
        flash(f"Team {team.team_name} disqualified successfully.")
    return redirect(url_for('teams'))

@app.route('/submissions')
@admin_required
def submissions():
    db = get_db()
    submissions_list = db.query(Submission).order_by(Submission.id.desc()).all()
    return render_template('submission.html', submissions=submissions_list)

# ----- STUDENT ROUTES -----
@app.route('/student/dashboard')
@login_required
def student_dashboard():
    db = get_db()
    team = db.query(Team).first() # Mocking current team for now
    teams = db.query(Team).order_by(Team.score.desc()).limit(5).all()
    return render_template('dashboardstudent.html', team=team, teams=teams, user=session)

@app.route('/student/arena')
@app.route('/student/arena/<int:question_id>')
@login_required
def student_arena(question_id=None):
    db = get_db()
    user = db.query(User).filter(User.id == session.get('user_id')).first()
    if not user or not user.team_id:
        flash("You are not part of a team.")
        return redirect(url_for('student_dashboard'))
    
    submissions = db.query(Submission).filter(Submission.team_id == user.team_id).all()
    submitted_question_ids = [s.question_id for s in submissions]
    submitted_dict = {s.question_id: s for s in submissions}
    
    all_questions = db.query(Question).all()
    
    if question_id:
        current_question = next((q for q in all_questions if q.id == question_id), None)
    else:
        current_question = next((q for q in all_questions if q.id not in submitted_question_ids), None)
    
    total_questions = len(all_questions)
    answered_questions = len(submitted_question_ids)
    
    return render_template('arenastudent.html', 
                           question=current_question,
                           all_questions=all_questions,
                           submitted_dict=submitted_dict,
                           total_questions=total_questions,
                           answered_questions=answered_questions,
                           user=session, 
                           team=user.team)

@app.route('/student/submit_answer', methods=['POST'])
@login_required
def submit_answer():
    db = get_db()
    user = db.query(User).filter(User.id == session.get('user_id')).first()
    if not user or not user.team_id:
        return redirect(url_for('student_dashboard'))
    
    question_id = request.form.get('question_id')
    answer = request.form.get('answer')
    
    if question_id and answer:
        question = db.query(Question).filter(Question.id == question_id).first()
        if question:
            existing = db.query(Submission).filter_by(team_id=user.team_id, question_id=question.id).first()
            if not existing:
                is_correct = (answer == question.correct_option)
                sub = Submission(
                    team_id=user.team_id,
                    question_id=question.id,
                    submitted_option=answer,
                    is_correct=is_correct
                )
                db.add(sub)
                
                if is_correct:
                    user.team.score += question.points
                    
                db.commit()
    
    return redirect(url_for('student_arena'))

@app.route('/student/event')
@login_required
def student_event():
    return render_template('eventstudent.html', user=session)

@app.route('/student/register')
def student_register():
    return render_template('registerstudent.html')



@app.route('/student/leaderboard')
@login_required
def student_leaderboard():
    db = get_db()
    teams = db.query(Team).order_by(Team.score.desc()).all()
    return render_template('leaderboardstudent.html', teams=teams, user=session)

@app.route('/student/profile')
@login_required
def student_profile():
    db = get_db()
    user = db.query(User).filter(User.id == session.get('user_id')).first()
    return render_template('profilestudent.html', user=user)

@app.route('/student/team')
@login_required
def student_team():
    db = get_db()
    team = db.query(Team).first()
    return render_template('teamstudent.html', team=team, user=session)


def seed_db():
    db = SessionLocal()
    
    if db.query(Team).first() is None:
        teams = [
            Team(team_name="Code Warriors", score=120),
            Team(team_name="Byte Masters", score=110),
            Team(team_name="Logic Lords", score=90),
            Team(team_name="Cyber Knights", score=85),
            Team(team_name="Algo Rhythms", score=70),
            Team(team_name="Quantum Qubits", score=65)
        ]
        db.add_all(teams)
        db.commit()

    if db.query(User).first() is None:
        admin_user = User(fullname="Admin User", email="admin@admin.com", password="password", role="admin")
        student_user = User(fullname="Test Student", email="student@college.edu", password="password", role="student")
        cw = db.query(Team).filter_by(team_name="Code Warriors").first()
        ram_user = User(fullname="Ram", email="ram@college.edu", password="password", role="student", team_id=cw.id if cw else None)
        
        db.add(admin_user)
        db.add(student_user)
        db.add(ram_user)
        
        # Add members to teams
        team_members = {
            "Code Warriors": ["Alex", "Sarah", "David", "Elena"],
            "Byte Masters": ["Liam", "Noah", "Emma", "Maya"],
            "Logic Lords": ["James", "Oliver", "Sophia"],
            "Cyber Knights": ["Daniel", "Lucas", "Mia", "Zoe"],
            "Algo Rhythms": ["Ethan", "Mason", "Ava", "Isabella"],
            "Quantum Qubits": ["Benjamin", "Henry", "Chloe", "Evelyn"]
        }
        
        for team_name, members in team_members.items():
            team = db.query(Team).filter_by(team_name=team_name).first()
            if team:
                for member_name in members:
                    db.add(User(
                        fullname=member_name,
                        email=f"{member_name.lower()}@college.edu",
                        password="password",
                        role="student",
                        team_id=team.id
                    ))
        db.commit()
    
    if db.query(Question).first() is None:
        questions = [
            Question(question_text="What is a Turing Machine?", option_a="Model", option_b="Car", option_c="Bot", option_d="None", correct_option="A", type="MCQ", points=10),
            Question(question_text="What is a State Automaton?", option_a="Car", option_b="State Machine", option_c="None", option_d="Bot", correct_option="B", type="MCQ", points=15),
            Question(question_text="What is a Binary Search Tree?", option_a="Tree data structure", option_b="Graph", option_c="List", option_d="None", correct_option="A", type="Riddle", points=20),
            Question(question_text="What is a Linked List?", option_a="Array", option_b="Nodes", option_c="None", option_d="List", correct_option="B", type="Riddle", points=25),
            Question(question_text="What is Dynamic Programming?", option_a="Method", option_b="Code", option_c="None", option_d="Bot", correct_option="A", type="MCQ", points=10)
        ]
        db.add_all(questions)
        db.commit()
        
    if db.query(Submission).first() is None:
        t1 = db.query(Team).filter_by(team_name="Code Warriors").first()
        q1 = db.query(Question).first()
        if t1 and q1:
            db.add(Submission(team_id=t1.id, question_id=q1.id, submitted_option="A", is_correct=True))
            db.commit()
            
    db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    seed_db()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=4000)
