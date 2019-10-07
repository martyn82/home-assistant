"""Handle interactions with the HomeWizard gateway"""

import json

from homeassistant.const import CONF_HOST, CONF_PASSWORD
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

from .const import (
    LOGGER,
    CONF_TIMEOUT,
    PRESETS
)


class Gateway(object):
    def __init__(self, hass, config):
        self._config = config
        self._hass = hass
        self._timeout = config[CONF_TIMEOUT]
        self._base_url = f"http://{config[CONF_HOST]}/{config[CONF_PASSWORD]}"
        self._sensors = None

    def api(self, path):
        try:
            response = urlopen(
                Request(self._base_url + path),
                timeout=self._timeout
            )

        except HTTPError as e:
            LOGGER.exception("The device couldn't fulfill the request. Error: ", e.code)
            return "error"

        except URLError as e:
            LOGGER.exception("Unable to reach device: ", e.reason)
            return "error"

        else:
            return json.loads(
                response.read().decode("utf-8", "ignore")
            )

    def update(self):
        response = self.api("/get-sensors")
        self._sensors = response['response']

    @property
    def heatlinks(self):
        return self._sensors['heatlinks']

    def heatlink(self, identifier):
        for hl in self.heatlinks:
            if hl['id'] == identifier:
                return hl

    @property
    def switches(self):
        return self._sensors['switches']

    def switch(self, identifier):
        for switch in self.switches:
            if switch['id'] == identifier:
                return switch

    @property
    def thermometers(self):
        return self._sensors['thermometers']

    def thermometer(self, identifier):
        for thermo in self.thermometers:
            if thermo['id'] == identifier:
                return thermo

    @property
    def energylinks(self):
        return self._sensors['energylinks']

    def energylink(self, identifier):
        for el in self.energylinks:
            if el['id'] == identifier:
                return el

    @property
    def smoke_detectors(self):
        sd = []
        for s in self._sensors['kakusensors']:
            if s['type'] == "smoke":
                sd.append(s)
        return sd

    def smoke_detector(self, identifier):
        for s in self.smoke_detectors:
            if s['id'] == identifier:
                return s

    @property
    def presets(self):
        return PRESETS

    @property
    def active_preset(self) -> int:
        return self._sensors['preset']

    def set_preset(self, name):
        for p in self.presets:
            if p['name'] == name:
                self.api(f"/preset/{p['id']}")
                break
