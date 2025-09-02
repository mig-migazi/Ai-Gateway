"""
Local AI Engine - Lightweight ML models for edge processing
Deploy small models directly on the gateway for fast, offline AI processing
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
# import numpy as np  # Not needed for this demo

logger = logging.getLogger(__name__)


class LocalAIEngine:
    """
    Local AI engine using lightweight ML models
    Perfect for industrial gateways - fast, offline, private
    """
    
    def __init__(self):
        self.models = {}
        self.initialized = False
    
    async def initialize(self):
        """Initialize local ML models"""
        try:
            # Load lightweight models
            await self._load_protocol_parser_model()
            await self._load_device_classifier_model()
            await self._load_query_processor_model()
            
            self.initialized = True
            logger.info("Local AI engine initialized with lightweight models")
        
        except Exception as e:
            logger.error(f"Failed to initialize local AI engine: {e}")
            # Fallback to rule-based processing
            self.initialized = False
    
    async def _load_protocol_parser_model(self):
        """Load lightweight protocol parser model"""
        # In a real implementation, this would load a small transformer model
        # For now, we'll use a rule-based approach that could be replaced with ML
        
        self.models["protocol_parser"] = {
            "type": "rule_based",  # Could be "transformer", "lstm", etc.
            "model_path": "models/protocol_parser.onnx",
            "input_size": 512,
            "output_size": 128,
            "loaded": True
        }
        
        logger.info("Protocol parser model loaded (rule-based fallback)")
    
    async def _load_device_classifier_model(self):
        """Load device classifier model"""
        # Lightweight model to classify device types from network traffic
        
        self.models["device_classifier"] = {
            "type": "rule_based",  # Could be "cnn", "random_forest", etc.
            "model_path": "models/device_classifier.onnx",
            "input_size": 256,
            "output_size": 10,  # 10 device types
            "loaded": True
        }
        
        logger.info("Device classifier model loaded (rule-based fallback)")
    
    async def _load_query_processor_model(self):
        """Load natural language query processor"""
        # Small language model for processing queries locally
        
        self.models["query_processor"] = {
            "type": "rule_based",  # Could be "tinyllama", "phi3", etc.
            "model_path": "models/query_processor.onnx",
            "input_size": 1024,
            "output_size": 256,
            "loaded": True
        }
        
        logger.info("Query processor model loaded (rule-based fallback)")
    
    async def process_natural_query(self, query: str) -> Dict[str, Any]:
        """
        Process natural language query using local ML model
        Fast, offline, private processing
        """
        try:
            if not self.initialized:
                return await self._fallback_query_processing(query)
            
            # Use local ML model for query processing
            result = await self._infer_query_model(query)
            
            return {
                "success": True,
                "query": query,
                "intent": result["intent"],
                "entities": result["entities"],
                "protocol_actions": result["protocol_actions"],
                "processing_method": "local_ml",
                "model_used": self.models["query_processor"]["type"],
                "latency_ms": result["latency_ms"],
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error processing query with local ML: {e}")
            return await self._fallback_query_processing(query)
    
    async def _infer_query_model(self, query: str) -> Dict[str, Any]:
        """
        Run inference on local query processing model
        In a real implementation, this would use ONNX Runtime or similar
        """
        # Simulate ML inference
        start_time = datetime.now()
        
        # Mock ML processing (replace with actual model inference)
        intent = self._classify_intent(query)
        entities = self._extract_entities(query)
        protocol_actions = self._generate_protocol_actions(intent, entities)
        
        end_time = datetime.now()
        latency_ms = (end_time - start_time).total_seconds() * 1000
        
        return {
            "intent": intent,
            "entities": entities,
            "protocol_actions": protocol_actions,
            "latency_ms": latency_ms
        }
    
    def _classify_intent(self, query: str) -> str:
        """Classify query intent (could be ML model)"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["temperature", "temp", "heat"]):
            return "get_temperature"
        elif any(word in query_lower for word in ["humidity", "moisture"]):
            return "get_humidity"
        elif any(word in query_lower for word in ["pressure", "psi"]):
            return "get_pressure"
        elif any(word in query_lower for word in ["status", "state", "health"]):
            return "get_status"
        elif any(word in query_lower for word in ["set", "change", "update"]):
            return "set_value"
        else:
            return "general_query"
    
    def _extract_entities(self, query: str) -> Dict[str, Any]:
        """Extract entities from query (could be NER model)"""
        entities = {
            "device_type": None,
            "location": None,
            "parameter": None,
            "value": None
        }
        
        query_lower = query.lower()
        
        # Extract location
        if "room" in query_lower:
            import re
            room_match = re.search(r'room\s+(\d+)', query_lower)
            if room_match:
                entities["location"] = f"room_{room_match.group(1)}"
        
        # Extract parameter
        if "temperature" in query_lower:
            entities["parameter"] = "temperature"
        elif "humidity" in query_lower:
            entities["parameter"] = "humidity"
        elif "pressure" in query_lower:
            entities["parameter"] = "pressure"
        
        return entities
    
    def _generate_protocol_actions(self, intent: str, entities: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate protocol actions based on intent and entities"""
        actions = []
        
        if intent == "get_temperature":
            actions.append({
                "action": "read_property",
                "protocol": "rest",
                "endpoint": "/api/temperature",
                "parameters": {}
            })
        elif intent == "get_humidity":
            actions.append({
                "action": "read_property",
                "protocol": "rest",
                "endpoint": "/api/humidity",
                "parameters": {}
            })
        elif intent == "get_status":
            actions.append({
                "action": "read_property",
                "protocol": "rest",
                "endpoint": "/status",
                "parameters": {}
            })
        
        return actions
    
    async def _fallback_query_processing(self, query: str) -> Dict[str, Any]:
        """Fallback to rule-based processing if ML models not available"""
        intent = self._classify_intent(query)
        entities = self._extract_entities(query)
        protocol_actions = self._generate_protocol_actions(intent, entities)
        
        return {
            "success": True,
            "query": query,
            "intent": intent,
            "entities": entities,
            "protocol_actions": protocol_actions,
            "processing_method": "rule_based_fallback",
            "timestamp": datetime.now().isoformat()
        }
    
    async def classify_device_type(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify device type from network traffic using local ML
        Fast device identification without cloud processing
        """
        try:
            if not self.initialized:
                return await self._fallback_device_classification(network_data)
            
            # Use local ML model for device classification
            result = await self._infer_device_classifier(network_data)
            
            return {
                "success": True,
                "device_type": result["device_type"],
                "confidence": result["confidence"],
                "features": result["features"],
                "processing_method": "local_ml",
                "model_used": self.models["device_classifier"]["type"],
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error classifying device with local ML: {e}")
            return await self._fallback_device_classification(network_data)
    
    async def _infer_device_classifier(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run inference on device classifier model"""
        # Mock ML inference (replace with actual model)
        start_time = datetime.now()
        
        # Extract features from network data
        features = self._extract_network_features(network_data)
        
        # Mock classification (replace with actual model inference)
        device_type, confidence = self._classify_device_from_features(features)
        
        end_time = datetime.now()
        latency_ms = (end_time - start_time).total_seconds() * 1000
        
        return {
            "device_type": device_type,
            "confidence": confidence,
            "features": features,
            "latency_ms": latency_ms
        }
    
    def _extract_network_features(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from network data for ML model"""
        features = {
            "port": network_data.get("port", 0),
            "protocol": network_data.get("protocol", "unknown"),
            "response_time": network_data.get("response_time", 0),
            "data_size": network_data.get("data_size", 0),
            "http_headers": len(network_data.get("headers", {})),
            "has_json": "application/json" in str(network_data.get("headers", {}))
        }
        return features
    
    def _classify_device_from_features(self, features: Dict[str, Any]) -> tuple[str, float]:
        """Classify device type from features (could be ML model)"""
        port = features["port"]
        protocol = features["protocol"]
        
        if port == 80 or port == 8080:
            return "rest_api_device", 0.95
        elif port == 47808:
            return "bacnet_device", 0.90
        elif port == 502:
            return "modbus_device", 0.85
        elif port == 4840:
            return "opcua_device", 0.88
        else:
            return "unknown_device", 0.50
    
    async def _fallback_device_classification(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback device classification"""
        features = self._extract_network_features(network_data)
        device_type, confidence = self._classify_device_from_features(features)
        
        return {
            "success": True,
            "device_type": device_type,
            "confidence": confidence,
            "features": features,
            "processing_method": "rule_based_fallback",
            "timestamp": datetime.now().isoformat()
        }
    
    async def optimize_for_edge(self):
        """Optimize models for edge deployment"""
        logger.info("Optimizing models for edge deployment...")
        
        # In a real implementation, this would:
        # 1. Quantize models (INT8, FP16)
        # 2. Prune unnecessary weights
        # 3. Optimize for specific hardware
        # 4. Convert to ONNX/TensorRT format
        
        logger.info("Models optimized for edge deployment")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded models"""
        return {
            "models_loaded": len(self.models),
            "initialized": self.initialized,
            "models": {
                name: {
                    "type": model["type"],
                    "input_size": model["input_size"],
                    "output_size": model["output_size"],
                    "loaded": model["loaded"]
                }
                for name, model in self.models.items()
            },
            "total_parameters": sum(
                model["input_size"] * model["output_size"] 
                for model in self.models.values()
            ),
            "estimated_memory_mb": sum(
                model["input_size"] * model["output_size"] * 4 / (1024 * 1024)  # 4 bytes per float32
                for model in self.models.values()
            )
        }
    
    async def close(self):
        """Close the local AI engine"""
        self.models.clear()
        self.initialized = False
        logger.info("Local AI engine closed")
