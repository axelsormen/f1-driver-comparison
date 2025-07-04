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

st.header("F1 Drivers Comparison")

######### MAIN #########

@st.fragment
def main():

    ######### SELECT YEAR #########

    years = [2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000]

    st.session_state.selected_year = st.selectbox("Select a year", years)
    st.session_state.drivers_array = get_drivers_data(st.session_state.selected_year)
    
    if 'view_options' not in st.session_state:
        st.session_state.view_options = "Standings" # Deault to Standings

    ######### MULTISELECT DRIVERS #########

    selected_drivers = st.multiselect(
        'Select drivers to compare:', 
        [f"{driver['given_name']} {driver['family_name']}" for driver in sorted(st.session_state.drivers_array, key=lambda x: x['given_name'])],
        placeholder="Choose a driver"
    )

    if selected_drivers:
        @st.fragment
        def views():
            if int(st.session_state.selected_year) > 2020:
                st.session_state.view_options = st.radio("Select View", ["Standings", "Grand Prix", "Qualifying", "Sprints"], horizontal=True, key='view_toggle', label_visibility="collapsed")
            
            else:
                st.session_state.view_options = st.radio("Select View", ["Standings", "Grand Prix", "Qualifying"], horizontal=True, key='view_toggle', label_visibility="collapsed")

            ######### Standings #########
            if st.session_state.view_options == "Standings":
                # Create a container that can be emptied
                progress_container = st.empty()

                with progress_container:
                    with st.status(label="Fetching Standings Data... 🔄", expanded=False, state="running") as status:
                        st.session_state.standings_array = get_standings_data(st.session_state.selected_year)
                        st.session_state.results_array = get_results_data(st.session_state.selected_year)
                    progress_container.empty()
                
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
                                                            "GP Wins": wins,
                                                            "GP Podiums": None,
                                                            "GP Top 10 Finishes": None, 
                                                            "GP Fastest Laps": None,
                                                            "Sprint Wins": None,
                                                            "Sprint Podiums": None,
                                                            "Sprint Top 8 Finishes": None
                                                            })
                            
                for selected in selected_drivers:
                    selected = selected.strip() 
                    for results_info in st.session_state.results_array:
                        full_name = f"{results_info['given_name']} {results_info['family_name']}".strip()
                        if selected == full_name:  
                            max_round = 0

                            for round in results_info:
                                # Check for the highest round number
                                if int(results_info["round"]) > max_round:
                                    max_round = int(results_info["round"])

                            ## DRIVERS WHO DID NOT TAKE PART IN ROUND 24 GETS NONE!!
                            if int(results_info["round"]) == max_round:
                                podiums = results_info["total_podiums"]
                                top10_finishes = results_info["total_top10_finishes"]
                                fastest_laps = results_info["total_fastest_laps"]
                                sprint_wins = results_info["total_sprint_wins"]
                                sprint_podiums = results_info["total_sprint_podiums"]
                                sprint_top8_finishes = results_info["total_sprint_top8_finishes"]

                                for driver in selected_standings_info:
                                    if driver['Driver'] == full_name:
                                        driver["GP Podiums"] = podiums
                                        driver["GP Top 10 Finishes"] = top10_finishes
                                        driver["GP Fastest Laps"] = fastest_laps
                                        driver["Sprint Wins"] = sprint_wins
                                        driver["Sprint Podiums"] = sprint_podiums
                                        driver["Sprint Top 8 Finishes"] = sprint_top8_finishes

                selected_drivers_info_sorted = sorted(selected_standings_info, key=lambda x: int(x["Position"]))
                df = pd.DataFrame(selected_drivers_info_sorted)

                if selected_drivers_info_sorted:
                    st.header("Standings")
                    
                    st.dataframe(df.set_index(df.columns[0]), use_container_width=True)

            ######### Grand Prix #########
            if st.session_state.view_options == "Grand Prix":
                # Create a container that can be emptied
                progress_container = st.empty()

                with progress_container:
                    with st.status(label="Fetching Grand Prix Data... 🔄", expanded=False, state="running") as status:
                        st.session_state.results_array = get_results_data(st.session_state.selected_year)
                    progress_container.empty()

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
                            total_wins = results_info["total_wins"]
                            total_podiums = results_info["total_podiums"]
                            total_top10_finishes = results_info["total_top10_finishes"]
                            total_fastest_laps = results_info["total_fastest_laps"]
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
                                                    "total_wins": total_wins,
                                                    "total_podiums": total_podiums,
                                                    "total_top10_finishes": total_top10_finishes,
                                                    "total_fastest_laps": total_fastest_laps,
                                                    "circuit_name": circuit_name,
                                                    "date": date})
                            
                results_round_array = []
                results_status_array = []
                results_driver_array = []
                results_constructor_array = []
                results_race_array = []
                results_points_array = []
                results_total_points_array = []
                results_total_wins_array = []
                results_total_podiums_array = []
                results_total_top10_finishes_array = []
                results_total_fastest_laps_array = []
                results_array = []

                for round in selected_results_info:
                    results_round_array.append(int(round["round"]))

                for status in selected_results_info:
                    results_status_array.append(status["status"])

                for driver in selected_results_info:
                    results_driver_array.append(driver["driver"])

                for constructor in selected_results_info:
                    results_constructor_array.append(constructor["constructor"])

                for race in selected_results_info:
                    results_race_array.append(race["race_name"])

                for points in selected_results_info:
                    results_points_array.append(int(points["race_points"]))

                for position in selected_results_info:
                    results_array.append(int(position["position"]))

                for total_points in selected_results_info:
                    results_total_points_array.append(int(total_points["total_points"]))

                for total_wins in selected_results_info:
                    results_total_wins_array.append(int(total_wins["total_wins"]))

                for total_podiums in selected_results_info:
                    results_total_podiums_array.append(int(total_podiums["total_podiums"]))

                for total_top10_finishes in selected_results_info:
                    results_total_top10_finishes_array.append(int(total_top10_finishes["total_top10_finishes"]))

                for total_fastest_laps in selected_results_info:
                    results_total_fastest_laps_array.append(int(total_fastest_laps["total_fastest_laps"]))
                
                ######### GP Results #########

                st.header("GP Results")

                results_data = pd.DataFrame(
                    {
                        "Round": results_round_array,
                        "Position": results_array,
                        "Driver": results_driver_array,
                        "Constructor": results_constructor_array,
                        "Status": results_status_array,
                        "Grand Prix": results_race_array,
                        "Points": results_points_array
                    }
                )

                results_chart = alt.Chart(results_data).mark_line(size=5).encode(
                    alt.X('Round', sort='ascending').scale(zero=False),
                    alt.Y('Position').scale(zero=False),
                    color='Driver',
                    tooltip=['Round', 'Grand Prix', 'Driver', 'Constructor', 'Position', 'Points', 'Status']
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

                ######### Points Development #########

                st.header("Points Development")

                total_points_data = pd.DataFrame(
                    {
                        "Round": results_round_array,
                        "Total Points": results_total_points_array,
                        "Driver": results_driver_array,
                        "Constructor": results_constructor_array,
                        "Grand Prix": results_race_array
                    }
                )

                total_points_chart = alt.Chart(total_points_data).mark_line(size=5).encode(
                    alt.X('Round', sort='ascending').scale(zero=False),
                    alt.Y('Total Points').scale(zero=False),
                    color='Driver',
                    tooltip=['Round', 'Grand Prix', 'Driver', 'Constructor','Total Points']
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

                ######### Top 10 Finishes Development #########

                st.header("Top 10 Finishes Development")

                total_top10_finishes_data = pd.DataFrame(
                    {
                        "Round": results_round_array,
                        "Total Top 10 Finishes": results_total_top10_finishes_array,
                        "Driver": results_driver_array,
                        "Constructor": results_constructor_array,
                        "Grand Prix": results_race_array
                    }
                )

                total_top10_finishes_chart = alt.Chart(total_top10_finishes_data).mark_line(size=5).encode(
                    alt.X('Round', sort='ascending').scale(zero=False),
                    alt.Y('Total Top 10 Finishes').scale(zero=False),
                    color='Driver',
                    tooltip=['Round', 'Grand Prix', 'Driver', 'Constructor','Total Top 10 Finishes']
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

                st.altair_chart(total_top10_finishes_chart, use_container_width=True)

                ######### Podiums Development #########

                st.header("Podiums Development")

                total_podiums_data = pd.DataFrame(
                    {
                        "Round": results_round_array,
                        "Total Podiums": results_total_podiums_array,
                        "Driver": results_driver_array,
                        "Constructor": results_constructor_array,
                        "Grand Prix": results_race_array
                    }
                )

                total_podiums_chart = alt.Chart(total_podiums_data).mark_line(size=5).encode(
                    alt.X('Round', sort='ascending').scale(zero=False),
                    alt.Y('Total Podiums').scale(zero=False),
                    color='Driver',
                    tooltip=['Round', 'Grand Prix', 'Driver', 'Constructor','Total Podiums']
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

                st.altair_chart(total_podiums_chart, use_container_width=True)

                ######### Wins Development #########

                st.header("Wins Development")

                total_wins_data = pd.DataFrame(
                    {
                        "Round": results_round_array,
                        "Total Wins": results_total_wins_array,
                        "Driver": results_driver_array,
                        "Constructor": results_constructor_array,
                        "Grand Prix": results_race_array
                    }
                )

                total_wins_chart = alt.Chart(total_wins_data).mark_line(size=5).encode(
                    alt.X('Round', sort='ascending').scale(zero=False),
                    alt.Y('Total Wins').scale(zero=False),
                    color='Driver',
                    tooltip=['Round', 'Grand Prix', 'Driver', 'Constructor','Total Wins']
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

                st.altair_chart(total_wins_chart, use_container_width=True)

                ######### Fastest Laps Development #########

                st.header("Fastest Laps Development")

                total_fastest_laps_data = pd.DataFrame(
                    {
                        "Round": results_round_array,
                        "Total Fastest Laps": results_total_fastest_laps_array,
                        "Driver": results_driver_array,
                        "Constructor": results_constructor_array,
                        "Grand Prix": results_race_array
                    }
                )

                total_fastest_laps_chart = alt.Chart(total_fastest_laps_data).mark_line(size=5).encode(
                    alt.X('Round', sort='ascending').scale(zero=False),
                    alt.Y('Total Fastest Laps').scale(zero=False),
                    color='Driver',
                    tooltip=['Round', 'Grand Prix', 'Driver', 'Constructor','Total Fastest Laps']
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

                st.altair_chart(total_fastest_laps_chart, use_container_width=True)

            ######### Qualifying Results #########
            if st.session_state.view_options == "Qualifying":
                # Create a container that can be emptied
                progress_container = st.empty()

                with progress_container:
                    with st.status(label="Fetching Qualifying Data... 🔄", expanded=False, state="running") as status:
                        st.session_state.qualifying_array = get_qualifying_data(st.session_state.selected_year)
                    progress_container.empty()

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
                qualifying_constructor_array = []
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

                for constructor in selected_qualifying_info:
                    qualifying_constructor_array.append(constructor["constructor"])

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
                        "Constructor": qualifying_constructor_array,
                        "Grand Prix": qualifying_race_array
                    }
                )

                qualifying_chart = alt.Chart(qualifying_data).mark_line(size=5).encode(
                    alt.X('Round', sort='ascending').scale(zero=False),
                    alt.Y('Position').scale(zero=False),
                    color='Driver',
                    tooltip=['Round', 'Grand Prix', 'Driver', 'Constructor', 'Position']
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
                        "Constructor": qualifying_constructor_array,
                        "Q1 Lap Time": q1_lap_time_array,
                        "Fastest Q1 Lap Time": fastest_q1_time_array,
                        "Grand Prix": qualifying_race_array
                    }
                )

                q1_chart = alt.Chart(q1_data).mark_line(size=5).encode(
                    alt.X('Round', sort='ascending').scale(zero=False),
                    alt.Y('Difference (sec)').scale(zero=False),
                    color='Driver',
                    tooltip=['Round', 'Grand Prix', 'Driver', 'Constructor', 'Q1 Lap Time', "Fastest Q1 Lap Time", "Difference (sec)"]
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
                        "Constructor": qualifying_constructor_array,
                        "Q2 Lap Time": q2_lap_time_array,
                        "Fastest Q2 Lap Time": fastest_q2_time_array,
                        "Grand Prix": qualifying_race_array
                    }
                )

                q2_chart = alt.Chart(q2_data).mark_line(size=5).encode(
                    alt.X('Round', sort='ascending').scale(zero=False),
                    alt.Y('Difference (sec)').scale(zero=False),
                    color='Driver',
                    tooltip=['Round', 'Grand Prix', 'Driver', 'Constructor', 'Q2 Lap Time', "Fastest Q2 Lap Time",  "Difference (sec)"]
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
                        "Constructor": qualifying_constructor_array,
                        "Q3 Lap Time": q3_lap_time_array,
                        "Fastest Q3 Lap Time": fastest_q3_time_array,
                        "Grand Prix": qualifying_race_array
                    }
                )

                q3_chart = alt.Chart(q3_data).mark_line(size=5).encode(
                    alt.X('Round', sort='ascending').scale(zero=False),
                    alt.Y('Difference (sec)').scale(zero=False),
                    color='Driver',
                    tooltip=['Round', 'Grand Prix', 'Driver', 'Constructor', 'Q3 Lap Time', "Fastest Q3 Lap Time", "Difference (sec)"]
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

            ######### Sprint #########
            if st.session_state.view_options == "Sprints":
                # Create a container that can be emptied
                progress_container = st.empty()

                with progress_container:
                    with st.status(label="Fetching Sprints Data... 🔄", expanded=False, state="running") as status:
                        st.session_state.results_array = get_results_data(st.session_state.selected_year)
                    progress_container.empty()

                selected_sprint_info = []

                for selected in selected_drivers:
                    selected = selected.strip()  
                    for results_info in st.session_state.results_array:
                        if results_info["sprint_date"]:
                            full_name = f"{results_info['given_name']} {results_info['family_name']}".strip()
                            if selected == full_name: 
                                if results_info["sprint_status"]:
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
                                    sprint_position = results_info["sprint_position"]
                                    sprint_points = results_info["sprint_points"]
                                    sprint_status = results_info["sprint_status"]
                                    sprint_date = results_info["sprint_date"]

                                    selected_sprint_info.append({"driver": selected, 
                                                            "constructor": constructor, 
                                                            "position": position,
                                                            "status": status,
                                                            "season": season,
                                                            "round": round, 
                                                            "race_name": race_name, 
                                                            "race_points": race_points,
                                                            "total_points": total_points,
                                                            "circuit_name": circuit_name,
                                                            "date": date,
                                                            "sprint_position": sprint_position,
                                                            "sprint_points": sprint_points,
                                                            "sprint_status": sprint_status,
                                                            "sprint_date": sprint_date}
                                                            )
                                                            
                sprint_results_round_array = []
                sprint_results_status_array = []
                sprint_results_driver_array = []
                sprint_results_constructor_array = []
                sprint_results_race_array = []
                sprint_results_points_array = []
                sprint_results_array = []

                for sprint_round in selected_sprint_info:
                    sprint_results_round_array.append(int(sprint_round["round"]))

                for sprint_status in selected_sprint_info:
                    sprint_results_status_array.append(sprint_status["sprint_status"])

                for driver in selected_sprint_info:
                    sprint_results_driver_array.append(driver["driver"])

                for constructor in selected_sprint_info:
                    sprint_results_constructor_array.append(constructor["constructor"])

                for sprint_race in selected_sprint_info:
                    sprint_results_race_array.append(sprint_race["race_name"])
                
                for sprint_points in selected_sprint_info:
                    sprint_results_points_array.append(int(sprint_points["sprint_points"]))

                for sprint_position in selected_sprint_info:
                    if sprint_position["sprint_position"] is not None:
                        sprint_results_array.append(int(sprint_position["sprint_position"]))
                    else:
                        sprint_results_array.append(None)

                st.header("Sprint Results")

                sprint_results_data = pd.DataFrame(
                    {
                        "Round": sprint_results_round_array,
                        "Position": sprint_results_array,
                        "Driver": sprint_results_driver_array,
                        "Constructor": sprint_results_constructor_array,
                        "Status": sprint_results_status_array,
                        "Grand Prix": sprint_results_race_array,
                        "Points": sprint_results_points_array
                    }
                )

                unique_rounds = sorted(sprint_results_data['Round'].unique())

                sprint_results_chart = alt.Chart(sprint_results_data).mark_line(size=5).encode(
                    alt.X('Round', sort='ascending',axis=alt.Axis(values=unique_rounds)).scale(zero=False),
                    alt.Y('Position').scale(zero=False),
                    color='Driver',
                    tooltip=['Round', 'Grand Prix', 'Driver', 'Constructor', 'Position', 'Points', 'Status']
                ).interactive(
                ).properties(
                    height=600
                ).configure(
                    background='#ffffff'
                ).configure_axis(
                    labelFontSize=16,
                    titleFontSize=18,
                    labelAngle=0
                ).configure_title(
                    fontSize=20  
                )

                st.altair_chart(sprint_results_chart, use_container_width=True)

        views()

main()