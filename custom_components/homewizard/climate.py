"""HomeWizard climate platform (a.k.a HeatLink)"""

from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS
from homeassistant.components.climate import ClimateDevice
from homeassistant.components.climate.const import (
    CURRENT_HVAC_IDLE,
    CURRENT_HVAC_HEAT,
    HVAC_MODE_HEAT,
    SUPPORT_TARGET_TEMPERATURE
)
from typing import List, Optional

from .const import DOMAIN, SRV_GATEWAY, DEFAULT_HEATLINK_NAME
from .gateway import Gateway
from .heatlink import Heatlink

DEFAULT_MAX_TEMP = 30.0
DEFAULT_MIN_TEMP = 7.0
TEMPERATURE_PRECISION = 0.5


def setup_platform(hass, config, add_entities, discovery_info=None):
    if discovery_info is None:
        return

    gw: Gateway = hass.data[DOMAIN][SRV_GATEWAY]
    add_entities(HeatlinkDevice(DEFAULT_HEATLINK_NAME, Heatlink(heatlink, gw)) for heatlink in gw.heatlinks)


class HeatlinkDevice(ClimateDevice):
    def __init__(self, name, heatlink: Heatlink):
        self._name = f"{name}{heatlink.identifier}"
        self._heatlink = heatlink
        self._current_temperature = None
        self._target_temperature = None
        self._hvac_action = None
        self.set()

    def set(self):
        self._current_temperature = self._heatlink.read_temperature
        self._target_temperature = self._heatlink.target_temperature

        if self._heatlink.pump_is_on:
            self._hvac_action = CURRENT_HVAC_HEAT
        else:
            self._hvac_action = CURRENT_HVAC_IDLE

    def update(self):
        self._heatlink.update()
        self.set()

    def set_temperature(self, **kwargs) -> None:
        target = kwargs.get(ATTR_TEMPERATURE)
        if target is not None:
            self._heatlink.set_temperature(target)
            self._current_temperature = target

    def set_hvac_mode(self, hvac_mode: str) -> None:
        return None  # not supported

    @property
    def should_poll(self) -> bool:
        return True

    @property
    def supported_features(self) -> int:
        return SUPPORT_TARGET_TEMPERATURE

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def device_state_attributes(self):
        return None

    @property
    def temperature_unit(self) -> str:
        return TEMP_CELSIUS

    @property
    def current_temperature(self) -> Optional[float]:
        return self._current_temperature

    @property
    def target_temperature(self) -> Optional[float]:
        return self._target_temperature

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
