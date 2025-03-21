import requests
import streamlit as st
import xml.etree.ElementTree as ET

def get_results_data():
    results_array = []

    # Loop through all races (for example, 24 races for the season)
    for i in range(1, 25):  # Assuming there are 24 rounds for the season
        # API endpoint for results 2024
        results_api = f"http://ergast.com/api/f1/2024/{i}/results"
        
        # Make the API request
        results_response = requests.get(results_api)

        # Check if the request was successful (status code 200)
        if results_response.status_code == 200:
            namespace = {"": "http://ergast.com/mrd/1.5"}  # Default namespace for the XML

            # Parse the XML response
            root = ET.fromstring(results_response.text)

            # Extract each results data entry from the XML
            for race in root.findall('.//Race', namespace):  
                season = race.get('season')  
                round_number = race.get('round')  

                # Extract race name and circuit details
                race_name = race.find('.//RaceName', namespace).text if race.find('.//RaceName', namespace) is not None else 'N/A'
                circuit_name = race.find('.//CircuitName', namespace).text if race.find('.//CircuitName', namespace) is not None else 'N/A'
                date = race.find('.//Date', namespace).text if race.find('.//Date', namespace) is not None else 'N/A'

                # Extract results
                results = race.findall('.//Result', namespace)

                for result in results:
                    position = result.get('position') 
                    points = result.get('points') 
                    status = result.find('.//Status', namespace)

                    driver = result.find('.//Driver', namespace)

                    if driver is not None:
                        given_name = driver.find('GivenName', namespace).text if driver.find('GivenName', namespace) is not None else 'N/A'
                        family_name = driver.find('FamilyName', namespace).text if driver.find('FamilyName', namespace) is not None else 'N/A'

                    constructor = result.find('.//Constructor', namespace)
                    if constructor is not None:
                        constructor_name = constructor.find('Name', namespace).text if constructor.find('Name', namespace) is not None else 'N/A'

                    # Append the collected data to the qualifying_array
                    results_array.append({
                        "given_name": given_name,
                        "family_name": family_name,
                        "constructor_name": constructor_name,
                        "position": position,
                        "points": points,
                        "status": status,
                        "season": season,
                        "round": round_number,
                        "race_name": race_name,
                        "circuit_name": circuit_name,
                        "date": date
                    })
        else:
            print(f"Failed to retrieve data for round {i}.")
            continue  # Continue to next round if request failed

    return results_array
