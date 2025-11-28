# CRUD API Quick Start

Fast reference for managing monitors and incidents via API.

## 🚀 Quick Links

- **API Docs (Interactive):** http://localhost:8000/docs
- **Status Page:** http://localhost
- **Full Guide:** See `API_CRUD_GUIDE.md`

## ⚡ Most Common Operations

### Add a New Monitor

```bash
curl -X POST http://localhost:8000/api/monitors \
  -H "Content-Type: application/json" \
  -d '{
    "url_monitor": "YOUR_DATADOG_MONITOR_ID",
    "nome_monitor": "Service Name",
    "descricao_monitor": "What this monitor checks"
  }'
```

### Create an Incident

```bash
curl -X POST http://localhost:8000/api/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "id": "INC-2025-005",
    "title": "Service Outage",
    "status": "investigating",
    "severity": "major",
    "created_at": "2025-11-28T14:00:00",
    "resolved_at": null,
    "affected_services": ["API", "Database"],
    "updates": [{
      "timestamp": "2025-11-28T14:00:00",
      "status": "investigating",
      "message": "We are investigating the issue."
    }]
  }'
```

### Add Update to Incident

```bash
curl -X POST http://localhost:8000/api/incidents/INC-2025-005/updates \
  -H "Content-Type: application/json" \
  -d '{
    "status": "resolved",
    "message": "Issue resolved. All services operational."
  }'
```

### List Everything

```bash
# List monitors
curl http://localhost:8000/api/monitors/list

# List incidents
curl http://localhost:8000/api/incidents/list
```

### Delete Resources

```bash
# Delete monitor
curl -X DELETE http://localhost:8000/api/monitors/MONITOR_ID

# Delete incident
curl -X DELETE http://localhost:8000/api/incidents/INC-2025-005
```

## 🧪 Test All Operations

Run the test script:

```bash
./test_crud_api.sh
```

This tests all CRUD operations for both monitors and incidents.

## 📊 Using Swagger UI (Recommended)

1. Open http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in the data
5. Click "Execute"
6. See the response

Much easier than curl!

## 📝 Field Reference

### Monitor Fields
- `url_monitor` - Datadog monitor ID (string, required)
- `nome_monitor` - Display name (string, required)
- `descricao_monitor` - Description (string, required)

### Incident Fields
- `id` - Unique ID like "INC-2025-001" (string, required)
- `title` - Incident title (string, required)
- `status` - One of: `investigating`, `identified`, `monitoring`, `resolved`
- `severity` - One of: `minor`, `major`, `critical`
- `created_at` - ISO 8601 timestamp (required)
- `resolved_at` - ISO 8601 timestamp or null
- `affected_services` - Array of service names
- `updates` - Array of status updates

### Incident Update Fields
- `status` - One of: `investigating`, `identified`, `monitoring`, `resolved`
- `message` - Customer-facing message (string, required)
- `timestamp` - Auto-generated if not provided

## 🔄 Workflow Example

```bash
# 1. Create incident
curl -X POST http://localhost:8000/api/incidents -H "Content-Type: application/json" \
  -d '{"id":"INC-2025-006","title":"API Slowdown","status":"investigating","severity":"major","created_at":"2025-11-28T15:00:00","resolved_at":null,"affected_services":["API"],"updates":[{"timestamp":"2025-11-28T15:00:00","status":"investigating","message":"Investigating slow API responses."}]}'

# 2. Add update (identified)
curl -X POST http://localhost:8000/api/incidents/INC-2025-006/updates -H "Content-Type: application/json" \
  -d '{"status":"identified","message":"Root cause: Database query timeout. Fixing now."}'

# 3. Add update (monitoring)
curl -X POST http://localhost:8000/api/incidents/INC-2025-006/updates -H "Content-Type: application/json" \
  -d '{"status":"monitoring","message":"Fix deployed. Monitoring API performance."}'

# 4. Resolve
curl -X POST http://localhost:8000/api/incidents/INC-2025-006/updates -H "Content-Type: application/json" \
  -d '{"status":"resolved","message":"API performance back to normal."}'
```

## 💡 Tips

1. **Use the interactive docs** - Much easier than curl
2. **IDs are case-sensitive** - "INC-001" ≠ "inc-001"
3. **Backups are automatic** - `.backup` files created before changes
4. **Changes sync instantly** - Updates appear on frontend in ~60 seconds
5. **Test in Swagger first** - Then copy the curl command

## 🆘 Common Issues

**409 Conflict:**
- Resource already exists
- Solution: Use a different ID or UPDATE instead

**404 Not Found:**
- Resource doesn't exist
- Solution: Check the ID spelling

**422 Validation Error:**
- Invalid request data
- Solution: Check required fields and data types

## 📚 Full Documentation

See `API_CRUD_GUIDE.md` for:
- Complete API reference
- All response codes
- Error handling
- Advanced examples
- Automation tips
