"""
configuration.yml

climate:
    - platform: homewizard
      name: {DEVICE_NAME (optional)}
      host: {HOST_ADDRESS}
      password: {PASSWORD}
"""

from homeassistant.const import (
    CONF_NAME,
    CONF_HOST,
    CONF_PASSWORD,
    ATTR_TEMPERATURE,
    TEMP_CELSIUS
)
from homeassistant.components.climate import (
    ClimateDevice,
    PLATFORM_SCHEMA
)
from homeassistant.components.climate.const import (
    SUPPORT_TARGET_TEMPERATURE,
    HVAC_MODE_HEAT,
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_IDLE
)

import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from typing import Any, Dict, List, Optional
from . import Heatlink

DEFAULT_NAME = "Thermostaat"
DEFAULT_MIN_TEMP = 7.0
DEFAULT_MAX_TEMP = 30.0
TEMPERATURE_PRECISION = 0.5

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    from . import HomeWizard

    hw = HomeWizard(config.get(CONF_HOST), config.get(CONF_PASSWORD))
    heatlink = hw.get_heatlink()

    name = config.get(CONF_NAME)

    add_entities([
        Thermostat(name, heatlink, hw)
    ])


class Thermostat(ClimateDevice):
    def __init__(self, name, data, hw):
        self._hl = Heatlink(data, hw)
        self._name = name

        self._current_target = None
        self._current_temp = None
        self._hvac_action = None

        self.set()

    def update(self) -> None:
        self._hl.update()
        self.set()

    def set(self):
        self._current_temp = round(self._hl.info['rte'], 1)
        self._current_target = round(self._hl.info['tte'], 1)

        if self._hl.info['pump'] == 'on':
            self._hvac_action = CURRENT_HVAC_HEAT
        else:
            self._hvac_action = CURRENT_HVAC_IDLE

    def set_temperature(self, **kwargs) -> None:
        target_temp = kwargs.get(ATTR_TEMPERATURE)
        if target_temp is not None:
            self._hl.set_temperature(target_temp)
            self._current_target = target_temp

    def set_hvac_mode(self, hvac_mode: str) -> None:
        return None

    @property
    def should_poll(self) -> bool:
        return True

    @property
    def supported_features(self) -> int:
        return SUPPORT_TARGET_TEMPERATURE

    @property
    def name(self) -> str:
        return self._name

    @property
    def device_state_attributes(self) -> Dict[str, Any]:
        return self._hl.info

    @property
    def temperature_unit(self) -> str:
        return TEMP_CELSIUS

    @property
    def current_temperature(self) -> Optional[float]:
        return self._current_temp

    @property
    def target_temperature(self) -> Optional[float]:
        return self._current_target

    @property
    def target_temperature_step(self) -> Optional[float]:
        return TEMPERATURE_PRECISION

    @property
    def min_temp(self) -> float:
        return DEFAULT_MIN_TEMP

    @property
    def max_temp(self) -> float:
        return DEFAULT_MAX_TEMP

    @property
    def hvac_mode(self) -> str:
        return HVAC_MODE_HEAT

    @property
    def hvac_modes(self) -> List[str]:
        return [HVAC_MODE_HEAT]

    @property
    def hvac_action(self) -> Optional[str]:
        return self._hvac_action
