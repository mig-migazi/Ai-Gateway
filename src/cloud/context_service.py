#!/usr/bin/env python3
"""
Cloud Context Service
Provides device context and documentation from vector database
Uses free LLMs for device identification and context extraction
"""

import asyncio
import json
import logging
import hashlib
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import aiohttp
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class DeviceFingerprint:
    """Device fingerprint for cloud lookup"""
    protocol: str
    port: int
    device_id: Optional[str] = None
    vendor_id: Optional[str] = None
    model_name: Optional[str] = None
    firmware_version: Optional[str] = None
    network_features: Dict[str, Any] = None
    communication_pattern: Dict[str, Any] = None


@dataclass
class DeviceContext:
    """Device context returned from cloud"""
    device_id: str
    device_type: str
    manufacturer: str
    model: str
    protocol_spec: Dict[str, Any]
    parameters: Dict[str, Any]
    error_codes: Dict[str, str]
    troubleshooting_guide: List[str]
    maintenance_schedule: Dict[str, int]
    vector_similarity: float
    confidence: float


class FreeLLMService:
    """Service for using free LLMs (Hugging Face, Ollama, etc.)"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://api-inference.huggingface.co/models"
        self.model = "microsoft/DialoGPT-medium"  # Free model for text generation
    
    async def identify_device(self, fingerprint: DeviceFingerprint) -> Dict[str, Any]:
        """Use free LLM to identify device from fingerprint"""
        try:
            # Create prompt for device identification
            prompt = self._create_identification_prompt(fingerprint)
            
            # For demo, we'll simulate LLM response
            # In real implementation, this would call Hugging Face API
            response = await self._simulate_llm_identification(fingerprint)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in LLM device identification: {e}")
            return {"error": str(e)}
    
    def _create_identification_prompt(self, fingerprint: DeviceFingerprint) -> str:
        """Create prompt for device identification"""
        return f"""
        Identify this industrial device based on its network fingerprint:
        
        Protocol: {fingerprint.protocol}
        Port: {fingerprint.port}
        Device ID: {fingerprint.device_id}
        Vendor ID: {fingerprint.vendor_id}
        Model: {fingerprint.model_name}
        Firmware: {fingerprint.firmware_version}
        
        Please identify the device type, manufacturer, and model.
        """
    
    async def _simulate_llm_identification(self, fingerprint: DeviceFingerprint) -> Dict[str, Any]:
        """Simulate LLM response for device identification"""
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        # Mock device identification based on fingerprint
        if fingerprint.protocol == "BACnet":
            if fingerprint.port == 47808:
                return {
                    "device_type": "hvac_controller",
                    "manufacturer": "Honeywell",
                    "model": "T6 Pro Smart Thermostat",
                    "confidence": 0.92,
                    "reasoning": "BACnet/IP on standard port 47808, Honeywell vendor ID detected"
                }
            elif fingerprint.vendor_id == "260":
                return {
                    "device_type": "building_controller",
                    "manufacturer": "Johnson Controls",
                    "model": "Metasys NAE55",
                    "confidence": 0.88,
                    "reasoning": "Johnson Controls vendor ID 260 with BACnet protocol"
                }
        
        elif fingerprint.protocol == "REST":
            if fingerprint.port == 8000:
                return {
                    "device_type": "environmental_sensor",
                    "manufacturer": "Sensirion",
                    "model": "SHT40 Temperature/Humidity Sensor",
                    "confidence": 0.85,
                    "reasoning": "REST API on port 8000, environmental sensor endpoints detected"
                }
        
        return {
            "device_type": "unknown_device",
            "manufacturer": "unknown",
            "model": "unknown",
            "confidence": 0.1,
            "reasoning": "Unable to identify device from fingerprint"
        }


class VectorDatabase:
    """Vector database for device documentation storage and retrieval"""
    
    def __init__(self):
        self.device_docs = {}
        self.vector_embeddings = {}
        self._initialize_sample_docs()
    
    def _initialize_sample_docs(self):
        """Initialize with sample device documentation"""
        # Honeywell T6 Pro Smart Thermostat
        self.device_docs["honeywell_t6_pro"] = {
            "device_id": "honeywell_t6_pro",
            "device_type": "hvac_controller",
            "manufacturer": "Honeywell",
            "model": "T6 Pro Smart Thermostat",
            "protocol": "BACnet",
            "documentation": {
                "parameters": {
                    "room_temperature": {
                        "name": "Room Temperature",
                        "type": "analog_input",
                        "object_type": "AI",
                        "object_instance": 1,
                        "units": "degrees-celsius",
                        "range": [15.0, 35.0],
                        "resolution": 0.1,
                        "description": "Current room temperature reading"
                    },
                    "setpoint": {
                        "name": "Temperature Setpoint",
                        "type": "analog_value",
                        "object_type": "AV",
                        "object_instance": 1,
                        "units": "degrees-celsius",
                        "range": [16.0, 30.0],
                        "resolution": 0.5,
                        "description": "Desired temperature setting"
                    },
                    "fan_mode": {
                        "name": "Fan Mode",
                        "type": "multi_state_value",
                        "object_type": "MSV",
                        "object_instance": 1,
                        "states": ["auto", "on", "circulate"],
                        "description": "Fan operation mode"
                    }
                },
                "error_codes": {
                    "E001": "Temperature sensor failure - Check sensor connection and calibration",
                    "E002": "Communication timeout - Verify network connectivity",
                    "E003": "Setpoint out of range - Adjust setpoint within valid range",
                    "E004": "Fan motor fault - Check fan motor and wiring",
                    "E005": "Display error - Reset thermostat or replace display"
                },
                "troubleshooting": [
                    "If temperature reading is incorrect, check sensor placement and calibration",
                    "For communication issues, verify BACnet network configuration",
                    "If setpoint changes are not working, check user permissions",
                    "For fan issues, inspect fan motor and electrical connections",
                    "Display problems may require thermostat reset or replacement"
                ],
                "maintenance": {
                    "sensor_calibration": 90,  # days
                    "filter_replacement": 30,  # days
                    "system_inspection": 180,  # days
                    "firmware_update": 365     # days
                }
            }
        }
        
        # Sensirion SHT40 Environmental Sensor
        self.device_docs["sensirion_sht40"] = {
            "device_id": "sensirion_sht40",
            "device_type": "environmental_sensor",
            "manufacturer": "Sensirion",
            "model": "SHT40 Temperature/Humidity Sensor",
            "protocol": "REST",
            "documentation": {
                "parameters": {
                    "temperature": {
                        "name": "Temperature",
                        "type": "float",
                        "endpoint": "/api/temperature",
                        "units": "celsius",
                        "range": [-40.0, 85.0],
                        "accuracy": "±0.1°C",
                        "description": "Ambient temperature reading"
                    },
                    "humidity": {
                        "name": "Relative Humidity",
                        "type": "float",
                        "endpoint": "/api/humidity",
                        "units": "percent",
                        "range": [0.0, 100.0],
                        "accuracy": "±1.5%RH",
                        "description": "Relative humidity reading"
                    },
                    "pressure": {
                        "name": "Atmospheric Pressure",
                        "type": "float",
                        "endpoint": "/api/pressure",
                        "units": "hPa",
                        "range": [300.0, 1100.0],
                        "accuracy": "±1hPa",
                        "description": "Atmospheric pressure reading"
                    }
                },
                "error_codes": {
                    "S001": "Sensor reading out of range - Check sensor calibration",
                    "S002": "Communication error - Verify network connection",
                    "S003": "Sensor calibration required - Perform calibration procedure",
                    "S004": "Power supply issue - Check power connections",
                    "S005": "Sensor drift detected - Recalibrate or replace sensor"
                },
                "troubleshooting": [
                    "For inaccurate readings, check sensor placement and environmental conditions",
                    "Communication errors may indicate network or power issues",
                    "Regular calibration ensures measurement accuracy",
                    "Check for condensation or contamination on sensor surface",
                    "Verify sensor is not exposed to extreme conditions"
                ],
                "maintenance": {
                    "calibration": 180,    # days
                    "cleaning": 90,       # days
                    "replacement": 365,   # days
                    "firmware_update": 365 # days
                }
            }
        }
        
        # Generate simple vector embeddings (in real implementation, use proper embeddings)
        for device_id, doc in self.device_docs.items():
            self.vector_embeddings[device_id] = self._generate_embedding(doc)
    
    def _generate_embedding(self, doc: Dict[str, Any]) -> np.ndarray:
        """Generate simple embedding for document (in real implementation, use proper embeddings)"""
        # Simple hash-based embedding for demo
        text = f"{doc['manufacturer']} {doc['model']} {doc['device_type']} {doc['protocol']}"
        hash_obj = hashlib.md5(text.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert to numpy array
        embedding = np.frombuffer(hash_bytes, dtype=np.uint8).astype(np.float32)
        embedding = embedding / 255.0  # Normalize to 0-1
        
        # Pad or truncate to fixed size
        target_size = 128
        if len(embedding) < target_size:
            embedding = np.pad(embedding, (0, target_size - len(embedding)))
        else:
            embedding = embedding[:target_size]
        
        return embedding
    
    async def search_similar_devices(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Tuple[str, float]]:
        """Search for similar devices using vector similarity"""
        similarities = []
        
        for device_id, embedding in self.vector_embeddings.items():
            # Calculate cosine similarity
            similarity = np.dot(query_embedding, embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(embedding)
            )
            similarities.append((device_id, similarity))
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def get_device_context(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Get device context by ID"""
        return self.device_docs.get(device_id)


