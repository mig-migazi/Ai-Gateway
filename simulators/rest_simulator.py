"""
REST API Simulator - Simulates REST API devices for testing
"""

import asyncio
import json
import logging
from typing import Dict, Any
from datetime import datetime, timedelta
import random
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="REST Device Simulator", version="1.0.0")

# Add CORS middleware for web dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulated device data with realistic variations
device_data = {
    "temperature": 72.5,
    "humidity": 45.2,
    "pressure": 1013.25,
    "status": "online",
    "last_updated": datetime.now().isoformat(),
    "device_id": "rest_sensor_001",
    "location": "room_101",
    "energy_usage": 150.5,  # watts
    "efficiency": 0.85
}

# Data streaming settings
streaming_active = False
stream_interval = 5  # seconds
data_history = []


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "REST Device Simulator",
        "version": "1.0.0",
        "status": "online",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/status")
async def get_status():
    """Get device status"""
    return {
        "status": "online",
        "device_id": "rest_simulator_001",
        "device_name": "Temperature Sensor Simulator",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/status")
async def get_api_status():
    """Get API status"""
    return {
        "api_status": "online",
        "version": "1.0.0",
        "endpoints": [
            "/",
            "/status",
            "/api/status",
            "/api/temperature",
            "/api/humidity",
            "/api/pressure",
            "/api/sensors",
            "/api/health"
        ]
    }


@app.get("/api/temperature")
async def get_temperature():
    """Get temperature reading"""
    # Simulate temperature variation
    temperature = 72.0 + random.uniform(-2.0, 2.0)
    device_data["temperature"] = round(temperature, 1)
    device_data["last_updated"] = datetime.now().isoformat()
    
    return {
        "temperature": device_data["temperature"],
        "units": "degrees_fahrenheit",
        "timestamp": datetime.now().isoformat(),
        "sensor_id": "temp_001"
    }


@app.get("/api/humidity")
async def get_humidity():
    """Get humidity reading"""
    # Simulate humidity variation
    humidity = 45.0 + random.uniform(-5.0, 5.0)
    device_data["humidity"] = round(humidity, 1)
    device_data["last_updated"] = datetime.now().isoformat()
    
    return {
        "humidity": device_data["humidity"],
        "units": "percent",
        "timestamp": datetime.now().isoformat(),
        "sensor_id": "hum_001"
    }


@app.get("/api/pressure")
async def get_pressure():
    """Get pressure reading"""
    # Simulate pressure variation
    pressure = 1013.0 + random.uniform(-10.0, 10.0)
    device_data["pressure"] = round(pressure, 2)
    device_data["last_updated"] = datetime.now().isoformat()
    
    return {
        "pressure": device_data["pressure"],
        "units": "hPa",
        "timestamp": datetime.now().isoformat(),
        "sensor_id": "press_001"
    }


@app.get("/api/sensors")
async def get_all_sensors():
    """Get all sensor readings"""
    return {
        "sensors": {
            "temperature": {
                "value": device_data["temperature"],
                "units": "degrees_fahrenheit",
                "sensor_id": "temp_001"
            },
            "humidity": {
                "value": device_data["humidity"],
                "units": "percent",
                "sensor_id": "hum_001"
            },
            "pressure": {
                "value": device_data["pressure"],
                "units": "hPa",
                "sensor_id": "press_001"
            }
        },
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/sensors/{sensor_type}")
async def get_sensor_by_type(sensor_type: str):
    """Get specific sensor reading by type"""
    if sensor_type == "temperature":
        return await get_temperature()
    elif sensor_type == "humidity":
        return await get_humidity()
    elif sensor_type == "pressure":
        return await get_pressure()
    else:
        raise HTTPException(status_code=404, detail=f"Sensor type '{sensor_type}' not found")


@app.get("/api/health")
async def get_health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "uptime": "24h 15m 30s",
        "memory_usage": "45%",
        "cpu_usage": "12%",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/set")
async def set_value(data: Dict[str, Any]):
    """Set a device value"""
    if "value" not in data:
        raise HTTPException(status_code=400, detail="Value not provided")
    
    value = data["value"]
    return {
        "success": True,
        "message": f"Value set to {value}",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/room/{room_id}")
async def get_room_data(room_id: str):
    """Get room-specific data"""
    return {
        "room_id": room_id,
        "temperature": 72.5 + random.uniform(-2.0, 2.0),
        "humidity": 45.2 + random.uniform(-5.0, 5.0),
        "occupancy": random.choice(["occupied", "vacant"]),
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/room/{room_id}/temperature")
async def get_room_temperature(room_id: str):
    """Get room temperature"""
    return {
        "room_id": room_id,
        "temperature": 72.5 + random.uniform(-2.0, 2.0),
        "units": "degrees_fahrenheit",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/stream")
@app.head("/api/stream")
async def stream_data():
    """Stream real-time data updates"""
    async def generate_data():
        global streaming_active, data_history
        
        # Only stream if streaming is active
        if not streaming_active:
            yield "data: {\"message\": \"Streaming not active\"}\n\n"
            return
        
        while streaming_active:
            # Generate realistic sensor data with trends
            current_time = datetime.now()
            
            # Temperature with daily cycle (cooler at night)
            hour = current_time.hour
            base_temp = 70 + 10 * (0.5 + 0.5 * (1 + (hour - 12) / 12))  # 70-80°F range
            temperature = base_temp + random.uniform(-2.0, 2.0)
            
            # Humidity with inverse relationship to temperature
            humidity = 60 - (temperature - 70) * 2 + random.uniform(-5.0, 5.0)
            humidity = max(20, min(80, humidity))  # Clamp between 20-80%
            
            # Pressure with slight variations
            pressure = 1013.25 + random.uniform(-5.0, 5.0)
            
            # Energy usage based on temperature difference from setpoint
            energy_usage = 100 + abs(temperature - 72) * 10 + random.uniform(-10, 10)
            
            data_point = {
                "timestamp": current_time.isoformat(),
                "temperature": round(temperature, 1),
                "humidity": round(humidity, 1),
                "pressure": round(pressure, 2),
                "energy_usage": round(energy_usage, 1),
                "efficiency": round(0.8 + random.uniform(-0.1, 0.1), 2),
                "device_id": "rest_sensor_001",
                "location": "room_101"
            }
            
            # Store in history (keep last 100 points)
            data_history.append(data_point)
            if len(data_history) > 100:
                data_history.pop(0)
            
            # Update device data
            device_data.update(data_point)
            
            # Yield data as JSON
            yield f"data: {json.dumps(data_point)}\n\n"
            
            # Wait for next interval
            await asyncio.sleep(stream_interval)
    
    return StreamingResponse(
        generate_data(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control"
        }
    )


@app.post("/api/stream/start")
async def start_streaming():
    """Start data streaming"""
    global streaming_active
    streaming_active = True
    return {"message": "Data streaming started", "interval": stream_interval}


@app.post("/api/stream/stop")
async def stop_streaming():
    """Stop data streaming"""
    global streaming_active
    streaming_active = False
    return {"message": "Data streaming stopped"}


@app.get("/api/stream/status")
async def get_streaming_status():
    """Get streaming status"""
    return {
        "streaming": streaming_active,
        "interval": stream_interval,
        "data_points": len(data_history),
        "last_update": device_data["last_updated"]
    }


@app.get("/api/history")
async def get_data_history(limit: int = 50):
    """Get historical data"""
    return {
        "history": data_history[-limit:] if limit > 0 else data_history,
        "total_points": len(data_history),
        "streaming": streaming_active
    }


@app.get("/api/analytics")
async def get_analytics():
    """Get basic analytics from historical data"""
    if not data_history:
        return {"message": "No data available for analytics"}
    
    temps = [d["temperature"] for d in data_history]
    humidities = [d["humidity"] for d in data_history]
    energies = [d["energy_usage"] for d in data_history]
    
    return {
        "temperature": {
            "min": min(temps),
            "max": max(temps),
            "avg": round(sum(temps) / len(temps), 1),
            "trend": "increasing" if temps[-1] > temps[0] else "decreasing"
        },
        "humidity": {
            "min": min(humidities),
            "max": max(humidities),
            "avg": round(sum(humidities) / len(humidities), 1)
        },
        "energy": {
            "min": min(energies),
            "max": max(energies),
            "avg": round(sum(energies) / len(energies), 1),
            "total": round(sum(energies), 1)
        },
        "data_points": len(data_history),
        "time_range": {
            "start": data_history[0]["timestamp"],
            "end": data_history[-1]["timestamp"]
        }
    }


if __name__ == "__main__":
    print("Starting REST API Simulator...")
    print("Available endpoints:")
    print("  GET  /                    - Root endpoint")
    print("  GET  /status              - Device status")
    print("  GET  /api/status          - API status")
    print("  GET  /api/temperature     - Temperature reading")
    print("  GET  /api/humidity        - Humidity reading")
    print("  GET  /api/pressure        - Pressure reading")
    print("  GET  /api/sensors         - All sensor readings")
    print("  GET  /api/sensors/{type}  - Specific sensor reading")
    print("  GET  /api/health          - Health check")
    print("  POST /api/set             - Set device value")
    print("  GET  /api/room/{id}       - Room data")
    print("  GET  /api/room/{id}/temperature - Room temperature")
    print()
    print("Access the API at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
