# Koplista Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/twids/koplista-home-assistant.svg)](https://github.com/twids/koplista-home-assistant/releases)
[![License](https://img.shields.io/github/license/twids/koplista-home-assistant.svg)](LICENSE)

A Home Assistant integration for [Koplista](https://github.com/twids/k-plista), a grocery list application. This integration allows you to manage your Koplista shopping lists directly from Home Assistant and use voice commands via Google Home to add items to your lists.

## Features

- 🛒 **Shopping List Management**: View and manage your Koplista shopping lists as Todo entities in Home Assistant
- 🗣️ **Voice Commands**: Add items using voice commands like "Lägg till mjölk på köplistan" (Swedish) or "Add milk to the shopping list" (English)
- 🔄 **Real-time Sync**: Automatic polling to keep your lists up to date
- 🎛️ **Services**: Use Home Assistant services to add/remove items programmatically
- 🌐 **Multi-language**: Support for Swedish and English

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
   - **URL**: Your Koplista instance URL (e.g., `https://koplista.example.com`)
   - **API Key**: Your personal API key from Koplista
5. Click **Submit**

The integration will validate your connection and create Todo entities for each of your shopping lists.

## Usage

### Todo Entities

After configuration, you'll see Todo entities for each of your Koplista shopping lists:
- `todo.koplista_[list_name]`

You can:
- View items in the Home Assistant Todo card
- Add new items
- Mark items as bought (complete)
- Remove items

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

**Parameters:**
- `list_name` (optional): Name of the shopping list (uses default if not specified)
- `item` (required): Name of the item to add

**Example:**
```yaml
service: koplista.add_item
data:
  list_name: "Inköpslista"
  item: "Mjölk"
```

#### `koplista.remove_item`

Remove an item from a Koplista shopping list.

**Parameters:**
- `list_name` (optional): Name of the shopping list
- `item` (required): Name of the item to remove

**Example:**
```yaml
service: koplista.remove_item
data:
  list_name: "Inköpslista"
  item: "Mjölk"
```

## Troubleshooting

### Connection Issues

If the integration fails to connect:
1. Verify your Koplista instance URL is correct and accessible
2. Check that your API key is valid
3. Ensure your Koplista instance has API key support enabled
4. Check Home Assistant logs for detailed error messages

### Voice Commands Not Working

1. Ensure the Conversation integration is enabled in Home Assistant
2. Configure your voice assistant (Google Home, Alexa, etc.) with Home Assistant
3. Check that the intent handlers are registered in the Home Assistant logs

### Items Not Syncing

The integration polls for updates every 30 seconds. If items aren't syncing:
1. Check your network connection
2. Verify the API key hasn't expired
3. Check Home Assistant logs for API errors

## Development

### API Endpoints

The integration uses the following Koplista API endpoints:
- `GET /api/external/lists` - Fetch all lists
- `GET /api/external/lists/{id}/items` - Fetch items in a list
- `POST /api/external/add-item` - Add an item
- `DELETE /api/external/items/{id}` - Remove an item
- `PUT /api/external/items/{id}/bought` - Mark item as bought/unbought

All requests require the `X-API-Key` header.

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
