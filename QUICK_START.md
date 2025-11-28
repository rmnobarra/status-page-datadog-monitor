# Quick Start Guide

## 🚀 Accessing Your Status Page

### Main Web Interface
```
http://localhost
```

This is your **public-facing status page** where customers can see:
- Real-time service status
- Incident timeline with updates
- Overall system health

---

## 📍 All Available Endpoints

### Frontend (React App)
- **URL:** `http://localhost`
- **What it shows:**
  - Service status cards (from Datadog monitors)
  - Incident timeline (from incidents.json)
  - Overall system health banner
  - Auto-refreshes every 60 seconds

### Backend API Endpoints

#### 1. Get All Monitors
```bash
curl http://localhost:8000/api/monitors
```
Returns current status of all configured services.

#### 2. Get Recent Incidents
```bash
curl http://localhost:8000/api/incidents
```
Returns incidents from the last 30 days with all updates.

#### 3. Get Overall Status
```bash
curl http://localhost:8000/api/status
```
Returns system-wide health: `operational`, `partial_outage`, `major_outage`, or `unknown`.

#### 4. Legacy Status Page (Jinja2 Template)
```bash
curl http://localhost:8000/
```
Old HTML template version (still works for backward compatibility).

#### 5. API Documentation (Interactive)
```
http://localhost:8000/docs
```
Swagger UI with interactive API testing.

---

## 📝 Managing Incidents

### View Current Incidents
```bash
cat incidents.json
```

### Add a New Incident

Edit `incidents.json` and add:

```json
{
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
}
```

### Restart Backend to Apply Changes
```bash
docker-compose restart backend
```

Or wait 60 seconds for auto-refresh on the frontend.

### See Full Guide
```bash
cat INCIDENT_GUIDE.md
```

---

## 🔧 Managing Monitors

### View Current Monitors
```bash
cat monitors.json
```

### Update Monitor IDs

1. Get real monitor IDs from Datadog (see `DATADOG_SETUP.md`)
2. Edit `monitors.json`:

```json
[
  {
    "url_monitor": "YOUR_REAL_MONITOR_ID",
    "nome_monitor": "Production API",
    "descricao_monitor": "Main API health check"
  }
]
```

3. Restart backend:
```bash
docker-compose restart backend
```

---

## 🐳 Docker Commands

### Start Everything
```bash
docker-compose up -d
```

### View Logs
```bash
# All logs
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

### Restart Services
```bash
# Restart everything
docker-compose restart

# Restart backend only
docker-compose restart backend

# Restart frontend only
docker-compose restart frontend
```

### Stop Everything
```bash
docker-compose down
```

### Rebuild and Start
```bash
docker-compose up --build -d
```

---

## 🔍 Troubleshooting

### Check if Services are Running
```bash
docker-compose ps
```

Should show:
- `status-page-backend` - Up
- `status-page-frontend` - Up

### Test Backend API
```bash
curl http://localhost:8000/api/status
```

### Test Frontend
```bash
curl -I http://localhost
```

Should return `200 OK`.

### View Backend Logs for Errors
```bash
docker-compose logs backend | grep -E "(ERROR|WARNING)"
```

### Common Issues

**"Connection refused" on port 80:**
- Check if frontend is running: `docker-compose ps`
- Check logs: `docker-compose logs frontend`

**"Connection refused" on port 8000:**
- Check if backend is running: `docker-compose ps`
- Check logs: `docker-compose logs backend`

**Monitors show "No Data":**
- You're using placeholder monitor IDs
- See `DATADOG_SETUP.md` to get real IDs

**Incidents not showing:**
- Check if incidents.json exists
- Verify JSON syntax: `python3 -m json.tool incidents.json`
- Check backend logs: `docker-compose logs backend | grep incident`

**Frontend not updating:**
- Clear browser cache
- Check browser console for errors (F12)
- Verify API is reachable: `curl http://localhost:8000/api/monitors`

---

## 🎨 Customization

### Change Page Title
Edit `frontend/index.html`:
```html
<title>Your Company Status</title>
```

### Change Refresh Interval
Edit `frontend/src/App.tsx` line 42:
```typescript
const interval = setInterval(fetchData, 60000) // 60 seconds
```

### Change Colors
Edit `frontend/src/index.css` - modify CSS variables.

### Add More shadcn/ui Components
```bash
cd frontend
npx shadcn-ui@latest add [component-name]
```

---

## 📚 Documentation

- **Full Documentation:** `README.md`
- **Datadog Setup:** `DATADOG_SETUP.md`
- **Incident Management:** `INCIDENT_GUIDE.md`
- **This Guide:** `QUICK_START.md`

---

## ✨ Features

✅ Real-time service monitoring from Datadog
✅ Customer incident notifications with timeline
✅ Auto-refresh every 60 seconds
✅ Responsive design (mobile, tablet, desktop)
✅ REST API for integrations
✅ Docker-based deployment
✅ No database required (JSON-based)
✅ Modern UI with shadcn/ui

---

## 🎯 Quick Test

Test everything is working:

```bash
# 1. Check services are up
docker-compose ps

# 2. Test backend
curl http://localhost:8000/api/monitors | python3 -m json.tool

# 3. Test frontend
curl -I http://localhost

# 4. Open in browser
echo "Open http://localhost in your browser"
```

You should see:
- ✅ Services running
- ✅ API returning JSON
- ✅ Frontend returning HTML
- ✅ Status page loading in browser with incidents timeline

---

**Need more help?**
- Check the logs: `docker-compose logs -f`
- Read the full docs: `cat README.md`
- Review troubleshooting: See sections above
