HomeWizard integration
======================

## Thermo/Hygro sensors

```
Thermometer data:
     name: str              # Name of the sensor
     model: int             # Model indication
     lowBattery: yes|no     # Battery indicator
     version: float         # Version of the device
     te: float              # Measured temperature
     hu: float              # Measured humidity
     te+: float             # Max. measured temp
     te-: float             # Min. measured temp
     te+t: str              # Time maximum temp was measured
     te-t: str              # Time minimum temp was measured
     hu+: float             # Max. measured humidity
     hu-: float             # Min. measured humidity
     hu+t: str              # Time maximum humidity was measured
     hu-t: str              # Time minimum humidity was measured
     outside: yes|no        # Whether the sensor is put outside (uncertain)
```

## Heatlink

```
Heatlink data:
    pump: on|off        # heating pump
    heating: on|off     # burner on/off
    dhw: on|off         # hot tap water pump
    rte: float          # read/measured temperature
    rsp: float          # set temperature on thermostat
    tte: float          # set temperature on heatlink
    ttm: float|null     # timer
    wp: float           # water pressure
    wte: float          # water temperature
    ofc: int            # error code (0 = OK)
    odc: int            # diagnostic code (0 = OK)
```
