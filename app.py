import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from api.drivers_api import get_drivers_data
from api.standings_api import get_standings_data 
from api.qualifying_api import get_qualifying_data 
from functions.time_converter import time_to_milliseconds 

st.set_page_config(layout="wide")

# Display the header
st.header("F1 Drivers Comparison 2024")

@st.fragment
def api():
    st.session_state.drivers_array = get_drivers_data()
    st.session_state.standings_array = get_standings_data()
    st.session_state.qualifying_array = get_qualifying_data()
api()

@st.fragment
def main():
    # Add a multiselect widget to allow users to choose drivers
    selected_drivers = st.multiselect(
        'Select drivers to compare:', 
        [f"{driver['given_name']} {driver['family_name']}" for driver in st.session_state.drivers_array]
    )   
                                
    selected_standings_info = []

    # Iterate through the selected drivers
    for selected in selected_drivers:
        selected = selected.strip()  # Remove any leading/trailing whitespace
        for standings_info in st.session_state.standings_array:
            full_name = f"{standings_info['given_name']} {standings_info['family_name']}".strip()
            if selected == full_name:  # Match the full name exactly
                position = standings_info["position"]
                points = standings_info["points"]
                wins = standings_info["wins"]
                constructor = standings_info["constructor_name"]
                # Add driver and position as a dictionary to the list
                selected_standings_info.append({"Position": position, "Driver": selected, "Constructor": constructor, "Points": points, "Wins": wins})

    # Sort the selected drivers by position (ascending order)
    selected_drivers_info_sorted = sorted(selected_standings_info, key=lambda x: int(x["Position"]))
    df = pd.DataFrame(selected_drivers_info_sorted)

    # Display the selected drivers and their positions in a table format
    if selected_drivers_info_sorted:
        st.header("Standings:")
        st.dataframe(df.set_index(df.columns[0]))

    selected_qualifying_info = []

    # Iterate through the selected drivers
    for selected in selected_drivers:
        selected = selected.strip()  # Remove any leading/trailing whitespace
        for qualifying_info in st.session_state.qualifying_array:
            full_name = f"{qualifying_info['given_name']} {qualifying_info['family_name']}".strip()
            if selected == full_name:  # Match the full name exactly
                q1 = qualifying_info["q1"]
                q2 = qualifying_info["q2"]
                q3 = qualifying_info["q3"]
                season = qualifying_info["season"]
                round = qualifying_info["round"]
                race_name = qualifying_info["race_name"]
                circuit_name = qualifying_info["circuit_name"]
                date = qualifying_info["date"]
                constructor = qualifying_info["constructor_name"]
                # Add driver and position as a dictionary to the list
                selected_qualifying_info.append({"Driver": selected, 
                                        "Constructor": constructor, 
                                        "q1": q1, 
                                        "q2": q2,
                                        "q3": q3, 
                                        "season": season,
                                        "round": round, 
                                        "race_name": race_name, 
                                        "circuit_name": circuit_name,
                                        "date": date})
    # Prepare data
    round_array = []
    q1_lap_time_milliseconds_array = []
    q1_lap_time_array = []
    driver_array = []
    race_array = []

    for round in selected_qualifying_info:
        round_array.append(int(round["round"]))

    for lap_time_milliseconds in selected_qualifying_info:
        q1_lap_time_milliseconds_array.append(time_to_milliseconds(lap_time_milliseconds["q1"]))

    for lap_time in selected_qualifying_info:
        q1_lap_time_array.append(lap_time["q1"])

    for driver in selected_qualifying_info:
        driver_array.append(driver["Driver"])

    for race in selected_qualifying_info:
        race_array.append(race["race_name"])

    # Create DataFrame
    chart_data = pd.DataFrame(
        {
            "Round": round_array,
            "Q1 Lap Time (ms)": q1_lap_time_milliseconds_array,
            "Driver": driver_array,
            "Q1 Lap Time": q1_lap_time_array,
            "Grand Prix": race_array
        }
    )

    # Display the chart with Altair
    st.header("Best Qualifying Times per Driver (Q1)")

    # Create the chart using Altair
    chart = alt.Chart(chart_data).mark_line().encode(
        alt.X('Round', sort='ascending').scale(zero=False),
        alt.Y('Q1 Lap Time (ms)').scale(zero=False),
        color='Driver',
        tooltip=['Round', 'Grand Prix', 'Driver', 'Q1 Lap Time']
    ).interactive().properties(width=1200, height=500)

    # Display the chart
    st.altair_chart(chart)

main()