from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import jwt
import datetime
import os
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

app = Flask(__name__)
CORS(app)

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
DATABASE = "app.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)

    existing_user = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        ("admin",)
    ).fetchone()

    if existing_user is None:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", "password123")
        )

    existing_message = conn.execute("SELECT * FROM messages").fetchone()

    if existing_message is None:
        conn.execute(
            "INSERT INTO messages (content) VALUES (?)",
            ("I don't know what to put here. retrieved from database.",)
        )

    conn.commit()
    conn.close()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token is missing"}), 401

        try:
            token = auth_header.split(" ")[1]
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except Exception:
            return jsonify({"error": "Invalid or expired token"}), 401

        return f(*args, **kwargs)

    return decorated


@app.route("/")
def home():
    return jsonify({"message": "Backend is running"})


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    ).fetchone()
    conn.close()

    if user is None:
        return jsonify({"error": "Invalid username or password"}), 401

    token = jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({"token": token})


@app.route("/api/message", methods=["GET"])
@token_required
def get_message():
    conn = get_db_connection()
    messages = conn.execute("SELECT * FROM messages").fetchall()
    conn.close()

    message_list = [message["content"] for message in messages]

    return jsonify({
        "message": "Protected GET request successful",
        "data": message_list
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)