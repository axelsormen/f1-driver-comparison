import requests
import xml.etree.ElementTree as ET

def get_standings_data(year):
    standings_array = []

    # API endpoint for standings {year} season
    standings_api = f"http://ergast.com/api/f1/{year}/driverStandings"

    # Make the API request
    standings_response = requests.get(standings_api)

    # Check if the request was successful (status code 200)
    if standings_response.status_code == 200:
        namespace = {"": "http://ergast.com/mrd/1.5"}  # Default namespace for the XML

        # Parse the XML response
        root = ET.fromstring(standings_response.text)

        # Extract each driver from the XML and get their full name along with position
        for standing in root.findall('.//DriverStanding', namespace):  
            position = standing.get('position') 
            points = standing.get('points')
            wins = standing.get('wins')
            
            driver = standing.find('.//Driver', namespace) 

            if driver is not None:
                given_name = driver.find('GivenName', namespace).text if driver.find('GivenName', namespace) is not None else None
                family_name = driver.find('FamilyName', namespace).text if driver.find('FamilyName', namespace) is not None else None

            constructor = standing.find('.//Constructor', namespace) 

            if constructor is not None:
                constructor_name = constructor.find('Name', namespace).text if constructor.find('Name', namespace) is not None else None
                
            standings_array.append({
                "given_name": given_name, 
                "family_name": family_name, 
                "constructor_name": constructor_name,
                "position": position, 
                "points": points, 
                "wins": wins
            })

    else:
        print(f"Failed to retrieve driver standings.")
    
    return standings_array
