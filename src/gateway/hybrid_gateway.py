#!/usr/bin/env python3
"""
Hybrid Gateway - Edge AI + Cloud Context
Minimal local AI processing with cloud context retrieval
"""

import asyncio
import json
import logging
import aiohttp
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ml.local_ai_engine import LocalAIEngine
from cloud.context_service import CloudContextService, DeviceFingerprint, DeviceContext

logger = logging.getLogger(__name__)


class HybridGateway:
    """Hybrid gateway with edge AI and cloud context"""
    
    def __init__(self, cloud_service_url: str = "http://localhost:8080"):
        self.local_ai = LocalAIEngine()
        self.cloud_service_url = cloud_service_url
        self.device_contexts = {}  # Cache for device contexts
        self.initialized = False
    
    async def initialize(self):
        """Initialize the hybrid gateway"""
        try:
            # Initialize local AI engine
            await self.local_ai.initialize()
            
            self.initialized = True
            logger.info("Hybrid gateway initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize hybrid gateway: {e}")
            self.initialized = False
    
    async def handle_device_connection(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle new device connection with hybrid AI approach"""
        try:
            if not self.initialized:
                return {"error": "Gateway not initialized"}
            
            # Step 1: Use local TinyML to identify protocol
            logger.info("🔍 Step 1: Local AI protocol identification")
            protocol_result = await self.local_ai.classify_device_type(network_data)
            
            if not protocol_result.get("success"):
                return {"error": "Failed to identify protocol"}
            
            protocol = protocol_result["device_type"]
            confidence = protocol_result["confidence"]
            
            logger.info(f"   Protocol identified: {protocol} (confidence: {confidence:.3f})")
            
            # Step 2: Create device fingerprint
            fingerprint = self._create_device_fingerprint(network_data, protocol)
            
            # Step 3: Check if we have cached context
            cache_key = self._generate_cache_key(fingerprint)
            if cache_key in self.device_contexts:
                logger.info("📋 Step 3: Using cached device context")
                context = self.device_contexts[cache_key]
            else:
                # Step 4: Request context from cloud
                logger.info("☁️ Step 4: Requesting device context from cloud")
                context = await self._request_cloud_context(fingerprint)
                
                if context:
                    self.device_contexts[cache_key] = context
                    logger.info(f"   Context retrieved: {context.manufacturer} {context.model}")
                else:
                    logger.warning("   No context found in cloud")
                    return {"error": "Device context not available"}
            
            # Step 5: Use context to handle device
            logger.info("🔧 Step 5: Using context to handle device")
            result = await self._handle_device_with_context(network_data, context)
            
            return {
                "success": True,
                "protocol": protocol,
                "device_context": {
                    "manufacturer": context.manufacturer,
                    "model": context.model,
                    "device_type": context.device_type,
                    "confidence": context.confidence,
                    "vector_similarity": context.vector_similarity
                },
                "handling_result": result,
                "processing_method": "hybrid_edge_cloud",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error handling device connection: {e}")
            return {"error": str(e)}
    
    def _create_device_fingerprint(self, network_data: Dict[str, Any], protocol: str) -> DeviceFingerprint:
        """Create device fingerprint from network data"""
        return DeviceFingerprint(
            protocol=protocol,
            port=network_data.get("port", 0),
            device_id=network_data.get("device_id"),
            vendor_id=network_data.get("vendor_id"),
            model_name=network_data.get("model_name"),
            firmware_version=network_data.get("firmware_version"),
            network_features={
                "response_time": network_data.get("response_time", 0),
                "data_size": network_data.get("data_size", 0),
                "http_headers": network_data.get("http_headers", 0),
                "has_json": network_data.get("has_json", False)
            },
            communication_pattern={
                "request_frequency": network_data.get("request_frequency", 0),
                "data_pattern": network_data.get("data_pattern", "unknown")
            }
        )
    
    def _generate_cache_key(self, fingerprint: DeviceFingerprint) -> str:
        """Generate cache key for device fingerprint"""
        key_data = f"{fingerprint.protocol}_{fingerprint.port}_{fingerprint.vendor_id}_{fingerprint.model_name}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    async def _request_cloud_context(self, fingerprint: DeviceFingerprint) -> Optional[DeviceContext]:
        """Request device context from cloud service"""
        try:
            # In a real implementation, this would make an HTTP request to the cloud service
            # For demo, we'll simulate the cloud service locally
            
            # Simulate cloud service call
            cloud_service = CloudContextService()
            context = await cloud_service.get_device_context(fingerprint)
            
            return context
            
        except Exception as e:
            logger.error(f"Error requesting cloud context: {e}")
            return None
    
    async def _handle_device_with_context(self, network_data: Dict[str, Any], context: DeviceContext) -> Dict[str, Any]:
        """Handle device using cloud context"""
        try:
            # Use the context to understand device capabilities
            result = {
                "device_handled": True,
                "parameters_available": list(context.parameters.keys()),
                "error_codes_known": list(context.error_codes.keys()),
                "troubleshooting_available": len(context.troubleshooting_guide),
                "maintenance_schedule": context.maintenance_schedule,
                "protocol_spec": {
                    "type": context.device_type,
                    "manufacturer": context.manufacturer,
                    "model": context.model
                }
            }
            
            # Simulate device interaction based on context
            if context.device_type == "hvac_controller":
                result["interaction"] = await self._handle_hvac_device(network_data, context)
            elif context.device_type == "environmental_sensor":
                result["interaction"] = await self._handle_sensor_device(network_data, context)
            else:
                result["interaction"] = await self._handle_generic_device(network_data, context)
            
            return result
            
        except Exception as e:
            logger.error(f"Error handling device with context: {e}")
            return {"error": str(e)}
    
    async def _handle_hvac_device(self, network_data: Dict[str, Any], context: DeviceContext) -> Dict[str, Any]:
        """Handle HVAC device using context"""
        return {
            "device_type": "hvac_controller",
            "actions": [
                "Read room temperature",
                "Set temperature setpoint",
                "Control fan mode",
                "Monitor system status"
            ],
            "parameters": {
                "room_temperature": "AI:1 - Current room temperature",
                "setpoint": "AV:1 - Temperature setpoint",
                "fan_mode": "MSV:1 - Fan operation mode"
            },
            "error_handling": "BACnet error codes available",
            "maintenance": "Filter replacement every 30 days"
        }
    
    async def _handle_sensor_device(self, network_data: Dict[str, Any], context: DeviceContext) -> Dict[str, Any]:
        """Handle sensor device using context"""
        return {
            "device_type": "environmental_sensor",
            "actions": [
                "Read temperature",
                "Read humidity",
                "Read pressure",
                "Check sensor status"
            ],
            "endpoints": {
                "temperature": "/api/temperature",
                "humidity": "/api/humidity",
                "pressure": "/api/pressure"
            },
            "accuracy": "±0.1°C temperature, ±1.5%RH humidity",
            "maintenance": "Calibration every 180 days"
        }
    
    async def _handle_generic_device(self, network_data: Dict[str, Any], context: DeviceContext) -> Dict[str, Any]:
        """Handle generic device using context"""
        return {
            "device_type": "generic_device",
            "actions": ["Read device values", "Monitor status"],
            "parameters": list(context.parameters.keys()),
            "error_handling": "Generic error codes available"
        }
    
    async def get_device_status(self, device_id: str) -> Dict[str, Any]:
        """Get status of a connected device"""
        if device_id not in self.device_contexts:
            return {"error": "Device not found"}
        
        context = self.device_contexts[device_id]
        return {
            "device_id": device_id,
            "manufacturer": context.manufacturer,
            "model": context.model,
            "device_type": context.device_type,
            "confidence": context.confidence,
            "vector_similarity": context.vector_similarity,
            "parameters_available": len(context.parameters),
            "error_codes_known": len(context.error_codes),
            "troubleshooting_steps": len(context.troubleshooting_guide)
        }
    
    async def troubleshoot_device(self, device_id: str, error_code: str) -> Dict[str, Any]:
        """Troubleshoot device issue using cloud context"""
        if device_id not in self.device_contexts:
            return {"error": "Device not found"}
        
        context = self.device_contexts[device_id]
        
        # Look up error code
        error_description = context.error_codes.get(error_code, "Unknown error code")
        
        # Get troubleshooting steps
        troubleshooting_steps = context.troubleshooting_guide
        
        return {
            "device_id": device_id,
            "error_code": error_code,
            "error_description": error_description,
            "troubleshooting_steps": troubleshooting_steps,
            "maintenance_schedule": context.maintenance_schedule,
            "context_source": "cloud_vector_db"
        }
    
    def get_gateway_info(self) -> Dict[str, Any]:
        """Get gateway information"""
        return {
            "gateway_type": "hybrid_edge_cloud",
            "local_ai_models": self.local_ai.get_model_info(),
            "cached_devices": len(self.device_contexts),
            "cloud_service_url": self.cloud_service_url,
            "capabilities": [
                "Local protocol identification",
                "Cloud device context retrieval",
                "Vector database search",
                "Free LLM integration",
                "Device troubleshooting",
                "Maintenance scheduling"
            ]
        }


# Demo function
async def demo_hybrid_gateway():
    """Demonstrate hybrid gateway functionality"""
    print("🔗 Hybrid Gateway Demo")
    print("=" * 50)
    
    # Initialize hybrid gateway
    gateway = HybridGateway()
    await gateway.initialize()
    
    print(f"✅ Gateway initialized")
    print(f"   Local AI Models: {gateway.local_ai.get_model_info()['total_models']}")
    print(f"   Total Model Size: {gateway.local_ai.get_model_info()['total_size_kb']:.2f} KB")
    
    # Test device connections
    test_devices = [
        {
            "port": 47808,
            "protocol": "udp",
            "response_time": 25,
            "data_size": 128,
            "device_id": "12345",
            "vendor_id": "260",
            "model_name": "Metasys NAE55",
            "firmware_version": "2.1.3"
        },
        {
            "port": 8000,
            "protocol": "tcp",
            "response_time": 50,
            "data_size": 1024,
            "http_headers": 8,
            "has_json": True,
            "device_id": "sensor_001",
            "model_name": "SHT40"
        }
    ]
    
    for i, device_data in enumerate(test_devices, 1):
        print(f"\n--- Device Connection {i} ---")
        print(f"Port: {device_data['port']}")
        print(f"Device ID: {device_data.get('device_id', 'N/A')}")
        print(f"Model: {device_data.get('model_name', 'N/A')}")
        
        # Handle device connection
        result = await gateway.handle_device_connection(device_data)
        
        if result.get("success"):
            print(f"✅ Device handled successfully")
            print(f"   Protocol: {result['protocol']}")
            print(f"   Manufacturer: {result['device_context']['manufacturer']}")
            print(f"   Model: {result['device_context']['model']}")
            print(f"   Confidence: {result['device_context']['confidence']:.3f}")
            print(f"   Vector Similarity: {result['device_context']['vector_similarity']:.3f}")
            
            # Show handling result
            handling = result['handling_result']
            print(f"   Parameters Available: {len(handling['parameters_available'])}")
            print(f"   Error Codes Known: {handling['error_codes_known']}")
            print(f"   Troubleshooting Steps: {handling['troubleshooting_available']}")
        else:
            print(f"❌ Device handling failed: {result.get('error', 'Unknown error')}")
    
    # Show gateway info
    print(f"\n📊 Gateway Information:")
    gateway_info = gateway.get_gateway_info()
    print(f"   Gateway Type: {gateway_info['gateway_type']}")
    print(f"   Cached Devices: {gateway_info['cached_devices']}")
    print(f"   Capabilities: {', '.join(gateway_info['capabilities'])}")
    
    print(f"\n🎉 Hybrid Gateway Demo Complete!")


if __name__ == "__main__":
    asyncio.run(demo_hybrid_gateway())
