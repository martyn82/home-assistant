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
     te+t: time             # Time maximum temp was measured
     te-t: time             # Time minimum temp was measured
     hu+: float             # Max. measured humidity
     hu-: float             # Min. measured humidity
     hu+t: time             # Time maximum humidity was measured
     hu-t: time             # Time minimum humidity was measured
     outside: yes|no        # Whether the sensor is put outside (uncertain)
```

## Energylink

```
Engerylink data:
    t1: none|           #
    t2: none|           #
    c1: int             #
    c2: int             #
    tariff: int         # Day/night energy tariff
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
```
