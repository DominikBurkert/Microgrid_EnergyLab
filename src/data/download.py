from io import BytesIO

import pandas as pd
import requests


def get_radiation_data(
    lat: float,
    lon: float,
    startyear: int,
    endyear: int,
    peakpower: int = 14,
    loss: int = 1,
):
    """
    This function downloads solar radiation data from the PVGIS web site
    that gives information about solar radiation and PhotoVoltaic system
    performance. It can be used to calculate how much energy one can get
    from different kinds of PV systems at nearly any place in the world.

    Parameters
    ----------
    lat : float
        Latitude, in decimal degrees, south is negative.
    lon : float
        Longitude, in decimal degrees, west is negative.
    startyear : int
        First year of the wanted period.
    endyear : int
        Last year of the wanted period.
    peakpower : int
        Nominal power of the PV system, in kW.
    loss : int
        Sum of system losses, in percent.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the hourly radiation data of the
        given location.
    """
    url = f"https://re.jrc.ec.europa.eu/api/v5_2/seriescalc?lat={str(lat)}&lon={str(lon)}&startyear={str(startyear)}&endyear={str(endyear)}&peakpower={str(peakpower)}&mountingplace={'building'}&loss={str(loss)}&optimalinclination={'1'}&optimalangles={'1'}&inclined_optimum={'1'}&inclinedaxisangle&outputformat=csv"  # noqa
    response_API = requests.get(url)
    data = response_API.text
    lines = data.splitlines()
    content = "\n".join(lines[8:-9])
    file = BytesIO(content.encode())
    df = pd.read_csv(file)
    df["year"] = [int(df["time"][x].split(":")[0][:4]) for x in df.index]
    df = df[df["year"].isin(list(range(startyear, endyear + 1)))].reset_index(drop=True)
    return df
