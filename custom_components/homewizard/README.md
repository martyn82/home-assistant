HomeWizard integration
======================

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
