"""Shared NIU entity definitions."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import NiuDataUpdateCoordinator


class NiuCoordinatorEntity(CoordinatorEntity[NiuDataUpdateCoordinator]):
    """Base entity attached to a scooter and its shared coordinator."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: NiuDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "Niu E-scooter")},
            translation_key="scooter",
            manufacturer="NIU",
            model="E-scooter",
        )
