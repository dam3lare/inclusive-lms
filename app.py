from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)

app = Flask(__name__)
CORS(app)

# SECRET KEY (IMPORTANT)
app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)

# -------------------------
# FAKE USERS DB
# -------------------------
users = [
    {"email": "admin@gmail.com", "password": "1234"}
]

# -------------------------
# LOGIN (RETURNS TOKEN)
# -------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    for user in users:
        if user["email"] == email and user["password"] == password:
            token = create_access_token(identity=email)
            return jsonify({
                "status": "success",
                "token": token,
                "user": email
            })

    return jsonify({
        "status": "fail",
        "message": "Invalid credentials"
    }), 401


# -------------------------
# PROTECTED LESSONS
# -------------------------
@app.route("/lessons", methods=["GET"])
@jwt_required()
def lessons():
    return jsonify([
        {"title": "Math Basics", "content": "Learn addition"},
        {"title": "AI Intro", "content": "Learn AI basics"}
    ])


# -------------------------
# PROTECTED AI
# -------------------------
@app.route("/ai-advanced", methods=["POST"])
@jwt_required()
def ai():
    data = request.json
    score = data.get("score", 50)

    if score < 50:
        level = "Beginner"
    elif score < 75:
        level = "Intermediate"
    else:
        level = "Advanced"

    return jsonify({
        "predicted_level": level,
        "recommended_lesson": "Personalized learning path"
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)