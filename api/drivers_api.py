import requests
import streamlit as st
import xml.etree.ElementTree as ET
import time

cache = {}

def get_drivers_data(year):
    if year in cache:
        return cache[year]

    start_time = time.time()

    drivers_array = []

    # API endpoint for the {year} season
    drivers_url = f"https://api.jolpi.ca/ergast/f1/{year}/drivers/"

    # Make the API request
    drivers_response = requests.get(drivers_url)

    # Check if the request was successful (status code 200)
    if drivers_response.status_code == 200:
        data = drivers_response.json()
        drivers = data['MRData']['DriverTable']['Drivers']

        for driver in drivers:
            given_name = driver.get('givenName')
            family_name = driver.get('familyName')

            # Append the driver info to the list
            if given_name and family_name:  
                drivers_array.append({"given_name": given_name, "family_name": family_name})    
    else:
        st.error("Failed to retrieve data. Please try again later.")

    cache[year] = drivers_array
    
    end_time = time.time()
    print(f"Drivers API time: {end_time - start_time:.2f} seconds")
   
    return drivers_array