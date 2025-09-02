"""
MCP Dashboard Integration
Connects the multi-protocol dashboard to the actual MCP server and device simulators
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import aiohttp
import httpx
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPDashboardIntegration:
    """Integrates the multi-protocol dashboard with the actual MCP server and device simulators"""
    
    def __init__(self):
        self.mcp_server_url = "http://localhost:8000"  # MCP server URL
        self.rest_simulator_url = "http://localhost:8001"  # REST simulator URL
        self.bacnet_simulator_url = "http://localhost:8002"  # BACnet simulator URL
        self.modbus_simulator_url = "http://localhost:8003"  # Modbus simulator URL
        self.dashboard_url = "http://localhost:8081"  # Dashboard server URL
        
        # Device registry
        self.devices = {}
        self.device_counter = 0
        
        # MCP server connection
        self.mcp_connected = False
        self.mcp_activity_log = []
        self.ai_decisions = []
        
    async def initialize(self):
        """Initialize the integration"""
        logger.info("Initializing MCP Dashboard Integration...")
        
        # Check MCP server status
        await self._check_mcp_server()
        
        # Check device simulators
        await self._check_device_simulators()
        
        # Start background tasks
        asyncio.create_task(self._monitor_mcp_activity())
        asyncio.create_task(self._monitor_device_status())
        
        logger.info("MCP Dashboard Integration initialized successfully")
    
    async def _check_mcp_server(self):
        """Check if MCP server is running"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.mcp_server_url}/health")
                if response.status_code == 200:
                    self.mcp_connected = True
                    logger.info("MCP server is connected")
                else:
                    logger.warning("MCP server is not responding")
        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {e}")
            self.mcp_connected = False
    
    async def _check_device_simulators(self):
        """Check if device simulators are running"""
        simulators = [
            ("REST", self.rest_simulator_url),
            ("BACnet", self.bacnet_simulator_url),
            ("Modbus", self.modbus_simulator_url)
        ]
        
        for protocol, url in simulators:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{url}/health")
                    if response.status_code == 200:
                        logger.info(f"{protocol} simulator is running")
                    else:
                        logger.warning(f"{protocol} simulator is not responding")
            except Exception as e:
                logger.error(f"Failed to connect to {protocol} simulator: {e}")
    
    async def _monitor_mcp_activity(self):
        """Monitor MCP server activity"""
        while True:
            try:
                if self.mcp_connected:
                    # Get MCP server status
                    async with httpx.AsyncClient() as client:
                        response = await client.get(f"{self.mcp_server_url}/status")
                        if response.status_code == 200:
                            status = response.json()
                            
                            # Log MCP activity
                            log_entry = {
                                "timestamp": datetime.now().isoformat(),
                                "type": "info",
                                "message": f"MCP server status: {status.get('status', 'unknown')}",
                                "details": status
                            }
                            self.mcp_activity_log.append(log_entry)
                            
                            # Keep only last 100 log entries
                            if len(self.mcp_activity_log) > 100:
                                self.mcp_activity_log.pop(0)
                
                await asyncio.sleep(5)  # Check every 5 seconds
            except Exception as e:
                logger.error(f"Error monitoring MCP activity: {e}")
                await asyncio.sleep(10)
    
    async def _monitor_device_status(self):
        """Monitor device simulator status"""
        while True:
            try:
                # Check each device simulator
                for device_id, device in self.devices.items():
                    protocol = device.get("protocol")
                    url = self._get_simulator_url(protocol)
                    
                    if url:
                        try:
                            async with httpx.AsyncClient() as client:
                                response = await client.get(f"{url}/health")
                                if response.status_code == 200:
                                    device["status"] = "online"
                                    device["last_seen"] = datetime.now().isoformat()
                                else:
                                    device["status"] = "offline"
                        except Exception as e:
                            device["status"] = "offline"
                            logger.error(f"Device {device_id} is offline: {e}")
                
                await asyncio.sleep(10)  # Check every 10 seconds
            except Exception as e:
                logger.error(f"Error monitoring device status: {e}")
                await asyncio.sleep(15)
    
    def _get_simulator_url(self, protocol: str) -> Optional[str]:
        """Get simulator URL for protocol"""
        urls = {
            "rest": self.rest_simulator_url,
            "bacnet": self.bacnet_simulator_url,
            "modbus": self.modbus_simulator_url
        }
        return urls.get(protocol.lower())
    
    async def add_device(self, protocol: str, name: str, ip: str, port: int, docs: Optional[str] = None) -> Dict[str, Any]:
        """Add a new device to the system"""
        device_id = f"device_{self.device_counter + 1}"
        self.device_counter += 1
        
        device = {
            "id": device_id,
            "protocol": protocol.lower(),
            "name": name,
            "ip": ip,
            "port": port,
            "status": "offline",
            "last_seen": None,
            "docs": docs,
            "created": datetime.now().isoformat(),
            "metrics": self._generate_device_metrics(protocol)
        }
        
        self.devices[device_id] = device
        
        # Try to connect to the device
        await self._connect_device(device)
        
        # Log device addition
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "info",
            "message": f"Device added: {name} ({protocol.upper()})",
            "details": {
                "device_id": device_id,
                "protocol": protocol,
                "ip": ip,
                "port": port
            }
        }
        self.mcp_activity_log.append(log_entry)
        
        return device
    
    async def _connect_device(self, device: Dict[str, Any]):
        """Connect to a device and get its data"""
        protocol = device["protocol"]
        url = self._get_simulator_url(protocol)
        
        if url:
            try:
                async with httpx.AsyncClient() as client:
                    # Try to get device data
                    if protocol == "rest":
                        response = await client.get(f"{url}/api/data")
                    elif protocol == "bacnet":
                        response = await client.get(f"{url}/bacnet/data")
                    elif protocol == "modbus":
                        response = await client.get(f"{url}/modbus/data")
                    
                    if response.status_code == 200:
                        device["status"] = "online"
                        device["last_seen"] = datetime.now().isoformat()
                        device["data"] = response.json()
                        
                        # Log successful connection
                        log_entry = {
                            "timestamp": datetime.now().isoformat(),
                            "type": "success",
                            "message": f"Connected to {device['name']} ({protocol.upper()})",
                            "details": {
                                "device_id": device["id"],
                                "protocol": protocol,
                                "data_points": len(device.get("data", {}))
                            }
                        }
                        self.mcp_activity_log.append(log_entry)
                    else:
                        device["status"] = "offline"
            except Exception as e:
                device["status"] = "offline"
                logger.error(f"Failed to connect to device {device['id']}: {e}")
    
    def _generate_device_metrics(self, protocol: str) -> Dict[str, str]:
        """Generate device-specific metrics"""
        metrics = {
            "rest": {
                "Response Time": "45ms",
                "Uptime": "99.9%",
                "Requests/min": "120",
                "Error Rate": "0.1%"
            },
            "bacnet": {
                "Response Time": "12ms",
                "Uptime": "99.8%",
                "Objects": "45",
                "Error Rate": "0.2%"
            },
            "modbus": {
                "Response Time": "8ms",
                "Uptime": "99.9%",
                "Registers": "128",
                "Error Rate": "0.1%"
            }
        }
        return metrics.get(protocol.lower(), {})
    
    async def read_device(self, device_id: str) -> Dict[str, Any]:
        """Read data from a device"""
        device = self.devices.get(device_id)
        if not device:
            return {"error": "Device not found"}
        
        protocol = device["protocol"]
        url = self._get_simulator_url(protocol)
        
        if not url:
            return {"error": "Simulator not available"}
        
        try:
            async with httpx.AsyncClient() as client:
                if protocol == "rest":
                    response = await client.get(f"{url}/api/data")
                elif protocol == "bacnet":
                    response = await client.get(f"{url}/bacnet/data")
                elif protocol == "modbus":
                    response = await client.get(f"{url}/modbus/data")
                
                if response.status_code == 200:
                    data = response.json()
                    device["data"] = data
                    device["last_seen"] = datetime.now().isoformat()
                    
                    # Log read operation
                    log_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "type": "info",
                        "message": f"Read data from {device['name']} ({protocol.upper()})",
                        "details": {
                            "device_id": device_id,
                            "data_points": len(data)
                        }
                    }
                    self.mcp_activity_log.append(log_entry)
                    
                    return {"success": True, "data": data}
                else:
                    return {"error": f"Failed to read from device: {response.status_code}"}
        except Exception as e:
            logger.error(f"Error reading device {device_id}: {e}")
            return {"error": str(e)}
    
    async def write_device(self, device_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Write data to a device"""
        device = self.devices.get(device_id)
        if not device:
            return {"error": "Device not found"}
        
        protocol = device["protocol"]
        url = self._get_simulator_url(protocol)
        
        if not url:
            return {"error": "Simulator not available"}
        
        try:
            async with httpx.AsyncClient() as client:
                if protocol == "rest":
                    response = await client.post(f"{url}/api/data", json=data)
                elif protocol == "bacnet":
                    response = await client.post(f"{url}/bacnet/data", json=data)
                elif protocol == "modbus":
                    response = await client.post(f"{url}/modbus/data", json=data)
                
                if response.status_code == 200:
                    # Log write operation
                    log_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "type": "info",
                        "message": f"Wrote data to {device['name']} ({protocol.upper()})",
                        "details": {
                            "device_id": device_id,
                            "data": data
                        }
                    }
                    self.mcp_activity_log.append(log_entry)
                    
                    return {"success": True, "message": "Data written successfully"}
                else:
                    return {"error": f"Failed to write to device: {response.status_code}"}
        except Exception as e:
            logger.error(f"Error writing to device {device_id}: {e}")
            return {"error": str(e)}
    
    async def troubleshoot_device(self, device_id: str) -> Dict[str, Any]:
        """Troubleshoot a device using MCP server"""
        device = self.devices.get(device_id)
        if not device:
            return {"error": "Device not found"}
        
        if not self.mcp_connected:
            return {"error": "MCP server not connected"}
        
        try:
            # Use MCP server to troubleshoot
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.mcp_server_url}/troubleshoot", json={
                    "device_id": device_id,
                    "protocol": device["protocol"],
                    "device_info": device
                })
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Log troubleshooting
                    log_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "type": "info",
                        "message": f"Troubleshooting {device['name']} ({device['protocol'].upper()})",
                        "details": {
                            "device_id": device_id,
                            "result": result
                        }
                    }
                    self.mcp_activity_log.append(log_entry)
                    
                    return {"success": True, "result": result}
                else:
                    return {"error": f"Troubleshooting failed: {response.status_code}"}
        except Exception as e:
            logger.error(f"Error troubleshooting device {device_id}: {e}")
            return {"error": str(e)}
    
    async def process_ai_query(self, query: str) -> Dict[str, Any]:
        """Process an AI query using the MCP server"""
        if not self.mcp_connected:
            return {"error": "MCP server not connected"}
        
        try:
            # Use MCP server to process query
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.mcp_server_url}/query", json={
                    "query": query,
                    "devices": list(self.devices.values())
                })
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Log AI query
                    log_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "type": "info",
                        "message": f"AI query processed: {query[:50]}...",
                        "details": {
                            "query": query,
                            "result": result
                        }
                    }
                    self.mcp_activity_log.append(log_entry)
                    
                    # Add to AI decisions
                    decision = {
                        "timestamp": datetime.now().isoformat(),
                        "query": query,
                        "action": "AI Query Processing",
                        "reasoning": result.get("reasoning", "AI processed the query"),
                        "confidence": result.get("confidence", 0.9),
                        "result": result
                    }
                    self.ai_decisions.append(decision)
                    
                    return {"success": True, "result": result}
                else:
                    return {"error": f"Query processing failed: {response.status_code}"}
        except Exception as e:
            logger.error(f"Error processing AI query: {e}")
            return {"error": str(e)}
    
    def get_devices(self) -> List[Dict[str, Any]]:
        """Get all devices"""
        return list(self.devices.values())
    
    def get_device(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific device"""
        return self.devices.get(device_id)
    
    def remove_device(self, device_id: str) -> bool:
        """Remove a device"""
        if device_id in self.devices:
            device = self.devices.pop(device_id)
            
            # Log device removal
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "type": "warning",
                "message": f"Device removed: {device['name']} ({device['protocol'].upper()})",
                "details": {
                    "device_id": device_id,
                    "protocol": device["protocol"]
                }
            }
            self.mcp_activity_log.append(log_entry)
            
            return True
        return False
    
    def get_mcp_status(self) -> Dict[str, Any]:
        """Get MCP server status"""
        return {
            "connected": self.mcp_connected,
            "devices": len(self.devices),
            "activity_log_entries": len(self.mcp_activity_log),
            "ai_decisions": len(self.ai_decisions),
            "last_activity": self.mcp_activity_log[-1]["timestamp"] if self.mcp_activity_log else None
        }
    
    def get_activity_log(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get activity log"""
        return self.mcp_activity_log[-limit:] if limit > 0 else self.mcp_activity_log
    
    def get_ai_decisions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get AI decisions"""
        return self.ai_decisions[-limit:] if limit > 0 else self.ai_decisions

# Global integration instance
integration = MCPDashboardIntegration()
