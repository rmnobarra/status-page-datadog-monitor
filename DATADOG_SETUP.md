# Datadog Setup Guide

This guide will help you configure your Datadog integration and find the monitor IDs you need.

## Step 1: Get Your Datadog API Keys

### 1.1 Log into Datadog

Go to [https://app.datadoghq.com](https://app.datadoghq.com) (or your region's Datadog URL).

### 1.2 Navigate to API Keys

1. Click on your profile icon (bottom left)
2. Go to **Organization Settings**
3. Click on **API Keys** tab

### 1.3 Create or Copy API Key

- If you don't have an API key, click **+ New Key**
- Give it a name like "Status Page"
- Copy the key value

### 1.4 Get Application Key

1. Go to **Application Keys** tab
2. Click **+ New Key**
3. Give it a name like "Status Page App"
4. Copy the key value

### 1.5 Update Your .env File

```bash
DATADOG_API_KEY=your_api_key_here
DATADOG_APP_KEY=your_app_key_here
DATADOG_API_HOST=https://api.datadoghq.com
```

**Important:** Change `DATADOG_API_HOST` based on your region:
- US1: `https://api.datadoghq.com`
- US3: `https://api.us3.datadoghq.com`
- US5: `https://api.us5.datadoghq.com`
- EU: `https://api.datadoghq.eu`
- AP1: `https://api.ap1.datadoghq.com`

## Step 2: Find Your Monitor IDs

### Method 1: From Datadog UI

1. Go to **Monitors** → **Manage Monitors**
2. Click on the monitor you want to display
3. Look at the URL in your browser:
   ```
   https://app.datadoghq.com/monitors/12345678
                                            ^^^^^^^^
                                        This is your Monitor ID
   ```
4. Copy the number from the URL

### Method 2: Using Datadog API

You can list all your monitors using this curl command:

```bash
curl -X GET "https://api.datadoghq.com/api/v1/monitor" \
  -H "DD-API-KEY: ${DATADOG_API_KEY}" \
  -H "DD-APPLICATION-KEY: ${DATADOG_APP_KEY}"
```

This will return JSON with all your monitors, including their IDs and names.

### Method 3: Using Python Script

Create a file `list_monitors.py`:

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('DATADOG_API_KEY')
APP_KEY = os.getenv('DATADOG_APP_KEY')
API_HOST = os.getenv('DATADOG_API_HOST', 'https://api.datadoghq.com')

headers = {
    'DD-API-KEY': API_KEY,
    'DD-APPLICATION-KEY': APP_KEY,
}

response = requests.get(f'{API_HOST}/api/v1/monitor', headers=headers)
monitors = response.json()

print("Your Datadog Monitors:")
print("=" * 80)
for monitor in monitors:
    print(f"ID: {monitor['id']}")
    print(f"Name: {monitor['name']}")
    print(f"Type: {monitor['type']}")
    print(f"Status: {monitor.get('overall_state', 'Unknown')}")
    print("-" * 80)
```

Run it:
```bash
pip install requests python-dotenv
python list_monitors.py
```

## Step 3: Update monitors.json

Once you have your monitor IDs, update `monitors.json`:

```json
[
  {
    "url_monitor": "123456789",
    "nome_monitor": "Production API",
    "descricao_monitor": "Main API endpoint health check"
  },
  {
    "url_monitor": "987654321",
    "nome_monitor": "Database",
    "descricao_monitor": "PostgreSQL primary database"
  }
]
```

**Fields:**
- `url_monitor` - The numeric Monitor ID from Datadog
- `nome_monitor` - Display name (can be anything you want)
- `descricao_monitor` - Description shown on the status page

## Step 4: Test Your Configuration

### 4.1 Test API Access

Test if your API keys work:

```bash
curl -X GET "https://api.datadoghq.com/api/v1/validate" \
  -H "DD-API-KEY: ${DATADOG_API_KEY}" \
  -H "DD-APPLICATION-KEY: ${DATADOG_APP_KEY}"
```

Should return: `{"valid": true}`

### 4.2 Test a Specific Monitor

Test fetching a specific monitor:

```bash
curl -X GET "https://api.datadoghq.com/api/v1/monitor/YOUR_MONITOR_ID" \
  -H "DD-API-KEY: ${DATADOG_API_KEY}" \
  -H "DD-APPLICATION-KEY: ${DATADOG_APP_KEY}"
```

### 4.3 Run the Application

```bash
# Start the backend
docker-compose up backend

# Or locally
uvicorn app.main:app --reload
```

Check the logs for any errors:
- ✅ "Loaded X monitors from monitors.json"
- ✅ Monitor names and IDs should be listed
- ❌ If you see 404 errors, the monitor IDs are wrong
- ❌ If you see 403 errors, check your API keys

## Common Issues

### "404 Not Found" Error

**Problem:** Monitor ID doesn't exist in your Datadog account.

**Solution:**
1. Double-check the monitor ID in Datadog UI
2. Ensure you're using the correct Datadog region
3. Verify the monitor hasn't been deleted

### "403 Forbidden" Error

**Problem:** API keys don't have permission.

**Solution:**
1. Verify your API key is correct
2. Check your Application key has proper permissions
3. Ensure keys are from the same Datadog organization

### "Connection Refused" or Timeout

**Problem:** Wrong API host or network issues.

**Solution:**
1. Check your `DATADOG_API_HOST` matches your region
2. Verify you have internet connectivity
3. Check if Datadog is experiencing outages: [status.datadoghq.com](https://status.datadoghq.com)

### Monitor Shows "No Data"

**Possible causes:**
1. Monitor ID is wrong (404 error - check logs)
2. API keys are invalid (403 error - check logs)
3. Monitor actually has no data in Datadog
4. Network timeout (check logs)

The application now handles these errors gracefully and will show "No Data" status instead of crashing.

## Monitor Status Values

Datadog monitors can have these statuses:
- **OK** - Everything is normal
- **Alert** - Monitor is in alert state
- **Warn** - Monitor is in warning state
- **No Data** - Monitor has no data or cannot be reached
- **Skipped** - Monitor check was skipped

These map to the status page UI:
- OK → Green "Operational"
- Alert → Red "Major Outage"
- Warn → Yellow "Degraded Performance"
- No Data / Skipped → Gray "No Data"

## Security Best Practices

1. **Never commit .env file** - It's in .gitignore, keep it that way
2. **Rotate keys regularly** - Generate new API keys periodically
3. **Use read-only keys** - The status page only needs read access
4. **Limit key scope** - In Datadog, you can limit what an API key can access
5. **Monitor key usage** - Check Datadog audit logs for unusual activity

## Next Steps

Once your monitors are configured:

1. Test the status page: http://localhost
2. Verify all monitors show correct status
3. Set up incident notifications (see INCIDENT_GUIDE.md)
4. Customize the UI if needed
5. Deploy to production

## Need Help?

- **Datadog API Docs:** https://docs.datadoghq.com/api/
- **Monitor API:** https://docs.datadoghq.com/api/latest/monitors/
- **Status Page Logs:** `docker-compose logs -f backend`
