from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


# Monitor Models
class MonitorCreate(BaseModel):
    """Model for creating a new monitor"""
    url_monitor: str = Field(..., description="Datadog monitor ID")
    nome_monitor: str = Field(..., description="Display name for the monitor")
    descricao_monitor: str = Field(..., description="Description of what this monitor checks")


class MonitorUpdate(BaseModel):
    """Model for updating an existing monitor"""
    url_monitor: Optional[str] = Field(None, description="Datadog monitor ID")
    nome_monitor: Optional[str] = Field(None, description="Display name for the monitor")
    descricao_monitor: Optional[str] = Field(None, description="Description of what this monitor checks")


class MonitorResponse(BaseModel):
    """Model for monitor response"""
    url_monitor: str
    nome_monitor: str
    descricao_monitor: str


# Incident Models
class IncidentUpdate(BaseModel):
    """Model for incident status updates"""
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    status: Literal["investigating", "identified", "monitoring", "resolved"]
    message: str = Field(..., description="Update message for customers")


class IncidentCreate(BaseModel):
    """Model for creating a new incident"""
    id: str = Field(..., description="Unique incident ID (e.g., INC-2025-001)")
    title: str = Field(..., description="Incident title")
    status: Literal["investigating", "identified", "monitoring", "resolved"]
    severity: Literal["minor", "major", "critical"]
    created_at: str = Field(..., description="ISO 8601 timestamp when incident started")
    resolved_at: Optional[str] = Field(None, description="ISO 8601 timestamp when resolved (null if ongoing)")
    affected_services: List[str] = Field(..., description="List of affected service names")
    updates: List[IncidentUpdate] = Field(..., description="List of status updates")


class IncidentUpdateModel(BaseModel):
    """Model for updating an existing incident"""
    title: Optional[str] = None
    status: Optional[Literal["investigating", "identified", "monitoring", "resolved"]] = None
    severity: Optional[Literal["minor", "major", "critical"]] = None
    resolved_at: Optional[str] = None
    affected_services: Optional[List[str]] = None
    updates: Optional[List[IncidentUpdate]] = None


class IncidentResponse(BaseModel):
    """Model for incident response"""
    id: str
    title: str
    status: str
    severity: str
    created_at: str
    resolved_at: Optional[str]
    affected_services: List[str]
    updates: List[IncidentUpdate]


class AddIncidentUpdate(BaseModel):
    """Model for adding a single update to an existing incident"""
    status: Literal["investigating", "identified", "monitoring", "resolved"]
    message: str = Field(..., description="Update message for customers")
