"""Constants for the HomeWizard component"""

import logging

LOGGER = logging.getLogger('homeassistant.components.homewizard')
DOMAIN = "homewizard"

SRV_GATEWAY = "gateway"

CONF_TIMEOUT = "timeout"

DEFAULT_ENERGYLINK_NAME = "Energylink"
DEFAULT_HEATLINK_NAME = "Heatlink"

PRESET_HOME = 0
PRESET_AWAY = 1
PRESET_SLEEP = 2
PRESET_HOLIDAY = 3

PRESET_NAME_HOME = "home"
PRESET_NAME_AWAY = "away"
PRESET_NAME_SLEEP = "sleep"
PRESET_NAME_HOLIDAY = "holiday"

PRESETS = [
    {"id": PRESET_HOME, "name": PRESET_NAME_HOME},
    {"id": PRESET_AWAY, "name": PRESET_NAME_AWAY},
    {"id": PRESET_SLEEP, "name": PRESET_NAME_SLEEP},
    {"id": PRESET_HOLIDAY, "name": PRESET_NAME_HOLIDAY}
]
