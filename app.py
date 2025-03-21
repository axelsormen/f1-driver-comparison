######### IMPORTS & LAYOUT #########

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from api.drivers_api import get_drivers_data
from api.results_api import get_results_data 
from api.standings_api import get_standings_data 
from api.qualifying_api import get_qualifying_data 
from functions.time_converter import time_to_milliseconds 

st.set_page_config(layout="wide")

# Display the header
st.header("F1 Drivers Comparison 2024")

######### APIS #########

@st.fragment
def api():
    st.session_state.drivers_array = get_drivers_data()
    st.session_state.standings_array = get_standings_data()
    st.session_state.results_array = get_results_data()
    st.session_state.qualifying_array = get_qualifying_data()
api()

######### MAIN #########

@st.fragment
def main():

    ######### MULTISELECT #########

    selected_drivers = st.multiselect(
        'Select drivers to compare:', 
        [f"{driver['given_name']} {driver['family_name']}" for driver in sorted(st.session_state.drivers_array, key=lambda x: x['given_name'])]
    )

    if selected_drivers:

        ######### STANDINGS #########
            
        selected_standings_info = []

        for selected in selected_drivers:
            selected = selected.strip() 
            for standings_info in st.session_state.standings_array:
                full_name = f"{standings_info['given_name']} {standings_info['family_name']}".strip()
                if selected == full_name:  
                    position = standings_info["position"]
                    points = standings_info["points"]
                    wins = standings_info["wins"]
                    constructor = standings_info["constructor_name"]
                    
                    selected_standings_info.append({"Position": position, "Driver": selected, "Constructor": constructor, "Points": points, "Wins": wins})

        selected_drivers_info_sorted = sorted(selected_standings_info, key=lambda x: int(x["Position"]))
        df = pd.DataFrame(selected_drivers_info_sorted)

        if selected_drivers_info_sorted:
            st.header("Standings:")
            st.dataframe(df.set_index(df.columns[0]))

        ######### GP Results #########

        selected_results_info = []

        for selected in selected_drivers:
            selected = selected.strip()  
            for results_info in st.session_state.results_array:
                full_name = f"{results_info['given_name']} {results_info['family_name']}".strip()
                if selected == full_name: 
                    position = results_info["position"]
                    status = results_info["status"]
                    season = results_info["season"]
                    round = results_info["round"]
                    race_name = results_info["race_name"]
                    circuit_name = results_info["circuit_name"]
                    date = results_info["date"]
                    constructor = results_info["constructor_name"]

                    selected_results_info.append({"Driver": selected, 
                                            "Constructor": constructor, 
                                            "position": position,
                                            "status": status,
                                            "season": season,
                                            "round": round, 
                                            "race_name": race_name, 
                                            "circuit_name": circuit_name,
                                            "date": date})
                    
        results_round_array = []
        results_status_array = []
        results_driver_array = []
        results_race_array = []
        results_array = []

        for round in selected_results_info:
            results_round_array.append(int(round["round"]))

        for status in selected_results_info:
            results_status_array.append(status["status"])

        for driver in selected_results_info:
            results_driver_array.append(driver["Driver"])

        for race in selected_results_info:
            results_race_array.append(race["race_name"])

        for position in selected_results_info:
            results_array.append(int(position["position"]))

        st.header("GP Results")

        results_data = pd.DataFrame(
            {
                "Round": results_round_array,
                "Position": results_array,
                "Driver": results_driver_array,
                "Status": results_status_array,
                "Grand Prix": results_race_array
            }
        )

        results_chart = alt.Chart(results_data).mark_line().encode(
            alt.X('Round', sort='ascending').scale(zero=False),
            alt.Y('Position').scale(zero=False),
            color='Driver',
            tooltip=['Round', 'Grand Prix', 'Driver', 'Position', 'Status']
        ).interactive().properties(width=1200, height=500)

        st.altair_chart(results_chart)

        ######### Qualifying Results #########

        selected_qualifying_info = []

        for selected in selected_drivers:
            selected = selected.strip()  
            for qualifying_info in st.session_state.qualifying_array:
                full_name = f"{qualifying_info['given_name']} {qualifying_info['family_name']}".strip()
                if selected == full_name: 
                    position = qualifying_info["position"]
                    q1 = qualifying_info["q1"]
                    q1_ms = qualifying_info["q1_ms"]
                    best_q1_time = qualifying_info["best_q1_time"]
                    difference_best_q1_time = qualifying_info["difference_best_q1_time"]
                    q2 = qualifying_info["q2"]
                    q2_ms = qualifying_info["q2_ms"]
                    best_q2_time = qualifying_info["best_q2_time"]
                    difference_best_q2_time = qualifying_info["difference_best_q2_time"]
                    q3 = qualifying_info["q3"]
                    q3_ms = qualifying_info["q3_ms"]
                    best_q3_time = qualifying_info["best_q3_time"]
                    difference_best_q3_time = qualifying_info["difference_best_q3_time"]
                    season = qualifying_info["season"]
                    round = qualifying_info["round"]
                    race_name = qualifying_info["race_name"]
                    circuit_name = qualifying_info["circuit_name"]
                    date = qualifying_info["date"]
                    constructor = qualifying_info["constructor_name"]

                    selected_qualifying_info.append({"Driver": selected, 
                                            "Constructor": constructor, 
                                            "position": position,
                                            "q1": q1, 
                                            "q1_ms": q1_ms,
                                            "best_q1_time": best_q1_time,
                                            "difference_best_q1_time": difference_best_q1_time,
                                            "q2": q2,
                                            "q2_ms": q2_ms,
                                            "best_q2_time": best_q2_time,
                                            "difference_best_q2_time": difference_best_q2_time,
                                            "q3": q3, 
                                            "best_q3_time": best_q3_time,
                                            "difference_best_q3_time": difference_best_q3_time,
                                            "q3_ms": q3_ms,
                                            "season": season,
                                            "round": round, 
                                            "race_name": race_name, 
                                            "circuit_name": circuit_name,
                                            "date": date})
        qualifying_round_array = []
        q1_lap_time_array = []
        best_q1_time_array = []
        difference_best_q1_time_array = []
        q2_lap_time_array = []
        best_q2_time_array = []
        difference_best_q2_time_array = []
        q3_lap_time_array = []
        best_q3_time_array = []
        difference_best_q3_time_array = []
        qualifying_driver_array = []
        qualifying_race_array = []
        qualiying_array = []

        for round in selected_qualifying_info:
            qualifying_round_array.append(int(round["round"]))

        for q1_lap_time in selected_qualifying_info:
            q1_lap_time_array.append(q1_lap_time["q1"])

        for q1_best in selected_qualifying_info:
            best_q1_time_array.append(q1_best["best_q1_time"])

        for q1_difference in selected_qualifying_info:
            difference_best_q1_time_array.append(q1_difference["difference_best_q1_time"])

        for q2_lap_time in selected_qualifying_info:
            q2_lap_time_array.append(q2_lap_time["q2"])

        for q2_best in selected_qualifying_info:
            best_q2_time_array.append(q2_best["best_q2_time"])

        for q2_difference in selected_qualifying_info:
            difference_best_q2_time_array.append(q2_difference["difference_best_q2_time"])

        for q3_lap_time in selected_qualifying_info:
            q3_lap_time_array.append(q3_lap_time["q3"])

        for q3_best in selected_qualifying_info:
            best_q3_time_array.append(q3_best["best_q3_time"])

        for q3_difference in selected_qualifying_info:
            difference_best_q3_time_array.append(q3_difference["difference_best_q3_time"])

        for driver in selected_qualifying_info:
            qualifying_driver_array.append(driver["Driver"])

        for race in selected_qualifying_info:
            qualifying_race_array.append(race["race_name"])

        for position in selected_qualifying_info:
            qualiying_array.append(int(position["position"]))

        st.header("Qualifying Position")

        qualifying_data = pd.DataFrame(
            {
                "Round": qualifying_round_array,
                "Position": qualiying_array,
                "Driver": qualifying_driver_array,
                "Grand Prix": qualifying_race_array
            }
        )

        qualifying_chart = alt.Chart(qualifying_data).mark_line().encode(
            alt.X('Round', sort='ascending').scale(zero=False),
            alt.Y('Position').scale(zero=False),
            color='Driver',
            tooltip=['Round', 'Grand Prix', 'Driver', 'Position']
        ).interactive().properties(width=1200, height=500)

        st.altair_chart(qualifying_chart)

        ######### Q1 #########

        st.header("Difference to best Q1 lap time")

        q1_data = pd.DataFrame(
            {
                "Round": qualifying_round_array,
                "Difference (ms)": difference_best_q1_time_array,
                "Driver": qualifying_driver_array,
                "Q1 Lap Time": q1_lap_time_array,
                "Q1 Best Lap Time": best_q1_time_array,
                "Grand Prix": qualifying_race_array
            }
        )

        q1_chart = alt.Chart(q1_data).mark_line().encode(
            alt.X('Round', sort='ascending').scale(zero=False),
            alt.Y('Difference (ms)').scale(zero=False),
            color='Driver',
            tooltip=['Round', 'Grand Prix', 'Driver', 'Q1 Lap Time', "Q1 Best Lap Time", "Difference (ms)"]
        ).interactive().properties(width=1200, height=500)

        st.altair_chart(q1_chart)

        ######### Q2 #########

        st.header("Difference to best Q2 lap time")

        q2_data = pd.DataFrame(
            {
                "Round": qualifying_round_array,
                "Difference (ms)": difference_best_q2_time_array,
                "Driver": qualifying_driver_array,
                "Q2 Lap Time": q2_lap_time_array,
                "Q2 Best Lap Time": best_q2_time_array,
                "Grand Prix": qualifying_race_array
            }
        )

        q2_chart = alt.Chart(q2_data).mark_line().encode(
            alt.X('Round', sort='ascending').scale(zero=False),
            alt.Y('Difference (ms)').scale(zero=False),
            color='Driver',
            tooltip=['Round', 'Grand Prix', 'Driver', 'Q2 Lap Time', "Q2 Best Lap Time",  "Difference (ms)"]
        ).interactive().properties(width=1200, height=500)

        st.altair_chart(q2_chart)

        ######### Q3 #########

        st.header("Difference to best Q3 lap time")

        q3_data = pd.DataFrame(
            {
                "Round": qualifying_round_array,
                "Difference (ms)": difference_best_q3_time_array,
                "Driver": qualifying_driver_array,
                "Q3 Lap Time": q3_lap_time_array,
                "Q3 Best Lap Time": best_q3_time_array,
                "Grand Prix": qualifying_race_array
            }
        )

        q3_chart = alt.Chart(q3_data).mark_line().encode(
            alt.X('Round', sort='ascending').scale(zero=False),
            alt.Y('Difference (ms)').scale(zero=False),
            color='Driver',
            tooltip=['Round', 'Grand Prix', 'Driver', 'Q3 Lap Time', "Q3 Best Lap Time", "Difference (ms)"]
        ).interactive().properties(width=1200, height=500)

        st.altair_chart(q3_chart)

main()