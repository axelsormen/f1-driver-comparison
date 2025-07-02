import requests
import streamlit as st
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

cache = {}

def fetch_round_data(year, offset):
    base_url = f"https://api.jolpi.ca/ergast/f1/{year}"
    results_url = f"{base_url}/results/?limit=30&offset={offset}"
    sprint_url = f"{base_url}/sprint/?limit=30&offset={offset}"

    results_response = requests.get(results_url)
    sprint_response = requests.get(sprint_url)

    return (results_response, sprint_response)

def get_results_data(year):
    if year in cache:
        return cache[year]
    
    start_time = time.time()

    results_array = []
    driver_points = {} 
    driver_wins = {} 
    driver_podiums = {}
    driver_top10_finishes = {}
    driver_fastest_laps = {}
    driver_sprint_wins = {}
    driver_sprint_podiums = {}
    driver_sprint_top8_finishes = {}

    all_races = []
    all_sprints = []

    with ThreadPoolExecutor(max_workers=1) as executor:
        max_offset = 500
        futures = {
            executor.submit(fetch_round_data, year, offset): offset
            for offset in range(0, max_offset + 1, 30)
        }

        for future in as_completed(futures):
            results_response, sprint_response = future.result()
            if results_response.status_code == 200:
                all_races.extend(results_response.json()['MRData']['RaceTable']['Races'])
            if sprint_response.status_code == 200:
                all_sprints.extend(sprint_response.json()['MRData']['RaceTable']['Races'])

    # Index sprints by round for quick lookup
    sprint_by_round = {s['round']: s for s in all_sprints}

    # Sort races by round
    all_races.sort(key=lambda r: int(r['round']))

    for race in all_races:
        round_number = race.get('round')
        race_name = race.get('raceName')
        circuit_name = race['Circuit'].get('circuitName')
        date = race.get('date')
        results = race.get('Results')

        sprint = sprint_by_round.get(round_number)
        sprint_results = sprint.get('SprintResults') if sprint else []

        sprint_driver_map = {}
        for sprint_result in sprint_results:
            d = sprint_result.get('Driver')
            key = f"{d.get('givenName')} {d.get('familyName')}"
            sprint_driver_map[key] = sprint_result

        for result in results:
            driver = result.get('Driver')
            if not driver:
                continue
            given_name = driver.get('givenName')
            family_name = driver.get('familyName')
            driver_key = f"{given_name} {family_name}"

            constructor = result.get('Constructor')
            constructor_name = constructor.get('name') if constructor else "Unknown"

            position = int(result.get('position', 99))
            status = result.get('status')
            points = float(result.get('points', 0))

            win = 1 if position == 1 else 0
            podium = 1 if position <= 3 else 0
            top10 = 1 if position <= 10 else 0

            fastest_lap = 0
            rank = result.get('FastestLap', {}).get('rank')
            fastest_lap_rank = int(rank) if rank and rank.isdigit() else None
            if fastest_lap_rank == 1:
                fastest_lap = 1

            # Update driver stats
            driver_points[driver_key] = driver_points.get(driver_key, 0) + points
            driver_wins[driver_key] = driver_wins.get(driver_key, 0) + win
            driver_podiums[driver_key] = driver_podiums.get(driver_key, 0) + podium
            driver_top10_finishes[driver_key] = driver_top10_finishes.get(driver_key, 0) + top10
            driver_fastest_laps[driver_key] = driver_fastest_laps.get(driver_key, 0) + fastest_lap

            # Sprint data for this driver (if exists)
            sprint_data = sprint_driver_map.get(driver_key)
            sprint_position = None
            sprint_points = None
            sprint_status = None
            sprint_date = sprint.get('date') if sprint else None

            if sprint_data:
                sprint_position = int(sprint_data.get('position', 99))
                sprint_status = sprint_data.get('status')
                sprint_points = float(sprint_data.get('points', 0))

                # Update totals
                driver_points[driver_key] += sprint_points
                driver_sprint_wins[driver_key] = driver_sprint_wins.get(driver_key, 0) + (1 if sprint_position == 1 else 0)
                driver_sprint_podiums[driver_key] = driver_sprint_podiums.get(driver_key, 0) + (1 if sprint_position <= 3 else 0)
                driver_sprint_top8_finishes[driver_key] = driver_sprint_top8_finishes.get(driver_key, 0) + (1 if sprint_position <= 8 else 0)
            else:
                # Initialize if missing
                driver_sprint_wins.setdefault(driver_key, 0)
                driver_sprint_podiums.setdefault(driver_key, 0)
                driver_sprint_top8_finishes.setdefault(driver_key, 0)

            results_array.append({
                "given_name": given_name,
                "family_name": family_name,
                "constructor_name": constructor_name,
                "position": position,
                "win": win,
                "podium": podium,
                "top10_finish": top10,
                "points": points,
                "status": status,
                "fastest_lap_rank": fastest_lap_rank,
                "season": race.get('season'),
                "round": round_number,
                "race_name": race_name,
                "circuit_name": circuit_name,
                "date": date,
                "sprint_position": sprint_position,
                "sprint_points": sprint_points,
                "sprint_status": sprint_status,
                "sprint_date": sprint_date,
                "total_points": driver_points[driver_key], 
                "total_wins": driver_wins[driver_key], 
                "total_podiums": driver_podiums[driver_key], 
                "total_top10_finishes": driver_top10_finishes[driver_key], 
                "total_fastest_laps": driver_fastest_laps[driver_key],
                "total_sprint_wins": driver_sprint_wins[driver_key],
                "total_sprint_podiums": driver_sprint_podiums[driver_key],
                "total_sprint_top8_finishes": driver_sprint_top8_finishes[driver_key]
            })

    end_time = time.time()
    print(f"Results API time: {end_time - start_time:.2f} seconds")
    cache[year] = results_array
    return results_array