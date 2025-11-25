from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Global storage
sessions = []
next_session_id = 1


# Helper: find session by ID
def find_session(sid):
    return next((s for s in sessions if s["session_id"] == sid), None)


# -------------------------------
# 1. Start a session
# -------------------------------
@app.post("/sessions/start")
def start_session():
    global next_session_id

    data = request.get_json() or {}
    task_name = data.get("task_name")

    # Validation
    if not task_name or not (3 <= len(task_name) <= 20):
        return jsonify({
            "error": "Invalid task name",
            "message": "Task name must be between 3 and 20 characters"
        }), 400

    session = {
        "session_id": next_session_id,
        "task_name": task_name,
        "started_at": datetime.now(),
        "stopped_at": None,
        "duration_seconds": None,
        "status": "running"
    }

    sessions.append(session)
    next_session_id += 1

    return jsonify({
        "session_id": session["session_id"],
        "task_name": session["task_name"],
        "started_at": session["started_at"].isoformat(),
        "status": "running"
    }), 201


# -------------------------------
# 2. Stop a session
# -------------------------------
@app.post("/sessions/<int:sid>/stop")
def stop_session(sid):
    session = find_session(sid)
    if not session:
        return jsonify({
            "error": "Session not found",
            "message": f"No session with ID {sid}"
        }), 404

    if session["status"] == "completed":
        return jsonify({
            "error": "Session already stopped",
            "message": f"Session {sid} was already stopped"
        }), 400

    session["stopped_at"] = datetime.now()
    duration = (session["stopped_at"] - session["started_at"]).total_seconds()
    session["duration_seconds"] = int(duration)
    session["status"] = "completed"

    return jsonify({
        "session_id": session["session_id"],
        "task_name": session["task_name"],
        "started_at": session["started_at"].isoformat(),
        "stopped_at": session["stopped_at"].isoformat(),
        "duration_seconds": session["duration_seconds"],
        "status": "completed"
    }), 200


# -------------------------------
# 3. List sessions (with filter)
# -------------------------------
@app.get("/sessions")
def list_sessions():
    status_filter = request.args.get("status")

    result = []
    for s in sessions:
        duration = s["duration_seconds"]

        # If running, calculate live duration
        if s["status"] == "running":
            duration = int((datetime.now() - s["started_at"]).total_seconds())

        if status_filter and s["status"] != status_filter:
            continue

        result.append({
            "session_id": s["session_id"],
            "task_name": s["task_name"],
            "started_at": s["started_at"].isoformat(),
            "stopped_at": s["stopped_at"].isoformat() if s["stopped_at"] else None,
            "duration_seconds": duration,
            "status": s["status"]
        })

    return jsonify({"sessions": result, "total": len(result)}), 200


# -------------------------------
# 4. Get a single session
# -------------------------------
@app.get("/sessions/<int:sid>")
def get_session(sid):
    s = find_session(sid)
    if not s:
        return jsonify({
            "error": "Session not found",
            "message": f"No session with ID {sid}"
        }), 404

    duration = s["duration_seconds"]
    if s["status"] == "running":
        duration = int((datetime.now() - s["started_at"]).total_seconds())

    return jsonify({
        "session_id": s["session_id"],
        "task_name": s["task_name"],
        "started_at": s["started_at"].isoformat(),
        "stopped_at": s["stopped_at"].isoformat() if s["stopped_at"] else None,
        "duration_seconds": duration,
        "status": s["status"]
    }), 200


# -------------------------------
# 5. Delete a session
# -------------------------------
@app.delete("/sessions/<int:sid>")
def delete_session(sid):
    s = find_session(sid)
    if not s:
        return jsonify({
            "error": "Session not found",
            "message": f"No session with ID {sid}"
        }), 404

    sessions.remove(s)
    return jsonify({
        "message": "Session deleted successfully",
        "session_id": sid,
        "task_name": s["task_name"]
    }), 200


# Run
if __name__ == "__main__":
    app.run(debug=True)
