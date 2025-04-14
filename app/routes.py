from flask import Blueprint, render_template, request, jsonify
from .models import Log
from . import db
from datetime import datetime
import html
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import os

# ✅ Use non-GUI backend for Matplotlib
matplotlib.use('Agg')

routes = Blueprint("routes", __name__)

GRAPH_FILE = "app/static/graph.png"

# ✅ Threat Classification Function
def classify_threat(message):
    threats = {
        "DDoS": ["traffic spike", "flood attack", "botnet"],
        "SQL Injection": ["sql", "database error", "malicious query"],
        "Brute Force": ["multiple failed logins", "password attack"],
        "XSS": ["script", "malicious code"],
        "Malware": ["virus detected", "trojan", "ransomware"]
    }
    for threat_type, keywords in threats.items():
        if any(keyword in message.lower() for keyword in keywords):
            return threat_type
    return "Unknown"

# ✅ Severity Classification
def get_severity(status, threat_type):
    if status == "Anomaly":
        if threat_type in ["DDoS", "Malware"]:
            return "High"
        elif threat_type in ["SQL Injection", "Brute Force"]:
            return "Medium"
        else:
            return "Low"
    return "Low"

# ✅ Generate Graph
def generate_graph(logs):
    if not logs:
        plt.figure(figsize=(10, 5))
        plt.title("Log Data Trend", fontsize=16)
        plt.xlabel("Timestamp", fontsize=12)
        plt.ylabel("Value", fontsize=12)
        plt.text(0.5, 0.5, "No logs available", fontsize=12, ha="center", va="center", transform=plt.gca().transAxes)
        plt.tight_layout()
        plt.savefig(GRAPH_FILE)
        plt.close()
        return

    logs.sort(key=lambda x: datetime.strptime(x.timestamp, "%Y-%m-%d %H:%M:%S"))
    timestamps = [datetime.strptime(log.timestamp, "%Y-%m-%d %H:%M:%S") for log in logs]
    values = [log.value for log in logs]

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, values, marker="o", label="Log Values", color="blue")
    plt.title("Log Data Trend", fontsize=16)
    plt.xlabel("Timestamp", fontsize=12)
    plt.ylabel("Value", fontsize=12)
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(DateFormatter("%Y-%m-%d %H:%M"))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(GRAPH_FILE)
    plt.close()

@routes.route("/")
def home():
    logs = Log.query.order_by(Log.timestamp.desc()).limit(10).all()
    generate_graph(logs)
    return render_template("dashboard.html", logs=logs)

@routes.route("/add_log", methods=["POST"])
def add_log():
    data = request.json
    logs = Log.query.all()
    values = [log.value for log in logs]

    if values:
        model = IsolationForest(contamination=0.1, random_state=42)
        model.fit(np.array(values).reshape(-1, 1))
        prediction = model.predict([[data["value"]]])
    else:
        prediction = [1]

    status = "Anomaly" if prediction[0] == -1 else "Normal"
    threat_type = classify_threat(data["message"])
    severity = get_severity(status, threat_type)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_log = Log(
        timestamp=timestamp,
        message=html.escape(data["message"]),
        value=data["value"],
        status=status,
        severity=severity
    )

    db.session.add(new_log)
    db.session.commit()
    generate_graph(Log.query.all())

    return jsonify({
        "message": "Log added",
        "status": status,
        "threat_type": threat_type,
        "severity": severity
    })

@routes.route("/remove_log/<int:log_id>", methods=["DELETE"])
def remove_log(log_id):
    log = Log.query.get(log_id)
    if log:
        db.session.delete(log)
        db.session.commit()
        generate_graph(Log.query.all())
        return jsonify({"message": f"Log {log_id} removed"})
    return jsonify({"error": "Log not found"}), 404

@routes.route("/logs", methods=["GET"])
def get_logs():
    logs = Log.query.all()
    return jsonify([{
        "id": log.id,
        "timestamp": log.timestamp,
        "message": log.message,
        "value": log.value,
        "status": log.status,
        "severity": getattr(log, "severity", "N/A")
    } for log in logs])

@routes.route("/search", methods=["GET"])
def search_logs():
    query = request.args.get("query", "").lower()
    logs = Log.query.filter(Log.message.ilike(f"%{query}%")).all()

    return jsonify([{
        "id": log.id,
        "timestamp": log.timestamp,
        "message": log.message,
        "value": log.value,
        "status": log.status,
        "severity": getattr(log, "severity", "N/A")
    } for log in logs])