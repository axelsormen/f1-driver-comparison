import requests
import xml.etree.ElementTree as ET
from functions.time_converter import time_to_seconds 

def get_qualifying_data(year):
    qualifying_array = []

    # Loop through all races (for example, 24 races for the season)
    for i in range(1, 25):  # Assuming there are 24 rounds for the season
        # API endpoint for qualifying {year}
        qualifying_api = f"http://ergast.com/api/f1/{year}/{i}/qualifying"
        
        # Make the API request
        qualifying_response = requests.get(qualifying_api)

        # Check if the request was successful (status code 200)
        if qualifying_response.status_code == 200:
            namespace = {"": "http://ergast.com/mrd/1.5"}  # Default namespace for the XML

            # Parse the XML response
            root = ET.fromstring(qualifying_response.text)

            if int(root.attrib['total']) == 0:
                break

            # Extract each qualifying data entry from the XML
            for race in root.findall('.//Race', namespace):  
                season = race.get('season') 
                round_number = race.get('round') 

                # Extract race name and circuit details
                race_name = race.find('.//RaceName', namespace).text if race.find('.//RaceName', namespace) is not None else None
                circuit_name = race.find('.//CircuitName', namespace).text if race.find('.//CircuitName', namespace) is not None else None
                date = race.find('.//Date', namespace).text if race.find('.//Date', namespace) is not None else None

                # Extract qualifying results
                qualifying_results = race.findall('.//QualifyingResult', namespace)

                for result in qualifying_results:
                    position = result.get('position') 

                    driver = result.find('.//Driver', namespace)

                    if driver is not None:
                        given_name = driver.find('GivenName', namespace).text if driver.find('GivenName', namespace) is not None else None
                        family_name = driver.find('FamilyName', namespace).text if driver.find('FamilyName', namespace) is not None else None

                    constructor = result.find('.//Constructor', namespace)
                    if constructor is not None:
                        constructor_name = constructor.find('Name', namespace).text if constructor.find('Name', namespace) is not None else None

                    # Extract the Q1, Q2, and Q3 times
                    q1 = result.find('.//Q1', namespace).text if result.find('.//Q1', namespace) is not None else None
                    q2 = result.find('.//Q2', namespace).text if result.find('.//Q2', namespace) is not None else None
                    q3 = result.find('.//Q3', namespace).text if result.find('.//Q3', namespace) is not None else None

                    q1_sec = time_to_seconds(q1)
                    q2_sec = time_to_seconds(q2)
                    q3_sec = time_to_seconds(q3)

                    # Append the collected data to the qualifying_array
                    qualifying_array.append({
                        "given_name": given_name,
                        "family_name": family_name,
                        "constructor_name": constructor_name,
                        "position": position,
                        "q1": q1,
                        "q1_sec": q1_sec,
                        "q2": q2,
                        "q2_sec": q2_sec,
                        "q3": q3,
                        "q3_sec": q3_sec,
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
        q1_seconds = entry["q1_sec"]

        if q1_seconds != float('inf'):
            if round_number not in fastest_q1_dict or q1_seconds < fastest_q1_dict[round_number]["q1_seconds"]:
                fastest_q1_dict[round_number] = {
                    "fastest_q1": q1_time,
                    "q1_seconds": q1_seconds
                }

    for entry in qualifying_array:
        round_number = entry["round"]
        
        if str(round_number) in fastest_q1_dict:
            entry["fastest_q1_time"] = fastest_q1_dict[str(round_number)]["fastest_q1"] 
            if entry["q1_sec"] == float('inf'):
                entry["difference_fastest_q1_time"] = None
            else:
                entry["difference_fastest_q1_time"] = entry["q1_sec"] - fastest_q1_dict[str(round_number)]["q1_seconds"]
        else:
            entry["difference_fastest_q1_time"] = None

    ####### Q2 difference #######
            
    fastest_q2_dict = {}

    for entry in qualifying_array:
        round_number = entry["round"]
        q2_time = entry["q2"]
        q2_seconds = entry["q2_sec"]

        if q2_seconds != float('inf'):
            if round_number not in fastest_q2_dict or q2_seconds < fastest_q2_dict[round_number]["q2_seconds"]:
                fastest_q2_dict[round_number] = {
                    "fastest_q2": q2_time,
                    "q2_seconds": q2_seconds
                }

    for entry in qualifying_array:
        round_number = entry["round"]
        
        if str(round_number) in fastest_q2_dict:
            entry["fastest_q2_time"] = fastest_q2_dict[str(round_number)]["fastest_q2"] 
            if entry["q2_sec"] == float('inf'):
                entry["difference_fastest_q2_time"] = None
            else:
                entry["difference_fastest_q2_time"] = entry["q2_sec"] - fastest_q2_dict[str(round_number)]["q2_seconds"]
        else:
            entry["difference_fastest_q2_time"] = None

    ####### Q3 difference #######
            
    fastest_q3_dict = {}

    for entry in qualifying_array:
        round_number = entry["round"]
        q3_time = entry["q3"]
        q3_seconds = entry["q3_sec"]

        if q3_seconds != float('inf'):
            if round_number not in fastest_q3_dict or q3_seconds < fastest_q3_dict[round_number]["q3_seconds"]:
                fastest_q3_dict[round_number] = {
                    "fastest_q3": q3_time,
                    "q3_seconds": q3_seconds
                }

    for entry in qualifying_array:
        round_number = entry["round"]
        
        if str(round_number) in fastest_q3_dict:
            entry["fastest_q3_time"] = fastest_q3_dict[str(round_number)]["fastest_q3"] 
            if entry["q3_sec"] == float('inf'):
                entry["difference_fastest_q3_time"] = None
            else:
                entry["difference_fastest_q3_time"] = entry["q3_sec"] - fastest_q3_dict[str(round_number)]["q3_seconds"]
        else:
            entry["difference_fastest_q3_time"] = None 

    return qualifying_array
