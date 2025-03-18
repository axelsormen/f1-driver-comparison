import streamlit as st
import pandas as pd
from api.drivers_api import get_drivers_data
from api.standings_api import get_standings_data  # Import the function from api_requests.py

# Display the header
st.header("F1 Drivers Comparison 2024")

drivers_array = get_drivers_data()
standings_array = get_standings_data()

# Add a multiselect widget to allow users to choose drivers
selected_drivers = st.multiselect(
    'Select drivers to compare:', 
    [f"{driver['given_name']} {driver['family_name']}" for driver in drivers_array]
)   
                            
selected_drivers_info = []

# Iterate through the selected drivers
for selected in selected_drivers:
    selected = selected.strip()  # Remove any leading/trailing whitespace
    for driver_info in standings_array:
        full_name = f"{driver_info['given_name']} {driver_info['family_name']}".strip()
        if selected == full_name:  # Match the full name exactly
            position = driver_info["position"]
            points = driver_info["points"]
            wins = driver_info["wins"]
            constructor = driver_info["constructor_name"]
            # Add driver and position as a dictionary to the list
            selected_drivers_info.append({"Position": position, "Driver": selected, "Constructor": constructor, "Points": points, "Wins": wins})

# Sort the selected drivers by position (ascending order)
selected_drivers_info_sorted = sorted(selected_drivers_info, key=lambda x: int(x["Position"]))
df = pd.DataFrame(selected_drivers_info_sorted)

# Display the selected drivers and their positions in a table format
if selected_drivers_info_sorted:
    st.header("Standings:")
    st.dataframe(df.set_index(df.columns[0]))