import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def load_data(file_path):
    return pd.read_csv(file_path)

def plot_world_map(df):
    fig = plt.figure(figsize=(12, 9))
    world_map = Basemap()

    # draw coastlines, country boundaries, fill continents.
    world_map.drawcoastlines(linewidth=0.25)
    world_map.drawcountries(linewidth=0.25)
    world_map.fillcontinents(color='coral', lake_color='aqua')
    world_map.drawmapboundary(fill_color='aqua')

    # Plotting the seismic stations and glaciers separately
    for idx, row in df.iterrows():
        x, y = world_map(row['Station_Longitude'], row['Station_Latitude'])
        world_map.scatter(x, y, color='red', marker='v', zorder=5)  # zorder=5 ensures the markers are on top layer
        plt.text(x, y, row['Station_Name'], color='darkred', fontsize=9, ha='right', va='bottom')  # Station names

    world_map.scatter(df['Glacier_Longitude'], df['Glacier_Latitude'], latlon=True, 
                      color='blue', marker='^', label='Glaciers')

    plt.legend(loc="lower right")
    plt.title('Seismic Stations and Glaciers')
    plt.savefig('world_map_with_names.png', dpi=300)
    plt.show()


def plot_regional_map(df):
    # User input for the boundary of the map
    min_lat = float(input("Enter minimum latitude: "))
    max_lat = float(input("Enter maximum latitude: "))
    min_lon = float(input("Enter minimum longitude: "))
    max_lon = float(input("Enter maximum longitude: "))

    fig = plt.figure(figsize=(12, 9))
    regional_map = Basemap(llcrnrlon=min_lon, llcrnrlat=min_lat, urcrnrlon=max_lon, urcrnrlat=max_lat)

    regional_map.drawcoastlines(linewidth=0.25)
    regional_map.drawcountries(linewidth=0.25)
    regional_map.fillcontinents(color='coral', lake_color='aqua')
    regional_map.drawmapboundary(fill_color='aqua')

    # Plotting the seismic stations and glaciers separately
    regional_map.scatter(df['Station_Longitude'], df['Station_Latitude'], latlon=True, 
                         color='red', marker='v', label='Seismic Stations')
    regional_map.scatter(df['Glacier_Longitude'], df['Glacier_Latitude'], latlon=True, 
                         color='blue', marker='^', label='Glaciers')

    plt.legend(loc="lower right")
    plt.title('Seismic Stations and Glaciers in the Selected Region')
    plt.savefig('regional_map.png', dpi=300)
    plt.show()

def main():
    data_file = 'stations_near_glaciers.csv'  # specify the correct path
    df = load_data(data_file)

    plot_world_map(df)
    #plot_regional_map(df)

if __name__ == "__main__":
    main()
