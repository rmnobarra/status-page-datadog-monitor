from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.datadog_client import get_monitor_status
import json
import os

app = FastAPI()  # <- isso precisa vir ANTES de usar @app.get

templates = Jinja2Templates(directory="app/templates")

# Carrega monitores do JSON
with open("monitors.json", "r") as f:
    MONITORES = json.load(f)


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
