from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)


from sklearn.neighbors import KNeighborsClassifier
import numpy as np

from flask_cors import CORS
CORS(app)

# Simple training dataset (demo data for ML model)
X = np.array([
    [20], [30], [40], [50], [60], [70], [80], [90]
])

y = [
    "Beginner", "Beginner", "Beginner",
    "Intermediate", "Intermediate",
    "Advanced", "Advanced", "Advanced"
]

model = KNeighborsClassifier(n_neighbors=3)
model.fit(X, y)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lms.db'
db = SQLAlchemy(app)

# ---------------- MODELS ----------------
class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(300))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    role = db.Column(db.String(20))

# ---------------- CREATE DB ----------------
with app.app_context():
    db.create_all()

    # Add sample data only if empty
    if Lesson.query.count() == 0:
        db.session.add(Lesson(title="Math Basics", content="Learn addition"))
        db.session.add(Lesson(title="AI Intro", content="Learn AI basics"))

    if User.query.count() == 0:
        db.session.add(User(username="student", password="1234", role="student"))
        db.session.add(User(username="teacher", password="admin", role="teacher"))

    db.session.commit()

# ---------------- LESSONS ----------------
@app.route("/lessons")
def lessons():
    lessons = Lesson.query.all()
    return jsonify([
        {"title": l.title, "content": l.content} for l in lessons
    ])

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(
        username=data.get("username"),
        password=data.get("password")
    ).first()

    if user:
        return jsonify({"role": user.role})

    return jsonify({"message": "Invalid credentials"}), 401

# ---------------- AI ----------------
@app.route("/ai-advanced", methods=["POST"])
def ai_advanced():
    data = request.json
    score = data.get("score")

    prediction = model.predict([[score]])[0]

    # map prediction to lesson
    if prediction == "Beginner":
        lesson = "Basic Mathematics"
    elif prediction == "Intermediate":
        lesson = "Introduction to AI"
    else:
        lesson = "Machine Learning Basics"

    return jsonify({
        "score": score,
        "predicted_level": prediction,
        "recommended_lesson": lesson
    })

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(port=5001, debug=True)


@app.route("/add-lesson", methods=["POST"])
def add_lesson():
    data = request.json

    new_lesson = Lesson(
        title=data.get("title"),
        content=data.get("content")
    )

    db.session.add(new_lesson)
    db.session.commit()

    return jsonify({"message": "Lesson added successfully"})

from app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)