"""Handle interactions with the HomeWizard gateway"""

import json

from homeassistant.const import CONF_HOST, CONF_PASSWORD
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

from .const import LOGGER, CONF_TIMEOUT


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

    def heatlink(self, identifier):
        for hl in self._sensors['heatlinks']:
            if hl['id'] == identifier:
                return hl

    def light(self, identifier):
        for light in self._sensors['switches']:
            if light['id'] == identifier:
                return light

    @property
    def heatlinks(self):
        return self._sensors['heatlinks']

    @property
    def lights(self):
        return self._sensors['switches']
