import streamlit as st
import requests
import xml.etree.ElementTree as ET
import pandas as pd

# Display the header
st.header("F1 Drivers Comparison 2024")

# API endpoint for the 2024 season
drivers_api = "http://ergast.com/api/f1/2024/drivers"

# Make the API request
drivers_response = requests.get(drivers_api)

# Initialize the list of drivers
drivers_array = []

# Check if the request was successful (status code 200)
if drivers_response.status_code == 200:
    # Define the namespace for the XML
    namespace = {"": "http://ergast.com/mrd/1.5"}  # Default namespace (empty prefix)
    
    # Parse the XML response
    root = ET.fromstring(drivers_response.text)

    # Extract each driver from the XML and get their full name
    for driver in root.findall('.//Driver', namespace):  # Correct namespace and search path
        given_name = driver.find('GivenName', namespace).text
        family_name = driver.find('FamilyName', namespace).text

        # Combine first and last name
        full_name = f"{given_name} {family_name}"

        # Append the full name to the list
        drivers_array.append({"full name": full_name})    
else:
    st.error("Failed to retrieve data. Please try again later.")

# API endpoint for standings 2024 season
standings_api = "http://ergast.com/api/f1/2024/driverStandings"

# Make the API request
standings_response = requests.get(standings_api)

standings_array = []

# Check if the request was successful (status code 200)
if standings_response.status_code == 200:
    namespace = {"": "http://ergast.com/mrd/1.5"}  

    # Parse the XML response
    root = ET.fromstring(standings_response.text)

    # Initialize an empty list to store standings
    standings_array = []

    # Extract each driver from the XML and get their full name along with position
    for standing in root.findall('.//DriverStanding', namespace):  
        position = standing.get('position')  # Extract position as an attribute
        points = standing.get('points')
        wins = standing.get('wins')
        
        # Get the driver details nested inside DriverStanding
        driver = standing.find('.//Driver', namespace)  # Find the driver element within DriverStanding
        
        given_name = driver.find('GivenName', namespace).text
        family_name = driver.find('FamilyName', namespace).text
        full_name = f"{given_name} {family_name}"
        
        # Append the driver's full name and position to the standings array
        standings_array.append({"full name": full_name, "position": position, "points": points, "wins": wins})

else:
    st.error("Failed to retrieve data. Please try again later.")

# Add a multiselect widget to allow users to choose drivers
selected_drivers = st.multiselect('Select drivers to compare:', [driver["full name"] for driver in drivers_array])
                               
selected_drivers_info = []

# Iterate through the selected drivers
for selected in selected_drivers:
    selected = selected.strip()  # Remove any leading/trailing whitespace
    for driver_info in standings_array:
        full_name = driver_info["full name"].strip()  # Remove any leading/trailing whitespace
        if selected == full_name:  # Match the full name exactly
            position = driver_info["position"]
            points = driver_info["points"]
            wins = driver_info["wins"]
            # Add driver and position as a dictionary to the list
            selected_drivers_info.append({"Position": position, "Driver": selected, "Points": points, "Wins": wins})

# Sort the selected drivers by position (ascending order)
selected_drivers_info_sorted = sorted(selected_drivers_info, key=lambda x: int(x["Position"]))
df = pd.DataFrame(selected_drivers_info_sorted)

# Display the selected drivers and their positions in a table format
if selected_drivers_info_sorted:
    st.header("Standings:")
    st.dataframe(df.set_index(df.columns[0]))