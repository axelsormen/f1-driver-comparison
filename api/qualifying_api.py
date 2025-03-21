import requests
import pandas as pd
import streamlit as st
import xml.etree.ElementTree as ET
from functions.time_converter import time_to_milliseconds 

def get_qualifying_data():
    qualifying_array = []

    # Loop through all races (for example, 24 races for the season)
    for i in range(1, 25):  # Assuming there are 24 rounds for the season
        # API endpoint for qualifying 2024
        qualifying_api = f"http://ergast.com/api/f1/2024/{i}/qualifying"
        
        # Make the API request
        qualifying_response = requests.get(qualifying_api)

        # Check if the request was successful (status code 200)
        if qualifying_response.status_code == 200:
            namespace = {"": "http://ergast.com/mrd/1.5"}  # Default namespace for the XML

            # Parse the XML response
            root = ET.fromstring(qualifying_response.text)

            # Extract each qualifying data entry from the XML
            for race in root.findall('.//Race', namespace):  
                season = race.get('season') 
                round_number = race.get('round') 

                # Extract race name and circuit details
                race_name = race.find('.//RaceName', namespace).text if race.find('.//RaceName', namespace) is not None else 'N/A'
                circuit_name = race.find('.//CircuitName', namespace).text if race.find('.//CircuitName', namespace) is not None else 'N/A'
                date = race.find('.//Date', namespace).text if race.find('.//Date', namespace) is not None else 'N/A'

                # Extract qualifying results
                qualifying_results = race.findall('.//QualifyingResult', namespace)

                for result in qualifying_results:
                    position = result.get('position') 

                    driver = result.find('.//Driver', namespace)

                    if driver is not None:
                        given_name = driver.find('GivenName', namespace).text if driver.find('GivenName', namespace) is not None else 'N/A'
                        family_name = driver.find('FamilyName', namespace).text if driver.find('FamilyName', namespace) is not None else 'N/A'

                    constructor = result.find('.//Constructor', namespace)
                    if constructor is not None:
                        constructor_name = constructor.find('Name', namespace).text if constructor.find('Name', namespace) is not None else 'N/A'

                    # Extract the Q1, Q2, and Q3 times
                    q1 = result.find('.//Q1', namespace).text if result.find('.//Q1', namespace) is not None else 'N/A'
                    q2 = result.find('.//Q2', namespace).text if result.find('.//Q2', namespace) is not None else 'N/A'
                    q3 = result.find('.//Q3', namespace).text if result.find('.//Q3', namespace) is not None else 'N/A'

                    q1_ms = time_to_milliseconds(q1)
                    q2_ms = time_to_milliseconds(q2)
                    q3_ms = time_to_milliseconds(q3)

                    # Append the collected data to the qualifying_array
                    qualifying_array.append({
                        "given_name": given_name,
                        "family_name": family_name,
                        "constructor_name": constructor_name,
                        "position": position,
                        "q1": q1,
                        "q1_ms": q1_ms,
                        "q2": q2,
                        "q2_ms": q2_ms,
                        "q3": q3,
                        "q3_ms": q3_ms,
                        "season": season,
                        "round": round_number,
                        "race_name": race_name,
                        "circuit_name": circuit_name,
                        "date": date
                    })
        else:
            print(f"Failed to retrieve data for round {i}.")
            continue  # Continue to next round if request failed

    ####### Q1 difference #######
        
    fastest_q1_dict = {}

    for entry in qualifying_array:
        round_number = entry["round"]
        q1_time = entry["q1"]
        q1_milliseconds = entry["q1_ms"]

        if q1_milliseconds != float('inf'):
            if round_number not in fastest_q1_dict or q1_milliseconds < fastest_q1_dict[round_number]["q1_milliseconds"]:
                fastest_q1_dict[round_number] = {
                    "fastest_q1": q1_time,
                    "q1_milliseconds": q1_milliseconds
                }

    for entry in qualifying_array:
        round_number = entry["round"]
        
        if str(round_number) in fastest_q1_dict:
            entry["best_q1_time"] = fastest_q1_dict[str(round_number)]["fastest_q1"] 
            if entry["q1_ms"] == float('inf'):
                entry["difference_best_q1_time"] = "N/A" 
            else:
                entry["difference_best_q1_time"] = entry["q1_ms"] - fastest_q1_dict[str(round_number)]["q1_milliseconds"] 
        else:
            entry["difference_best_q1_time"] = "N/A" 

    ####### Q2 difference #######
            
    fastest_q2_dict = {}

    for entry in qualifying_array:
        round_number = entry["round"]
        q2_time = entry["q2"]
        q2_milliseconds = entry["q2_ms"]

        if q2_milliseconds != float('inf'):
            if round_number not in fastest_q2_dict or q2_milliseconds < fastest_q2_dict[round_number]["q2_milliseconds"]:
                fastest_q2_dict[round_number] = {
                    "fastest_q2": q2_time,
                    "q2_milliseconds": q2_milliseconds
                }

    for entry in qualifying_array:
        round_number = entry["round"]
        
        if str(round_number) in fastest_q2_dict:
            entry["best_q2_time"] = fastest_q2_dict[str(round_number)]["fastest_q2"] 
            if entry["q2_ms"] == float('inf'):
                entry["difference_best_q2_time"] = "N/A" 
            else:
                entry["difference_best_q2_time"] = entry["q2_ms"] - fastest_q2_dict[str(round_number)]["q2_milliseconds"]
        else:
            entry["difference_best_q2_time"] = "N/A" 

    ####### Q3 difference #######
            
    fastest_q3_dict = {}

    for entry in qualifying_array:
        round_number = entry["round"]
        q3_time = entry["q3"]
        q3_milliseconds = entry["q3_ms"]

        if q3_milliseconds != float('inf'):
            if round_number not in fastest_q3_dict or q3_milliseconds < fastest_q3_dict[round_number]["q3_milliseconds"]:
                fastest_q3_dict[round_number] = {
                    "fastest_q3": q3_time,
                    "q3_milliseconds": q3_milliseconds
                }

    for entry in qualifying_array:
        round_number = entry["round"]
        
        if str(round_number) in fastest_q3_dict:
            entry["best_q3_time"] = fastest_q3_dict[str(round_number)]["fastest_q3"] 
            if entry["q3_ms"] == float('inf'):
                entry["difference_best_q3_time"] = "N/A" 
            else:
                entry["difference_best_q3_time"] = entry["q3_ms"] - fastest_q3_dict[str(round_number)]["q3_milliseconds"]
        else:
            entry["difference_best_q3_time"] = "N/A" 

    print(qualifying_array)

    return qualifying_array
