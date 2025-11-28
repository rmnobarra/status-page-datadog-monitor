from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import logging

from app.datadog_client import get_monitor_status
import json
import os

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
