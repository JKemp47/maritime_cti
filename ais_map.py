import plotly.express as px
from db import AIS, get_session

def get_ais_map():
    """
    Returns a corrected AIS map with proper latitude/longitude ordering
    and a land-focused basemap.
    """

    session = get_session()
    ais_records = session.query(AIS).all()

    # Extract fields
    lats = [a.latitude for a in ais_records]
    lons = [a.longitude for a in ais_records]
    names = [a.vessel_name for a in ais_records]
    status = [a.status for a in ais_records]

    # Build a clean DataFrame
    import pandas as pd
    df = pd.DataFrame({
        "latitude": lats,
        "longitude": lons,
        "name": names,
        "status": status
    })

    # 🔥 FIX #1: Enforce correct lat/lon mapping
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        hover_name="name",
        color="status",
        zoom=4,
        height=600
    )

    # 🔥 FIX #2: Use land-focused map style
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_center={"lat": 37.5, "lon": -95},
        margin={"l": 0, "r": 0, "t": 0, "b": 0}
    )

    return fig

