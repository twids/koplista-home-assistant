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

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration** (bottom right)
3. Search for **"Koplista"**
4. Click on **Koplista** in the results
5. Enter your configuration:
   - **Koplista URL**: Your instance URL (e.g., `https://koplista.example.com`)
   - **API Key**: Your API key from Koplista
6. Click **Submit**

The integration will:
- Validate your connection
- Create Todo entities for each of your shopping lists
- Register voice command intents
- Set up services for automation

## Verification

After successful configuration:

1. Check **Settings** → **Devices & Services** → **Koplista**
2. You should see:
   - Integration status: Connected
   - Devices/Entities created for your shopping lists
3. Go to **Settings** → **Entities**
4. Filter by **"koplista"**
5. You should see `todo.koplista_*` entities for each list

## Setting Up Voice Commands

### Google Home / Google Assistant

1. Ensure your Home Assistant is connected to Google Assistant (via Nabu Casa or manual setup)
2. Say: **"Hey Google, sync my devices"**
3. Test the integration: **"Hey Google, lägg till mjölk på köplistan"** (Swedish) or **"Hey Google, add milk to the shopping list"** (English)

### Amazon Alexa

1. Ensure your Home Assistant is connected to Alexa
2. Set up routines or use the shopping list skill
3. Test with Alexa-compatible phrases

### Home Assistant Voice Assistant

1. Enable **Assist** in Home Assistant
2. Configure your preferred wake word
3. Use the built-in sentence patterns:
   - **Swedish**: "lägg till {item} på köplistan"
   - **English**: "add {item} to the shopping list"

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

- Verify the Conversation integration is enabled
- Check that your voice assistant is properly connected to Home Assistant
- Review Home Assistant logs for intent registration messages
- Ensure your shopping lists exist in Koplista

### Entities Not Showing

- Restart Home Assistant after configuration
- Check that your Koplista instance has shopping lists created
- Review the integration logs for errors
- Try removing and re-adding the integration

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
