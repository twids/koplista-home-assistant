## Fix: Reconfigure Flow TypeError

**Problem:** The reconfigure flow was causing a `TypeError: expected str, got list` error when trying to reload the integration after updating configuration.

**Root Cause:** The old code attempted to manually call `async_reload()` during the config flow, which can cause race conditions and type errors. The incomplete fix removed the reload call but left the integration running with old config until manual reload.

**Solution:** Use Home Assistant's built-in `async_update_reload_and_abort()` method which safely:
1. Updates the config entry with new data
2. Schedules a proper integration reload
3. Aborts the flow with success

**Changes Made:**
- [config_flow.py](../custom_components/koplista/config_flow.py): Updated `async_step_reconfigure()` to use `async_update_reload_and_abort()` instead of manually updating and aborting

**Files Modified:**
- custom_components/koplista/config_flow.py

**Deployment Instructions:**

1. **Copy the updated integration to Home Assistant:**
   ```powershell
   # From your development directory
   cd c:\dev\koplista-home-assistant
   
   # Copy to Home Assistant (adjust path for your HA installation)
   # If running HA in Docker/Container:
   docker cp custom_components/koplista homeassistant:/config/custom_components/
   
   # If running HA OS with SSH/network access:
   # scp -r custom_components/koplista root@homeassistant.local:/config/custom_components/
   ```

2. **Restart Home Assistant:**
   - Go to Settings → System → Restart
   - Or use Developer Tools → YAML → Restart

3. **Test the reconfigure flow:**
   - Go to Settings → Devices & Services
   - Find Koplista integration
   - Click the three dots → Reconfigure
   - Update the URL or API key
   - Verify no errors occur and integration reloads automatically

**Alternative Deployment (HACS or manual):**
1. Commit and push these changes to your repository
2. If using HACS: Update the integration in HACS UI
3. Restart Home Assistant
4. Test reconfiguration

