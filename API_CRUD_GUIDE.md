# CRUD API Guide

Complete guide for managing monitors and incidents using REST API endpoints.

## 📍 Base URL

```
http://localhost:8000
```

## 🔧 Interactive API Documentation

Open in your browser for interactive testing:
```
http://localhost:8000/docs
```

This provides a Swagger UI where you can test all endpoints interactively.

---

## 🎯 Monitors CRUD API

### List All Monitors

**GET** `/api/monitors/list`

```bash
curl http://localhost:8000/api/monitors/list
```

**Response:**
```json
[
  {
    "url_monitor": "12345",
    "nome_monitor": "Authentication Service",
    "descricao_monitor": "Handles user authentication"
  }
]
```

---

### Get Single Monitor

**GET** `/api/monitors/{monitor_id}`

```bash
curl http://localhost:8000/api/monitors/12345
```

**Response:**
```json
{
  "url_monitor": "12345",
  "nome_monitor": "Authentication Service",
  "descricao_monitor": "Handles user authentication"
}
```

---

### Create New Monitor

**POST** `/api/monitors`

```bash
curl -X POST http://localhost:8000/api/monitors \
  -H "Content-Type: application/json" \
  -d '{
    "url_monitor": "123456789",
    "nome_monitor": "Production API",
    "descricao_monitor": "Main API endpoint health check"
  }'
```

**Request Body:**
```json
{
  "url_monitor": "string (required)",
  "nome_monitor": "string (required)",
  "descricao_monitor": "string (required)"
}
```

**Response (201 Created):**
```json
{
  "url_monitor": "123456789",
  "nome_monitor": "Production API",
  "descricao_monitor": "Main API endpoint health check"
}
```

**Errors:**
- `409 Conflict` - Monitor with that ID already exists
- `422 Unprocessable Entity` - Invalid request body

---

### Update Monitor

**PUT** `/api/monitors/{monitor_id}`

```bash
curl -X PUT http://localhost:8000/api/monitors/12345 \
  -H "Content-Type: application/json" \
  -d '{
    "nome_monitor": "Updated Name",
    "descricao_monitor": "Updated description"
  }'
```

**Request Body (all fields optional):**
```json
{
  "url_monitor": "string",
  "nome_monitor": "string",
  "descricao_monitor": "string"
}
```

**Response:**
```json
{
  "url_monitor": "12345",
  "nome_monitor": "Updated Name",
  "descricao_monitor": "Updated description"
}
```

**Errors:**
- `404 Not Found` - Monitor doesn't exist

---

### Delete Monitor

**DELETE** `/api/monitors/{monitor_id}`

```bash
curl -X DELETE http://localhost:8000/api/monitors/12345
```

**Response:** `204 No Content`

**Errors:**
- `404 Not Found` - Monitor doesn't exist

---

## 📢 Incidents CRUD API

### List All Incidents

**GET** `/api/incidents/list`

Returns ALL incidents (including those older than 30 days).

```bash
curl http://localhost:8000/api/incidents/list
```

**Response:**
```json
[
  {
    "id": "INC-2025-001",
    "title": "Database Issue",
    "status": "resolved",
    "severity": "major",
    "created_at": "2025-11-28T10:00:00",
    "resolved_at": "2025-11-28T12:00:00",
    "affected_services": ["Database"],
    "updates": [...]
  }
]
```

---

### Get Single Incident

**GET** `/api/incidents/{incident_id}`

```bash
curl http://localhost:8000/api/incidents/INC-2025-001
```

**Response:**
```json
{
  "id": "INC-2025-001",
  "title": "Database Issue",
  "status": "resolved",
  "severity": "major",
  "created_at": "2025-11-28T10:00:00",
  "resolved_at": "2025-11-28T12:00:00",
  "affected_services": ["Database"],
  "updates": [
    {
      "timestamp": "2025-11-28T10:00:00",
      "status": "investigating",
      "message": "We are investigating..."
    }
  ]
}
```

---

### Create New Incident

**POST** `/api/incidents`

