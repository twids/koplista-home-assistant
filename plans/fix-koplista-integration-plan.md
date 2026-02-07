## Plan: Fix Koplista Integration Voice Commands

Fix the Koplista Home Assistant integration to properly handle voice commands and resolve intent conflicts with the built-in shopping list. The integration should work correctly with Home Assistant's voice assistant (and via Google Assistant with Nabu Casa), properly register intents, and accurately represent its limited API capabilities.

**Phases: 4**

### Phase 1: Fix Intent Registration and Sentence Patterns
**Objective:** Make Koplista intents take priority over built-in shopping list intents by using more specific sentence patterns and ensuring proper registration.

**Files/Functions to Modify/Create:**
- [custom_components/koplista/sentences/sv.yaml](custom_components/koplista/sentences/sv.yaml)
- [custom_components/koplista/sentences/en.yaml](custom_components/koplista/sentences/en.yaml)
- [custom_components/koplista/intent.py](custom_components/koplista/intent.py) - `AddItemIntentHandler` and `async_setup_intents`

**Tests to Write:**
- Test that KoplistaAddItem intent handler is properly registered
- Test that intent handler correctly extracts item name from slots
- Test that intent handler calls client.add_item with correct parameters
- Test that intent returns success response with Swedish text when API succeeds
- Test that intent returns error response when API fails

**Steps:**
1. Write tests for intent handler registration and functionality
2. Run tests to confirm they fail (no changes yet)
3. Update sentence patterns in sv.yaml to use "koplista" explicitly to differentiate from built-in shopping list
4. Update sentence patterns in en.yaml similarly
5. Update intent handler to provide Swedish responses when appropriate
6. Run tests to verify they pass
7. Manually test by saying "Lägg till mjölk på koplista" in HA voice assistant

---

### Phase 2: Clean Up API Client and Remove Unimplemented Features
**Objective:** Remove references to unimplemented API methods (mark_bought, remove_item) and ensure api.py accurately represents available functionality.

**Files/Functions to Modify/Create:**
- [custom_components/koplista/api.py](custom_components/koplista/api.py) - `KoplistaApiClient.test_connection`
- [custom_components/koplista/const.py](custom_components/koplista/const.py) - Remove redundant CONF_API_KEY constant

**Tests to Write:**
- Test that add_item makes correct POST request with proper headers and body
- Test that add_item handles 401 auth errors correctly
- Test that add_item handles connection timeouts
- Test that test_connection returns appropriate values

**Steps:**
1. Write tests for API client add_item method and error handling
2. Run tests to see current failures
3. Fix test_connection method to actually test the connection (currently just returns True)
4. Remove redundant CONF_API_KEY from const.py (use homeassistant.const version)
5. Add docstring comments noting API limitations
6. Run tests to verify all pass
7. Run linter/formatter on api.py

---

### Phase 3: Fix or Remove Todo Platform
**Objective:** Either properly implement a limited todo platform (add-only) OR remove it entirely since it references non-existent API methods and isn't loaded anyway.

**Files/Functions to Modify/Create:**
- [custom_components/koplista/__init__.py](custom_components/koplista/__init__.py) - `async_setup_entry` and `async_unload_entry`  
- [custom_components/koplista/todo.py](custom_components/koplista/todo.py) - `KoplistaTodoList` class or remove file entirely
- [custom_components/koplista/coordinator.py](custom_components/koplista/coordinator.py) - Update or remove depending on decision

**Option A - Remove Todo Platform (Simpler):**
- Test that services still work without todo platform
- Remove todo.py file
- Remove coordinator.py file
- Remove coordinator references from __init__.py if any

**Option B - Implement Limited Todo Platform (More Features):**
- Test todo entity creation and registration
- Test that CREATE_TODO_ITEM feature works
- Test that todo_items property returns appropriate list
- Modify __init__.py to load todo platform
- Modify todo.py to only declare CREATE_TODO_ITEM feature
- Modify todo.py todo_items to return cached/empty list
- Remove update and delete methods from todo.py
- Update coordinator to maintain local cache of added items

**Tests to Write (Option A):**
- Test that integration loads without todo platform
- Test that services remain functional
- Test that intent handlers work independently

**Tests to Write (Option B):**
- Test todo entity is created when integration loads
- Test async_create_todo_item calls API correctly
- Test todo_items property returns list
- Test that unsupported features properly removed

**Steps (deciding on Option A for simplicity):**
1. Write tests to verify integration works without todo platform
2. Run tests to establish baseline
3. Remove todo.py completely
4. Remove coordinator.py completely  
5. Clean up any coordinator imports from __init__.py
6. Update manifest.json if needed
7. Run all tests to verify everything still works
8. Manually test integration loads and voice commands work

---

### Phase 4: Update Documentation
**Objective:** Update README.md and code comments to accurately reflect current capabilities, explain the Google Assistant limitation, and document the Nabu Casa workaround.

**Files/Functions to Modify/Create:**
- [README.md](README.md) - Update features section, add Google Assistant clarification, add Nabu Casa section
- [INSTALL.md](INSTALL.md) if it exists  
- Code docstrings in modified files

**Tests to Write:**
- Test that all documented code examples are valid
- Test that documented service calls work

**Steps:**
1. Write test validating service call examples from docs
2. Run test to see if current docs are accurate
3. Update README.md to clarify Google Assistant limitations
4. Add section explaining Nabu Casa integration benefits
5. Update sentence examples to use "koplista" explicitly
6. Add troubleshooting section for intent conflicts
7. Update feature list to remove unimplemented features
8. Add clear API limitations section
9. Update code docstrings with accurate information
10. Run documentation validation tests
11. Perform manual review of all documentation

---

**Open Questions:**
1. Should we implement Option A (remove todo platform) or Option B (implement limited todo with caching)? **Recommendation: Option A** - simpler, matches actual API capabilities
2. Do you want Swedish responses in the intent handler, or is English acceptable? **Recommendation: Use Swedish** for better UX
3. Should sentence patterns include "koplista" explicitly, or use different phrases? **Recommendation: Include "koplista"** to avoid conflicts
4. Do you want to keep coordinator.py for potential future use when API adds fetch endpoints? **Recommendation: Remove it** - can add back when needed
