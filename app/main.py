from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import logging

from app.datadog_client import get_monitor_status
from app.models import (
    MonitorCreate, MonitorUpdate, MonitorResponse,
    IncidentCreate, IncidentUpdateModel, IncidentResponse, AddIncidentUpdate
)
import json
import os
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Status Page API", version="2.0.0")

# CORS middleware for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="app/templates")

# Carrega monitores do JSON
try:
    with open("monitors.json", "r") as f:
        MONITORES = json.load(f)
        logger.info(f"Loaded {len(MONITORES)} monitors from monitors.json")
except FileNotFoundError:
    logger.error("monitors.json not found! Please create this file.")
    MONITORES = []
except json.JSONDecodeError as e:
    logger.error(f"Invalid JSON in monitors.json: {e}")
    MONITORES = []

# Carrega incidentes do JSON (com fallback caso não exista)
def load_incidents():
    try:
        with open("incidents.json", "r") as f:
            incidents = json.load(f)
            # Filter last 30 days
            thirty_days_ago = datetime.now() - timedelta(days=30)
            filtered = [
                inc for inc in incidents
                if datetime.fromisoformat(inc["created_at"]) >= thirty_days_ago
            ]
            logger.info(f"Loaded {len(filtered)} recent incidents (out of {len(incidents)} total)")
            return filtered
    except FileNotFoundError:
        logger.info("incidents.json not found - no incidents will be displayed")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in incidents.json: {e}")
        return []
    except Exception as e:
        logger.error(f"Error loading incidents: {e}")
        return []

@app.on_event("startup")
async def startup_event():
    logger.info("Status Page API starting up...")
    logger.info(f"Monitors configured: {len(MONITORES)}")
    if MONITORES:
        for monitor in MONITORES:
            logger.info(f"  - {monitor['nome_monitor']} (ID: {monitor['url_monitor']})")

@app.get("/", response_class=HTMLResponse)
async def status_page(request: Request):
    monitores_info = []
    for monitor in MONITORES:
        monitor_id = int(monitor["url_monitor"])
        estado = await get_monitor_status(monitor_id)

        monitores_info.append({
            "nome_monitor": monitor["nome_monitor"],
            "descricao_monitor": monitor["descricao_monitor"],
            "estado": estado
        })

    return templates.TemplateResponse("status.html", {
        "request": request,
        "monitores": monitores_info
    })

@app.get("/api/monitors")
async def get_monitors():
    """API endpoint to get all monitor statuses"""
    monitores_info = []
    for monitor in MONITORES:
        monitor_id = int(monitor["url_monitor"])
        estado = await get_monitor_status(monitor_id)

        monitores_info.append({
            "id": monitor_id,
            "name": monitor["nome_monitor"],
            "description": monitor["descricao_monitor"],
            "status": estado
        })

    return {"monitors": monitores_info}

@app.get("/api/incidents")
async def get_incidents():
    """API endpoint to get recent incidents (last 30 days)"""
    incidents = load_incidents()
    return {"incidents": incidents}

@app.get("/api/status")
async def get_overall_status():
    """API endpoint to get overall system status"""
    monitores_info = []
    for monitor in MONITORES:
        monitor_id = int(monitor["url_monitor"])
        estado = await get_monitor_status(monitor_id)
        monitores_info.append(estado)

    # Filter out "No Data" and "Skipped" for status calculation
    # These are informational, not failures
    active_statuses = [
        status for status in monitores_info
        if status not in ["No Data", "Skipped"]
    ]

    # Determine overall status based on active monitors
    if not active_statuses:
        # All monitors are "No Data" or "Skipped"
        overall = "unknown"
    elif any(status == "Alert" for status in active_statuses):
        # At least one monitor is in alert state
        overall = "major_outage"
    elif any(status == "Warn" for status in active_statuses):
        # At least one monitor is in warning state
        overall = "partial_outage"
    elif all(status == "OK" for status in active_statuses):
        # All active monitors are OK
        overall = "operational"
    else:
        # Unexpected status
        overall = "unknown"

    return {
        "status": overall,
        "updated_at": datetime.now().isoformat()
    }

# ============================================================================
# CRUD ENDPOINTS FOR MONITORS
# ============================================================================

from app.crud_helpers import read_json_file, write_json_file, MONITORS_FILE, INCIDENTS_FILE

@app.get("/api/monitors/list", response_model=List[MonitorResponse], tags=["Monitors"])
async def list_monitors():
    """Get all configured monitors (CRUD endpoint)"""
    monitors = read_json_file(MONITORS_FILE)
    return monitors

@app.post("/api/monitors", response_model=MonitorResponse, status_code=status.HTTP_201_CREATED, tags=["Monitors"])
async def create_monitor(monitor: MonitorCreate):
    """Create a new monitor"""
    monitors = read_json_file(MONITORS_FILE)
    
    # Check if monitor ID already exists
    for existing in monitors:
        if existing.get("url_monitor") == monitor.url_monitor:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Monitor with ID {monitor.url_monitor} already exists"
            )
    
    # Add new monitor
    new_monitor = monitor.model_dump()
    monitors.append(new_monitor)
    write_json_file(MONITORS_FILE, monitors)
    
    # Reload global cache
    global MONITORES
    MONITORES = monitors
    
    logger.info(f"Created monitor: {monitor.nome_monitor} (ID: {monitor.url_monitor})")
    return new_monitor

