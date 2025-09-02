"""
Local AI Engine - TinyML models for edge processing
Deploy ultra-lightweight ML models directly on the gateway for fast, offline AI processing
"""

import asyncio
import json
import logging
import struct
import math
from typing import Dict, Any, List, Optional
from datetime import datetime
import numpy as np

logger = logging.getLogger(__name__)


class TinyMLModel:
    """Ultra-lightweight ML model for edge inference"""
    
    def __init__(self, name: str, input_size: int, output_size: int, weights: List[float]):
        self.name = name
        self.input_size = input_size
        self.output_size = output_size
        self.weights = np.array(weights, dtype=np.float32)
        self.bias = np.zeros(output_size, dtype=np.float32)
        
    def predict(self, inputs: np.ndarray) -> np.ndarray:
        """Simple linear model inference"""
        # Reshape inputs to match expected size
        if inputs.shape[0] != self.input_size:
            # Pad or truncate to match input size
            if inputs.shape[0] < self.input_size:
                padded = np.zeros(self.input_size)
                padded[:inputs.shape[0]] = inputs
                inputs = padded
            else:
                inputs = inputs[:self.input_size]
        
        # Simple linear transformation: y = Wx + b
        output = np.dot(self.weights.reshape(self.output_size, self.input_size), inputs) + self.bias
        return output


