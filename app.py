from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
import urllib.request
import uvicorn
import gc
from hydraulics import calculate_road_depth
from router import FloodRouter
from drainage_manager import ManholeManager

app = FastAPI(title="Chennai Flood Early Warning & Emergency Navigation")

print("Initializing Chennai Geo-Data into Memory...")
with open("chennai_roads_elevated.geojson", "r", encoding="utf-8") as f:
        roads_data = json.load(f)

# Assign a unique integer ID to every road feature
for idx, feat in enumerate(roads_data.get("features", [])):
        feat["id"] = idx

with open("chennai_hospitals.geojson", "r", encoding="utf-8") as f:
        hospitals_data = json.load(f)

print(f"Loaded {len(roads_data['features'])} roads and {len(hospitals_data['features'])} medical centers.")

# Initialize the routing engine
router = FloodRouter(roads_data)
manhole_mgr = ManholeManager(roads_data=roads_data)
active_flood_depths = {}

gc.collect()

# Endpoints for Frontend Map Layers
@app.get("/api/roads")
def get_roads():
        return JSONResponse(content=roads_data)

@app.get("/api/hospitals")
def get_hospitals():
        return JSONResponse(content=hospitals_data)

@app.get("/api/manholes")
def get_manholes():
        return JSONResponse(content=manhole_mgr.get_manholes_geojson())

class IncidentReport(BaseModel):
        mh_id: str
        notes: str
        image_base64: str = ""

@app.post("/api/manholes/report")
def report_manhole_blockage(report: IncidentReport):
        res = manhole_mgr.report_blockage(report.mh_id, report.notes, report.image_base64)
        return JSONResponse(content=res)

@app.post("/api/manholes/resolve/{mh_id}
