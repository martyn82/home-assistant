"""
configuration.yml

sensor:
    - platform: homewizard
      host: {HOST_ADDRESS}
      password: {PASSWORD}
"""

from homeassistant.const import (
    TEMP_CELSIUS,
    DEVICE_CLASS_TEMPERATURE,
    CONF_HOST,
    CONF_PASSWORD
)
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA

import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from typing import Optional

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    from . import HomeWizard

    hw = HomeWizard(config.get(CONF_HOST), config.get(CONF_PASSWORD))
    thermometers = hw.get_thermometers()

    add_entities(TemperatureSensor(data, hw) for data in thermometers)


class TemperatureSensor(Entity):
    def __init__(self, data, hw):
        self._hw = hw
        self._data = data
        self._name = data['name']
        self._state = data['te']

    def update(self) -> None:
        """
        Thermometer data:
             name: str              # Name of the sensor
             model: int             # Model indication
             lowBattery: yes|no     # Battery indicator
             version: float         # Version of the device
             te: float              # Measured temperature
             hu: float              # Measured humidity
             te+: float             # Max. measured temp
             te-: float             # Min. measured temp
             te+t: str              # Time maximum temp was measured
             te-t: str              # Time minimum temp was measured
             hu+: float             # Max. measured humidity
             hu-: float             # Min. measured humidity
             hu+t: str              # Time maximum humidity was measured
             hu-t: str              # Time minimum humidity was measured
             outside: yes|no        # Whether the sensor is put outside (uncertain)
        """
        for m in self._hw.get_thermometers():
            if self._data['id'] == m['id']:
                self._data = m
                break

        self._name = self._data['name']
        self._state = self._data['te']

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def state(self) -> str:
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        return TEMP_CELSIUS

    @property
    def device_class(self) -> Optional[str]:
        return DEVICE_CLASS_TEMPERATURE
