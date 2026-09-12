import networkx as nx
import math
from scipy.spatial import cKDTree

class FloodRouter:
        def __init__(self, geojson_data):
                    self.graph = nx.Graph()
                    self.build_base_graph(geojson_data)
                    self.ensure_connected_network()

        def haversine(self, lat1, lon1, lat2, lon2):
                    R = 6371000 # meters
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
            dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def build_base_graph(self, data):
                for feat in data.get("features", []):
                                coords = feat.get("geometry", {}).get("coordinates", [])
                                fid = feat.get("id")
                                if len(coords) >= 2:
                                                    for i in range(len(coords) - 1):
                                                                            u = (round(coords[i][1], 5), round(coords[i][0], 5))
                                                                            v = (round(coords[i+1][1], 5), round(coords[i+1][0], 5))
                                                                            dist = max(1.0, self.haversine(u[0], u[1], v[0], v[1]))
                                                                            self.graph.add_edge(u, v, weight=dist, distance=dist, coords=[coords[i], coords[i+1]], fid=fid)

                                        def ensure_connected_network(self):
                                                    if not self.graph.nodes:
                                                                    return
                                                                components = sorted(nx.connected_components(self.graph), key=len, reverse=True)
                                                    if len(components) > 1:
                                                                    main_comp = list(components[0])
                                                                    tree = cKDTree(main_comp)
                                                                    for comp in components[1:30]:
                                                                                        sample_u = next(iter(comp))
                                                                                        dist, idx = tree.query(sample_u)
                                                                                        nearest_v = main_comp[idx]
                                                                                        d = self.haversine(sample_u[0], sample_u[1], nearest_v[0], nearest_v[1])
                                                                                        if d < 500:
                                                                                                                self.graph.add_edge(sample_u, nearest_v, weight=d, distance=d, coords=[[sample_u[1], sample_u[0]], [nearest_v[1], nearest_v[0]]], fid=-1)

                                                                            def update_flood_weights(self, flood_depths_dict):
                                                                                        for u, v, data in self.graph.edges(data=True):
                                                                                                        fid = data.get("fid")
                                                                                                        depth = flood_depths_dict.get(fid, 0.0)
                                                                                                        dist = data["distance"]
                                                                                                        if depth > 7.0:
                                                                                                                            penalty = 10000.0
                                                                                            elif depth >= 1.5:
                                                                                                penalty = 1.0 + (depth * 2.5)
                                                    else:
                                                                        penalty = 1.0
                                                                    data["weight"] = dist * penalty
                                                        data["depth"] = depth

                        def extract_path_geometry(self, path_nodes):
                                    coords = []
                                    total_dist = 0.0
                                    flooded_segments = 0
                                    for i
