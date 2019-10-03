"""HomeWizard light platform"""

from homeassistant.components.light import Light

from .const import DOMAIN, SRV_GATEWAY
from .gateway import Gateway


def setup_platform(hass, config, add_entities, discovery_info=None):
    if discovery_info is None:
        return

    gw: Gateway = hass.data[DOMAIN][SRV_GATEWAY]
    add_entities(LightSwitch(switch, gw) for switch in gw.switches)


class LightSwitch(Light):
    def __init__(self, data, gw: Gateway):
        self._gw = gw
        self._data = data
        self._id = data['id']
        self._name = None
        self._state = None
        self.set()

    def set(self):
        self._name = self._data['name']
        self._state = self._data['status']

    def update(self):
        self._gw.update()
        self._data = self._gw.switch(self._id)
        self.set()

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state == 'on'

    def turn_on(self, **kwargs) -> None:
        self._gw.api(f"/sw/{self._id}/on")

    def turn_off(self, **kwargs) -> None:
        self._gw.api(f"/sw/{self._id}/off")
