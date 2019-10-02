"""
Representation of the Thermo/Hygro sensors

Thermometer data:
     name: str              # Name of the sensor
     model: int             # Model indication
     lowBattery: yes|no     # Battery indicator
     version: float         # Version of the device
     te: float              # Measured temperature
     hu: float              # Measured humidity
     te+: float             # Max. measured temp
     te-: float             # Min. measured temp
     te+t: time             # Time maximum temp was measured
     te-t: time             # Time minimum temp was measured
     hu+: float             # Max. measured humidity
     hu-: float             # Min. measured humidity
     hu+t: time             # Time maximum humidity was measured
     hu-t: time             # Time minimum humidity was measured
     outside: yes|no        # Whether the sensor is put outside (seems not reliable/version dependent)

"""

from .gateway import Gateway


class ThermoHygrometer(object):
    def __init__(self, data, gw: Gateway):
        self._gw = gw
        self._data = data
        self._low = None
        self._id = data['id']

    def update(self):
        self._gw.update()
        self._data = self._gw.thermometer(self._id)

    @property
    def name(self):
        return self._data['name']

    @property
    def temperature(self):
        return self._data['te']

    @property
    def humidity(self):
        return self._data['hu']

    @property
    def battery_is_low(self) -> bool:
        return self._data['lowBattery'] == 'yes'
