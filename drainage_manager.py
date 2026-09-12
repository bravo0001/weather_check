import json
import os
from datetime import datetime

INCIDENTS_FILE = "manhole_incidents.json"

class ManholeManager:
        def __init__(self, roads_data=None, roads_geojson_path="chennai_roads_elevated.geojson"):
                    self.manholes = []
                    self.incidents = {}
                    self.load_incidents()
                    self.generate_municipal_manholes(roads_data, roads_geojson_path)

        def load_incidents(self):
                    if os.path.exists(INCIDENTS_FILE):
                                    try:
                                                        with open(INCIDENTS_FILE, "r", encoding="utf-8") as f:
                                                                                self.incidents = json.load(f)
                                    except Exception:
                                                        self.incidents = {}
                    else:
                                    self.incidents = {}

                def save_incidents(self):
                            with open(INCIDENTS_FILE, "w", encoding="utf-8") as f:
                                            json.dump(self.incidents, f, indent=2)

                        def generate_municipal_manholes(self, roads_data=None, roads_path="chennai_roads_elevated.geojson"):
                                    """
                                            CPHEEO / Indian Municipal Standards:
                                                    Stormwater inlets & maintenance manholes spaced every 40-50m along urban corridors and junctions.
                                                            """
                                    if roads_data is None:
                                                    if not os.path.exists(roads_path):
                                                                        return
                                                                    with open(roads_path, "r", encoding="utf-8") as f:
                                                                                        roads_data = json.load(f)

                                                mh_counter = 1000
        # Step through features to avoid memory bloat
        features = roads_data.get("features", [])[::5]
        for feat in features:
                        coords = feat.get("geometry", {}).get("coordinates", [])
            props = feat.get("properties", {})
            street_name = props.get("name", "Urban Corridor")
            elev = props.get("elevation_msl", 4.0)
            if len(coords) >= 2:
                                pt = coords[len(coords) // 2]
      
