import os
from dotenv import load_dotenv

load_dotenv()

DATADOG_API_KEY = os.getenv("DATADOG_API_KEY")
DATADOG_APP_KEY = os.getenv("DATADOG_APP_KEY")
DATADOG_API_HOST = os.getenv("DATADOG_API_HOST", "https://api.datadoghq.com")
