# Installation Guide

## Prerequisites

Before installing the Koplista Home Assistant integration, ensure you have:

1. **Home Assistant 2024.1.0 or newer** installed and running
2. **HACS (Home Assistant Community Store)** installed
3. A **Koplista instance** with API support running
4. An **API key** from your Koplista instance

## Getting Your API Key

1. Log in to your Koplista instance
2. Navigate to Settings or Account
3. Find the API section
4. Generate or copy your API key
5. Keep this key secure - you'll need it during integration setup

## Installation Methods

### Method 1: HACS (Recommended)

1. Open **HACS** in your Home Assistant instance
2. Go to **Integrations**
3. Click the **three dots** (⋮) in the top right corner
4. Select **Custom repositories**
5. Add the following:
   - **Repository**: `https://github.com/twids/koplista-home-assistant`
   - **Category**: Integration
6. Click **Add**
7. Search for **"Koplista"** in HACS
8. Click **Download**
9. **Restart Home Assistant**

### Method 2: Manual Installation

1. Download the latest release from the [GitHub releases page](https://github.com/twids/koplista-home-assistant/releases)
2. Extract the archive
3. Copy the `custom_components/koplista` folder to your Home Assistant's `config/custom_components/` directory
4. Your directory structure should look like:
   ```
   config/
   └── custom_components/
       └── koplista/
           ├── __init__.py
           ├── manifest.json
           └── ... (other files)
   ```
5. **Restart Home Assistant**

## Configuration

After installation and restart:

### Step 1: Add Integration via UI

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration** (bottom right)
3. Search for **"Koplista"**
4. Click on **Koplista** in the results
5. Enter your configuration:
   - **Koplista URL**: Your instance URL (e.g., `https://koplista.example.com`)
   - **API Key**: Your API key from Koplista
6. Click **Submit**

The integration will validate your connection.

### Step 2: Enable Voice Commands ⚠️ REQUIRED

**Important:** Custom integrations cannot auto-register voice commands. You must add this to your `configuration.yaml`:

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

**Restart Home Assistant** after adding this configuration.

See [configuration.yaml.example](configuration.yaml.example) for the complete example.

## Verification

After successful configuration:

1. Check **Settings** → **Devices & Services** → **Koplista**
2. You should see:
   - Integration status: Connected
3. Go to **Developer Tools** → **Services**
4. Search for **"koplista.add_item"**
5. Verify the service is available

## Using Voice Commands

### Home Assistant's Built-in Voice (Assist)

Voice commands work immediately after completing the configuration steps:

1. Click the **microphone button** in Home Assistant
2. Say: **"Lägg till mjölk på koplista"**
3. Done!

### Google Home / Google Assistant (Requires Nabu Casa)

**Note:** Standard Google Assistant integration does NOT support conversation routing. You need Nabu Casa Cloud.

1. **Subscribe** to [Nabu Casa](https://www.nabucasa.com/) ($6.50/month)
2. **Enable Google Assistant**:
   - **Settings** → **Home Assistant Cloud** → **Google Assistant**
   - Complete OAuth flow
3. **Test**: "Hey Google, lägg till mjölk på koplista"

**Optional:** To avoid conflicts with HA's built-in shopping list:
```yaml
conversation:
  intents:
    HassShoppingListAddItem:
      enabled: false
```

### Other Voice Assistants

- **ESP32 satellites** (Atom Echo, S3-Box): Full support
- **Wyoming protocol**: Full support  
- **Alexa/Siri**: Use Home Assistant skills/shortcuts

## Troubleshooting

### Integration Not Found

- Ensure you've restarted Home Assistant after installation
- Clear your browser cache (Ctrl+F5 or Cmd+Shift+R)
- Check the logs: **Settings** → **System** → **Logs**

### Connection Failed

- Verify your Koplista URL is correct and accessible
- Check that your API key is valid and hasn't expired
- Ensure your Koplista instance has API support enabled
- Check network connectivity between Home Assistant and Koplista

### Voice Commands Not Working

**Most common issue:** You haven't added the voice configuration to `configuration.yaml`.

1. Add the conversation intents to `configuration.yaml` (see Step 2 above)
2. Restart Home Assistant  
3. Test with: "Lägg till mjölk på koplista"
4. Check logs for intent handler messages

### Google Assistant Says "I don't understand"

- Standard Google Assistant integration does NOT support conversation routing
- You need **Nabu Casa Cloud** subscription for Google Home voice commands
- Alternative: Use HA mobile app or ESP32 voice satellites

## Next Steps

- [Configure automations](https://www.home-assistant.io/docs/automation/)
- [Create custom voice commands](https://www.home-assistant.io/docs/assist/)
- [Set up notifications](https://www.home-assistant.io/integrations/notify/)
- [Join the community](https://github.com/twids/koplista-home-assistant/discussions)

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Review [existing issues](https://github.com/twids/koplista-home-assistant/issues)
3. Search the [Home Assistant Community](https://community.home-assistant.io/)
4. [Open a new issue](https://github.com/twids/koplista-home-assistant/issues/new) with:
   - Home Assistant version
   - Koplista integration version
   - Error logs
   - Steps to reproduce
