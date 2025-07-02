import requests
import time
import streamlit as st

cache = {}

def get_standings_data(year):
    if year in cache:
        return cache[year]
    
    start_time = time.time()

    standings_array = []

    # API endpoint for standings {year} season
    standings_url = f"https://api.jolpi.ca/ergast/f1/{year}/driverstandings/"
    
    # Make the API request
    standings_response = requests.get(standings_url)

    # Check if the request was successful (status code 200)
    if standings_response.status_code == 200:
        st.write(standings_response.text)

        data = standings_response.json()
        standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

        for standing in standings:
            position = standing.get('position')
            points = standing.get('points')
            wins = standing.get('wins')

            driver = standing.get('Driver', {})
            given_name = driver.get('givenName')
            family_name = driver.get('familyName')

            constructors = standing.get('Constructors', [])
            constructor_name = constructors[0]['name'] if constructors else None

            standings_array.append({
                "given_name": given_name,
                "family_name": family_name,
                "constructor_name": constructor_name,
                "position": position,
                "points": points,
                "wins": wins
            })
        
        st.write(standings_array)

    else:
        st.error("Failed to retrieve data. Please try again later.")
    
    cache[year] = standings_array

    end_time = time.time()
    print(f"Standings API time: {end_time - start_time:.2f} seconds")

    return standings_array