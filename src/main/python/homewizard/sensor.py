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
    POWER_WATT,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_BATTERY,
    CONF_HOST,
    CONF_PASSWORD
)
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.components.binary_sensor import BinarySensorDevice

import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from typing import Optional
from . import (
    Energylink,
    Heatlink
)

_LOGGER = logging.getLogger(__name__)
HUMIDITY_UNIT = '%'
BATTERY_UNIT = '%'
GAS_UNIT = 'm³'
DEVICE_CLASS_SMOKE = "smoke"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    from . import HomeWizard

    hw = HomeWizard(config.get(CONF_HOST), config.get(CONF_PASSWORD))

    thermometers = hw.get_thermometers()
    heatlink = hw.get_heatlink()
    energylink = hw.get_energylink()
    smoke = hw.get_smoke_sensor()

    add_entities(TemperatureSensor(data, hw) for data in thermometers)
    add_entities(HygroSensor(data, hw) for data in thermometers)
    add_entities(BatterySensor(data, hw) for data in thermometers)

    add_entities([
        WaterTemperatureSensor("CV temperatuur", heatlink, hw),
        WaterPressureSensor("CV druk", heatlink, hw),
        PowerConsumptionSensor("Elektra", energylink, hw),
        GasConsumptionSensor("Gas", energylink, hw),
        SmokeSensor("Rook", smoke, hw)
    ])


class ClimateSensor(Entity):
    def __init__(self, data, hw):
        self._hw = hw
        self._data = data
        self._name = data['name']

    @abstractmethod
    def update(self):
        self._hw.update()
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


class PowerConsumptionSensor(Entity):
    def __init__(self, name, data, hw):
        self._el = Energylink(data, hw)
        self._name = name
        self._data = data
        self._state = None
        self.set()

    def update(self):
        self._el.update()
        self.set()

    def set(self):
        self._state = round(self._el.info['aggregate']['po'], 1)

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def state(self) -> str:
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        return POWER_WATT

    @property
    def device_class(self) -> Optional[str]:
        return DEVICE_CLASS_POWER


class GasConsumptionSensor(Entity):
    def __init__(self, name, data, hw):
        self._el = Energylink(data, hw)
        self._name = name
        self._data = data
        self._state = None
        self.set()

    def update(self):
        self._el.update()
        self.set()

    def set(self):
        self._state = round(self._el.info['gas']['lastHour'], 2)

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def state(self) -> str:
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        return GAS_UNIT

    @property
    def device_class(self) -> Optional[str]:
        return DEVICE_CLASS_POWER


class SmokeSensor(BinarySensorDevice):
    def __init__(self, name, data, hw):
        self._name = name
        self._data = data
        self._hw = hw
        self._state = None
        self.set()

    def update(self):
        self._hw.update()
        self.set()

    def set(self):
        smoke = self._hw.get_smoke_sensor()
        self._state = False
        if smoke is not None:
            if smoke['status'] is not None:
                self._state = True

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def is_on(self) -> bool:
        return self._state

    @property
    def device_class(self) -> Optional[str]:
        return DEVICE_CLASS_SMOKE

class BatterySensor(Entity):
    def __init__(self, data, hw):
        self._name = data['name']
        self._data = data
        self._hw = hw
        self._state = None
        self.set()

    def update(self):
        self._hw.update()
        self.set()

    def set(self):
        meters = self._hw.get_thermometers()
        for m in meters:
            if m['id'] == self._data['id']:
                if m['lowBattery'] == 'no':
                    self._state = 100
                else:
                    self._state = 0

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def state(self) -> str:
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        return BATTERY_UNIT

    @property
    def device_class(self) -> Optional[str]:
        return DEVICE_CLASS_BATTERY
