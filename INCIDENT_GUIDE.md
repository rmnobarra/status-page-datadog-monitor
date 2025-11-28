# Incident Notification Guide

This guide explains how to add, update, and manage incident notifications on your status page.

## What are Incident Notifications?

Incident notifications are a way to communicate with your customers about ongoing issues, outages, or maintenance events. They appear on the status page as a timeline showing the progression of an incident from detection to resolution.

## Incident JSON Structure

All incidents are stored in the `incidents.json` file. Each incident has the following structure:

```json
{
  "id": "INC-2025-001",
  "title": "Database Performance Degradation",
  "status": "resolved",
  "severity": "major",
  "created_at": "2025-11-20T14:30:00",
  "resolved_at": "2025-11-20T16:45:00",
  "affected_services": ["Database"],
  "updates": [
    {
      "timestamp": "2025-11-20T14:30:00",
      "status": "investigating",
      "message": "We are investigating reports of slow database queries."
    }
  ]
}
```

## Field Descriptions

### Required Fields

#### `id` (string)
- Unique identifier for the incident
- Format suggestion: `INC-YYYY-NNN` (e.g., `INC-2025-001`)
- Must be unique across all incidents

#### `title` (string)
- Brief, clear title describing the issue
- Examples:
  - "API Performance Degradation"
  - "Database Connection Failures"
  - "Scheduled Maintenance Window"

#### `status` (string)
- Current incident status
- **Must be one of:**
  - `investigating` - Team is looking into the issue
  - `identified` - Root cause has been identified
  - `monitoring` - Fix deployed, monitoring for stability
  - `resolved` - Issue completely resolved

#### `severity` (string)
- Impact level of the incident
- **Must be one of:**
  - `minor` - Small impact, limited users affected
  - `major` - Significant impact, service degraded
  - `critical` - Severe impact, service unavailable

#### `created_at` (ISO 8601 timestamp)
- When the incident started
- Format: `YYYY-MM-DDTHH:MM:SS`
- Example: `2025-11-28T09:00:00`

#### `resolved_at` (ISO 8601 timestamp or null)
- When the incident was resolved
- Set to `null` if still ongoing
- Format: `YYYY-MM-DDTHH:MM:SS`
- Example: `2025-11-28T11:30:00`

#### `affected_services` (array of strings)
- List of services impacted by this incident
- Should match the service names from your `monitors.json`
- Example: `["Authentication Service", "API Gateway"]`

#### `updates` (array of objects)
- Chronological list of status updates
- Each update has:
  - `timestamp` - When this update was posted
  - `status` - Status at this point (investigating/identified/monitoring/resolved)
  - `message` - Clear communication about what's happening

## How to Add a New Incident

### Step 1: Open incidents.json

Navigate to your project root and open `incidents.json`.

### Step 2: Add Your Incident

Add a new incident object to the array:

```json
[
  {
    "id": "INC-2025-003",
    "title": "Email Service Degradation",
    "status": "investigating",
    "severity": "minor",
    "created_at": "2025-11-28T14:00:00",
    "resolved_at": null,
    "affected_services": ["Email Service"],
    "updates": [
      {
        "timestamp": "2025-11-28T14:00:00",
        "status": "investigating",
        "message": "We are aware of delays in email delivery and are investigating the cause."
      }
    ]
  }
]
```

### Step 3: Save the File

The status page will automatically pick up the new incident on the next refresh (within 60 seconds).

## How to Update an Existing Incident

### Adding a Status Update

To add a new update to an existing incident:

1. Find the incident in `incidents.json`
2. Add a new update object to the `updates` array
3. Update the `status` field to match the new status
4. Save the file

Example:

```json
{
  "id": "INC-2025-003",
  "title": "Email Service Degradation",
  "status": "identified",  // Updated status
  "severity": "minor",
  "created_at": "2025-11-28T14:00:00",
  "resolved_at": null,
  "affected_services": ["Email Service"],
  "updates": [
    {
      "timestamp": "2025-11-28T14:00:00",
      "status": "investigating",
      "message": "We are aware of delays in email delivery and are investigating the cause."
    },
    {
      "timestamp": "2025-11-28T14:30:00",  // New update
      "status": "identified",
      "message": "The issue has been identified as a configuration error in our email routing. Team is working on a fix."
    }
  ]
}
```

