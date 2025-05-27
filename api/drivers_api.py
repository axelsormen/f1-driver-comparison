import requests
import streamlit as st
import xml.etree.ElementTree as ET

def get_drivers_data(year):
    drivers_array = []

    # API endpoint for the {year} season
    drivers_api = f"http://ergast.com/api/f1/{year}/drivers"

    # Make the API request
    drivers_response = requests.get(drivers_api)

    # Check if the request was successful (status code 200)
    if drivers_response.status_code == 200:
        # Define the namespace for the XML
        namespace = {"": "http://ergast.com/mrd/1.5"}  # Default namespace (empty prefix)
        
        # Parse the XML response
        root = ET.fromstring(drivers_response.text)

        # Extract each driver from the XML and get their full name
        for driver in root.findall('.//Driver', namespace): 

            given_name = driver.find('GivenName', namespace).text
            family_name = driver.find('FamilyName', namespace).text

            # Append the driver info to the list
            if given_name and family_name:  
                drivers_array.append({"given_name": given_name, "family_name": family_name})    
    else:
        st.error("Failed to retrieve data. Please try again later.")

    return drivers_array
