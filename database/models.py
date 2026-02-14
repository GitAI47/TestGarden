 #from extensions import db
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# definiering gebruier om in te loggen

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    role = db.Column(db.String(20), nullable=False, default="student")

    progress = db.relationship("Progress", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# definiering user id (om de gebruikers rollen in te kunnen opslaan)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=True)
    completed = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# definiering Testcases in database

from datetime import datetime

class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String(50), unique=True, nullable=False)   # bv TC-001
    title = db.Column(db.String(200), nullable=False)
    module = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)

    tags = db.Column(db.String(250), nullable=True)  # simpel: "smoke,auth"
    priority = db.Column(db.String(20), nullable=True)  # low/med/high

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    steps = db.relationship("TestStep", backref="test_case", cascade="all, delete-orphan", lazy=True)
    preconditions = db.relationship("Precondition", backref="test_case", cascade="all, delete-orphan", lazy=True)

# definiering stap in testcase

class TestStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_case_id = db.Column(db.Integer, db.ForeignKey("test_case.id"), nullable=False)

    step_no = db.Column(db.Integer, nullable=False)
    action = db.Column(db.Text, nullable=False)
    expected = db.Column(db.Text, nullable=True)

# definiering precondities nodig voor testcases in database

class Precondition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_case_id = db.Column(db.Integer, db.ForeignKey("test_case.id"), nullable=False)

    text = db.Column(db.Text, nullable=False)


# invoering velden voor het uitvoeren van de Testrun omgeving

class TestRun(db.Model):
    __tablename__ = "test_run"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime, nullable=True)

    results = db.relationship("TestResult", backref="run", cascade="all, delete-orphan")


class TestResult(db.Model):
    __tablename__ = "test_result"

    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.Integer, db.ForeignKey("test_run.id"), nullable=False)
    test_case_id = db.Column(db.Integer, db.ForeignKey("test_case.id"), nullable=False)

    status = db.Column(db.String(20))   # pass / fail / note / skip
    comment = db.Column(db.Text)
    
    step_results = db.relationship("StepResult", backref="result", cascade="all, delete-orphan", lazy=True)


class StepResult(db.Model):
    __tablename__ = "step_result"

    id = db.Column(db.Integer, primary_key=True)

    result_id = db.Column(db.Integer, db.ForeignKey("test_result.id"), nullable=False)

    # Snapshot velden (zodat oude runs kloppen als scripts later wijzigen)
    step_no = db.Column(db.Integer, nullable=False)
    action_text = db.Column(db.Text, nullable=False)
    expected_text = db.Column(db.Text, nullable=True)

    status = db.Column(db.String(20), nullable=False)  # pass / fail / note / skip
    comment = db.Column(db.Text, nullable=True)
