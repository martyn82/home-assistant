"""
This component provides basic support for the HomeWizard system.
"""

import ipaddress
import voluptuous as vol

from homeassistant.const import CONF_HOST, CONF_PASSWORD
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, LOGGER, CONF_TIMEOUT, SRV_GATEWAY
from .gateway import Gateway

DEFAULT_TIMEOUT = 30  # insanely high

CONF_GATEWAY = "gateway"

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        CONF_GATEWAY: vol.Schema({
            vol.Required(CONF_HOST): vol.All(ipaddress.ip_address, cv.string),
            vol.Required(CONF_PASSWORD): cv.string,
            vol.Optional(CONF_TIMEOUT): cv.positive_int
        })
    })
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    # TODO: async?
    # TODO: build config flow

    conf = config.get(DOMAIN)
    if conf is None:
        conf = {}

    hass.data[DOMAIN] = {}

    if CONF_GATEWAY in conf:
        gw_config = conf[CONF_GATEWAY]
        if CONF_TIMEOUT not in conf:
            gw_config[CONF_TIMEOUT] = DEFAULT_TIMEOUT

        gw = Gateway(hass, gw_config)
        gw.update()

        hass.data[DOMAIN][SRV_GATEWAY] = gw

        hass.helpers.discovery.load_platform('climate', DOMAIN, {}, conf)
        hass.helpers.discovery.load_platform('light', DOMAIN, {}, conf)
        hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, conf)

    return True
