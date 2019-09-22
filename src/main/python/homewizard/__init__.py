"""Setup HomeWizard platform"""

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

import logging
import json

DOMAIN = 'homewizard'

_LOGGER = logging.getLogger(__name__)
DEFAULT_TIMEOUT = 2


def setup(hass, config):
    return True


class HomeWizard:
    def __init__(self, host, password):
        self._base_url = "http://{0}/{1}".format(host, password)
        self._sensors = None
        self._status = None
        self.update()

    def call(self, path):
        try:
            req = Request(self._base_url + path)
            response = urlopen(req, timeout=DEFAULT_TIMEOUT)

        except HTTPError as e:
            _LOGGER.exception("The device couldn't fulfill the request. Error: ", e.code)
            return "error"

        except URLError as e:
            _LOGGER.exception("Unable to reach device: ", e.reason)
            return "error"

        else:
            r = response.read().decode("utf-8", "ignore")
            out = json.loads(r)
            return out

    def update(self):
        self._sensors = self.call("/get-sensors")
        self._status = self.call("/get-status")

    def get_thermometers(self):
        return self._sensors['response']['thermometers']

    def get_heatlink(self):
        return self._sensors['response']['heatlinks'][0]

    def get_energylink(self):
        return self._sensors['response']['energylinks'][0]

    def get_smoke_sensor(self):
        for s in self._sensors['response']['kakusensors']:
            if s['type'] == "smoke":
                return s

    def get_lights(self):
        return self._sensors['response']['switches']

    def get_preset(self):
        return self._status['response']['preset']


class Heatlink:
    def __init__(self, data, hw):
        self._hw = hw
        self._data = data

    def update(self) -> None:
        _LOGGER.debug("update called")
        self._hw.update()
        heatlink = self._hw.get_heatlink()

        if heatlink != "error":
            self._data = heatlink
        else:
            _LOGGER.exception("Update failed")

    def set_temperature(self, temperature):
        self._hw.call("/hl/0/settarget/{0}".format(temperature))

    @property
    def info(self):
        return self._data


class Energylink:
    def __init__(self, data, hw):
        self._hw = hw
        self._data = data

    def update(self) -> None:
        self._hw.update()
        energylink = self._hw.get_energylink()

        if energylink != "error":
            self._data = energylink
        else:
            _LOGGER.exception("Update failed")

    @property
    def info(self):
        return self._data