class CloudContextService:
    """Main cloud context service"""
    
    def __init__(self, llm_api_key: str = None):
        self.llm_service = FreeLLMService(llm_api_key)
        self.vector_db = VectorDatabase()
        self.request_cache = {}  # Cache for recent requests
    
    async def get_device_context(self, fingerprint: DeviceFingerprint) -> Optional[DeviceContext]:
        """Get device context from cloud based on fingerprint"""
        try:
            # Check cache first
            cache_key = self._generate_cache_key(fingerprint)
            if cache_key in self.request_cache:
                logger.info(f"Returning cached context for {cache_key}")
                return self.request_cache[cache_key]
            
            # Step 1: Use LLM to identify device
            identification = await self.llm_service.identify_device(fingerprint)
            
            if identification.get("error"):
                logger.error(f"Device identification failed: {identification['error']}")
                return None
            
            # Step 2: Generate query embedding for vector search
            query_text = f"{identification['manufacturer']} {identification['model']} {identification['device_type']}"
            query_embedding = self._generate_query_embedding(query_text)
            
            # Step 3: Search vector database for similar devices
            similar_devices = await self.vector_db.search_similar_devices(query_embedding, top_k=1)
            
            if not similar_devices:
                logger.warning("No similar devices found in vector database")
                return None
            
            device_id, similarity = similar_devices[0]
            
            # Step 4: Get device context
            device_doc = self.vector_db.get_device_context(device_id)
            
            if not device_doc:
                logger.error(f"Device context not found for {device_id}")
                return None
            
            # Step 5: Create device context response
            context = DeviceContext(
                device_id=device_id,
                device_type=device_doc["device_type"],
                manufacturer=device_doc["manufacturer"],
                model=device_doc["model"],
                protocol_spec=device_doc["documentation"],
                parameters=device_doc["documentation"]["parameters"],
                error_codes=device_doc["documentation"]["error_codes"],
                troubleshooting_guide=device_doc["documentation"]["troubleshooting"],
                maintenance_schedule=device_doc["documentation"]["maintenance"],
                vector_similarity=similarity,
                confidence=identification["confidence"]
            )
            
            # Cache the result
            self.request_cache[cache_key] = context
            
            logger.info(f"Successfully retrieved context for {device_id} (similarity: {similarity:.3f})")
            return context
            
        except Exception as e:
            logger.error(f"Error getting device context: {e}")
            return None
    
    def _generate_cache_key(self, fingerprint: DeviceFingerprint) -> str:
        """Generate cache key for fingerprint"""
        key_data = f"{fingerprint.protocol}_{fingerprint.port}_{fingerprint.vendor_id}_{fingerprint.model_name}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _generate_query_embedding(self, query_text: str) -> np.ndarray:
        """Generate embedding for query text"""
        # Simple hash-based embedding for demo
        hash_obj = hashlib.md5(query_text.encode())
        hash_bytes = hash_obj.digest()
        
        embedding = np.frombuffer(hash_bytes, dtype=np.uint8).astype(np.float32)
        embedding = embedding / 255.0
        
        # Pad or truncate to fixed size
        target_size = 128
        if len(embedding) < target_size:
            embedding = np.pad(embedding, (0, target_size - len(embedding)))
        else:
            embedding = embedding[:target_size]
        
        return embedding


