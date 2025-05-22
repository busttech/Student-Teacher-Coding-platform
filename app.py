from flask import Flask, render_template, request, jsonify, redirect, session, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
import pandas as pd
import subprocess
import sys
import os
import tempfile
import random

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CA_CERT_PATH = os.path.join(BASE_DIR, 'certs/isrgrootx1.pem')
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mysql+pymysql://3QkyK3w5GoLuPjo.root:r8jhtPzQbNRtJaSF@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/tes12?ssl_ca={CA_CERT_PATH}'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USERNAME'] = 'tarun1940v@gmail.com'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

db = SQLAlchemy(app)
app.secret_key = os.urandom(24)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    function_name = db.Column(db.String(100), nullable=False)
    parameters = db.Column(db.String(16), nullable=False)
    test_cases = db.relationship('TestCase', backref='question', lazy=True)

class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_data = db.Column(db.Text, nullable=False)
    expected_output = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_code = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    result = db.Column(db.String(16), nullable=False)
    email= db.Column(db.String(100), nullable=False)
    name= db.Column(db.String(100), nullable=False)
    branch= db.Column(db.String(100), nullable=False)

class SubmissionAll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_code = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    result = db.Column(db.String(16), nullable=False)
    email= db.Column(db.String(100), nullable=False)
    name= db.Column(db.String(100), nullable=False)
    branch= db.Column(db.String(100), nullable=False)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=False)
    activation_code = db.Column(db.String(6), nullable=True)
mail = Mail(app)
@app.route("/")
def home():
    return render_template('index.html')

@app.route('/logint', methods=['GET', 'POST'])
def logint():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'room330' and password == '329330':
            session['logged_in_teacher'] = True
            return redirect(url_for('teacher'))
        else:
            return render_template('logint.html', error="Invalid credentials, please try again.")
    return render_template('logint.html')

@app.route('/teacher', methods=['GET', 'POST'])
def teacher():
    if 'logged_in_teacher' not in session:
        return redirect(url_for('logint'))
    if request.method == 'POST':
        data = request.json
        question = Question(
            title=data['title'],
            description=data['description'],
            parameters = data['parameters'],
            function_name=data['function_name']
        )
        db.session.add(question)
        db.session.commit()
        for case in data['test_cases']:
            test_case = TestCase(
                input_data=case['input'],
                expected_output=case['output'],
                question_id=question.id
            )
            db.session.add(test_case)
        db.session.commit()
        return jsonify({'message': 'Question added successfully!'}), 201
    return render_template('teacher.html')
