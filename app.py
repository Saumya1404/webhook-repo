from flask import Flask,request, jsonify,render_template
from db import collection
from datetime import datetime

app = Flask(__name__)

@app.route('/webhook', methods=["POST"])
def webhook():
    event = request.headers.get('X-GitHub-Event')
    payload = request.get_json(silent=True)

    print("Event:", event)
    print("Payload received:", payload is not None)

    if payload is None:
        return jsonify({"error": "No JSON payload"}), 400

    try:
        if event == "push":
            handle_push(payload)
        elif event == "pull_request":
            handle_pull_request(payload)
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success"}), 200



@app.route('/events',methods = ["GET"])
def get_events():
    events= list(collection.find({},{"_id":0}).sort("timestamp",-1))
    return jsonify(events)


@app.route('/')
def home():
    return render_template("index.html")

def handle_push(payload):
    data = {
        "request_id": payload["head_commit"]["id"],
        "author": payload["head_commit"]["author"]["name"],
        "action": "PUSH",
        "from_branch":  "",
        "to_branch": payload["ref"].split("/")[-1],
        "timestamp": payload["head_commit"]["timestamp"]
    }
    collection.insert_one(data)

def handle_pull_request(payload):
    pr = payload["pull_request"]
    is_merged = pr.get("merged",False)

    data = {
        "request_id": str(pr["id"]),
        "author": pr["user"]["login"],
        "action": "MERGE" if is_merged else "PULL_REQUEST",
        "from_branch": pr["head"]["ref"],
        "to_branch": pr["base"]["ref"],
        "timestamp": pr["merged_at"] if is_merged else pr["created_at"]
        
    }
    collection.insert_one(data)
