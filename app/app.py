from flask import Flask, jsonify
import time

app = Flask(__name__)

REQUEST_COUNT = {"value": 0}


@app.route("/")
def home():
    REQUEST_COUNT["value"] += 1
    return jsonify(message="Hello from the DevOps Pipeline Demo App!", status="running")


@app.route("/health")
def health():
    # Used by Jenkins/K8s/monitoring to verify the app is alive
    return jsonify(status="healthy", timestamp=time.time()), 200


@app.route("/metrics-count")
def metrics_count():
    # Simple custom metric endpoint (Prometheus will scrape /metrics via
    # prometheus_flask_exporter in a full setup — this is a lightweight demo)
    return jsonify(requests_served=REQUEST_COUNT["value"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