```bash
curl -X POST http://localhost:8000/api/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "id": "INC-2025-003",
    "title": "API Slowdown",
    "status": "investigating",
    "severity": "major",
    "created_at": "2025-11-28T14:00:00",
    "resolved_at": null,
    "affected_services": ["API"],
    "updates": [
      {
        "timestamp": "2025-11-28T14:00:00",
        "status": "investigating",
        "message": "We are investigating reports of slow API responses."
      }
    ]
  }'
```

**Request Body:**
```json
{
  "id": "string (required, unique)",
  "title": "string (required)",
  "status": "investigating|identified|monitoring|resolved (required)",
  "severity": "minor|major|critical (required)",
  "created_at": "ISO 8601 timestamp (required)",
  "resolved_at": "ISO 8601 timestamp or null",
  "affected_services": ["array of strings (required)"],
  "updates": [
    {
      "timestamp": "ISO 8601 timestamp",
      "status": "investigating|identified|monitoring|resolved",
      "message": "string"
    }
  ]
}
```

**Response (201 Created):**
```json
{
  "id": "INC-2025-003",
  "title": "API Slowdown",
  ...
}
```

**Errors:**
- `409 Conflict` - Incident with that ID already exists
- `422 Unprocessable Entity` - Invalid request body

---

### Update Incident

**PUT** `/api/incidents/{incident_id}`

```bash
curl -X PUT http://localhost:8000/api/incidents/INC-2025-001 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "resolved",
    "resolved_at": "2025-11-28T15:00:00"
  }'
```

**Request Body (all fields optional):**
```json
{
  "title": "string",
  "status": "investigating|identified|monitoring|resolved",
  "severity": "minor|major|critical",
  "resolved_at": "ISO 8601 timestamp or null",
  "affected_services": ["array of strings"],
  "updates": [...]
}
```

**Response:**
```json
{
  "id": "INC-2025-001",
  "title": "...",
  "status": "resolved",
  ...
}
```

---

### Add Update to Incident

**POST** `/api/incidents/{incident_id}/updates`

Adds a new status update to an existing incident. Automatically sets timestamp and updates incident status.

```bash
curl -X POST http://localhost:8000/api/incidents/INC-2025-001/updates \
  -H "Content-Type: application/json" \
  -d '{
    "status": "monitoring",
    "message": "Fix has been deployed. Monitoring closely."
  }'
```

**Request Body:**
```json
{
  "status": "investigating|identified|monitoring|resolved (required)",
  "message": "string (required)"
}
```

**Response:**
```json
{
  "id": "INC-2025-001",
  "updates": [
    ...,
    {
      "timestamp": "2025-11-28T15:30:00",  // Auto-generated
      "status": "monitoring",
      "message": "Fix has been deployed. Monitoring closely."
    }
  ],
  "status": "monitoring"  // Updated to match new update
}
```

**Features:**
- Automatically adds current timestamp
- Updates incident status to match the update
- If status is "resolved" and no `resolved_at`, sets it automatically

---

### Delete Incident

**DELETE** `/api/incidents/{incident_id}`

```bash
curl -X DELETE http://localhost:8000/api/incidents/INC-2025-001
```

**Response:** `204 No Content`

**Errors:**
- `404 Not Found` - Incident doesn't exist

---

## 📊 Complete Workflow Examples

### Example 1: Report New Incident

```bash
# 1. Create the incident
curl -X POST http://localhost:8000/api/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "id": "INC-2025-004",
    "title": "Database Connection Issues",
    "status": "investigating",
    "severity": "critical",
    "created_at": "2025-11-28T16:00:00",
    "resolved_at": null,
    "affected_services": ["Database", "API"],
    "updates": [
      {
        "timestamp": "2025-11-28T16:00:00",
        "status": "investigating",
        "message": "We are aware of database connection timeouts and investigating."
      }
    ]
  }'

# 2. Add progress update
curl -X POST http://localhost:8000/api/incidents/INC-2025-004/updates \
  -H "Content-Type: application/json" \
  -d '{
    "status": "identified",
    "message": "Root cause identified: Connection pool exhausted. Increasing pool size."
  }'

# 3. Add monitoring update
curl -X POST http://localhost:8000/api/incidents/INC-2025-004/updates \
  -H "Content-Type: application/json" \
  -d '{
    "status": "monitoring",
    "message": "Fix deployed. Monitoring connection stability."
  }'

# 4. Resolve the incident
curl -X POST http://localhost:8000/api/incidents/INC-2025-004/updates \
  -H "Content-Type: application/json" \
  -d '{
    "status": "resolved",
    "message": "Database connections stable. Issue fully resolved."
  }'
```

