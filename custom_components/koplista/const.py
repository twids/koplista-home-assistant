"""Constants for the Koplista integration."""

DOMAIN = "koplista"

# Configuration
CONF_API_KEY = "api_key"

# Default values
DEFAULT_NAME = "Koplista"
DEFAULT_SCAN_INTERVAL = 30  # seconds

# API endpoints
# Note: Only the add-item endpoint is currently implemented in the Koplista API
API_ADD_ITEM = "/api/external/add-item"

# Services
SERVICE_ADD_ITEM = "add_item"

# Intent
INTENT_ADD_ITEM = "KoplistaAddItem"
