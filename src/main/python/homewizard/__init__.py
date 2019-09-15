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

    def get_thermometers(self):
        sensors = self.call("/get-sensors")
        return sensors['response']['thermometers']

    def get_heatlink(self):
        status = self.call("/get-status")
        return status['response']['heatlinks'][0]

    def heatlink_set_temperature(self, temperature):
        self.call("/hl/0/settarget/{0}".format(temperature))
