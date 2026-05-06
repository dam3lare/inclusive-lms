from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# -----------------------------
# USERS DATABASE
# -----------------------------
users = [
    {"email": "admin@gmail.com", "password": "1234"}
]

# -----------------------------
# LOGIN ROUTE (CLEAN + WORKING)
# -----------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)

    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    print("LOGIN ATTEMPT:", email, password)

    for user in users:
        if user["email"] == email and user["password"] == password:
            return jsonify({
                "status": "success",
                "user": email
            })

    return jsonify({
        "status": "fail",
        "message": "Invalid credentials"
    }), 401


# -----------------------------
# LESSONS API
# -----------------------------
@app.route("/lessons", methods=["GET"])
def lessons():
    return jsonify([
        {"title": "Math Basics", "content": "Learn addition"},
        {"title": "AI Intro", "content": "Learn AI basics"}
    ])


# -----------------------------
# AI ROUTE
# -----------------------------
@app.route("/ai-advanced", methods=["POST"])
def ai_advanced():
    data = request.json
    score = data.get("score", 50)

    if score < 50:
        level = "Beginner"
        lesson = "Introduction to Basics"
    elif score < 75:
        level = "Intermediate"
        lesson = "Practice Exercises"
    else:
        level = "Advanced"
        lesson = "Real-world Projects"

    return jsonify({
        "predicted_level": level,
        "recommended_lesson": lesson
    })


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5001)