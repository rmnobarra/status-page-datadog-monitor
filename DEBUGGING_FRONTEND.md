# Debugging Frontend - Incident Timeline Not Showing

If the incident timeline is not appearing on the frontend, follow these steps:

## Step 1: Test the API Directly

Open the test page in your browser:
```bash
# Option 1: Open the test file
firefox TEST_INCIDENTS.html
# or
google-chrome TEST_INCIDENTS.html
# or
open TEST_INCIDENTS.html  # macOS

# Option 2: Use curl
curl http://localhost:8000/api/incidents | python3 -m json.tool
```

**Expected Result:** You should see 2 incidents (Database Performance and Authentication Service).

## Step 2: Check Browser Console

1. **Open the main frontend:**
   ```
   http://localhost
   ```

2. **Open Browser Developer Tools:**
   - **Chrome/Edge:** Press `F12` or `Ctrl+Shift+I` (Windows/Linux) or `Cmd+Option+I` (Mac)
   - **Firefox:** Press `F12` or `Ctrl+Shift+K` (Windows/Linux) or `Cmd+Option+K` (Mac)

3. **Go to the Console tab**

4. **Look for log messages:**
   ```
   Fetching status data...
   Responses received: {monitors: 200, incidents: 200, status: 200}
   Data parsed: {monitors: 3, incidents: 2, status: "unknown"}
   ```

5. **Check for errors:**
   - ❌ Red error messages
   - ⚠️ Yellow warning messages
   - Network errors
   - CORS errors

## Step 3: Check Network Tab

1. In Developer Tools, go to **Network** tab
2. Reload the page (`F5` or `Ctrl+R`)
3. Look for these requests:
   - `/api/monitors` - Should return 200 OK
   - `/api/incidents` - Should return 200 OK
   - `/api/status` - Should return 200 OK

4. Click on `/api/incidents` request
5. Check the **Response** tab
6. You should see JSON with 2 incidents

## Step 4: Verify Incidents JSON

Check if the incidents file exists and is valid:

```bash
# Check file exists
ls -la incidents.json

# Validate JSON syntax
python3 -m json.tool incidents.json

# Check dates are recent (last 30 days)
cat incidents.json | grep created_at
```

## Step 5: Check React Component

The incident timeline might be rendering but scrolled below the fold. Try:

1. **Scroll down** on the status page
2. Look for the **"Incident History"** section
3. It should be below the "Services" section

## Step 6: Force Refresh

Clear browser cache and force reload:

- **Chrome/Firefox:** `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
- **Or:** Clear browser cache manually

## Step 7: Check Docker Containers

Ensure both containers are running:

```bash
docker-compose ps
```

Expected output:
```
NAME                      STATUS
status-page-backend       Up
status-page-frontend      Up
```

If not running:
```bash
docker-compose up -d
```

## Step 8: Check Container Logs

### Backend Logs
```bash
docker-compose logs backend | tail -50
```

Look for:
- ✅ `Loaded 2 recent incidents`
- ❌ `incidents.json not found`
- ❌ `Invalid JSON in incidents.json`

### Frontend Logs
```bash
docker-compose logs frontend | tail -20
```

Look for:
- ✅ `nginx` started successfully
- ❌ Any error messages

## Step 9: Rebuild Frontend

If incidents still don't show, rebuild the frontend:

```bash
# Rebuild and restart
docker-compose up --build -d frontend

# Wait a few seconds
sleep 5

# Force refresh browser (Ctrl+Shift+R)
```

## Step 10: Manual Test

Test the component directly:

```bash
# Check if incidents data is in the page source
curl -s http://localhost | grep -i incident
```

## Common Issues and Solutions

### Issue 1: "Cannot GET /api/incidents"

**Problem:** Nginx proxy not working

**Solution:**
```bash
# Check nginx config
docker exec status-page-frontend cat /etc/nginx/conf.d/default.conf | grep -A5 "location /api"

# Should show proxy_pass http://backend:8000
```

### Issue 2: Empty Incidents Array

**Problem:** All incidents are older than 30 days

**Solution:** Update `created_at` dates in `incidents.json`:
```bash
# Edit incidents.json and set created_at to today's date
nano incidents.json

# Change dates to recent ones, e.g., 2025-11-28
```

### Issue 3: CORS Error in Console

**Problem:** CORS not configured

**Solution:**
```bash
# Backend should have CORS middleware - check logs
docker-compose logs backend | grep CORS

# Restart backend
docker-compose restart backend
```

### Issue 4: White Screen

**Problem:** JavaScript error breaking the app

**Solution:**
1. Open browser console (F12)
2. Check for red error messages
3. Look for syntax errors or missing modules
4. Rebuild frontend:
   ```bash
   docker-compose up --build -d frontend
   ```

### Issue 5: Component Not Rendering

**Problem:** Incidents array is empty in React

**Solution:** Check browser console:
```javascript
// Look for this log message:
"Data parsed: {monitors: X, incidents: 0, status: ...}"
//                                        ^ Should be 2, not 0
```

If incidents is 0, the API is not returning data correctly.

## Step 11: Direct API Test in Browser

Open these URLs directly in your browser:

1. **Test incidents endpoint:**
   ```
   http://localhost:8000/api/incidents
   ```
   Should return JSON with incidents array.

2. **Test monitors endpoint:**
   ```
   http://localhost:8000/api/monitors
   ```
   Should return JSON with monitors array.

3. **Test status endpoint:**
   ```
   http://localhost:8000/api/status
   ```
   Should return overall status.

## Step 12: Verify React App Loading

Check if React is loading correctly:

1. Open http://localhost
2. Open browser console
3. Look for React DevTools message or logs starting with "Fetching status data..."
4. If you see nothing, React might not be loaded

## Final Checklist

Before reporting an issue, verify:

- [ ] Docker containers are running (`docker-compose ps`)
- [ ] Backend API works (`curl http://localhost:8000/api/incidents`)
- [ ] Frontend serves pages (`curl -I http://localhost`)
- [ ] incidents.json exists and is valid JSON
- [ ] Incident dates are within last 30 days
- [ ] Browser console shows no errors
- [ ] Network tab shows successful API calls (200 OK)
- [ ] Tried force refresh (`Ctrl+Shift+R`)
- [ ] Tried different browser

## Get Help

If still not working, collect this information:

```bash
# Save logs
docker-compose logs > debug-logs.txt

# Save API response
curl http://localhost:8000/api/incidents > incidents-api.json

# Browser console
# Take screenshot of console errors (F12 -> Console tab)
```

Then check:
1. Browser console screenshot
2. debug-logs.txt
3. incidents-api.json

Look for errors or unexpected values.
