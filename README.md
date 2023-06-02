# Data Sources

* [Solar hourly radiation data source](https://re.jrc.ec.europa.eu/pvg_tools/en/#HR) - 2 years (2019, 2020) of Data for Campus Nord with coordinates (49.102, 8.433) with optimized slope and azimuth,
* Demand: for 10 households  ([source](https://www.ggv-energie.de/cms/netz/allgemeine-daten/netzbilanzierung-download-aller-profile.php))
* Electricity Price 
* Wind Capacity Factors for 2019: remote energy hub example from the gboml repository (data was retreived from the European Center for Medium Range Weather  Forecasts (ECMWF), 2020 and converted into capacity factors using the transfer function of the Vestas V90 turbine available in the windpowerlib library) ([source](https://www.frontiersin.org/articles/10.3389/fenrg.2021.671279/full))
* Gas Data

# Benchmark Model

## Nodes and Variables
* $S_{gen}(t)$ - the generated amount of self produced solar energy
* $S_{used}(t)$ - the used amount of self produced solarenergy
* $D_e(t)$ - sum of electricity demand in kWh
* $D_g(t)$ - sum of gas demand in kWh
* $D_h(t)$ - sum of heating demand in kWh
* $c_p$ - cost per PV panel
* $n$ - number of PV panels 
* $c_e(t)$ - electricity price

1. Electricity Demand
    * $\text{min} \sum_t c_e(t) \cdot (D_e(t) - S_{used} (t))$ 
    * s.t. $c(t) >= 0$ \
           $D_e(t) - S_{used} (t) >= 0$

2. Gas Demand
    * $\text{min} \sum_t c_g(t) \cdot D_g(t)$ 
    * s.t. $D_g >= 0$

3. Heating Demand
    * $\text{min} \sum_t c_h \cdot D_h(t)$ 
    * s.t. $D_h >= 0$

4. Solar
    * $\text{min } c_{p} \cdot n$ 
    * s.t.  $n >= 0$ \
            $n >= 20$


# Further Components

5. Wind Plant
6. Battery Storage
7. CHP Plant
    * (information)[https://www.energieheld.de/heizung/bhkw]
    * (information_2)[https://www.heizungsfinder.de/bhkw/betriebsweisen/waermegefuehrt]

# Components To DO

## Charging station for an electric vehicle

## Electrolyzer
* power to hydrogen => only when we have excess renewable energy

## Fuel Cell
* hydrogen to power => in times of a lack of renewable energy