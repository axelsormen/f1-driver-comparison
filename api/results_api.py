import requests
import streamlit as st
import xml.etree.ElementTree as ET

def get_results_data():
    results_array = []
    driver_points = {} 
    driver_wins = {} 
    driver_podiums = {}
    driver_top10_finishes = {}
    driver_fastest_laps = {}

    # Loop through all races (for example, 24 races for the season)
    for i in range(1, 25):  # Assuming there are 24 rounds for the season
        # API endpoints for results 2024
        results_api = f"http://ergast.com/api/f1/2024/{i}/results"
        sprint_results_api = f"http://ergast.com/api/f1/2024/{i}/sprint"

        # Make the API requests
        results_response = requests.get(results_api)
        sprint_results_response = requests.get(sprint_results_api)

        # Check if the request was successful (status code 200)
        if sprint_results_response.status_code == 200 and results_response.status_code == 200:
            namespace = {"": "http://ergast.com/mrd/1.5"}  # Default namespace for the XML

            # Parse the XML response for race results
            race_root = ET.fromstring(results_response.text)

            # Extract each results data entry from the XML
            for race in race_root.findall('.//Race', namespace):  
                season = race.get('season')  
                round_number = race.get('round')  

                # Extract race name and circuit details
                race_name = race.find('.//RaceName', namespace).text if race.find('.//RaceName', namespace) is not None else None
                circuit_name = race.find('.//CircuitName', namespace).text if race.find('.//CircuitName', namespace) is not None else None
                date = race.find('.//Date', namespace).text if race.find('.//Date', namespace) is not None else None

                # Extract results
                results = race.findall('.//Result', namespace)

                for result in results:
                    status = result.find('Status', namespace).text if result.find('Status', namespace) is not None else None
                    position = result.get('position') if result.get('position') is not None else None

                    win = 0
                    podium = 0
                    top10_finish = 0

                    if int(position) == 1:
                        win = 1
                        podium = 1
                        top10_finish = 1

                    elif int(position) <= 3 : 
                        podium = 1
                        top10_finish = 1

                    elif int(position) <= 10: 
                        top10_finish = 1

                    fastest_lap_result = result.find('.//FastestLap', namespace)

                    if fastest_lap_result is not None:
                        fastest_lap_rank = fastest_lap_result.get('rank') 

                    if int(fastest_lap_rank) == 1:
                        fastest_lap = 1
                    else:
                        fastest_lap = 0

                    points = float(result.get('points', 0)) 
                    driver = result.find('.//Driver', namespace)

                    if driver is not None:
                        given_name = driver.find('GivenName', namespace).text if driver.find('GivenName', namespace) is not None else None
                        family_name = driver.find('FamilyName', namespace).text if driver.find('FamilyName', namespace) is not None else None

                    constructor = result.find('.//Constructor', namespace)
                    if constructor is not None:
                        constructor_name = constructor.find('Name', namespace).text if constructor.find('Name', namespace) is not None else None

                    # Update the total points for the driver
                    driver_key = f"{given_name} {family_name}"
                    if driver_key not in driver_points:
                        driver_points[driver_key] = 0  
                    driver_points[driver_key] += points  

                    # Update the total wins for the driver
                    driver_key = f"{given_name} {family_name}"
                    if driver_key not in driver_wins:
                        driver_wins[driver_key] = 0  
                    driver_wins[driver_key] += win  

                    # Update the total podiums for the driver
                    driver_key = f"{given_name} {family_name}"
                    if driver_key not in driver_podiums:
                        driver_podiums[driver_key] = 0  
                    driver_podiums[driver_key] += podium  

                    # Update the total top 10 finishes for the driver
                    driver_key = f"{given_name} {family_name}"
                    if driver_key not in driver_top10_finishes:
                        driver_top10_finishes[driver_key] = 0  
                    driver_top10_finishes[driver_key] += top10_finish  

                    # Update the total fastest lap for the driver
                    driver_key = f"{given_name} {family_name}"
                    if driver_key not in driver_fastest_laps:
                        driver_fastest_laps[driver_key] = 0  
                    driver_fastest_laps[driver_key] += fastest_lap  

                    # Append the collected race data to the results_array with total_points
                    results_array.append({
                        "given_name": given_name,
                        "family_name": family_name,
                        "constructor_name": constructor_name,
                        "position": position,
                        "win": win,
                        "podium": podium,
                        "top10_finish": top10_finish,
                        "points": points,
                        "status": status,
                        "fastest_lap_rank": fastest_lap_rank,
                        "season": season,
                        "round": round_number,
                        "race_name": race_name,
                        "circuit_name": circuit_name,
                        "date": date,
                        "sprint_position": None, 
                        "sprint_points": None,
                        "sprint_status": None,
                        "sprint_date": None,
                        "total_points": driver_points[driver_key], 
                        "total_wins": driver_wins[driver_key], 
                        "total_podiums": driver_podiums[driver_key], 
                        "total_top10_finishes": driver_top10_finishes[driver_key], 
                        "total_fastest_laps": driver_fastest_laps[driver_key]
                    })

            # Parse the XML response for sprint results
            sprint_root = ET.fromstring(sprint_results_response.text)

            # Extract each sprint results data entry from the XML
            for sprint in sprint_root.findall('.//Race', namespace):  
                round_number = sprint.get('round')  

                # Extract race name and circuit details
                race_name = sprint.find('.//RaceName', namespace).text if sprint.find('.//RaceName', namespace) is not None else None
                circuit_name = sprint.find('.//CircuitName', namespace).text if sprint.find('.//CircuitName', namespace) is not None else None
                sprint_date = sprint.find('.//Date', namespace).text if sprint.find('.//Date', namespace) is not None else None

                # Extract sprint results
                sprint_results = sprint.findall('.//SprintResult', namespace)

                for sprint_result in sprint_results:
                    sprint_status = sprint_result.find('Status', namespace).text if sprint_result.find('Status', namespace) is not None else None
                    sprint_position = sprint_result.get('position') if sprint_result.get('position') is not None else None

                    sprint_points = float(sprint_result.get('points', 0))  # Ensure points are treated as numbers
                    driver = sprint_result.find('.//Driver', namespace)

                    if driver is not None:
                        given_name = driver.find('GivenName', namespace).text if driver.find('GivenName', namespace) is not None else None
                        family_name = driver.find('FamilyName', namespace).text if driver.find('FamilyName', namespace) is not None else None

                    # Update the total points for the driver
                    driver_key = f"{given_name} {family_name}"
                    if driver_key not in driver_points:
                        driver_points[driver_key] = 0  # Initialize if driver not in dictionary
                    driver_points[driver_key] += sprint_points  # Add sprint points to total points

                    for result in results_array:
                        if result["round"] == round_number and f"{result['given_name']} {result['family_name']}" == driver_key:
                            result["sprint_position"] = sprint_position
                            result["sprint_points"] = sprint_points
                            result["sprint_status"] = sprint_status
                            result["sprint_date"] = sprint_date
                            result["total_points"] = driver_points[driver_key]

        else:
            print(f"Failed to retrieve data for round {i}.")
            continue  # Continue to next round if request failed
    
    return results_array
