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
