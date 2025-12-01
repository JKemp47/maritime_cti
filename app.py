import streamlit as st
import pandas as pd
import pydeck as pdk
import altair as alt
from db import get_session, Threat, AIS
from PIL import Image
import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(
                rgba(0, 0, 0, 0.45),   /* Top overlay: adjust opacity here */
                rgba(0, 0, 0, 0.45)
            ), 
            url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local("assets/uscg_background.jpg")

logo = Image.open("assets/uscg.png")
st.image(logo, width=150)
st.markdown("<h1 style='text-align: center;'>Maritime Cyber Threat Intelligence Dashboard</h1>", unsafe_allow_html=True)


def load_data():
    session = get_session()
    threats = pd.read_sql(session.query(Threat).statement, session.bind)
    ais = pd.read_sql(session.query(AIS).statement, session.bind)
    session.close()
    return threats, ais

threats, ais = load_data()

# -----------------------------------------------------
# Combined Histogram
# -----------------------------------------------------
import altair as alt

st.header("Threat Distribution by Source and Type")

# Ensure required columns exist
if "source" in threats.columns and "type" in threats.columns:
    chart = (
        alt.Chart(threats)
        .mark_bar()
        .encode(
            x=alt.X("source:N", title="Threat Source"),
            y=alt.Y("count():Q", title="Number of Threats"),
            color=alt.Color("type:N", title="Threat Type"),
            tooltip=["source", "type", "count()"]
        )
        .properties(width=700, height=400)
    )

    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("The database does not contain both 'source' and 'type' fields.")

# -----------------------------------------------------
# Threat Feed
# -----------------------------------------------------
# ---- Threat Distribution Histogram (Source × Type) ----
st.header("Threat Feed")
st.dataframe(threats.sort_values("published", ascending=False))

# -----------------------------------------------------
# FIXED AIS MAP
# -----------------------------------------------------
st.header("AIS Map")

layer = pdk.Layer(
    "ScatterplotLayer",
    data=ais,
    get_position=["longitude", "latitude"],
    get_radius=7000,
    get_fill_color=[255, 0, 0],
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=30,
    longitude=-70,
    zoom=4
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style=None
)

st.pydeck_chart(deck)


