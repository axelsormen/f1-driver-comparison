######### IMPORTS & LAYOUT #########

import streamlit as st
import pandas as pd
import os
import altair as alt
from api.drivers_api import get_drivers_data
from api.results_api import get_results_data 
from api.standings_api import get_standings_data 
from api.qualifying_api import get_qualifying_data 

st.set_page_config(layout="wide")

# Defines the file path to the CSS file
css_path = os.path.join("css.html") 

# Opens the CSS file in read mode and store its content
with open(css_path, "r") as f: 
    css_content = f.read() # Reads the content of the CSS file

st.markdown(f"{css_content}", unsafe_allow_html=True)

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
        [f"{driver['given_name']} {driver['family_name']}" for driver in sorted(st.session_state.drivers_array, key=lambda x: x['given_name'])],
        placeholder="Choose a driver"
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
                    standings_points = standings_info["points"]
                    wins = standings_info["wins"]
                    constructor = standings_info["constructor_name"]
                    
                    selected_standings_info.append({"Position": position, 
                                                    "Driver": selected, 
                                                    "Constructor": constructor, 
                                                    "Points": standings_points, 
                                                    "Wins": wins})

        selected_drivers_info_sorted = sorted(selected_standings_info, key=lambda x: int(x["Position"]))
        df = pd.DataFrame(selected_drivers_info_sorted)

        if selected_drivers_info_sorted:
            st.header("Standings")
            
            # Increase the table size by adjusting the width and height
            st.dataframe(df.set_index(df.columns[0]), width=500)

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
                    race_points = results_info["points"]
                    total_points = results_info["total_points"]
                    circuit_name = results_info["circuit_name"]
                    date = results_info["date"]
                    constructor = results_info["constructor_name"]

                    selected_results_info.append({"driver": selected, 
                                            "constructor": constructor, 
                                            "position": position,
                                            "status": status,
                                            "season": season,
                                            "round": round, 
                                            "race_name": race_name, 
                                            "race_points": race_points,
                                            "total_points": total_points,
                                            "circuit_name": circuit_name,
                                            "date": date})
                    
        results_round_array = []
        results_status_array = []
        results_driver_array = []
        results_race_array = []
        results_total_points_array = []
        results_array = []

        for round in selected_results_info:
            results_round_array.append(int(round["round"]))

        for status in selected_results_info:
            results_status_array.append(status["status"])

        for driver in selected_results_info:
            results_driver_array.append(driver["driver"])

        for race in selected_results_info:
            results_race_array.append(race["race_name"])

        for position in selected_results_info:
            results_array.append(int(position["position"]))

        for total_points in selected_results_info:
            results_total_points_array.append(int(total_points["total_points"]))

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

        results_chart = alt.Chart(results_data).mark_line(size=5).encode(
            alt.X('Round', sort='ascending').scale(zero=False),
            alt.Y('Position').scale(zero=False),
            color='Driver',
            tooltip=['Round', 'Grand Prix', 'Driver', 'Position', 'Status']
        ).interactive(
        ).properties(
            height=600
        ).configure(
            background='#ffffff'
        ).configure_axis(
            labelFontSize=16,
            titleFontSize=18 
        ).configure_title(
            fontSize=20  
        )

        st.altair_chart(results_chart, use_container_width=True)

        ######### GP Points Development #########

        st.header("GP Points Development")

        total_points_data = pd.DataFrame(
            {
                "Round": results_round_array,
                "Points": results_total_points_array,
                "Driver": results_driver_array,
                "Grand Prix": results_race_array
            }
        )

        total_points_chart = alt.Chart(total_points_data).mark_line(size=5).encode(
            alt.X('Round', sort='ascending').scale(zero=False),
            alt.Y('Points').scale(zero=False),
            color='Driver',
            tooltip=['Round', 'Grand Prix', 'Driver', 'Points']
        ).interactive(
        ).properties(
            height=600
        ).configure(
            background='#ffffff'
        ).configure_axis(
            labelFontSize=16,
            titleFontSize=18 
        ).configure_title(
            fontSize=20  
        )

        st.altair_chart(total_points_chart, use_container_width=True)

        ######### Qualifying Results #########

        selected_qualifying_info = []

        for selected in selected_drivers:
            selected = selected.strip()  
            for qualifying_info in st.session_state.qualifying_array:
                full_name = f"{qualifying_info['given_name']} {qualifying_info['family_name']}".strip()
                if selected == full_name: 
                    position = qualifying_info["position"]
                    q1 = qualifying_info["q1"]
                    q1_sec = qualifying_info["q1_sec"]
                    fastest_q1_time = qualifying_info["fastest_q1_time"]
                    difference_fastest_q1_time = qualifying_info["difference_fastest_q1_time"]
                    q2 = qualifying_info["q2"]
                    q2_sec = qualifying_info["q2_sec"]
                    fastest_q2_time = qualifying_info["fastest_q2_time"]
                    difference_fastest_q2_time = qualifying_info["difference_fastest_q2_time"]
                    q3 = qualifying_info["q3"]
                    q3_sec = qualifying_info["q3_sec"]
                    fastest_q3_time = qualifying_info["fastest_q3_time"]
                    difference_fastest_q3_time = qualifying_info["difference_fastest_q3_time"]
                    season = qualifying_info["season"]
                    round = qualifying_info["round"]
                    race_name = qualifying_info["race_name"]
                    circuit_name = qualifying_info["circuit_name"]
                    date = qualifying_info["date"]
                    constructor = qualifying_info["constructor_name"]

                    selected_qualifying_info.append({"driver": selected, 
                                            "constructor": constructor, 
                                            "position": position,
                                            "q1": q1, 
                                            "q1_sec": q1_sec,
                                            "fastest_q1_time": fastest_q1_time,
                                            "difference_fastest_q1_time": difference_fastest_q1_time,
                                            "q2": q2,
                                            "q2_sec": q2_sec,
                                            "fastest_q2_time": fastest_q2_time,
                                            "difference_fastest_q2_time": difference_fastest_q2_time,
                                            "q3": q3, 
                                            "q3_sec": q3_sec,
                                            "fastest_q3_time": fastest_q3_time,
                                            "difference_fastest_q3_time": difference_fastest_q3_time,
                                            "season": season,
                                            "round": round, 
                                            "race_name": race_name, 
                                            "circuit_name": circuit_name,
                                            "date": date})
        qualifying_round_array = []
        q1_lap_time_array = []
        fastest_q1_time_array = []
        difference_fastest_q1_time_array = []
        q2_lap_time_array = []
        fastest_q2_time_array = []
        difference_fastest_q2_time_array = []
        q3_lap_time_array = []
        fastest_q3_time_array = []
        difference_fastest_q3_time_array = []
        qualifying_driver_array = []
        qualifying_race_array = []
        qualiying_array = []

        for round in selected_qualifying_info:
            qualifying_round_array.append(int(round["round"]))

        for q1_lap_time in selected_qualifying_info:
            q1_lap_time_array.append(q1_lap_time["q1"])

        for q1_fastest in selected_qualifying_info:
            fastest_q1_time_array.append(q1_fastest["fastest_q1_time"])

        for q1_difference in selected_qualifying_info:
            difference_fastest_q1_time_array.append(q1_difference["difference_fastest_q1_time"])

        for q2_lap_time in selected_qualifying_info:
            q2_lap_time_array.append(q2_lap_time["q2"])

        for q2_fastest in selected_qualifying_info:
            fastest_q2_time_array.append(q2_fastest["fastest_q2_time"])

        for q2_difference in selected_qualifying_info:
            difference_fastest_q2_time_array.append(q2_difference["difference_fastest_q2_time"])

        for q3_lap_time in selected_qualifying_info:
            q3_lap_time_array.append(q3_lap_time["q3"])

        for q3_fastest in selected_qualifying_info:
            fastest_q3_time_array.append(q3_fastest["fastest_q3_time"])

        for q3_difference in selected_qualifying_info:
            difference_fastest_q3_time_array.append(q3_difference["difference_fastest_q3_time"])

        for driver in selected_qualifying_info:
            qualifying_driver_array.append(driver["driver"])

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

        qualifying_chart = alt.Chart(qualifying_data).mark_line(size=5).encode(
            alt.X('Round', sort='ascending').scale(zero=False),
            alt.Y('Position').scale(zero=False),
            color='Driver',
            tooltip=['Round', 'Grand Prix', 'Driver', 'Position']
        ).interactive(
        ).properties(
            height=600
        ).configure(
            background='#ffffff'
        ).configure_axis(
            labelFontSize=16,
            titleFontSize=18 
        ).configure_title(
            fontSize=20  
        )

        st.altair_chart(qualifying_chart, use_container_width=True)

        ######### Q1 #########

        st.header("Difference to fastest Q1 lap time")

        q1_data = pd.DataFrame(
            {
                "Round": qualifying_round_array,
                "Difference (sec)": difference_fastest_q1_time_array,
                "Driver": qualifying_driver_array,
                "Q1 Lap Time": q1_lap_time_array,
                "Fastest Q1 Lap Time": fastest_q1_time_array,
                "Grand Prix": qualifying_race_array
            }
        )

        q1_chart = alt.Chart(q1_data).mark_line(size=5).encode(
            alt.X('Round', sort='ascending').scale(zero=False),
            alt.Y('Difference (sec)').scale(zero=False),
            color='Driver',
            tooltip=['Round', 'Grand Prix', 'Driver', 'Q1 Lap Time', "Fastest Q1 Lap Time", "Difference (sec)"]
        ).interactive(
        ).properties(
            height=600
        ).configure(
            background='#ffffff'
        ).configure_axis(
            labelFontSize=16,
            titleFontSize=18 
        ).configure_title(
            fontSize=20  
        )

        st.altair_chart(q1_chart, use_container_width=True)

        ######### Q2 #########

        st.header("Difference to fastest Q2 lap time")

        q2_data = pd.DataFrame(
            {
                "Round": qualifying_round_array,
                "Difference (sec)": difference_fastest_q2_time_array,
                "Driver": qualifying_driver_array,
                "Q2 Lap Time": q2_lap_time_array,
                "Fastest Q2 Lap Time": fastest_q2_time_array,
                "Grand Prix": qualifying_race_array
            }
        )

        q2_chart = alt.Chart(q2_data).mark_line(size=5).encode(
            alt.X('Round', sort='ascending').scale(zero=False),
            alt.Y('Difference (sec)').scale(zero=False),
            color='Driver',
            tooltip=['Round', 'Grand Prix', 'Driver', 'Q2 Lap Time', "Fastest Q2 Lap Time",  "Difference (sec)"]
        ).interactive(
        ).properties(
            height=600
        ).configure(
            background='#ffffff'
        ).configure_axis(
            labelFontSize=16,
            titleFontSize=18 
        ).configure_title(
            fontSize=20  
        )

        st.altair_chart(q2_chart, use_container_width=True)

        ######### Q3 #########

        st.header("Difference to fastest Q3 lap time")

        q3_data = pd.DataFrame(
            {
                "Round": qualifying_round_array,
                "Difference (sec)": difference_fastest_q3_time_array,
                "Driver": qualifying_driver_array,
                "Q3 Lap Time": q3_lap_time_array,
                "Fastest Q3 Lap Time": fastest_q3_time_array,
                "Grand Prix": qualifying_race_array
            }
        )

        q3_chart = alt.Chart(q3_data).mark_line(size=5).encode(
            alt.X('Round', sort='ascending').scale(zero=False),
            alt.Y('Difference (sec)').scale(zero=False),
            color='Driver',
            tooltip=['Round', 'Grand Prix', 'Driver', 'Q3 Lap Time', "Fastest Q3 Lap Time", "Difference (sec)"]
        ).interactive(
        ).properties(
            height=600
        ).configure(
            background='#ffffff'
        ).configure_axis(
            labelFontSize=16,
            titleFontSize=18 
        ).configure_title(
            fontSize=20  
        )

        st.altair_chart(q3_chart, use_container_width=True)

main()