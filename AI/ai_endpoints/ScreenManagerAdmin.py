import subprocess
import threading
import time
from flask import Flask, request, jsonify

class ScreenManager:
    def __init__(self):
        self.sessions = {}  # Store session details

    def session_exists(self, session_name):
        """Check if a session with the given name exists."""
        return session_name in self.sessions
		
    def create_session(self, session_name, script_path, port_number, timeout_seconds):
        """Create a new screen session running a Python script."""
        if session_name in self.sessions:
            return {"error": f"Session '{session_name}' already exists."}

        # Start the screen session
        subprocess.run([
            "screen", "-dmS", session_name, 
            "bash", "-c", f"python3 {script_path} {port_number}"
        ])

        # Start a thread to monitor session timeout
        session_thread = threading.Thread(
            target=self._monitor_session, 
            args=(session_name,),
            daemon=True
        )
        session_thread.start()

        # Store session details
        self.sessions[session_name] = {
            "script_path": script_path,
            "timeout_seconds": timeout_seconds,
            "start_time": time.time(),
            "thread": session_thread,
        }

        return {"status": "session_created", "session_name": session_name}

    def _monitor_session(self, session_name):
        """Monitor session timeout and terminate if time runs out."""
        while session_name in self.sessions:
            session_data = self.sessions.get(session_name)
            if not session_data:
                break

            elapsed_time = time.time() - session_data["start_time"]
            if elapsed_time >= session_data["timeout_seconds"]:
                self.destroy_session(session_name)
                break
            time.sleep(1)

    def destroy_session(self, session_name):
        """Terminate a screen session."""
        if session_name not in self.sessions:
            return {"error": f"Session '{session_name}' does not exist."}

        # Terminate the screen session
        subprocess.run(["screen", "-S", session_name, "-X", "quit"])

        # Remove from the session manager
        del self.sessions[session_name]

        return {"status": "session_destroyed", "session_name": session_name}

    def add_time_to_session(self, session_name, additional_seconds):
        """Increase the timeout for a session."""
        if session_name not in self.sessions:
            return {"error": f"Session '{session_name}' does not exist."}

        self.sessions[session_name]["timeout_seconds"] += additional_seconds
        return {
            "status": "timeout_extended",
            "session_name": session_name,
            "new_timeout_seconds": self.sessions[session_name]["timeout_seconds"],
        }

    def list_sessions(self):
        """List all active sessions."""
        return {
            session_name: {
                "script_path": details["script_path"],
                "timeout_seconds": details["timeout_seconds"],
                "elapsed_time": time.time() - details["start_time"],
            }
            for session_name, details in self.sessions.items()
        }


# Flask app to manage sessions
app = Flask(__name__)
screen_manager = ScreenManager()

@app.route("/session_exists/<session_name>", methods=["GET"])
def session_exists(session_name):
    """Endpoint to check if a session already exists."""
    exists = screen_manager.session_exists(session_name)
    return jsonify({"session_name": session_name, "exists": exists})
	
@app.route("/create_session", methods=["POST"])
def create_session():
    """Endpoint to create a new screen session."""
    data = request.json
    session_name = data.get("session_name")
    script_path = data.get("script_path")
    timeout_seconds = data.get("timeout_seconds", 60)
	port_number = data.get("port_number", -1)

    if not session_name or not script_path:
        return jsonify({"error": "Missing session_name or script_path"}), 400

    result = screen_manager.create_session(session_name, script_path, port_number, timeout_seconds)
    return jsonify(result)
	
@app.route("/add_time_session", methods=["POST"])
def add_time_session():
    """Endpoint to add time to an existing session."""
    data = request.json
    session_name = data.get("session_name")
    additional_seconds = data.get("additional_seconds")

    if not session_name or additional_seconds is None:
        return jsonify({"error": "Missing session_name or additional_seconds"}), 400

    if not isinstance(additional_seconds, (int, float)) or additional_seconds <= 0:
        return jsonify({"error": "additional_seconds must be a positive number"}), 400

    result = screen_manager.add_time_to_session(session_name, additional_seconds)
    return jsonify(result)	

@app.route("/destroy_session/<session_name>", methods=["DELETE"])
def destroy_session(session_name):
    """Endpoint to destroy a screen session."""
    result = screen_manager.destroy_session(session_name)
    return jsonify(result)

@app.route("/list_sessions", methods=["GET"])
def list_sessions():
    """Endpoint to list all active screen sessions."""
    result = screen_manager.list_sessions()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)