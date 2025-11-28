"""
Helper functions for CRUD operations on JSON files
"""
import json
import os
from typing import List, Dict, Any
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

MONITORS_FILE = "monitors.json"
INCIDENTS_FILE = "incidents.json"


def read_json_file(filename: str) -> List[Dict[str, Any]]:
    """Read and parse a JSON file"""
    try:
        if not os.path.exists(filename):
            logger.warning(f"{filename} not found, creating empty file")
            write_json_file(filename, [])
            return []

        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {filename}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Invalid JSON in {filename}"
        )
    except Exception as e:
        logger.error(f"Error reading {filename}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reading {filename}"
        )


def write_json_file(filename: str, data: List[Dict[str, Any]]) -> None:
    """Write data to a JSON file with backup"""
    try:
        # Create backup if file exists
        if os.path.exists(filename):
            backup_file = f"{filename}.backup"
            with open(filename, 'r', encoding='utf-8') as f:
                backup_data = f.read()
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(backup_data)

        # Write new data
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"Successfully wrote {len(data)} items to {filename}")
    except Exception as e:
        logger.error(f"Error writing to {filename}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error writing to {filename}"
        )


def reload_monitors_cache():
    """Reload monitors cache in memory"""
    # This will be called after any monitor CRUD operation
    # to ensure the in-memory cache is updated
    global MONITORES
    try:
        with open(MONITORS_FILE, 'r', encoding='utf-8') as f:
            MONITORES = json.load(f)
            logger.info(f"Reloaded {len(MONITORES)} monitors from {MONITORS_FILE}")
    except Exception as e:
        logger.error(f"Error reloading monitors: {e}")
