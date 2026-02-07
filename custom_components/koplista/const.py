"""Constants for the Koplista integration."""

DOMAIN = "koplista"

# Default values
DEFAULT_NAME = "Koplista"

# API endpoints
# Current API Limitations:
# The Koplista API currently only supports adding items via the add-item endpoint.
# Future endpoints for fetching, updating, and deleting items are planned but not yet implemented.
API_ADD_ITEM = "/api/external/add-item"

# Services
SERVICE_ADD_ITEM = "add_item"

# Intent
INTENT_ADD_ITEM = "KoplistaAddItem"
