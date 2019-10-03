"""
Representation of the HomeWizard Heatlink device

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

Commands:
    /hl/{id}/settarget/{tte}[/{minutes}]

"""

from typing import Optional
from .gateway import Gateway


class Heatlink(object):
    def __init__(self, data, gw: Gateway):
        self._id = data['id']
        self._gw = gw
        self._data = data

    def update(self):
        self._gw.update()
        self._data = self._gw.heatlink(self._id)

    @property
    def identifier(self) -> int:
        return self._id

    @property
    def read_temperature(self) -> float:
        return self._data['rte']

    @property
    def target_temperature(self) -> float:
        return self._data['tte']

    @property
    def pump_is_on(self) -> bool:
        return self._data['pump'] == 'on'

    @property
    def burner_is_on(self) -> bool:
        return self._data['heating'] == 'on'

    @property
    def hotwater_is_on(self) -> bool:
        return self._data['dhw'] == 'on'

    @property
    def water_pressure(self) -> float:
        return self._data['wp']

    @property
    def water_temperature(self) -> float:
        return self._data['wte']

    @property
    def error_code(self) -> Optional[int]:
        if self._data['ofc'] == 0:
            return None
        else:
            return self._data['ofc']

    @property
    def diagnostic_code(self) -> Optional[int]:
        if self._data['odc'] == 0:
            return None
        else:
            return self._data['odc']

    def set_temperature(self, temperature: float):
        self._gw.api(f"/hl/{self._id}/settarget/{temperature}")
