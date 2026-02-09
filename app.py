from datetime import datetime, timezone
import os
import sqlite3
from flask import Flask, jsonify, make_response, request, send_from_directory


app = Flask(__name__, static_folder=".", static_url_path="")
app.config.setdefault("DB_PATH", os.environ.get("BLOG_DB_PATH", "blog.db"))
app.config.setdefault("CORS_ORIGIN", os.environ.get("BLOG_CORS_ORIGIN", "*"))
ALLOWED_STATUSES = {"draft", "published"}


def get_db():
    conn = sqlite3.connect(app.config["DB_PATH"])
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            date TEXT,
            url TEXT,
            content TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def row_to_dict(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "category": row["category"],
        "date": row["date"],
        "url": row["url"],
        "content": row["content"],
        "status": row["status"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }

@app.before_request
def handle_options():
    if request.method == "OPTIONS" and request.path.startswith("/api/"):
        return make_response("", 204)


@app.after_request
def add_cors_headers(response):
    if request.path.startswith("/api/"):
        response.headers["Access-Control-Allow-Origin"] = app.config["CORS_ORIGIN"]
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/index.html")
def index_html():
    return send_from_directory(".", "index.html")


@app.route("/blog")
def blog():
    return send_from_directory(".", "blog.html")


@app.route("/blog.html")
def blog_html():
    return send_from_directory(".", "blog.html")


@app.route("/assets/<path:filename>")
def assets(filename):
    return send_from_directory("assets", filename)


@app.route("/api/posts", methods=["GET"])
def list_posts():
    status = request.args.get("status")
    category = request.args.get("category")
    conn = get_db()
    clauses = []
    params = []
    if status and status != "all":
        clauses.append("status = ?")
        params.append(status)
    if category and category != "all":
        clauses.append("category = ?")
        params.append(category)

    query = "SELECT * FROM posts"
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY id DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([row_to_dict(row) for row in rows])


@app.route("/api/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(row_to_dict(row))


@app.route("/api/posts", methods=["POST"])
def create_post():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400
    required = ["title", "category", "content", "status"]
    missing = [key for key in required if not data.get(key)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400
    if data.get("status") not in ALLOWED_STATUSES:
        return jsonify({"error": "Invalid status"}), 400

    now = (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )
    conn = get_db()
    cursor = conn.execute(
        """
        INSERT INTO posts (title, category, date, url, content, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["title"],
            data["category"],
            data.get("date"),
            data.get("url"),
            data["content"],
            data["status"],
            now,
            now,
        ),
    )
    conn.commit()
    post_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    return jsonify(row_to_dict(row)), 201


@app.route("/api/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400
    now = (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )

    conn = get_db()
    row = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Post not found"}), 404

    updated = {
        "title": data.get("title", row["title"]),
        "category": data.get("category", row["category"]),
        "date": data.get("date", row["date"]),
        "url": data.get("url", row["url"]),
        "content": data.get("content", row["content"]),
        "status": data.get("status", row["status"]),
    }
    if updated["status"] not in ALLOWED_STATUSES:
        conn.close()
        return jsonify({"error": "Invalid status"}), 400

    conn.execute(
        """
        UPDATE posts
        SET title = ?, category = ?, date = ?, url = ?, content = ?, status = ?, updated_at = ?
        WHERE id = ?
        """,
        (
            updated["title"],
            updated["category"],
            updated["date"],
            updated["url"],
            updated["content"],
            updated["status"],
            now,
            post_id,
        ),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    return jsonify(row_to_dict(row))


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Post not found"}), 404
    conn.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "deleted"})


init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
