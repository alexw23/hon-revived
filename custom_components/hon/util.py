import logging
from contextlib import suppress
from typing import Any

from .typedefs import HonEntityDescription, HonOptionEntityDescription, T

_LOGGER = logging.getLogger(__name__)

CONNECTION_KEY = "attributes.lastConnEvent.category"


def seed_connection(hon: Any) -> None:
    """Seed each appliance's live connection flag from the loaded REST data.

    pyhon initialises the flag before attributes are loaded, so it always starts
    as connected. MQTT presence events keep it current from then on.
    """
    for appliance in hon.appliances:
        category = appliance.get(CONNECTION_KEY)
        if category:
            appliance.connection = category != "DISCONNECTED"


def connection_category(device: Any) -> str:
    """Live connection state; lastConnEvent only reflects the last REST load."""
    return "CONNECTED" if device.connection else "DISCONNECTED"


def unique_entities(
    base_entities: tuple[T, ...],
    new_entities: tuple[T, ...],
) -> tuple[T, ...]:
    result = list(base_entities)
    existing_entities = [entity.key for entity in base_entities]
    entity: HonEntityDescription
    for entity in new_entities:
        if entity.key not in existing_entities:
            result.append(entity)
    return tuple(result)


def get_readable(
    description: HonOptionEntityDescription, value: float | str
) -> float | str:
    if description.option_list is not None:
        with suppress(ValueError):
            return description.option_list.get(int(value), value)
    return value