### Example 2: Add New Datadog Monitor

```bash
# 1. Get your monitor ID from Datadog UI
# URL: https://app.datadoghq.com/monitors/123456789
#                                              ^^^^^^^^^ This is the ID

# 2. Add the monitor
curl -X POST http://localhost:8000/api/monitors \
  -H "Content-Type: application/json" \
  -d '{
    "url_monitor": "123456789",
    "nome_monitor": "Redis Cache",
    "descricao_monitor": "Monitors Redis cache availability and response time"
  }'

# 3. Verify it appears on status page
# Visit: http://localhost
```

### Example 3: Update Monitor Description

```bash
curl -X PUT http://localhost:8000/api/monitors/123456789 \
  -H "Content-Type: application/json" \
  -d '{
    "descricao_monitor": "Updated: Monitors Redis cache with 5-minute intervals"
  }'
```

### Example 4: Remove Old Incident

```bash
# Delete incident that's no longer relevant
curl -X DELETE http://localhost:8000/api/incidents/INC-2024-999
```

---

## 🔐 Security Notes

**Current Setup:**
- No authentication required (suitable for internal networks)
- JSON files are backed up before modification (`.backup` files)

**For Production:**
Consider adding:
- API key authentication
- Rate limiting
- Audit logging
- Role-based access control

---

## 💡 Tips & Best Practices

### Monitor Management
1. **Use real Datadog monitor IDs** - Get them from your Datadog UI
2. **Test monitors first** - Verify they exist before adding
3. **Keep descriptions clear** - Help users understand what's being monitored

### Incident Management
1. **Use consistent ID format** - e.g., `INC-YYYY-NNN`
2. **Update regularly** - Keep customers informed every 30-60 minutes
3. **Be specific** - Mention affected services and expected resolution
4. **Always resolve** - Don't leave incidents in monitoring status indefinitely

### Automation
You can automate incident creation using webhooks or scripts:

```python
import requests
from datetime import datetime

def create_incident(title, severity, services):
    incident_id = f"INC-{datetime.now().strftime('%Y-%m-%d-%H%M')}"

    data = {
        "id": incident_id,
        "title": title,
        "status": "investigating",
        "severity": severity,
        "created_at": datetime.now().isoformat(),
        "resolved_at": None,
        "affected_services": services,
        "updates": [{
            "timestamp": datetime.now().isoformat(),
            "status": "investigating",
            "message": f"We are investigating reports of {title.lower()}."
        }]
    }

    response = requests.post(
        "http://localhost:8000/api/incidents",
        json=data
    )
    return response.json()

# Usage
create_incident(
    "High API Error Rate",
    "major",
    ["API", "Authentication Service"]
)
```

---

## 🧪 Testing with Swagger UI

1. Open http://localhost:8000/docs
2. Click on any endpoint (e.g., "POST /api/monitors")
3. Click "Try it out"
4. Fill in the request body
5. Click "Execute"
6. See the response below

This is the easiest way to test all endpoints!

---

## 📝 Response Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 204 | No Content - Deletion successful |
| 404 | Not Found - Resource doesn't exist |
| 409 | Conflict - Resource already exists |
| 422 | Unprocessable Entity - Invalid request data |
| 500 | Internal Server Error - Server-side error |

---

## 🔄 Data Persistence

- All changes are immediately written to `monitors.json` and `incidents.json`
- Backup files (`.backup`) are created before each write
- Changes are visible on the frontend within 60 seconds (auto-refresh)
- No database required - everything stored in JSON

---

## 📚 Related Documentation

- **INCIDENT_GUIDE.md** - Detailed guide on incident management concepts
- **DATADOG_SETUP.md** - How to get Datadog API keys and monitor IDs
- **README.md** - Full project documentation
- **QUICK_START.md** - Quick reference for common tasks
