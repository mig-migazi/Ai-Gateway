"""
Simple Dashboard Server
Serves the AI Gateway dashboard and provides API endpoints for MCP monitoring
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="AI Gateway Dashboard Server", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
dashboard_path = Path(__file__).parent / "dashboard"
app.mount("/static", StaticFiles(directory=dashboard_path), name="static")

# MCP monitoring data
mcp_activity_log = []
active_connections = {}
ai_decisions = []

# Hybrid architecture data
edge_gateway_status = {
    "tinyml_models": 3,
    "model_size_kb": 2.44,
    "inference_time_ms": 1,
    "power_usage": "ultra-low",
    "offline_capable": True,
    "status": "online"
}

cloud_context_status = {
    "api_cost": 0.00,
    "device_contexts": 1247,
    "response_time_ms": 200,
    "uptime_percent": 99.9,
    "status": "online"
}

anomaly_detections = []

@app.get("/")
async def serve_dashboard():
    """Serve the main dashboard - redirect to hybrid dashboard"""
    return FileResponse(dashboard_path / "hybrid_dashboard.html")

@app.get("/hybrid")
async def serve_hybrid_dashboard():
    """Serve the hybrid edge-cloud dashboard"""
    return FileResponse(dashboard_path / "hybrid_dashboard.html")

@app.get("/legacy")
async def serve_legacy_dashboard():
    """Serve the legacy dashboard"""
    return FileResponse(dashboard_path / "index.html")

@app.get("/api/mcp/status")
async def get_mcp_status():
    """Get MCP server status"""
    return {
        "status": "active",
        "connections": len(active_connections),
        "ai_decisions": len(ai_decisions),
        "uptime": "2h 15m 30s",
        "last_activity": datetime.now().isoformat()
    }

@app.get("/api/mcp/connections")
async def get_mcp_connections():
    """Get active MCP connections"""
    return {
        "connections": active_connections,
        "total": len(active_connections)
    }

@app.get("/api/mcp/decisions")
async def get_ai_decisions(limit: int = 10):
    """Get recent AI decisions"""
    return {
        "decisions": ai_decisions[-limit:] if limit > 0 else ai_decisions,
        "total": len(ai_decisions)
    }

@app.get("/api/mcp/activity")
async def get_activity_log(limit: int = 50):
    """Get activity log"""
    return {
        "log": mcp_activity_log[-limit:] if limit > 0 else mcp_activity_log,
        "total": len(mcp_activity_log)
    }

@app.post("/api/mcp/simulate")
async def simulate_mcp_activity():
    """Simulate MCP activity for demo purposes"""
    # Simulate a new connection
    connection_id = f"conn_{len(active_connections) + 1}"
    active_connections[connection_id] = {
        "id": connection_id,
        "protocol": "REST",
        "device": "rest_sensor_001",
        "status": "active",
        "created": datetime.now().isoformat()
    }
    
    # Simulate an AI decision
    decision = {
        "timestamp": datetime.now().isoformat(),
        "action": "Protocol Selection",
        "reasoning": "AI analyzed device characteristics and selected REST protocol for optimal communication",
        "confidence": 0.95,
        "protocol_used": "REST"
    }
    ai_decisions.append(decision)
    
    # Add to activity log
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": "info",
        "message": f"New connection established: {connection_id}",
        "details": {
            "protocol": "REST",
            "device": "rest_sensor_001"
        }
    }
    mcp_activity_log.append(log_entry)
    
    return {
        "success": True,
        "message": "MCP activity simulated",
        "connection_id": connection_id,
        "decision": decision
    }

@app.post("/api/mcp/query")
async def simulate_mcp_query(request: dict):
    """Simulate MCP query processing"""
    query = request.get("query", "")
    
    # Simulate AI processing
    decision = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "action": "Query Processing",
        "reasoning": f"AI processed query: '{query}' and determined optimal response strategy",
        "confidence": 0.92,
        "processing_time_ms": 150
    }
    ai_decisions.append(decision)
    
    # Add to activity log
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": "info",
        "message": f"Query processed: {query[:50]}...",
        "details": {
            "query": query,
            "processing_time": "150ms"
        }
    }
    mcp_activity_log.append(log_entry)
    
    return {
        "success": True,
        "query": query,
        "response": f"AI processed your query: '{query}' and generated an appropriate response",
        "decision": decision
    }

@app.get("/api/analytics")
async def get_analytics():
    """Get analytics data"""
    return {
        "mcp_server": {
            "total_connections": len(active_connections),
            "total_decisions": len(ai_decisions),
            "total_queries": len([d for d in ai_decisions if "query" in d]),
            "average_confidence": sum(d.get("confidence", 0) for d in ai_decisions) / max(len(ai_decisions), 1)
        },
        "protocols": {
            "REST": len([c for c in active_connections.values() if c["protocol"] == "REST"]),
            "BACnet": len([c for c in active_connections.values() if c["protocol"] == "BACnet"]),
            "Modbus": len([c for c in active_connections.values() if c["protocol"] == "Modbus"])
        },
        "performance": {
            "average_processing_time": 120,  # ms
            "success_rate": 0.98,
            "uptime": "99.9%"
        }
    }

@app.get("/api/hybrid/edge-status")
async def get_edge_gateway_status():
    """Get edge gateway status"""
    return edge_gateway_status

@app.get("/api/hybrid/cloud-status")
async def get_cloud_context_status():
    """Get cloud context service status"""
    return cloud_context_status

@app.get("/api/hybrid/anomalies")
async def get_anomalies():
    """Get current anomalies"""
    return {
        "anomalies": anomaly_detections,
        "total_count": len(anomaly_detections),
        "critical_count": len([a for a in anomaly_detections if a.get("severity") == "critical"]),
        "high_count": len([a for a in anomaly_detections if a.get("severity") == "high"]),
        "medium_count": len([a for a in anomaly_detections if a.get("severity") == "medium"]),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/hybrid/simulate-anomaly")
async def simulate_anomaly():
    """Simulate a new anomaly"""
    import random
    
    anomaly_types = ["sensor_drift", "maintenance_overdue", "value_out_of_range", "environmental_anomaly"]
    severities = ["critical", "high", "medium"]
    parameters = ["temperature", "humidity", "pressure", "setpoint"]
    
    anomaly = {
        "id": f"anomaly_{len(anomaly_detections) + 1}",
        "type": random.choice(anomaly_types),
        "severity": random.choice(severities),
        "parameter": random.choice(parameters),
        "description": f"Simulated {random.choice(anomaly_types).replace('_', ' ')} detected",
        "timestamp": datetime.now().isoformat(),
        "confidence": round(random.uniform(0.7, 0.95), 2)
    }
    
    anomaly_detections.append(anomaly)
    
    # Keep only last 50 anomalies
    if len(anomaly_detections) > 50:
        anomaly_detections.pop(0)
    
    return anomaly

@app.delete("/api/hybrid/anomalies")
async def clear_anomalies():
    """Clear all anomalies"""
    anomaly_detections.clear()
    return {"message": "All anomalies cleared", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    print("🚀 Starting AI Gateway Dashboard Server...")
    print("📊 Dashboard will be available at: http://localhost:8081")
    print("🔧 API endpoints available at: http://localhost:8081/api/")
    print()
    print("Available endpoints:")
    print("  GET  /                    - Main dashboard")
    print("  GET  /hybrid              - Hybrid edge-cloud dashboard")
    print("  GET  /api/mcp/status      - MCP server status")
    print("  GET  /api/mcp/connections - Active connections")
    print("  GET  /api/mcp/decisions   - AI decisions")
    print("  GET  /api/mcp/activity    - Activity log")
    print("  POST /api/mcp/simulate    - Simulate MCP activity")
    print("  POST /api/mcp/query       - Simulate query processing")
    print("  GET  /api/analytics       - Analytics data")
    print("  GET  /api/hybrid/edge-status    - Edge gateway status")
    print("  GET  /api/hybrid/cloud-status   - Cloud context status")
    print("  GET  /api/hybrid/anomalies      - Current anomalies")
    print("  POST /api/hybrid/simulate-anomaly - Simulate anomaly")
    print("  DELETE /api/hybrid/anomalies    - Clear anomalies")
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8081)
