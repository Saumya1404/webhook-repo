# GitHub Webhook Event Tracker

This project receives GitHub webhook events from a repository, stores only the required information in MongoDB, and displays recent repository activity in a simple UI that polls every 15 seconds.

The system tracks the following GitHub actions:
- Push
- Pull Request
- Merge (derived from Pull Request events)

---

## Architecture Overview

- **action-repo**
  - GitHub repository that emits webhook events
  - Configured to send Push and Pull Request events
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

Each event is stored in the following format:

```json
{
  "request_id": "string",
  "author": "string",
  "action": "PUSH | PULL_REQUEST | MERGE",
  "from_branch": "string",
  "to_branch": "string",
  "timestamp": "UTC datetime string"
}