### Resolving an Incident

When an incident is resolved:

1. Change the `status` to `resolved`
2. Set the `resolved_at` timestamp
3. Add a final update with status `resolved`

Example:

```json
{
  "id": "INC-2025-003",
  "title": "Email Service Degradation",
  "status": "resolved",
  "severity": "minor",
  "created_at": "2025-11-28T14:00:00",
  "resolved_at": "2025-11-28T15:00:00",
  "affected_services": ["Email Service"],
  "updates": [
    {
      "timestamp": "2025-11-28T14:00:00",
      "status": "investigating",
      "message": "We are aware of delays in email delivery and are investigating the cause."
    },
    {
      "timestamp": "2025-11-28T14:30:00",
      "status": "identified",
      "message": "The issue has been identified as a configuration error in our email routing. Team is working on a fix."
    },
    {
      "timestamp": "2025-11-28T15:00:00",
      "status": "resolved",
      "message": "The configuration has been corrected and email delivery is back to normal. All queued emails have been sent."
    }
  ]
}
```

## Best Practices

### Communication

1. **Be Clear**: Use simple, jargon-free language
2. **Be Timely**: Post updates as significant progress is made
3. **Be Honest**: Don't sugarcoat or hide issues
4. **Be Specific**: Mention affected services and expected resolution times when known

### Update Frequency

- **Investigating**: Update every 30-60 minutes
- **Identified**: Update when fix is being deployed
- **Monitoring**: Update when monitoring is complete
- **Resolved**: Final update confirming resolution

### Example Messages by Status

#### Investigating
```
"We are investigating reports of intermittent errors affecting the API service."
"Our team has been alerted and is investigating the root cause of the outage."
```

#### Identified
```
"Root cause identified: database connection pool exhaustion. Deploying fix now."
"Issue identified as a memory leak in the authentication service. Team is working on a patch."
```

#### Monitoring
```
"Fix has been deployed. Monitoring service performance closely."
"Patch applied successfully. Watching metrics to ensure stability."
```

#### Resolved
```
"All services have returned to normal operation. No further action required."
"Issue fully resolved. We've implemented additional monitoring to prevent recurrence."
```

## Automatic Filtering

The status page automatically:
- Shows only incidents from the **last 30 days**
- Displays updates in **reverse chronological order** (newest first)
- Filters incidents when you refresh the page

## Testing Your Changes

After modifying `incidents.json`:

1. Save the file
2. Wait 60 seconds for auto-refresh OR
3. Manually refresh your browser
4. Check that your incident appears correctly
5. Verify timestamps and messages are formatted properly

## Common Issues

### Incident not showing up?

- Check that `created_at` is within the last 30 days
- Verify JSON syntax is valid (use a JSON validator)
- Ensure all required fields are present
- Check browser console for errors

### Formatting looks wrong?

- Verify ISO 8601 timestamp format: `YYYY-MM-DDTHH:MM:SS`
- Check that service names match those in `monitors.json`
- Ensure status values are exactly: investigating, identified, monitoring, or resolved

### Need to hide an old incident?

- Either delete it from the JSON file OR
- Change its `created_at` date to more than 30 days ago

## Quick Reference

### Valid Status Values
- `investigating`
- `identified`
- `monitoring`
- `resolved`

### Valid Severity Values
- `minor`
- `major`
- `critical`

### Timestamp Format
```
YYYY-MM-DDTHH:MM:SS
2025-11-28T14:30:00
```

## Need Help?

If you encounter issues:
1. Validate your JSON syntax using jsonlint.com
2. Check the browser console for errors
3. Review the backend logs: `docker-compose logs -f backend`
4. Ensure all timestamps are in ISO 8601 format
