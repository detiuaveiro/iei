#!/usr/bin/env python3

import os
import json
import time
import requests
import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

# --- Setup Logger ---
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
# --------------------

# --- Configuration ---
CACHE_FILE = "ip_cache.json"
CACHE_DEADLINE_SECONDS = 3600  # 1 hour
FAVICON_PATH = 'ip-address.png' 
# ---------------------

app = FastAPI()

def load_cache():
    """Loads the cache from a JSON file."""
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        logger.warning("Cache file corrupted, starting fresh.")
        return {}

def save_cache(cache_data):
    """Saves the cache to a JSON file."""
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache_data, f, indent=4)
    except IOError as e:
        logger.error(f"Error saving cache: {e}")

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(FAVICON_PATH)

@app.get("/ip/{ip_address}")
def get_ip_info(ip_address: str):
    """
    Fetches geolocation data for an IP, using a local cache.
    """
    cache = load_cache()
    current_time = time.time()

    # 1. Check if IP is in cache
    if ip_address in cache:
        entry = cache[ip_address]
        # 2. Check if cache entry is stale
        if (current_time - entry['timestamp']) < CACHE_DEADLINE_SECONDS:
            logger.info(f"Returning cached data for {ip_address}")
            return entry['data']
        else:
            logger.info(f"Cache for {ip_address} is stale.")
    
    # 3. Cache miss or stale: Query the external API
    logger.info(f"Querying external API for {ip_address}...")
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        
        # Check if the API returned an error (e.g., private IP)
        if data.get('status') == 'fail':
            logger.warning(f"API failed to find {ip_address}: {data.get('message')}")
            raise HTTPException(status_code=404, detail=data.get('message'))

        # 4. Update cache
        cache[ip_address] = {
            'timestamp': current_time,
            'data': data
        }
        save_cache(cache)
        
        return data

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP Request failed: {e}")
        raise HTTPException(status_code=502, detail="External API request failed")

@app.get("/")
def read_root():
    return {"message": "Welcome to the IP Caching API. Use /ip/{ip_address}"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Run this app with: uvicorn main:app --reload")
    uvicorn.run(app, host="127.0.0.1", port=8000)
