import pandas as pd
from scipy.spatial import cKDTree

def read_seismic_stations(file_path):
    return pd.read_csv(file_path, encoding='ISO-8859-1')  # Adjust encoding as necessary

def read_glacier_data(file_path):
    return pd.read_csv(file_path)

def get_stations_near_glaciers(df_stations, df_glaciers):
    glacier_coords = df_glaciers[['lat', 'lon']].values
    station_coords = df_stations[['Latitude', 'Longitude']].values

    glacier_tree = cKDTree(glacier_coords)
    stations_tree = cKDTree(station_coords)

    # Perform the proximity search and capture which stations are close to which glaciers.
    indices = stations_tree.query_ball_tree(glacier_tree, 0.05)  # radius in degrees

    # Prepare a DataFrame to hold the results
    results = []

    # Check if there are any stations within the radius of any glacier
    for station_idx, glaciers_list in enumerate(indices):
        if glaciers_list:
            station = df_stations.iloc[station_idx]
            for glacier_idx in glaciers_list:
                glacier = df_glaciers.iloc[glacier_idx]
                result = {
                    'Station_Name': station['Station'],
                    'Station_Latitude': station['Latitude'],
                    'Station_Longitude': station['Longitude'],
                    'Glacier_Name': glacier['wgi_glacier_id'],  # Adjust based on your column name for glacier names
                    'Glacier_Latitude': glacier['lat'],
                    'Glacier_Longitude': glacier['lon']
                }
                results.append(result)

    return pd.DataFrame(results)

def main():
    stations_file = 'gmap-stations.csv'  # specify the correct path
    glaciers_file = 'wgi_feb2012_edited.csv'  # specify the correct path

    df_stations = read_seismic_stations(stations_file)
    df_glaciers = read_glacier_data(glaciers_file)

    nearby_stations = get_stations_near_glaciers(df_stations, df_glaciers)

    # Save the results to a CSV file
    if not nearby_stations.empty:
        nearby_stations.to_csv('stations_near_glaciers.csv', index=False)
    else:
        print("No stations found within 0.25 degrees of any glaciers.")

if __name__ == "__main__":
    main()
