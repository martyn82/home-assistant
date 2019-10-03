"""
Representation of the HomeWizard Energylink device.

Engerylink data:
    t1: none|           #
    t2: none|           #
    c1: int             #
    c2: int             #
    tariff: int         # Day/night energy tariff (day=1, night=2)
    s1: |null           # Return energy port S1
    s2: |null           # Return energy port S2
    aggregate:
        po: int         # Current aggregated power consumption (Watt)
        dayTotal: float # Aggregated total consumed power today (kW)
        po+: int        # Aggregated peak power consumption (Watt)
        po+t: time      # Time aggregated peak power consumption was measured
        po-: int        # Aggregated lowest power consumption (Watt)
        po-t: time      # Time aggregated lowest power consumption was measured
    used:
        po: int         # Current used power (Watt)
        dayTotal: float # Total consumed power today (kW)
        po+: int        # Peak power consumption (Watt)
        po+t: time      # Time peak power consumption was measured
        po-: int        # Lowest power consumption (Watt)
        po-t: time      # Time lowest power consumption was measured
    gas:
        lastHour: float # Gas consumption in the last hour (m3)
        dayTotal: float # Gas consumption today (m3)
    kwhindex: float     #
    wp: int             #
"""

from .gateway import Gateway


class Energylink(object):
    def __init__(self, data, gw: Gateway):
        self._id = data['id']
        self._gw = gw
        self._data = data

    def update(self):
        self._gw.update()
        self._data = self._gw.energylink(self._id)

    @property
    def identifier(self) -> int:
        return self._id

    @property
    def tariff(self) -> int:
        return self._data['tariff']

    @property
    def power_consumption(self) -> int:
        return self._data['used']['po']

    @property
    def today_power_consumption(self) -> float:
        return self._data['used']['dayTotal']

    @property
    def hour_gas_consumption(self) -> float:
        return self._data['gas']['lastHour']

    @property
    def today_gas_consumption(self) -> float:
        return self._data['gas']['dayTotal']
