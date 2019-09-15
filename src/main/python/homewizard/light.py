"""
configuration.yml

light:
    - platform: homewizard
      host: {HOST_ADDRESS}
      password: {PASSWORD}
"""

from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
    STATE_ON,
    STATE_OFF
)
from homeassistant.components.light import (
    PLATFORM_SCHEMA,
    Light
)

import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    from . import HomeWizard

    hw = HomeWizard(config.get(CONF_HOST), config.get(CONF_PASSWORD))
    lights = hw.get_lights()

    add_entities(LightSwitch(light, hw) for light in lights)


class LightSwitch(Light):
    def __init__(self, data, hw):
        self._hw = hw
        self._data = data
        self._name = None
        self._state = None
        self.set()

    def update(self) -> None:
        self._hw.update()
        self.set()

    def set(self) -> None:
        lights = self._hw.get_lights()
        for l in lights:
            if l['id'] == self._data['id']:
                self._data = l
                break
        self._state = self._data['status']
        self._name = self._data['name']

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_on(self) -> bool:
        return self._state == STATE_ON

    def turn_on(self, **kwargs):
        self._hw.call("/sw/{0}/on".format(self._data['id']))

    def turn_off(self, **kwargs):
        self._hw.call("/sw/{0}/off".format(self._data['id']))

