import requests
import streamlit as st
import xml.etree.ElementTree as ET

def get_drivers_data():
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
            driver_id = driver.get('driverId')  # Use .get('driverId') for attributes

            given_name = driver.find('GivenName', namespace).text
            family_name = driver.find('FamilyName', namespace).text

            # Append the driver info to the list
            if driver_id and given_name and family_name:  # Ensure the values exist before appending
                drivers_array.append({"driver_id": driver_id, "given_name": given_name, "family_name": family_name})    
    else:
        st.error("Failed to retrieve data. Please try again later.")

    return drivers_array
