"""HomeWizard sensor platform"""

from typing import Optional

from homeassistant.const import (
    POWER_WATT,
    PRESSURE_BAR,
    TEMP_CELSIUS,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_TEMPERATURE,
    STATE_ON,
    STATE_OFF
)
from homeassistant.helpers.entity import Entity
from homeassistant.components.binary_sensor import BinarySensorDevice, DEVICE_CLASS_PRESENCE, DEVICE_CLASS_SMOKE

from .const import (
    DOMAIN,
    SRV_GATEWAY,
    DEFAULT_ENERGYLINK_NAME,
    DEFAULT_HEATLINK_NAME,
    PRESET_HOME
)
from .energylink import Energylink
from .gateway import Gateway
from .heatlink import Heatlink
from .thermo_hygro import ThermoHygrometer

GAS_CUBIC = "m³"
HUMIDITY_PERCENT = "%"


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

    for e in gw.energylinks:
        energylink = Energylink(e, gw)
        entities.append(Powermeter(f"{DEFAULT_ENERGYLINK_NAME}{energylink.identifier}", energylink))
        entities.append(Gasmeter(f"{DEFAULT_ENERGYLINK_NAME}{energylink.identifier}", energylink))

    for s in gw.smoke_detectors:
        entities.append(SmokeDetector(s, gw))

    for p in gw.presets:
        entities.append(Preset(p, gw))

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
        return HUMIDITY_PERCENT

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
        return STATE_ON if self._meter.battery_is_low else STATE_OFF

    @property
    def is_on(self):
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


class Powermeter(Entity):
    def __init__(self, name, energylink: Energylink):
        self._energylink = energylink
        self._name = name
        self._state = None
        self.set()

    def update(self):
        self._energylink.update()
        self.set()

    def set(self):
        self._state = round(self._energylink.power_consumption, 1)

    @property
    def name(self):
        return self._name + "_watt"

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return POWER_WATT

    @property
    def device_class(self) -> Optional[str]:
        return DEVICE_CLASS_POWER


class Gasmeter(Entity):
    def __init__(self, name, energylink: Energylink):
        self._energylink = energylink
        self._name = name
        self._state = None
        self.set()

    def update(self):
        self._energylink.update()
        self.set()

    def set(self):
        self._state = round(self._energylink.hour_gas_consumption, 2)

    @property
    def name(self):
        return self._name + "_gas"

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return GAS_CUBIC

    @property
    def device_class(self) -> Optional[str]:
        return DEVICE_CLASS_POWER


class SmokeDetector(BinarySensorDevice):
    def __init__(self, data, gw: Gateway):
        self._gw = gw
        self._id = data['id']
        self._data = data
        self._name = None
        self._state = None
        self.set()

    def update(self):
        self._gw.update()
        self.set()

    def set(self):
        self._data = self._gw.smoke_detector(self._id)
        self._name = self._data['name']
        self._state = True if self._data['status'] is not None else False

    @property
    def state(self):
        return STATE_ON if self._state else STATE_OFF

    @property
    def is_on(self) -> bool:
        return self._state

    @property
    def name(self):
        return self._name

    @property
    def device_class(self):
        return DEVICE_CLASS_SMOKE


class Preset(BinarySensorDevice):
    def __init__(self, data, gw: Gateway):
        self._gw = gw
        self._id = data['id']
        self._name = data['name']
        self._state = None
        self._class = DEVICE_CLASS_PRESENCE if self._id == PRESET_HOME else None
        self.set()

    def update(self):
        self._gw.update()
        self.set()

    def set(self):
        self._state = STATE_ON if self._gw.active_preset == self._id else STATE_OFF

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def is_on(self):
        return self._state == STATE_ON

    @property
    def device_class(self):
        return self._class