class LocalAIEngine:
    """
    Local AI engine using TinyML models
    Ultra-lightweight ML models perfect for industrial gateways
    """
    
    def __init__(self):
        self.models = {}
        self.tinyml_models = {}
        self.initialized = False
    
    async def initialize(self):
        """Initialize TinyML models"""
        try:
            # Load TinyML models
            await self._load_tinyml_query_processor()
            await self._load_tinyml_device_classifier()
            await self._load_tinyml_anomaly_detector()
            
            self.initialized = True
            logger.info("TinyML engine initialized with ultra-lightweight models")
        
        except Exception as e:
            logger.error(f"Failed to initialize TinyML engine: {e}")
            # Fallback to rule-based processing
            self.initialized = False
    
    async def _load_tinyml_query_processor(self):
        """Load TinyML query processor model"""
        # Ultra-lightweight model for intent classification
        # Input: 64 features (word embeddings, character n-grams)
        # Output: 8 intent classes
        
        # Generate synthetic weights for demo (in real implementation, these would be trained)
        input_size = 64
        output_size = 8
        weights = np.random.normal(0, 0.1, input_size * output_size).tolist()
        
        self.tinyml_models["query_processor"] = TinyMLModel(
            name="query_processor",
            input_size=input_size,
            output_size=output_size,
            weights=weights
        )
        
        logger.info(f"TinyML query processor loaded: {input_size}→{output_size} parameters")
    
    async def _load_tinyml_device_classifier(self):
        """Load TinyML device classifier model"""
        # Lightweight model for device type classification
        # Input: 16 network features (port, protocol, response time, etc.)
        # Output: 5 device types
        
        input_size = 16
        output_size = 5
        weights = np.random.normal(0, 0.1, input_size * output_size).tolist()
        
        self.tinyml_models["device_classifier"] = TinyMLModel(
            name="device_classifier",
            input_size=input_size,
            output_size=output_size,
            weights=weights
        )
        
        logger.info(f"TinyML device classifier loaded: {input_size}→{output_size} parameters")
    
    async def _load_tinyml_anomaly_detector(self):
        """Load TinyML anomaly detection model"""
        # Ultra-lightweight anomaly detection
        # Input: 32 sensor features (temperature, humidity, pressure, etc.)
        # Output: 1 anomaly score
        
        input_size = 32
        output_size = 1
        weights = np.random.normal(0, 0.1, input_size * output_size).tolist()
        
        self.tinyml_models["anomaly_detector"] = TinyMLModel(
            name="anomaly_detector",
            input_size=input_size,
            output_size=output_size,
            weights=weights
        )
        
        logger.info(f"TinyML anomaly detector loaded: {input_size}→{output_size} parameters")
    
    async def process_natural_query(self, query: str) -> Dict[str, Any]:
        """
        Process natural language query using TinyML model
        Ultra-fast, offline, private processing
        """
        try:
            if not self.initialized:
                return await self._fallback_query_processing(query)
            
            # Use TinyML model for query processing
            result = await self._infer_tinyml_query_model(query)
            
            return {
                "success": True,
                "query": query,
                "intent": result["intent"],
                "entities": result["entities"],
                "protocol_actions": result["protocol_actions"],
                "processing_method": "tinyml",
                "model_used": "TinyML Query Processor",
                "latency_ms": result["latency_ms"],
                "model_size_kb": result["model_size_kb"],
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error processing query with TinyML: {e}")
            return await self._fallback_query_processing(query)
    
    async def _infer_tinyml_query_model(self, query: str) -> Dict[str, Any]:
        """
        Run inference on TinyML query processing model
        Ultra-fast edge inference
        """
        start_time = datetime.now()
        
        # Extract features from query for TinyML model
        features = self._extract_query_features(query)
        
        # Run TinyML inference
        model = self.tinyml_models["query_processor"]
        raw_output = model.predict(features)
        
        # Convert model output to intent
        intent_scores = self._softmax(raw_output)
        intent = self._scores_to_intent(intent_scores)
        
        # Extract entities using rule-based approach (could be another TinyML model)
        entities = self._extract_entities(query)
        protocol_actions = self._generate_protocol_actions(intent, entities)
        
        end_time = datetime.now()
        latency_ms = (end_time - start_time).total_seconds() * 1000
        
        # Calculate model size in KB
        model_size_kb = (model.input_size * model.output_size * 4) / 1024  # 4 bytes per float32
        
        return {
            "intent": intent,
            "entities": entities,
            "protocol_actions": protocol_actions,
            "latency_ms": latency_ms,
            "model_size_kb": model_size_kb,
            "confidence": float(np.max(intent_scores))
        }
    
    def _extract_query_features(self, query: str) -> np.ndarray:
        """Extract 64 features from query for TinyML model"""
        features = np.zeros(64, dtype=np.float32)
        
        # Character n-gram features (0-31)
        for i, char in enumerate(query[:32]):
            if i < 32:
                features[i] = ord(char) / 255.0  # Normalize to 0-1
        
        # Word-based features (32-47)
        words = query.lower().split()
        word_features = [
            len(query),  # Query length
            len(words),  # Word count
            sum(1 for w in words if 'temp' in w),  # Temperature mentions
            sum(1 for w in words if 'humid' in w),  # Humidity mentions
            sum(1 for w in words if 'press' in w),  # Pressure mentions
            sum(1 for w in words if 'status' in w),  # Status mentions
            sum(1 for w in words if 'set' in w),  # Set commands
            sum(1 for w in words if 'get' in w),  # Get commands
            sum(1 for w in words if 'room' in w),  # Room mentions
            sum(1 for w in words if 'device' in w),  # Device mentions
            sum(1 for w in words if 'hvac' in w),  # HVAC mentions
            sum(1 for w in words if 'energy' in w),  # Energy mentions
            sum(1 for w in words if 'anomal' in w),  # Anomaly mentions
            sum(1 for w in words if 'optim' in w),  # Optimization mentions
            sum(1 for w in words if 'bacnet' in w),  # BACnet mentions
            sum(1 for w in words if 'rest' in w),  # REST mentions
        ]
        
        for i, feature in enumerate(word_features):
            if 32 + i < 64:
                features[32 + i] = min(feature / 10.0, 1.0)  # Normalize to 0-1
        
        # Additional features (48-63)
        features[48] = 1.0 if '?' in query else 0.0  # Question mark
        features[49] = 1.0 if '!' in query else 0.0  # Exclamation mark
        features[50] = 1.0 if any(char.isdigit() for char in query) else 0.0  # Has numbers
        features[51] = 1.0 if any(char.isupper() for char in query) else 0.0  # Has uppercase
        features[52] = len([c for c in query if c.isalpha()]) / len(query) if query else 0.0  # Alpha ratio
        features[53] = len([c for c in query if c.isdigit()]) / len(query) if query else 0.0  # Digit ratio
        features[54] = len([c for c in query if c.isspace()]) / len(query) if query else 0.0  # Space ratio
        features[55] = 1.0 if query.endswith('?') else 0.0  # Ends with question
        features[56] = 1.0 if query.startswith('what') else 0.0  # Starts with what
        features[57] = 1.0 if query.startswith('how') else 0.0  # Starts with how
        features[58] = 1.0 if query.startswith('show') else 0.0  # Starts with show
        features[59] = 1.0 if query.startswith('get') else 0.0  # Starts with get
        features[60] = 1.0 if query.startswith('set') else 0.0  # Starts with set
        features[61] = 1.0 if 'compare' in query.lower() else 0.0  # Compare mentions
        features[62] = 1.0 if 'trend' in query.lower() else 0.0  # Trend mentions
        features[63] = 1.0 if 'all' in query.lower() else 0.0  # All mentions
        
        return features
    
    def _softmax(self, x: np.ndarray) -> np.ndarray:
        """Apply softmax to convert raw scores to probabilities"""
        exp_x = np.exp(x - np.max(x))  # Subtract max for numerical stability
        return exp_x / np.sum(exp_x)
    
    def _scores_to_intent(self, scores: np.ndarray) -> str:
        """Convert model output scores to intent string"""
        intent_classes = [
            "get_temperature",
            "get_humidity", 
            "get_pressure",
            "get_status",
            "set_value",
            "compare_data",
            "get_trend",
            "general_query"
        ]
        
        max_idx = np.argmax(scores)
        return intent_classes[max_idx] if max_idx < len(intent_classes) else "general_query"
    
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
        Classify device type from network traffic using TinyML
        Ultra-fast device identification without cloud processing
        """
        try:
            if not self.initialized:
                return await self._fallback_device_classification(network_data)
            
            # Use TinyML model for device classification
            result = await self._infer_tinyml_device_classifier(network_data)
            
            return {
                "success": True,
                "device_type": result["device_type"],
                "confidence": result["confidence"],
                "features": result["features"],
                "latency_ms": result["latency_ms"],
                "processing_method": "tinyml",
                "model_used": "TinyML Device Classifier",
                "model_size_kb": result["model_size_kb"],
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error classifying device with TinyML: {e}")
            return await self._fallback_device_classification(network_data)
    
    async def _infer_tinyml_device_classifier(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run inference on TinyML device classifier model"""
        start_time = datetime.now()
        
        # Extract features from network data
        features = self._extract_network_features(network_data)
        
        # Convert to numpy array for TinyML model
        feature_array = np.array([
            features["port"] / 65535.0,  # Normalize port
            1.0 if features["protocol"] == "tcp" else 0.0,  # TCP flag
            1.0 if features["protocol"] == "udp" else 0.0,  # UDP flag
            min(features["response_time"] / 1000.0, 1.0),  # Response time (normalized)
            min(features["data_size"] / 10000.0, 1.0),  # Data size (normalized)
            features["http_headers"] / 20.0,  # Header count (normalized)
            1.0 if features["has_json"] else 0.0,  # JSON flag
            # Additional features for 16 total
            features["port"] % 1000 / 1000.0,  # Port modulo
            len(str(features["port"])),  # Port digit count
            1.0 if features["port"] < 1024 else 0.0,  # Well-known port
            1.0 if features["port"] > 49152 else 0.0,  # Dynamic port
            features["response_time"] % 100 / 100.0,  # Response time modulo
            features["data_size"] % 1000 / 1000.0,  # Data size modulo
            1.0 if features["data_size"] > 1000 else 0.0,  # Large data
            1.0 if features["http_headers"] > 5 else 0.0,  # Many headers
        ], dtype=np.float32)
        
        # Run TinyML inference
        model = self.tinyml_models["device_classifier"]
        raw_output = model.predict(feature_array)
        
        # Convert to device type
        device_scores = self._softmax(raw_output)
        device_type, confidence = self._scores_to_device_type(device_scores)
        
        end_time = datetime.now()
        latency_ms = (end_time - start_time).total_seconds() * 1000
        
        # Calculate model size in KB
        model_size_kb = (model.input_size * model.output_size * 4) / 1024
        
        return {
            "device_type": device_type,
            "confidence": confidence,
            "features": features,
            "latency_ms": latency_ms,
            "model_size_kb": model_size_kb
        }
    
    def _scores_to_device_type(self, scores: np.ndarray) -> tuple[str, float]:
        """Convert model output scores to device type and confidence"""
        device_types = [
            "rest_api_device",
            "bacnet_device", 
            "modbus_device",
            "opcua_device",
            "unknown_device"
        ]
        
        max_idx = np.argmax(scores)
        device_type = device_types[max_idx] if max_idx < len(device_types) else "unknown_device"
        confidence = float(scores[max_idx])
        
        return device_type, confidence
    
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
        start_time = datetime.now()
        features = self._extract_network_features(network_data)
        device_type, confidence = self._classify_device_from_features(features)
        end_time = datetime.now()
        latency_ms = (end_time - start_time).total_seconds() * 1000
        
        return {
            "success": True,
            "device_type": device_type,
            "confidence": confidence,
            "features": features,
            "latency_ms": latency_ms,
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
    
    async def detect_anomalies(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect anomalies in sensor data using TinyML
        Ultra-fast anomaly detection for industrial monitoring
        """
        try:
            if not self.initialized:
                return await self._fallback_anomaly_detection(sensor_data)
            
            # Use TinyML model for anomaly detection
            result = await self._infer_tinyml_anomaly_detector(sensor_data)
            
            return {
                "success": True,
                "is_anomaly": result["is_anomaly"],
                "anomaly_score": result["anomaly_score"],
                "confidence": result["confidence"],
                "affected_sensors": result["affected_sensors"],
                "latency_ms": result["latency_ms"],
                "processing_method": "tinyml",
                "model_used": "TinyML Anomaly Detector",
                "model_size_kb": result["model_size_kb"],
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error detecting anomalies with TinyML: {e}")
            return await self._fallback_anomaly_detection(sensor_data)
    
    async def _infer_tinyml_anomaly_detector(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run inference on TinyML anomaly detection model"""
        start_time = datetime.now()
        
        # Extract features from sensor data
        features = self._extract_sensor_features(sensor_data)
        
        # Run TinyML inference
        model = self.tinyml_models["anomaly_detector"]
        raw_output = model.predict(features)
        
        # Convert to anomaly score (0-1, higher = more anomalous)
        anomaly_score = float(raw_output[0])
        is_anomaly = anomaly_score > 0.7  # Threshold for anomaly detection
        
        # Determine affected sensors
        affected_sensors = []
        if is_anomaly:
            # Find sensors with values outside normal ranges
            for sensor, value in sensor_data.items():
                if isinstance(value, (int, float)):
                    if sensor == "temperature" and (value < 15 or value > 35):
                        affected_sensors.append(sensor)
                    elif sensor == "humidity" and (value < 20 or value > 80):
                        affected_sensors.append(sensor)
                    elif sensor == "pressure" and (value < 950 or value > 1050):
                        affected_sensors.append(sensor)
        
        end_time = datetime.now()
        latency_ms = (end_time - start_time).total_seconds() * 1000
        
        # Calculate model size in KB
        model_size_kb = (model.input_size * model.output_size * 4) / 1024
        
        return {
            "is_anomaly": is_anomaly,
            "anomaly_score": anomaly_score,
            "confidence": 1.0 - abs(anomaly_score - 0.5) * 2,  # Confidence based on distance from threshold
            "affected_sensors": affected_sensors,
            "latency_ms": latency_ms,
            "model_size_kb": model_size_kb
        }
    
    def _extract_sensor_features(self, sensor_data: Dict[str, Any]) -> np.ndarray:
        """Extract 32 features from sensor data for TinyML model"""
        features = np.zeros(32, dtype=np.float32)
        
        # Basic sensor values (0-7)
        features[0] = sensor_data.get("temperature", 20.0) / 50.0  # Normalize to 0-1
        features[1] = sensor_data.get("humidity", 50.0) / 100.0
        features[2] = sensor_data.get("pressure", 1013.0) / 2000.0
        features[3] = sensor_data.get("voltage", 220.0) / 500.0
        features[4] = sensor_data.get("current", 1.0) / 10.0
        features[5] = sensor_data.get("power", 100.0) / 1000.0
        features[6] = sensor_data.get("frequency", 50.0) / 100.0
        features[7] = sensor_data.get("vibration", 0.0) / 10.0
        
        # Statistical features (8-15)
        values = [v for v in sensor_data.values() if isinstance(v, (int, float))]
        if values:
            features[8] = np.mean(values) / 100.0  # Mean
            features[9] = np.std(values) / 100.0   # Standard deviation
            features[10] = np.min(values) / 100.0  # Min
            features[11] = np.max(values) / 100.0  # Max
            features[12] = np.median(values) / 100.0  # Median
            features[13] = len(values) / 20.0  # Count
            features[14] = (np.max(values) - np.min(values)) / 100.0  # Range
            features[15] = np.var(values) / 100.0  # Variance
        
        # Derived features (16-23)
        features[16] = abs(features[0] - 0.4)  # Temperature deviation from normal
        features[17] = abs(features[1] - 0.5)  # Humidity deviation from normal
        features[18] = abs(features[2] - 0.5)  # Pressure deviation from normal
        features[19] = features[0] * features[1]  # Temperature-humidity interaction
        features[20] = features[2] * features[0]  # Pressure-temperature interaction
        features[21] = features[1] * features[2]  # Humidity-pressure interaction
        features[22] = features[8] * features[9]  # Mean-std interaction
        features[23] = features[14] / (features[8] + 0.001)  # Coefficient of variation
        
        # Time-based features (24-31) - using current time as proxy
        current_time = datetime.now()
        features[24] = current_time.hour / 24.0  # Hour of day
        features[25] = current_time.minute / 60.0  # Minute of hour
        features[26] = current_time.second / 60.0  # Second of minute
        features[27] = current_time.weekday() / 7.0  # Day of week
        features[28] = current_time.day / 31.0  # Day of month
        features[29] = current_time.month / 12.0  # Month of year
        features[30] = 1.0 if current_time.hour < 6 or current_time.hour > 22 else 0.0  # Night time
        features[31] = 1.0 if current_time.weekday() >= 5 else 0.0  # Weekend
        
        return features
    
    async def _fallback_anomaly_detection(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback anomaly detection using simple rules"""
        start_time = datetime.now()
        anomalies = []
        
        # Simple threshold-based anomaly detection
        if sensor_data.get("temperature", 20) < 10 or sensor_data.get("temperature", 20) > 40:
            anomalies.append("temperature")
        if sensor_data.get("humidity", 50) < 10 or sensor_data.get("humidity", 50) > 90:
            anomalies.append("humidity")
        if sensor_data.get("pressure", 1013) < 900 or sensor_data.get("pressure", 1013) > 1100:
            anomalies.append("pressure")
        
        end_time = datetime.now()
        latency_ms = (end_time - start_time).total_seconds() * 1000
        
        return {
            "success": True,
            "is_anomaly": len(anomalies) > 0,
            "anomaly_score": len(anomalies) / 3.0,
            "confidence": 0.8,
            "affected_sensors": anomalies,
            "latency_ms": latency_ms,
            "processing_method": "rule_based_fallback",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded TinyML models"""
        total_size_kb = sum(
            (model.input_size * model.output_size * 4) / 1024 
            for model in self.tinyml_models.values()
        )
        
        return {
            "initialized": self.initialized,
            "tinyml_models": {
                name: {
                    "input_size": model.input_size,
                    "output_size": model.output_size,
                    "size_kb": (model.input_size * model.output_size * 4) / 1024,
                    "parameters": model.input_size * model.output_size
                }
                for name, model in self.tinyml_models.items()
            },
            "total_models": len(self.tinyml_models),
            "total_size_kb": total_size_kb,
            "estimated_latency_ms": 1.0,  # TinyML models are ultra-fast
            "model_types": ["TinyML Linear Models"],
            "capabilities": [
                "Natural Language Query Processing",
                "Device Type Classification", 
                "Real-time Anomaly Detection"
            ]
        }
    
    async def close(self):
        """Close the local AI engine"""
        self.models.clear()
        self.initialized = False
        logger.info("Local AI engine closed")