@app.get("/api/monitors/{monitor_id}", response_model=MonitorResponse, tags=["Monitors"])
async def get_monitor(monitor_id: str):
    """Get a specific monitor by ID"""
    monitors = read_json_file(MONITORS_FILE)
    
    for monitor in monitors:
        if monitor.get("url_monitor") == monitor_id:
            return monitor
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Monitor {monitor_id} not found"
    )

@app.put("/api/monitors/{monitor_id}", response_model=MonitorResponse, tags=["Monitors"])
async def update_monitor(monitor_id: str, monitor_update: MonitorUpdate):
    """Update an existing monitor"""
    monitors = read_json_file(MONITORS_FILE)
    
    for i, monitor in enumerate(monitors):
        if monitor.get("url_monitor") == monitor_id:
            # Update only provided fields
            update_data = monitor_update.model_dump(exclude_unset=True)
            monitors[i].update(update_data)
            write_json_file(MONITORS_FILE, monitors)
            
            # Reload global cache
            global MONITORES
            MONITORES = monitors
            
            logger.info(f"Updated monitor: {monitor_id}")
            return monitors[i]
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Monitor {monitor_id} not found"
    )

@app.delete("/api/monitors/{monitor_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Monitors"])
async def delete_monitor(monitor_id: str):
    """Delete a monitor"""
    monitors = read_json_file(MONITORS_FILE)
    
    for i, monitor in enumerate(monitors):
        if monitor.get("url_monitor") == monitor_id:
            deleted = monitors.pop(i)
            write_json_file(MONITORS_FILE, monitors)
            
            # Reload global cache
            global MONITORES
            MONITORES = monitors
            
            logger.info(f"Deleted monitor: {monitor_id}")
            return
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Monitor {monitor_id} not found"
    )


# ============================================================================
# CRUD ENDPOINTS FOR INCIDENTS
# ============================================================================

@app.get("/api/incidents/list", response_model=List[IncidentResponse], tags=["Incidents"])
async def list_all_incidents():
    """Get all incidents (including those older than 30 days)"""
    incidents = read_json_file(INCIDENTS_FILE)
    return incidents

@app.post("/api/incidents", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED, tags=["Incidents"])
async def create_incident(incident: IncidentCreate):
    """Create a new incident"""
    incidents = read_json_file(INCIDENTS_FILE)
    
    # Check if incident ID already exists
    for existing in incidents:
        if existing.get("id") == incident.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Incident {incident.id} already exists"
            )
    
    # Add new incident
    new_incident = incident.model_dump()
    incidents.append(new_incident)
    write_json_file(INCIDENTS_FILE, incidents)
    
    logger.info(f"Created incident: {incident.id} - {incident.title}")
    return new_incident

@app.get("/api/incidents/{incident_id}", response_model=IncidentResponse, tags=["Incidents"])
async def get_incident(incident_id: str):
    """Get a specific incident by ID"""
    incidents = read_json_file(INCIDENTS_FILE)
    
    for incident in incidents:
        if incident.get("id") == incident_id:
            return incident
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Incident {incident_id} not found"
    )

@app.put("/api/incidents/{incident_id}", response_model=IncidentResponse, tags=["Incidents"])
async def update_incident(incident_id: str, incident_update: IncidentUpdateModel):
    """Update an existing incident"""
    incidents = read_json_file(INCIDENTS_FILE)
    
    for i, incident in enumerate(incidents):
        if incident.get("id") == incident_id:
            # Update only provided fields
            update_data = incident_update.model_dump(exclude_unset=True)
            incidents[i].update(update_data)
            write_json_file(INCIDENTS_FILE, incidents)
            
            logger.info(f"Updated incident: {incident_id}")
            return incidents[i]
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Incident {incident_id} not found"
    )

@app.post("/api/incidents/{incident_id}/updates", response_model=IncidentResponse, tags=["Incidents"])
async def add_incident_update(incident_id: str, update: AddIncidentUpdate):
    """Add a new update to an existing incident"""
    incidents = read_json_file(INCIDENTS_FILE)
    
    for i, incident in enumerate(incidents):
        if incident.get("id") == incident_id:
            # Add timestamp if not provided
            new_update = update.model_dump()
            new_update["timestamp"] = datetime.now().isoformat()
            
            # Add update to incident
            if "updates" not in incidents[i]:
                incidents[i]["updates"] = []
            incidents[i]["updates"].append(new_update)
            
            # Update incident status to match the update
            incidents[i]["status"] = update.status
            
            # If status is resolved and no resolved_at, set it
            if update.status == "resolved" and not incidents[i].get("resolved_at"):
                incidents[i]["resolved_at"] = datetime.now().isoformat()
            
            write_json_file(INCIDENTS_FILE, incidents)
            
            logger.info(f"Added update to incident: {incident_id} - {update.status}")
            return incidents[i]
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Incident {incident_id} not found"
    )

@app.delete("/api/incidents/{incident_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Incidents"])
async def delete_incident(incident_id: str):
    """Delete an incident"""
    incidents = read_json_file(INCIDENTS_FILE)
    
    for i, incident in enumerate(incidents):
        if incident.get("id") == incident_id:
            deleted = incidents.pop(i)
            write_json_file(INCIDENTS_FILE, incidents)
            
            logger.info(f"Deleted incident: {incident_id}")
            return
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Incident {incident_id} not found"
    )
