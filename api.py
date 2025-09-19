from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

# Percorso PGDATA del monitor/keeper
PGDATA = "/var/lib/postgresql/pgaf"  # cambia in base al tuo setup

def run_pg_autoctl(cmd):
    try:
        full_cmd = ["pg_autoctl", cmd, "--pgdata", PGDATA]
        result = subprocess.run(full_cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Errore: {e.stderr}"

@app.route("/monitor")
def monitor():
    settings_output = run_pg_autoctl("show settings")
    state_output = run_pg_autoctl("show state")
    
    # restituisci entrambi in un JSON testuale
    return jsonify({
        "settings": settings_output,
        "state": state_output
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6001)
