# GitHub Webhook Event Tracker

This project receives GitHub webhook events from a repository, stores only the required information in MongoDB, and displays recent repository activity in a simple UI that polls every 15 seconds.

The system tracks the following GitHub actions:
- Push
- Pull Request
- Merge (derived from Pull Request events)

---

## Architecture Overview

- **action-repo**
  - GitHub repository configured to emit webhook events
  - Sends Push and Pull Request events
  - Repository link:  
    https://github.com/Saumya1404/Action-repo

- **webhook-repo** (this repository)
  - Flask backend to receive webhooks
  - MongoDB to store normalized event data
  - Minimal frontend that polls the backend every 15 seconds

---

## Tech Stack

- Backend: Flask (Python)
- Database: MongoDB
- Frontend: HTML + JavaScript
- Webhooks: GitHub Webhooks
- Local tunneling: ngrok (for testing)

---

## MongoDB Schema

```json
{
  "request_id": "string",
  "author": "string",
  "action": "PUSH | PULL_REQUEST | MERGE",
  "from_branch": "string",
  "to_branch": "string",
  "timestamp": "UTC datetime string"
}
```

**Notes**
- `from_branch` is empty for PUSH events because GitHub does not provide a source branch.
- MERGE events are derived from pull request payloads where `merged == true`.

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone <webhook-repo-url>
cd webhook-repo
```

### 2. (Optional) Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:
```env
MONGO_URI=mongodb://localhost:27017
```

> MongoDB databases and collections are created automatically on first insert.

---

## Running the Application Locally

### 1. Start MongoDB
```bash
mongod
```

### 2. Start the Flask application
```bash
flask run --port 8000
```

### 3. Expose the application using ngrok
```bash
ngrok http 8000
```

Copy the generated HTTPS URL.

---

## GitHub Webhook Configuration (action-repo)

In the **action-repo**:

1. Go to `Settings → Webhooks → Add webhook`
2. Payload URL:
```
https://<ngrok-url>/webhook
```
3. Content type:
```
application/json
```
4. Events to enable:
   - Push
   - Pull requests

Save the webhook.

---

## Application Endpoints

### POST `/webhook`
Receives GitHub webhook events, normalizes the payload, and stores the data in MongoDB.

### GET `/events`
Returns all stored events sorted by timestamp (descending).

### GET `/`
Serves the web UI.

---

## UI Behavior

- The frontend polls `/events` every **15 seconds**
- Events are rendered in the following formats:

**Push**
```
{author} pushed to {to_branch} on {timestamp}
```

**Pull Request**
```
{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}
```

**Merge**
```
{author} merged branch {from_branch} to {to_branch} on {timestamp}
```

---

## Testing Flow

1. Make a commit → PUSH event
2. Open a pull request → PULL_REQUEST event
3. Merge the pull request → MERGE event
4. Verify MongoDB entries
5. Verify UI updates automatically every 15 seconds

---

## Notes

- Polling is intentionally used as per the problem requirements
- Only minimal required data is stored and rendered
- `.env` is excluded from version control

---

## Author

Built as part of a GitHub Webhook + MongoDB assessment task.
