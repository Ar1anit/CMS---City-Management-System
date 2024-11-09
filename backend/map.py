import folium
import json
import os
import glob
from pyproj import Proj, transform

class MapGenerator:

    def __init__(self):
        self.utm = Proj(proj='utm', zone=32, ellps='WGS84', south=False)
        self.lonlat = Proj(proj='longlat', ellps='WGS84', datum='WGS84')

        # Path to the datasets directory
        self.datasets_dir = os.path.join(os.getcwd(), 'datasets')

        # Create a map object with the folium package
        self.m = folium.Map(location=[50.74253872133164, 6.117324829101563], zoom_start=12)

    def create_map(self):
        # Loop through each GeoJSON file in the datasets directory
        for file in glob.glob(os.path.join(self.datasets_dir, "*.geojson")):
            filename = os.path.basename(file).split(".")[0]
            with open(file, "r") as f:
                data = json.load(f)
                for feature in data["features"]:
                    coordinates = feature["geometry"]["coordinates"]
                    lon, lat = transform(self.utm, self.lonlat, coordinates[0], coordinates[1])

                    if filename == "knotenpunkte":
                        folium.Marker(
                            location=[lat, lon],
                            popup=feature["id"],
                            icon=folium.Icon(icon="info", prefix="fa", color="blue")
                        ).add_to(self.m)
                    elif filename == "rettungspunkte":
                        folium.Marker(
                            location=[lat, lon],
                            popup=feature["id"],
                            icon=folium.Icon(icon="heart", prefix="fa", color="red")
                        ).add_to(self.m)
                    elif filename == "schutzhütten":
                        folium.Marker(
                            location=[lat, lon],
                            popup=feature["id"],
                            icon=folium.Icon(icon="home", prefix="fa", color="green")
                        ).add_to(self.m)

        self.m.save(os.path.join('static', 'output.html'))