@app.route('/loginsi')
def loginsi():
    return render_template('loginsi.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        branch = request.form['branch']
        password =request.form['password']
        
        # Check if the email already exists in the database
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            if existing_user.is_active:
                flash('Email is already registered. Please log in or use a different email.', 'danger')
                return redirect(url_for('signup'))
            else:
                db.session.delete(existing_user)
                db.session.commit()

        
        # Generate activation code
        activation_code = str(random.randint(100000, 999999))
        
        # Store the new user in the database
        new_user = User(email=email, name=name, branch=branch, activation_code=activation_code,password=password)
        db.session.add(new_user)
        db.session.commit()
        session['a'] = email
        
        msg = Message('Activation Code', sender='nonreplaygmail.com', recipients=[email])
        msg.body = f'Hello {name},\n\nYour activation code is: {activation_code}\n\nThank you!'
        mail.send(msg)
        
        flash('Activation code sent to your email. Please activate your account.', 'info')
        return redirect(url_for('activate', email=email))
    return render_template('signup.html')


@app.route('/activate', methods=['GET', 'POST'])
def activate():
    email = session.get('a')
    if request.method == 'POST':
        email = session.get('a')
        code = request.form['code']
        user = User.query.filter_by(email=email).first()
        if user and user.activation_code == code:
            user.is_active = True
            db.session.commit()
            print("User  activated successfully.")
            return redirect(url_for('login'))
        else:
            flash('Invalid activation code. Please try again.', 'danger')
    return render_template('activate.html', email=email)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        print(user)
        if(user == None):
            return redirect(url_for("signup"))
        if user and user.is_active and user.password==password:
            session['email'] = email
            flash('Login successful!', 'success')
            session["login_completed_student"] = True
            return redirect(url_for('student'))
        else:
            return render_template('login.html', error="Invalid credentials, please try again.")
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop("login_completed_student", None)
    session.pop('email', None)
    flash('Logged out successfully!', 'info')
    return redirect(url_for('loginsi'))
@app.route('/student')
def student():
    if 'login_completed_student' not in session:
        return redirect(url_for('loginsi'))
    questions = Question.query.all()
    return render_template('student.html', questions=questions)
@app.route('/Allquestions')
def showallquestions():
    questions = Question.query.all()
    return render_template('Allquestions.html', questions=questions)

@app.route('/editor/<int:question_id>')
def editor(question_id):
    if 'login_completed_student' not in session:
        return redirect(url_for('loginsi'))
    question = Question.query.get_or_404(question_id)
    return render_template('editor.html', question=question)
@app.route('/editor')
def practiceditor():
    question = {
        "title": "Practice question",
        "description": "You can write code in code editor and then ",
        "function_name": "function",
        "parameters":"a"
    }
    return render_template('editor.html',question=question)
@app.route('/run_code', methods=['POST'])
def run_code():
    code = request.json.get('code')
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.py')
    temp_file.write(code.encode())
    temp_file.close()
    try:
        result = subprocess.run([sys.executable, temp_file.name], capture_output=True, text=True)
        os.remove(temp_file.name)
        output = result.stdout if result.returncode == 0 else result.stderr
        return jsonify({'output': output, 'status': 'success'})
    except Exception as e:
        return jsonify({'output': str(e), 'status': 'error'})

@app.route('/submit_code/<int:question_id>', methods=['POST'])
def submit_code(question_id):
    code = request.json.get('code')
    question = Question.query.get_or_404(question_id)
    test_cases = TestCase.query.filter_by(question_id=question.id).all()
    results = []
    all_passed = True
    for case in test_cases:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.py')
        temp_file.write(code.encode())
        temp_file.close()
        input_data = case.input_data
        try:
            with open(temp_file.name, 'a') as f:
                f.write(f'\nprint({question.function_name}({input_data}))')
            result = subprocess.run([sys.executable, temp_file.name], capture_output=True, text=True)
            output = result.stdout.strip()
            passed = output == case.expected_output
            if not passed:
                all_passed = False
            results.append({
                'input': input_data, 
                'expected': case.expected_output, 
                'output': output, 
                'passed': passed
            })
            os.remove(temp_file.name)
        except Exception as e:
            results.append({'error': str(e)})
    if all_passed:
        n = User.query.filter_by(email = session.get("email")).first()
        submission = Submission(student_code=code, question_id=question_id, email= session.get("email"),name= n.name ,branch = n.branch,result="Passed")
        db.session.add(submission)
        db.session.commit()
    elif not all_passed :
        n = User.query.filter_by(email = session.get("email")).first()
        submissiondsd = SubmissionAll(student_code=code, question_id=question_id, email= session.get("email"), name= n.name ,branch = n.branch,result="Failed")
        db.session.add(submissiondsd)
        db.session.commit()
    return jsonify({'results': results, 'status': 'success' if all_passed else 'failure'})

@app.route('/passedsub/<int:question_id>')
def view_submissions(question_id):
    if 'logged_in_teacher' not in session:
        return redirect(url_for('logint'))
    question = Question.query.get_or_404(question_id)
    submissions = Submission.query.filter_by(question_id=question_id).all()
    has_passed_submission = any(submission.result == 'Passed' for submission in submissions)
    return render_template('submission.html', question=question, submissions=submissions, has_passed_submission=has_passed_submission)
@app.route('/failedsub/<int:question_id>')
def view_failed_submissions(question_id):
    if 'logged_in_teacher' not in session:
        return redirect(url_for('logint'))
    question = Question.query.get_or_404(question_id)
    submissions = SubmissionAll.query.filter_by(question_id=question_id).all()
    return render_template('submission.html', question=question, submissions=submissions)
@app.route('/logoutt')
def logoutt():
    session.pop("logged_in_teacher", None)
    return redirect(url_for("logint"))
@app.route('/profile')
def profile():
    if 'login_completed_student' not in session:
        return redirect(url_for('loginsi'))
    
    email = session.get('email')
    user = User.query.filter_by(email=email).first()
    
    # Get all submissions for this user
    submissionsp = Submission.query.filter_by(email=email).all()
    submissionsf = SubmissionAll.query.filter_by(email=email).all()
    total_submissions = len(submissionsp+submissionsf)
    sp= len(submissionsp)
    solved_questions = (
        db.session.query(Submission.question_id)
        .filter_by(email=email, result='Passed')
        .distinct()
        .all()
    )
    so = len(solved_questions)
    
    # Calculate accuracy as percentage
    accuracy = (sp / total_submissions * 100) if total_submissions > 0 else 0
    
    return render_template('profile.html', user=user, accuracy=accuracy,so=so)
@app.route('/class_report')
def class_report():
    # Fetch data from the database
    students = User.query.filter_by(is_active=True)
    submissions = Submission.query.all()
    failed_submissions = SubmissionAll.query.all()

    # Process data into a DataFrame
    student_data = []
    for student in students:
        total_submissions = len(
            [sub for sub in submissions + failed_submissions if sub.email == student.email]
        )
        passed_questions = len(
            {sub.question_id for sub in submissions if sub.email == student.email and sub.result == "Passed"}
        )
        submissionsp = Submission.query.filter_by(email=student.email).all()

        accuracy = (len(submissionsp) / total_submissions * 100) if total_submissions > 0 else 0

        student_data.append({
            "Name": student.name,
            "Email": student.email,
            "Branch": student.branch,
            "Solved Questions": passed_questions,
            "Total Submissions": total_submissions,
            "Accuracy (%)": round(accuracy, 2)
        })

    # Create a DataFrame
    df = pd.DataFrame(student_data)

    # Render the report as an HTML table
    return render_template('class_report.html', table=df.to_html(classes='table table-striped', index=False))

@app.route("/dropalllll12121212fdfjdf")
def dropalll():
    with app.app_context():
        db.drop_all()
        db.session.commit()
        print("All tables dropped!")
    return render_template("index.html")
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
