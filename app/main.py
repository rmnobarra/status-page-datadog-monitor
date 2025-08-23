from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json
import os

from app.datadog_client import get_monitor_status

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

with open("monitors.json") as f:
    MONITORS = json.load(f)

@app.get("/", response_class=HTMLResponse)
async def status_page(request: Request):
    statuses = []
    for monitor in MONITORS:
        monitor_id = monitor["url_monitor"].split("/")[-1]
        state = await get_monitor_status(monitor_id)
        statuses.append({
            "nome": monitor["nome_monitor"],
            "descricao": monitor["descricao_monitor"],
            "estado": state
        })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "monitors": statuses
    })
