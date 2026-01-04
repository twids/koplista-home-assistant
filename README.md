# Koplista Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/twids/koplista-home-assistant.svg)](https://github.com/twids/koplista-home-assistant/releases)
[![License](https://img.shields.io/github/license/twids/koplista-home-assistant.svg)](LICENSE)

A Home Assistant integration for [Koplista](https://github.com/twids/k-plista), a grocery list application. This integration allows you to add items to your Koplista shopping lists using voice commands via Google Home or Home Assistant services.

## Features

- 🗣️ **Voice Commands**: Add items using voice commands like "Lägg till mjölk på köplistan" (Swedish) or "Add milk to the shopping list" (English)
- 🎛️ **Services**: Use Home Assistant services to add items programmatically
- 🌐 **Multi-language**: Support for Swedish and English
- 🔐 **Secure**: API key authentication

## Current Limitations

**Note**: The Koplista API currently only supports adding items. Features like viewing lists, removing items, and marking items as bought require additional API endpoints that are not yet implemented. This integration will be expanded as more API endpoints become available.

## Prerequisites

- Home Assistant 2024.1.0 or newer
- A running Koplista instance with API key support
- An API key from your Koplista instance

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add `https://github.com/twids/koplista-home-assistant` as an integration
6. Click "Add"
7. Search for "Koplista" in HACS
8. Click "Download"
9. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/koplista` folder to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

1. In Home Assistant, go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Koplista"
4. Enter your Koplista configuration:
   - **URL**: Your Koplista instance URL (must start with `http://` or `https://`, e.g., `https://koplista.example.com`)
   - **API Key**: Your personal API key from Koplista
5. Click **Submit**

The integration will validate your connection.

## Usage

### Voice Commands

The integration registers intents for voice assistant integration. You can use phrases like:

**Swedish:**
- "Lägg till mjölk på köplistan"
- "Lägg till ägg på inköpslistan"
- "Köp bröd"

**English:**
- "Add milk to the shopping list"
- "Add eggs to the grocery list"
- "Buy bread"

### Services

The integration provides the following services:

#### `koplista.add_item`

Add an item to a Koplista shopping list.

### Services

The integration provides the following service:

#### `koplista.add_item`

Add an item to a Koplista shopping list.

**Parameters:**
- `list_id` (optional): ID of the shopping list (defaults to "default" if not specified)
- `item` (required): Name of the item to add

**Example:**
```yaml
service: koplista.add_item
data:
  list_id: "default"
  item: "Mjölk"
```

## Troubleshooting

### Connection Issues

If the integration fails to connect:
1. Verify your Koplista instance URL is correct and accessible (must start with `http://` or `https://`)
2. Check that your API key is valid
3. Ensure your Koplista instance has API key support enabled
4. Check Home Assistant logs for detailed error messages

### Voice Commands Not Working

1. Ensure the Conversation integration is enabled in Home Assistant
2. Configure your voice assistant (Google Home, Alexa, etc.) with Home Assistant
3. Check that the intent handlers are registered in the Home Assistant logs

## Development

### API Endpoints

The integration currently uses the following Koplista API endpoint:
- `POST /api/external/add-item` - Add an item (with `listId` and `itemName` in request body)

All requests require the `X-API-Key` header.

**Note**: Additional endpoints for fetching lists, viewing items, and removing items are planned for future implementation in the Koplista API. This integration will be expanded once those endpoints are available.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- [Koplista Main Repository](https://github.com/twids/k-plista)
- [Home Assistant](https://www.home-assistant.io/)
- [HACS](https://hacs.xyz/)

## Support

For issues and feature requests, please use the [GitHub issue tracker](https://github.com/twids/koplista-home-assistant/issues).
