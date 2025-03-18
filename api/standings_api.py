import requests
import streamlit as st
import xml.etree.ElementTree as ET

def get_standings_data():

    # API endpoint for standings 2024 season
    standings_api = "http://ergast.com/api/f1/2024/driverStandings"

    # Make the API request
    standings_response = requests.get(standings_api)

    standings_array = []

    # Check if the request was successful (status code 200)
    if standings_response.status_code == 200:
        namespace = {"": "http://ergast.com/mrd/1.5"}  # Default namespace for the XML

        # Parse the XML response
        root = ET.fromstring(standings_response.text)

        # Extract each driver from the XML and get their full name along with position
        for standing in root.findall('.//DriverStanding', namespace):  
            position = standing.get('position')  # Extract position as an attribute
            points = standing.get('points')
            wins = standing.get('wins')
            
            driver = standing.find('.//Driver', namespace)  # Find the driver element within DriverStanding

            if driver is not None:
                driver_id = driver.find('driverId', namespace).text if driver.find('driverId', namespace) is not None else 'N/A'
                given_name = driver.find('GivenName', namespace).text if driver.find('GivenName', namespace) is not None else 'N/A'
                family_name = driver.find('FamilyName', namespace).text if driver.find('FamilyName', namespace) is not None else 'N/A'

            constructor = standing.find('.//Constructor', namespace) 

            if constructor is not None:
                constructor_id = driver.find('constructorId', namespace).text if driver.find('constructorId', namespace) is not None else 'N/A'
                constructor_name = constructor.find('Name', namespace).text if constructor.find('Name', namespace) is not None else 'N/A'
                
            standings_array.append({
                "driver_id": driver_id, 
                "given_name": given_name, 
                "family_name": family_name, 
                "constructor_id": constructor_id,
                "constructor_name": constructor_name,
                "position": position, 
                "points": points, 
                "wins": wins
            })

    else:
        st.error("Failed to retrieve data. Please try again later.")

    return standings_array
