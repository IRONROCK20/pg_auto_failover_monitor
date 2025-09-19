from flask import Flask, jsonify
import subprocess
app = Flask(__name__)
PGDATA = "/var/lib/postgresql/pgaf"

def run_pg_autoctl(cmd_list):
    try:
        result = subprocess.run(cmd_list, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Errore: {e.stderr}"

@app.route("/monitor")
def monitor():
    settings_output = run_pg_autoctl(["pg_autoctl", "show", "settings"])
    state_output = run_pg_autoctl(["pg_autoctl", "show", "state"])
    return jsonify({
        "settings": settings_output,
        "state": state_output
    })

@app.route("/maintenance/on")
def maintenance_on():
    output = run_pg_autoctl(["pg_autoctl", "enable", "maintenance", "--allow-failover"])
    return jsonify({
        "action": "maintenance on",
        "result": output
    })

@app.route("/maintenance/off")
def maintenance_off():
    output = run_pg_autoctl(["pg_autoctl", "disable", "maintenance"])
    return jsonify({
        "action": "maintenance off",
        "result": output
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6001)
