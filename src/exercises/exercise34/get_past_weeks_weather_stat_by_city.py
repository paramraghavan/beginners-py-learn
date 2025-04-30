import pandas as pd
import requests
from datetime import datetime, timedelta


def get_daily_temperatures(city_name, state=None, csv_file='uscities.csv'):
    """
    Get daily max and min temperatures for a city using NWS API.

    Args:
        city_name (str): Name of the city
        state (str, optional): State abbreviation or name
        csv_file (str): Path to CSV file with city data

    Returns:
        DataFrame with date, max_temp_f, min_temp_f, and common_weather
    """
    # 1. Set up basic variables
    base_url = "https://api.weather.gov"
    headers = {
        "User-Agent": "WeatherApp/1.0 (your@email.com)",
        "Accept": "application/geo+json"
    }

    # 2. Find city coordinates from CSV
    print(f"Looking up coordinates for {city_name}...")
    cities_df = pd.read_csv(csv_file)

    # Filter by city name (case-insensitive)
    city_matches = cities_df[cities_df['city_ascii'].str.lower() == city_name.lower()]

    # If state provided, narrow down further
    if state and len(city_matches) > 1:
        state_matches = city_matches[
            (city_matches['state_id'].str.lower() == state.lower()) |
            (city_matches['state_name'].str.lower() == state.lower())
            ]
        if len(state_matches) > 0:
            city_matches = state_matches

    # If multiple matches, take the one with the highest population
    if len(city_matches) > 1:
        city_matches = city_matches.sort_values(by='population', ascending=False)

    # Check if we found the city
    if len(city_matches) == 0:
        print(f"City '{city_name}' not found in database")
        return None

    # Extract coordinates
    lat = float(city_matches.iloc[0]['lat'])
    lng = float(city_matches.iloc[0]['lng'])
    print(f"Found coordinates: ({lat}, {lng})")

    # 3. Get NWS metadata for this location
    print("Getting weather station information...")
    try:
        # Get metadata for this point
        point_url = f"{base_url}/points/{lat},{lng}"
        response = requests.get(point_url, headers=headers)
        response.raise_for_status()
        point_data = response.json()

        # Get stations near this point
        stations_url = point_data['properties']['observationStations']
        response = requests.get(stations_url, headers=headers)
        response.raise_for_status()
        stations_data = response.json()

        # Use the closest station (first in the list)
        if len(stations_data['features']) == 0:
            print("No weather stations found near this location")
            return None

        station = stations_data['features'][0]
        station_id = station['properties']['stationIdentifier']
        station_name = station['properties']['name']
        print(f"Using station: {station_name} (ID: {station_id})")
    except Exception as e:
        print(f"Error getting station data: {e}")
        return None

    # 4. Get observations for the past week
    print("Retrieving weather observations...")
    try:
        # Calculate date range (past 7 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        # Format dates for API
        start_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Get observations
        observations_url = f"{base_url}/stations/{station_id}/observations"
        response = requests.get(
            f"{observations_url}?start={start_str}&end={end_str}",
            headers=headers
        )
        response.raise_for_status()
        observations = response.json()
    except Exception as e:
        print(f"Error getting observations: {e}")
        return None

    # 5. Extract temperature data
    print("Processing temperature data...")
    temp_data = []

    for feature in observations['features']:
        props = feature['properties']

        # Get timestamp
        if not props.get('timestamp'):
            continue
        dt = datetime.fromisoformat(props['timestamp'].replace('Z', '+00:00'))

        # Get temperature
        temp_c = None
        if props.get('temperature') and props['temperature'].get('value') is not None:
            temp_c = props['temperature']['value']
        else:
            continue

        # Convert to Fahrenheit
        temp_f = temp_c * 9 / 5 + 32

        # Add to list
        temp_data.append({
            'date': dt.date(),
            'temperature_f': temp_f,
            'description': props.get('textDescription', '')
        })

    # 6. Calculate daily min and max
    if not temp_data:
        print("No temperature data found")
        return None

    # Create DataFrame
    df = pd.DataFrame(temp_data)

    # Group by date and calculate stats
    daily_stats = df.groupby('date').agg({
        'temperature_f': ['max', 'min'],
        'description': lambda x: x.value_counts().index[0] if len(x) > 0 else "Unknown"
    })

    # Clean up column names
    daily_stats.columns = ['max_temp_f', 'min_temp_f', 'common_weather']
    daily_stats = daily_stats.reset_index()

    # Sort by date (most recent first)
    daily_stats = daily_stats.sort_values('date', ascending=False)

    # 7. Display results
    print("\nDaily Maximum and Minimum Temperatures (°F):")
    print(daily_stats[['date', 'max_temp_f', 'min_temp_f', 'common_weather']])

    return daily_stats


# Example usage
if __name__ == "__main__":
    city = input("Enter city name: ")
    state = input("Enter state (optional): ")

    if not state.strip():
        state = None

    # Get daily temperatures
    daily_temps = get_daily_temperatures(city, state)

    # Save results to CSV
    if daily_temps is not None:
        filename = f"{city.lower().replace(' ', '_')}_daily_temps.csv"
        daily_temps.to_csv(filename, index=False)
        print(f"\nSaved temperature data to {filename}")