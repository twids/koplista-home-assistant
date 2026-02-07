# Koplista Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/twids/koplista-home-assistant.svg)](https://github.com/twids/koplista-home-assistant/releases)
[![License](https://img.shields.io/github/license/twids/koplista-home-assistant.svg)](LICENSE)

A Home Assistant integration for [Koplista](https://github.com/twids/k-plista), a grocery list application. This integration allows you to add items to your Koplista shopping lists using voice commands or Home Assistant services.

## Features

- 🗣️ **Voice Commands**: Add items using natural language - "Lägg till mjölk på koplista" (Swedish) or "Add milk to koplista" (English)
- 🎛️ **Services**: Use `koplista.add_item` service in automations and scripts
- 🌐 **Multi-language**: Bilingual voice responses (Swedish/English)
- 🔐 **Secure**: API key authentication
- 🏠 **Works with**: Home Assistant Assist, Nabu Casa/Google Assistant, ESP32 voice satellites

## Current Limitations

**API Limitations**: The Koplista API currently only supports adding items. Features like viewing lists, removing items, and marking items as complete require additional API endpoints that are not yet implemented. This integration will be expanded as the API grows.

**No Visual UI**: This integration does not create todo list entities or provide a visual shopping list interface. It focuses on voice control and programmatic access via services.

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

### Step 1: Add Integration via UI

1. In Home Assistant, go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Koplista"
4. Enter your Koplista configuration:
   - **URL**: Your Koplista instance URL (must start with `http://` or `https://`, e.g., `https://koplista.example.com`)
   - **API Key**: Your personal API key from Koplista
5. Click **Submit**

The integration will validate your connection.

### Step 2: Enable Voice Commands ⚠️ REQUIRED

**Important:** Custom integrations cannot auto-register voice commands. You must add the following to your Home Assistant `configuration.yaml` file:

```yaml
conversation:
  intents:
    KoplistaAddItem:
      - "lägg till {item} på koplista"
      - "lägg till {item} till koplista"
      - "köp {item}"
      - "vi behöver {item}"
      - "köp in {item}"
```

After adding this configuration:
1. Restart Home Assistant
2. Voice commands will now work!

See [configuration.yaml.example](configuration.yaml.example) for the complete configuration example.

## Configuration for Voice Assistants

### Home Assistant's Built-in Voice (Assist)

After completing the configuration steps above, voice commands work immediately with Home Assistant's Assist:

1. Click the microphone button in Home Assistant
2. Say: "Lägg till mjölk på koplista"
3. Done!

Works with:
- HA web interface microphone
- HA mobile app voice
- ESP32-based voice satellites (Atom Echo, S3-Box, etc.)
- Wyoming protocol satellites

### Google Assistant via Nabu Casa Cloud ⭐ Recommended

**Note:** The standard Google Assistant integration does NOT support custom conversation intents. You need **Nabu Casa Cloud** for this to work.

**Why Nabu Casa?** Manual Google Assistant setup only exposes entities (lights, switches), not conversation commands. Nabu Casa's version includes conversation routing.

**Setup:**

1. **Subscribe** to [Home Assistant Cloud / Nabu Casa](https://www.nabucasa.com/) ($6.50/month)

2. **Enable Google Assistant** in Nabu Casa settings:
   - **Settings** → **Home Assistant Cloud** → **Google Assistant**
   - Complete the OAuth flow

3. **Your voice commands now work with Google Home!**
   - "Hey Google, lägg till mjölk på koplista"
   - The conversation goes: Google → Nabu Casa → HA Conversation → Your Intent

**Optional:** To avoid conflicts with HA's built-in shopping list, you can disable it:
```yaml
conversation:
  intents:
    HassShoppingListAddItem:
      enabled: false
```

### Alternative: Google Assistant Routines (Without Nabu Casa)

If you have a manual Google Assistant setup and don't want Nabu Casa, you can use webhooks:

1. Create automation with webhook trigger
2. Create Google Routine that calls the webhook
3. See [this guide](https://www.home-assistant.io/docs/automation/trigger/#webhook-trigger) for details

**Trade-off:** Less flexible than natural language through Nabu Casa.

### Other Voice Assistants

The integration works with any voice assistant using HA's conversation component:

## Usage

### Voice Commands

After adding the configuration above, you can use voice commands like:

**Swedish:**
- "Lägg till mjölk på koplista"
- "Köp bröd"
- "Vi behöver ägg"

**English:**
- "Add milk to koplista"
- "Buy bread"
- "We need eggs"

**Note:** The phrase "på koplista" is used instead of "på köplistan" to avoid conflicts with Home Assistant's built-in shopping list.

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

### Voice Commands Not Working

**Most common issue:** You haven't added the voice command configuration to `configuration.yaml`.

1. Make sure you've added the conversation intent configuration (see [Step 2 above](#step-2-enable-voice-commands-️-required))
2. Restart Home Assistant after adding the configuration
3. Test with: "Lägg till mjölk på koplista" (use "koplista", not "köplistan")
4. Check Home Assistant logs for any errors from the Koplista integration

### Connection Issues

If the integration fails to connect:
1. Verify your Koplista instance URL is correct and accessible (must start with `http://` or `https://`)
2. Check that your API key is valid
3. Ensure your Koplista instance has API key support enabled
4. Check Home Assistant logs for detailed error messages

### Google Assistant Says "I don't understand"

If using Google Home without Nabu Casa:
- Google Assistant's standard integration does NOT support conversation routing
- You need Nabu Casa Cloud subscription for voice commands to work with Google Home
- Alternative: Use Home Assistant's mobile app or voice satellites (ESP32-based devices)

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
