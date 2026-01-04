"""Constants for the Koplista integration."""

DOMAIN = "koplista"

# Configuration
CONF_URL = "url"
CONF_API_KEY = "api_key"

# Default values
DEFAULT_NAME = "Koplista"
DEFAULT_SCAN_INTERVAL = 30  # seconds

# API endpoints
API_LISTS = "/api/external/lists"
API_LIST_ITEMS = "/api/external/lists/{list_id}/items"
API_ADD_ITEM = "/api/external/add-item"
API_REMOVE_ITEM = "/api/external/items/{item_id}"
API_UPDATE_ITEM = "/api/external/items/{item_id}/bought"

# Services
SERVICE_ADD_ITEM = "add_item"
SERVICE_REMOVE_ITEM = "remove_item"

# Intent
INTENT_ADD_ITEM = "KoplistaAddItem"
