"""
This component provides basic support for the HomeWizard system.
"""

import ipaddress
import voluptuous as vol

from homeassistant.const import CONF_HOST, CONF_PASSWORD
from homeassistant.helpers import config_validation as cv

from .const import (
    DOMAIN,
    LOGGER,
    CONF_TIMEOUT,
    SRV_GATEWAY,
    PRESET_NAME_HOME,
    PRESET_NAME_AWAY,
    PRESET_NAME_SLEEP,
    PRESET_NAME_HOLIDAY
)
from .gateway import Gateway

DEFAULT_TIMEOUT = 30  # insanely high

CONF_GATEWAY = "gateway"
ATTR_NAME = "name"
ATTR_ID = "id"

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

        # Platforms

        hass.helpers.discovery.load_platform('climate', DOMAIN, {}, conf)
        hass.helpers.discovery.load_platform('light', DOMAIN, {}, conf)
        hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, conf)

        # Services

        def handle_set_preset(call):
            """Handle the set_preset service call"""
            name = call.data.get(ATTR_NAME, None)
            if name is None:
                return False

            gw: Gateway = hass.data[DOMAIN][SRV_GATEWAY]
            gw.set_preset(name)
            return True

        hass.services.register(DOMAIN, 'set_preset', handle_set_preset)

        def handle_test_smoke_detector(call):
            """Handle the test_smoke_detector service call"""
            id = call.data.get(ATTR_ID, None)
            if id is None:
                return False

            gw: Gateway = hass.data[DOMAIN][SRV_GATEWAY]
            gw.test_smoke_detector(id)
            return True

        hass.services.register(DOMAIN, 'test_smoke_detector', handle_test_smoke_detector)

    return True
