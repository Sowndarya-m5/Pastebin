
from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta, timezone
import uuid
import os

from db import get_db_connection
from config import TEST_MODE

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


def current_time():
    if TEST_MODE and request.headers.get("x-test-now-ms"):
        ms = int(request.headers.get("x-test-now-ms"))
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
    return datetime.now(timezone.utc)


@app.route("/api/healthz")
def healthz():
    return jsonify({"ok": True}), 200


@app.route("/api/pastes", methods=["POST"])
def create_paste():
    data = request.get_json()
    if not data or not data.get("content"):
        return jsonify({"error": "content required"}), 400

    paste_id = uuid.uuid4().hex[:8]
    created_at = current_time()

    ttl = data.get("ttl_seconds")
    max_views = data.get("max_views")
    expires_at = created_at + timedelta(seconds=ttl) if ttl else None

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO pastes (id, content, created_at, expires_at, max_views, views_used)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (paste_id, data["content"], created_at, expires_at, max_views, 0))
    conn.commit()
    conn.close()

    return jsonify({
        "id": paste_id,
        "url": f"{request.host_url}p/{paste_id}"
    }), 201


def get_paste(paste_id, count=True):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pastes WHERE id=%s", (paste_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return None

    # Convert tuple to dictionary manually
    paste = {
        "id": row[0],
        "content": row[1],
        "created_at": row[2],
        "expires_at": row[3],
        "max_views": row[4],
        "views_used": row[5]
    }

    now = current_time()
    if paste["expires_at"] and now > paste["expires_at"]:
        conn.close()
        return None

    if paste["max_views"] is not None and paste["views_used"] >= paste["max_views"]:
        conn.close()
        return None

    if count:
        cur.execute("UPDATE pastes SET views_used=views_used+1 WHERE id=%s", (paste_id,))
        conn.commit()

    conn.close()
    return paste


@app.route("/api/pastes/<pid>")
def paste_api(pid):
    paste = get_paste(pid)
    if not paste:
        return jsonify({"error": "not found"}), 404

    remaining = None
    if paste["max_views"] is not None:
        remaining = paste["max_views"] - paste["views_used"] - 1

    return jsonify({
        "content": paste["content"],
        "remaining_views": remaining,
        "expires_at": paste["expires_at"].isoformat() if paste["expires_at"] else None
    })


@app.route("/p/<pid>")
def paste_page(pid):
    paste = get_paste(pid)
    if not paste:
        return render_template("404.html"), 404
    return render_template("paste.html", content=paste["content"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