# Example usage and testing
async def main():
    """Test the cloud context service"""
    print("☁️ Cloud Context Service Demo")
    print("=" * 50)
    
    # Initialize cloud service
    cloud_service = CloudContextService()
    
    # Test device fingerprints
    test_fingerprints = [
        DeviceFingerprint(
            protocol="BACnet",
            port=47808,
            device_id="12345",
            vendor_id="260",  # Johnson Controls
            model_name="Metasys NAE55",
            firmware_version="2.1.3"
        ),
        DeviceFingerprint(
            protocol="REST",
            port=8000,
            device_id="sensor_001",
            model_name="SHT40",
            network_features={"endpoints": ["/api/temperature", "/api/humidity"]}
        ),
        DeviceFingerprint(
            protocol="BACnet",
            port=47808,
            device_id="thermostat_001",
            vendor_id="123",  # Honeywell
            model_name="T6 Pro",
            firmware_version="1.5.2"
        )
    ]
    
    for i, fingerprint in enumerate(test_fingerprints, 1):
        print(f"\n--- Test {i}: {fingerprint.protocol} Device ---")
        print(f"Port: {fingerprint.port}")
        print(f"Vendor ID: {fingerprint.vendor_id}")
        print(f"Model: {fingerprint.model_name}")
        
        # Get device context from cloud
        context = await cloud_service.get_device_context(fingerprint)
        
        if context:
            print(f"✅ Device Identified:")
            print(f"   Manufacturer: {context.manufacturer}")
            print(f"   Model: {context.model}")
            print(f"   Type: {context.device_type}")
            print(f"   Confidence: {context.confidence:.2f}")
            print(f"   Vector Similarity: {context.vector_similarity:.3f}")
            print(f"   Parameters: {len(context.parameters)}")
            print(f"   Error Codes: {len(context.error_codes)}")
            print(f"   Troubleshooting Steps: {len(context.troubleshooting_guide)}")
            
            # Show sample parameters
            print(f"   Sample Parameters:")
            for param_name, param_spec in list(context.parameters.items())[:2]:
                print(f"     - {param_spec.get('name', param_name)}: {param_spec.get('description', 'N/A')}")
        else:
            print("❌ Device context not found")
    
    print(f"\n🎉 Cloud Context Service Demo Complete!")


if __name__ == "__main__":
    asyncio.run(main())
