"""
configuration.yml

sensor:
    - platform: homewizard
      host: {HOST_ADDRESS}
      password: {PASSWORD}
"""

from abc import abstractmethod
from homeassistant.const import (
    TEMP_CELSIUS,
    PRESSURE_BAR,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_PRESSURE,
    CONF_HOST,
    CONF_PASSWORD
)
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA

import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from typing import Optional
from .climate import Heatlink

_LOGGER = logging.getLogger(__name__)
HUMIDITY_UNIT = '%'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    from . import HomeWizard

    hw = HomeWizard(config.get(CONF_HOST), config.get(CONF_PASSWORD))
    thermometers = hw.get_thermometers()
    heatlink = hw.get_heatlink()

    add_entities(TemperatureSensor(data, hw) for data in thermometers)
    add_entities(HygroSensor(data, hw) for data in thermometers)

    add_entities([
        WaterTemperatureSensor("CV", heatlink, hw),
        WaterPressureSensor("CV", heatlink, hw)
    ])


class ClimateSensor(Entity):
    def __init__(self, data, hw):
        self._hw = hw
        self._data = data
        self._name = data['name']

    @abstractmethod
    def update(self):
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


class TemperatureSensor(ClimateSensor):
    def __init__(self, data, hw):
        super().__init__(data, hw)
        self._state = None
        self.set()

    def update(self) -> None:
        super().update()
        self.set()

    def set(self):
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


class HygroSensor(ClimateSensor):
    def __init__(self, data, hw):
        super().__init__(data, hw)
        self._state = None
        self.set()

    def update(self):
        super().update()
        self.set()

    def set(self):
        self._state = self._data['hu']

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def state(self) -> str:
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        return HUMIDITY_UNIT

    @property
    def device_class(self) -> Optional[str]:
        return DEVICE_CLASS_HUMIDITY


class WaterTemperatureSensor(Entity):
    def __init__(self, name, data, hw):
        self._hl = Heatlink(data, hw)
        self._name = name
        self._data = data
        self._state = None
        self.set()

    def update(self):
        self._hl.update()
        self.set()

    def set(self):
        self._state = round(self._hl.info['wte'], 1)

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


class WaterPressureSensor(Entity):
    def __init__(self, name, data, hw):
        self._hl = Heatlink(data, hw)
        self._name = name
        self._data = data
        self._state = None

        self.set()

    def update(self):
        self._hl.update()
        self.set()

    def set(self):
        self._state = round(self._hl.info['wp'], 1)

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def state(self) -> str:
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        return PRESSURE_BAR

    @property
    def device_class(self) -> Optional[str]:
        return DEVICE_CLASS_PRESSURE
