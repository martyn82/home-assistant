"""HomeWizard sensor platform"""

from typing import Optional

from homeassistant.const import (
    PRESSURE_BAR,
    TEMP_CELSIUS,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_TEMPERATURE
)
from homeassistant.helpers.entity import Entity
from homeassistant.components.binary_sensor import BinarySensorDevice

from .const import DOMAIN, SRV_GATEWAY, DEFAULT_HEATLINK_NAME
from .gateway import Gateway
from .heatlink import Heatlink
from .thermo_hygro import ThermoHygrometer

HUMIDITY_UNIT = "%"


def setup_platform(hass, config, add_entities, discovery_info=None):
    if discovery_info is None:
        return

    entities = []
    gw: Gateway = hass.data[DOMAIN][SRV_GATEWAY]

    for t in gw.thermometers:
        meter = ThermoHygrometer(t, gw)
        entities.append(Thermometer(meter))
        entities.append(Hygrometer(meter))
        entities.append(BatteryIndicator(meter))

    for h in gw.heatlinks:
        heatlink = Heatlink(h, gw)
        entities.append(WaterTemperature(f"{DEFAULT_HEATLINK_NAME}{heatlink.identifier}", heatlink))
        entities.append(WaterPressure(f"{DEFAULT_HEATLINK_NAME}{heatlink.identifier}", heatlink))

    add_entities(entities)


class Thermometer(Entity):
    def __init__(self, meter: ThermoHygrometer):
        self._meter = meter
        self._state = None
        self.set()

    def update(self):
        self._meter.update()
        self.set()

    def set(self):
        self._state = self._meter.temperature

    @property
    def name(self):
        return self._meter.name + "_temp"

    @property
    def state(self) -> str:
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        return TEMP_CELSIUS

    @property
    def device_class(self) -> Optional[str]:
        return DEVICE_CLASS_TEMPERATURE


class Hygrometer(Entity):
    def __init__(self, meter: ThermoHygrometer):
        self._meter = meter
        self._state = None
        self.set()

    def update(self):
        self._meter.update()
        self.set()

    def set(self):
        self._state = self._meter.humidity

    @property
    def name(self):
        return self._meter.name + "_hum"

    @property
    def state(self) -> str:
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        return HUMIDITY_UNIT

    @property
    def device_class(self) -> Optional[str]:
        return DEVICE_CLASS_HUMIDITY


class BatteryIndicator(BinarySensorDevice):
    def __init__(self, meter: ThermoHygrometer):
        self._meter = meter

    def update(self):
        self._meter.update()

    @property
    def name(self):
        return self._meter.name + "_bat"

    @property
    def state(self):
        return self._meter.battery_is_low

    @property
    def device_class(self):
        return DEVICE_CLASS_BATTERY


class WaterTemperature(Entity):
    def __init__(self, name, heatlink: Heatlink):
        self._heatlink = heatlink
        self._name = name
        self._state = None
        self.set()

    def update(self):
        self._heatlink.update()
        self.set()

    def set(self):
        self._state = round(self._heatlink.water_temperature, 1)

    @property
    def name(self):
        return self._name + "_temp"

    @property
    def state(self) -> str:
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        return TEMP_CELSIUS

    @property
    def device_class(self) -> Optional[str]:
        return DEVICE_CLASS_TEMPERATURE


class WaterPressure(Entity):
    def __init__(self, name, heatlink: Heatlink):
        self._heatlink = heatlink
        self._name = name
        self._state = None
        self.set()

    def update(self):
        self._heatlink.update()
        self.set()

    def set(self):
        self._state = round(self._heatlink.water_pressure, 1)

    @property
    def name(self):
        return self._name + "_pres"

    @property
    def state(self) -> str:
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        return PRESSURE_BAR

    @property
    def device_class(self) -> Optional[str]:
        return DEVICE_CLASS_PRESSURE
