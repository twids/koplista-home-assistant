"""Todo platform for Koplista."""
import logging
from typing import Any

from homeassistant.components.todo import (
    TodoItem,
    TodoItemStatus,
    TodoListEntity,
    TodoListEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import KoplistaDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Koplista todo platform."""
    coordinator: KoplistaDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        "coordinator"
    ]
    client = hass.data[DOMAIN][entry.entry_id]["client"]

    entities = []
    for list_id, list_data in coordinator.data.items():
        entities.append(KoplistaTodoList(coordinator, client, list_id))

    async_add_entities(entities)


class KoplistaTodoList(CoordinatorEntity, TodoListEntity):
    """A Koplista shopping list as a todo entity."""

    _attr_supported_features = (
        TodoListEntityFeature.CREATE_TODO_ITEM
        | TodoListEntityFeature.DELETE_TODO_ITEM
        | TodoListEntityFeature.UPDATE_TODO_ITEM
    )

    def __init__(
        self,
        coordinator: KoplistaDataUpdateCoordinator,
        client: Any,
        list_id: str,
    ) -> None:
        """Initialize the todo list."""
        super().__init__(coordinator)
        self._client = client
        self._list_id = list_id
        self._attr_unique_id = f"koplista_{list_id}"

    @property
    def name(self) -> str:
        """Return the name of the todo list."""
        list_data = self.coordinator.data.get(self._list_id, {})
        list_info = list_data.get("info", {})
        return f"Koplista {list_info.get('name', 'Shopping List')}"

    @property
    def todo_items(self) -> list[TodoItem]:
        """Return the todo items."""
        list_data = self.coordinator.data.get(self._list_id, {})
        items_data = list_data.get("items", [])
        items = []

        for item in items_data:
            status = (
                TodoItemStatus.COMPLETED
                if item.get("bought", False)
                else TodoItemStatus.NEEDS_ACTION
            )
            items.append(
                TodoItem(
                    uid=item["id"],
                    summary=item["name"],
                    status=status,
                )
            )

        return items

    async def async_create_todo_item(self, item: TodoItem) -> None:
        """Create a todo item."""
        await self._client.add_item(self._list_id, item.summary)
        await self.coordinator.async_request_refresh()

    async def async_update_todo_item(self, item: TodoItem) -> None:
        """Update a todo item."""
        bought = item.status == TodoItemStatus.COMPLETED
        await self._client.mark_bought(item.uid, bought)
        await self.coordinator.async_request_refresh()

    async def async_delete_todo_items(self, uids: list[str]) -> None:
        """Delete todo items."""
        for uid in uids:
            await self._client.remove_item(uid)
        await self.coordinator.async_request_refresh()
