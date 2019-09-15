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
    HVAC_MODE_OFF
)

import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from typing import Any, Dict, List, Optional

SUPPORT_FLAGS = SUPPORT_TARGET_TEMPERATURE
SUPPORT_MODES = [HVAC_MODE_HEAT, HVAC_MODE_OFF]

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


class Heatlink:
    def __init__(self, data, hw):
        self._hw = hw
        self._data = data

    def update(self) -> None:
        """
        Heatlink data:
            pump: on|off        # heating pump
            heating: on|off     # burner on/off
            dhw: on|off         # hot tap water pump
            rte: float          # read/measured temperature
            rsp: float          # set temperature on thermostat
            tte: float          # set temperature on heatlink
            ttm: float|null     # timer
            wp: float           # water pressure
            wte: float          # water temperature
            ofc: int            # error code (0 = OK)
            odc: int            # diagnostic code (0 = OK)
        """
        _LOGGER.debug("update called")
        heatlink = self._hw.get_heatlink()

        if heatlink != "error":
            self._data = heatlink
        else:
            _LOGGER.exception("Update failed")

    def set_temperature(self, temperature):
        self._hw.heatlink_set_temperature(temperature)

    @property
    def info(self):
        return self._data


class Thermostat(ClimateDevice):
    def __init__(self, name, data, hw):
        self._hl = Heatlink(data, hw)
        self._name = name

        self._current_target = None
        self._current_temp = None
        self._hvac_mode = None

        self.set()

    def update(self) -> None:
        self._hl.update()
        self.set()

    def set(self):
        self._current_temp = round(self._hl.info['rte'], 1)
        self._current_target = round(self._hl.info['tte'], 1)

        if self._hl.info['heating'] == 'on':
            self._hvac_mode = HVAC_MODE_HEAT
        else:
            self._hvac_mode = HVAC_MODE_OFF

    def set_temperature(self, **kwargs) -> None:
        target_temp = kwargs.get(ATTR_TEMPERATURE)
        if target_temp is not None:
            self._hl.set_temperature(target_temp)
            self._current_target = target_temp

    def set_hvac_mode(self, hvac_mode: str) -> None:
        self._hvac_mode = hvac_mode

    @property
    def should_poll(self) -> bool:
        return True

    @property
    def supported_features(self) -> int:
        return SUPPORT_FLAGS

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
        return self._hvac_mode

    @property
    def hvac_modes(self) -> List[str]:
        return SUPPORT_MODES
