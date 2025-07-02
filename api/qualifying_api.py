import requests
import streamlit as st
import xml.etree.ElementTree as ET
from functions.time_converter import time_to_seconds 
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

cache = {}

def fetch_qualifying(year, offset):
    qualifying_url = f"https://api.jolpi.ca/ergast/f1/{year}/qualifying?limit=30&offset={offset}"
    response = requests.get(qualifying_url)
    return response

def get_qualifying_data(year):
    if year in cache:
        return cache[year]

    start_time = time.time()

    qualifying_array = []
    all_qualifyings = []

    with ThreadPoolExecutor(max_workers=1) as executor:
        max_offset = 500
        futures = {
            executor.submit(fetch_qualifying, year, offset): offset
            for offset in range(0, max_offset + 1, 30)
        }

        for future in as_completed(futures):
            qualifying_response = future.result()
            if qualifying_response.status_code == 200:
                races = qualifying_response.json()['MRData']['RaceTable']['Races']
                if not races:
                    continue
                all_qualifyings.extend(races)

    # Sort races by round
    all_qualifyings.sort(key=lambda r: int(r['round']))

    for qualifying in all_qualifyings:
        season = qualifying.get('season') 
        round_number = qualifying.get('round') 

        # Extract race name and circuit details
        race_name = qualifying.get('raceName')
        circuit_name = qualifying.get('Circuit').get('circuitName')
        date = qualifying.get('date')
                               
        # Extract qualifying results
        qualifying_results = qualifying.get('QualifyingResults')

        if qualifying_results is None:
            continue 

        for result in qualifying_results:
            position = result.get('position') 

            driver = result.get('Driver')

            if driver is not None:
                given_name = driver.get('givenName')
                family_name = driver.get('familyName')
                                          
            constructor = result.get('Constructor')
            if constructor is not None:
                constructor_name = constructor.get('name')

            # Extract the Q1, Q2, and Q3 times
            q1 = result.get('Q1')
            q2 = result.get('Q2')
            q3 = result.get('Q3')

            q1_sec = time_to_seconds(q1)
            q2_sec = time_to_seconds(q2)
            q3_sec = time_to_seconds(q3)

            # Append the collected data to the qualifying_array
            qualifying_array.append({
                "given_name": given_name,
                "family_name": family_name,
                "constructor_name": constructor_name,
                "position": position,
                "q1": q1,
                "q1_sec": q1_sec,
                "q2": q2,
                "q2_sec": q2_sec,
                "q3": q3,
                "q3_sec": q3_sec,
                "season": season,
                "round": round_number,
                "race_name": race_name,
                "circuit_name": circuit_name,
                "date": date
            })

    ####### Q1 difference #######
        
    fastest_q1_dict = {}

    for entry in qualifying_array:
        round_number = entry["round"]
        q1_time = entry["q1"]
        q1_seconds = entry["q1_sec"]

        if q1_seconds != float('inf'):
            if round_number not in fastest_q1_dict or q1_seconds < fastest_q1_dict[round_number]["q1_seconds"]:
                fastest_q1_dict[round_number] = {
                    "fastest_q1": q1_time,
                    "q1_seconds": q1_seconds
                }

    for entry in qualifying_array:
        round_number = entry["round"]
        
        if str(round_number) in fastest_q1_dict:
            entry["fastest_q1_time"] = fastest_q1_dict[str(round_number)]["fastest_q1"] 
            if entry["q1_sec"] == float('inf'):
                entry["difference_fastest_q1_time"] = None
            else:
                entry["difference_fastest_q1_time"] = entry["q1_sec"] - fastest_q1_dict[str(round_number)]["q1_seconds"]
        else:
            entry["difference_fastest_q1_time"] = None

    ####### Q2 difference #######
            
    fastest_q2_dict = {}

    for entry in qualifying_array:
        round_number = entry["round"]
        q2_time = entry["q2"]
        q2_seconds = entry["q2_sec"]

        if q2_seconds != float('inf'):
            if round_number not in fastest_q2_dict or q2_seconds < fastest_q2_dict[round_number]["q2_seconds"]:
                fastest_q2_dict[round_number] = {
                    "fastest_q2": q2_time,
                    "q2_seconds": q2_seconds
                }

    for entry in qualifying_array:
        round_number = entry["round"]
        
        if str(round_number) in fastest_q2_dict:
            entry["fastest_q2_time"] = fastest_q2_dict[str(round_number)]["fastest_q2"] 
            if entry["q2_sec"] == float('inf'):
                entry["difference_fastest_q2_time"] = None
            else:
                entry["difference_fastest_q2_time"] = entry["q2_sec"] - fastest_q2_dict[str(round_number)]["q2_seconds"]
        else:
            entry["difference_fastest_q2_time"] = None

    ####### Q3 difference #######
            
    fastest_q3_dict = {}

    for entry in qualifying_array:
        round_number = entry["round"]
        q3_time = entry["q3"]
        q3_seconds = entry["q3_sec"]

        if q3_seconds != float('inf'):
            if round_number not in fastest_q3_dict or q3_seconds < fastest_q3_dict[round_number]["q3_seconds"]:
                fastest_q3_dict[round_number] = {
                    "fastest_q3": q3_time,
                    "q3_seconds": q3_seconds
                }

    for entry in qualifying_array:
        round_number = entry["round"]
        
        if str(round_number) in fastest_q3_dict:
            entry["fastest_q3_time"] = fastest_q3_dict[str(round_number)]["fastest_q3"] 
            if entry["q3_sec"] == float('inf'):
                entry["difference_fastest_q3_time"] = None
            else:
                entry["difference_fastest_q3_time"] = entry["q3_sec"] - fastest_q3_dict[str(round_number)]["q3_seconds"]
        else:
            entry["difference_fastest_q3_time"] = None 

    cache[year] = qualifying_array

    end_time = time.time()
    print(f"Qualifying API time: {end_time - start_time:.2f} seconds")
    
    return qualifying_array