#!/usr/bin/env python3
"""
Documentation-Driven Device Simulator
Loads device documentation and uses AI to extract rules, behaviors, and troubleshooting
"""

import asyncio
import json
import logging
import random
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ml.local_ai_engine import LocalAIEngine

logger = logging.getLogger(__name__)


@dataclass
class DeviceParameter:
    """Device parameter with documentation-driven behavior"""
    name: str
    value_type: str
    min_value: float
    max_value: float
    default_value: float
    unit: str
    description: str
    normal_range: Tuple[float, float]
    warning_range: Tuple[float, float]
    error_range: Tuple[float, float]
    troubleshooting_tips: List[str]
    dependencies: List[str] = None


@dataclass
class DeviceState:
    """Current device state with context"""
    device_id: str
    device_type: str
    status: str  # normal, warning, error, maintenance
    parameters: Dict[str, float]
    last_maintenance: datetime
    error_history: List[Dict[str, Any]]
    performance_metrics: Dict[str, float]
    documentation_context: Dict[str, Any]


class DocumentationParser:
    """AI-powered parser to extract device rules from documentation"""
    
    def __init__(self, ai_engine: LocalAIEngine):
        self.ai_engine = ai_engine
        self.extracted_rules = {}
    
    async def parse_device_documentation(self, doc_path: str) -> Dict[str, Any]:
        """Parse device documentation and extract rules"""
        try:
            # In a real implementation, this would use OCR, PDF parsing, etc.
            # For demo, we'll simulate parsing from structured documentation
            
            if "hvac" in doc_path.lower():
                return await self._parse_hvac_documentation()
            elif "sensor" in doc_path.lower():
                return await self._parse_sensor_documentation()
            elif "bacnet" in doc_path.lower():
                return await self._parse_bacnet_documentation()
            else:
                return await self._parse_generic_documentation()
                
        except Exception as e:
            logger.error(f"Error parsing documentation: {e}")
            return {}
    
    async def _parse_hvac_documentation(self) -> Dict[str, Any]:
        """Parse HVAC device documentation"""
        return {
            "device_type": "hvac_controller",
            "protocol": "BACnet",
            "parameters": {
                "temperature": {
                    "name": "Room Temperature",
                    "type": "float",
                    "min": 15.0,
                    "max": 35.0,
                    "default": 22.0,
                    "unit": "°C",
                    "description": "Current room temperature reading",
                    "normal_range": (18.0, 26.0),
                    "warning_range": (15.0, 30.0),
                    "error_range": (10.0, 40.0),
                    "troubleshooting": [
                        "Check temperature sensor calibration",
                        "Verify HVAC system is running",
                        "Check for air flow obstructions",
                        "Verify setpoint configuration"
                    ]
                },
                "humidity": {
                    "name": "Relative Humidity",
                    "type": "float",
                    "min": 20.0,
                    "max": 80.0,
                    "default": 45.0,
                    "unit": "%",
                    "description": "Current relative humidity",
                    "normal_range": (30.0, 60.0),
                    "warning_range": (20.0, 70.0),
                    "error_range": (10.0, 90.0),
                    "troubleshooting": [
                        "Check humidity sensor for condensation",
                        "Verify HVAC dehumidification settings",
                        "Check for water leaks",
                        "Calibrate humidity sensor"
                    ]
                },
                "setpoint": {
                    "name": "Temperature Setpoint",
                    "type": "float",
                    "min": 16.0,
                    "max": 30.0,
                    "default": 22.0,
                    "unit": "°C",
                    "description": "Desired temperature setting",
                    "normal_range": (18.0, 26.0),
                    "warning_range": (16.0, 28.0),
                    "error_range": (15.0, 35.0),
                    "troubleshooting": [
                        "Verify setpoint is within acceptable range",
                        "Check for conflicting setpoints",
                        "Verify user permissions",
                        "Check for schedule overrides"
                    ]
                }
            },
            "error_codes": {
                "E001": "Temperature sensor failure",
                "E002": "Communication timeout",
                "E003": "Setpoint out of range",
                "E004": "HVAC system not responding",
                "E005": "Humidity sensor calibration error"
            },
            "maintenance_schedule": {
                "sensor_calibration": 90,  # days
                "filter_replacement": 30,  # days
                "system_inspection": 180   # days
            },
            "performance_metrics": {
                "energy_efficiency": "kWh/°C",
                "response_time": "seconds",
                "accuracy": "±0.5°C"
            }
        }
    
    async def _parse_sensor_documentation(self) -> Dict[str, Any]:
        """Parse sensor device documentation"""
        return {
            "device_type": "environmental_sensor",
            "protocol": "REST",
            "parameters": {
                "temperature": {
                    "name": "Temperature",
                    "type": "float",
                    "min": -40.0,
                    "max": 85.0,
                    "default": 20.0,
                    "unit": "°C",
                    "description": "Ambient temperature reading",
                    "normal_range": (15.0, 35.0),
                    "warning_range": (10.0, 40.0),
                    "error_range": (-40.0, 85.0),
                    "troubleshooting": [
                        "Check sensor placement",
                        "Verify sensor calibration",
                        "Check for environmental interference",
                        "Test sensor response time"
                    ]
                },
                "humidity": {
                    "name": "Humidity",
                    "type": "float",
                    "min": 0.0,
                    "max": 100.0,
                    "default": 50.0,
                    "unit": "%",
                    "description": "Relative humidity reading",
                    "normal_range": (20.0, 80.0),
                    "warning_range": (10.0, 90.0),
                    "error_range": (0.0, 100.0),
                    "troubleshooting": [
                        "Check for condensation on sensor",
                        "Verify sensor is not blocked",
                        "Check sensor drift over time",
                        "Verify environmental conditions"
                    ]
                },
                "pressure": {
                    "name": "Atmospheric Pressure",
                    "type": "float",
                    "min": 800.0,
                    "max": 1200.0,
                    "default": 1013.0,
                    "unit": "hPa",
                    "description": "Atmospheric pressure reading",
                    "normal_range": (950.0, 1050.0),
                    "warning_range": (900.0, 1100.0),
                    "error_range": (800.0, 1200.0),
                    "troubleshooting": [
                        "Check for altitude changes",
                        "Verify sensor calibration",
                        "Check for weather system effects",
                        "Test sensor stability"
                    ]
                }
            },
            "error_codes": {
                "S001": "Sensor reading out of range",
                "S002": "Communication error",
                "S003": "Sensor calibration required",
                "S004": "Power supply issue",
                "S005": "Sensor drift detected"
            },
            "maintenance_schedule": {
                "calibration": 180,  # days
                "cleaning": 90,      # days
                "replacement": 365   # days
            }
        }
    
    async def _parse_bacnet_documentation(self) -> Dict[str, Any]:
        """Parse BACnet device documentation"""
        return {
            "device_type": "bacnet_device",
            "protocol": "BACnet/IP",
            "parameters": {
                "analog_input_1": {
                    "name": "Temperature Input",
                    "type": "float",
                    "min": 0.0,
                    "max": 100.0,
                    "default": 22.0,
                    "unit": "°C",
                    "description": "BACnet analog input for temperature",
                    "normal_range": (18.0, 26.0),
                    "warning_range": (15.0, 30.0),
                    "error_range": (0.0, 100.0),
                    "troubleshooting": [
                        "Check BACnet object configuration",
                        "Verify analog input scaling",
                        "Check for communication errors",
                        "Verify device addressing"
                    ]
                },
                "binary_output_1": {
                    "name": "HVAC Control",
                    "type": "boolean",
                    "min": 0.0,
                    "max": 1.0,
                    "default": 0.0,
                    "unit": "On/Off",
                    "description": "BACnet binary output for HVAC control",
                    "normal_range": (0.0, 1.0),
                    "warning_range": (0.0, 1.0),
                    "error_range": (0.0, 1.0),
                    "troubleshooting": [
                        "Check BACnet object status",
                        "Verify output configuration",
                        "Check for device communication",
                        "Verify control logic"
                    ]
                }
            },
            "error_codes": {
                "B001": "BACnet communication timeout",
                "B002": "Object not found",
                "B003": "Property not supported",
                "B004": "Device not responding",
                "B005": "Network configuration error"
            },
            "bacnet_properties": {
                "device_id": 12345,
                "object_name": "HVAC_Controller_01",
                "vendor_id": 260,
                "model_name": "SmartHVAC Pro",
                "firmware_revision": "2.1.3"
            }
        }
    
    async def _parse_generic_documentation(self) -> Dict[str, Any]:
        """Parse generic device documentation"""
        return {
            "device_type": "generic_device",
            "protocol": "REST",
            "parameters": {
                "value": {
                    "name": "Device Value",
                    "type": "float",
                    "min": 0.0,
                    "max": 100.0,
                    "default": 50.0,
                    "unit": "units",
                    "description": "Generic device reading",
                    "normal_range": (20.0, 80.0),
                    "warning_range": (10.0, 90.0),
                    "error_range": (0.0, 100.0),
                    "troubleshooting": [
                        "Check device power",
                        "Verify communication",
                        "Check for environmental factors",
                        "Verify device configuration"
                    ]
                }
            },
            "error_codes": {
                "G001": "Generic error",
                "G002": "Communication error",
                "G003": "Configuration error"
            }
        }


class DocumentationDrivenSimulator:
    """Simulator that uses documentation to drive device behavior"""
    
    def __init__(self, device_id: str, doc_path: str, ai_engine: LocalAIEngine):
        self.device_id = device_id
        self.doc_path = doc_path
        self.ai_engine = ai_engine
        self.parser = DocumentationParser(ai_engine)
        self.device_spec = {}
        self.current_state = None
        self.error_history = []
        self.performance_metrics = {}
        
    async def initialize(self):
        """Initialize simulator with documentation"""
        logger.info(f"Initializing documentation-driven simulator for {self.device_id}")
        
        # Parse documentation
        self.device_spec = await self.parser.parse_device_documentation(self.doc_path)
        
        if not self.device_spec:
            raise ValueError(f"Failed to parse documentation for {self.device_id}")
        
        # Initialize device state
        await self._initialize_device_state()
        
        logger.info(f"Simulator initialized with {len(self.device_spec.get('parameters', {}))} parameters")
    
    async def _initialize_device_state(self):
        """Initialize device state from documentation"""
        parameters = {}
        for param_name, param_spec in self.device_spec.get('parameters', {}).items():
            # Add some realistic variation to default values
            base_value = param_spec['default']
            variation = random.uniform(-0.1, 0.1) * base_value
            parameters[param_name] = base_value + variation
        
        self.current_state = DeviceState(
            device_id=self.device_id,
            device_type=self.device_spec.get('device_type', 'unknown'),
            status='normal',
            parameters=parameters,
            last_maintenance=datetime.now() - timedelta(days=random.randint(1, 30)),
            error_history=[],
            performance_metrics={
                'uptime': 99.5,
                'response_time': random.uniform(0.1, 0.5),
                'accuracy': random.uniform(0.95, 0.99)
            },
            documentation_context=self.device_spec
        )
    
    async def get_device_status(self) -> Dict[str, Any]:
        """Get current device status with AI-driven analysis"""
        if not self.current_state:
            return {"error": "Device not initialized"}
        
        # Use AI to analyze current state
        analysis = await self._analyze_device_state()
        
        return {
            "device_id": self.device_id,
            "device_type": self.current_state.device_type,
            "status": self.current_state.status,
            "parameters": self.current_state.parameters,
            "analysis": analysis,
            "error_history": self.error_history[-5:],  # Last 5 errors
            "performance_metrics": self.current_state.performance_metrics,
            "last_maintenance": self.current_state.last_maintenance.isoformat(),
            "documentation_context": {
                "protocol": self.device_spec.get('protocol'),
                "error_codes": self.device_spec.get('error_codes', {}),
                "maintenance_schedule": self.device_spec.get('maintenance_schedule', {})
            }
        }
    
    async def _analyze_device_state(self) -> Dict[str, Any]:
        """Use AI to analyze device state and provide insights"""
        try:
            # Prepare sensor data for AI analysis
            sensor_data = self.current_state.parameters.copy()
            sensor_data.update(self.current_state.performance_metrics)
            
            # Use TinyML anomaly detection
            anomaly_result = await self.ai_engine.detect_anomalies(sensor_data)
            
            # Generate contextual analysis
            analysis = {
                "anomaly_detected": anomaly_result.get('is_anomaly', False),
                "anomaly_score": anomaly_result.get('anomaly_score', 0.0),
                "confidence": anomaly_result.get('confidence', 0.0),
                "recommendations": [],
                "troubleshooting_steps": [],
                "maintenance_alerts": []
            }
            
            # Generate recommendations based on documentation
            await self._generate_recommendations(analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing device state: {e}")
            return {"error": str(e)}
    
    async def _generate_recommendations(self, analysis: Dict[str, Any]):
        """Generate recommendations based on documentation and AI analysis"""
        recommendations = []
        troubleshooting = []
        maintenance_alerts = []
        
        # Check each parameter against documentation ranges
        for param_name, value in self.current_state.parameters.items():
            param_spec = self.device_spec.get('parameters', {}).get(param_name, {})
            
            if not param_spec:
                continue
            
            normal_range = param_spec.get('normal_range', (0, 100))
            warning_range = param_spec.get('warning_range', (0, 100))
            error_range = param_spec.get('error_range', (0, 100))
            
            # Check for errors
            if value < error_range[0] or value > error_range[1]:
                error_code = f"E{random.randint(100, 999)}"
                error_msg = f"{param_spec.get('name', param_name)} reading {value} {param_spec.get('unit', '')} is outside error range"
                troubleshooting.extend(param_spec.get('troubleshooting', []))
                recommendations.append(f"URGENT: {error_msg}")
                
                # Add to error history
                self.error_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "error_code": error_code,
                    "parameter": param_name,
                    "value": value,
                    "message": error_msg
                })
            
            # Check for warnings
            elif value < warning_range[0] or value > warning_range[1]:
                warning_msg = f"{param_spec.get('name', param_name)} reading {value} {param_spec.get('unit', '')} is outside normal range"
                recommendations.append(f"WARNING: {warning_msg}")
        
        # Check maintenance schedule
        maintenance_schedule = self.device_spec.get('maintenance_schedule', {})
        days_since_maintenance = (datetime.now() - self.current_state.last_maintenance).days
        
        for maintenance_type, interval_days in maintenance_schedule.items():
            if days_since_maintenance >= interval_days:
                maintenance_alerts.append(f"{maintenance_type.replace('_', ' ').title()} due (last: {days_since_maintenance} days ago)")
        
        analysis["recommendations"] = recommendations
        analysis["troubleshooting_steps"] = troubleshooting
        analysis["maintenance_alerts"] = maintenance_alerts
    
    async def simulate_realistic_behavior(self):
        """Simulate realistic device behavior with occasional anomalies"""
        if not self.current_state:
            return
        
        # Simulate parameter changes
        for param_name, param_spec in self.device_spec.get('parameters', {}).items():
            current_value = self.current_state.parameters[param_name]
            
            # Add realistic variation
            variation = random.uniform(-0.02, 0.02) * current_value
            new_value = current_value + variation
            
            # Keep within bounds
            min_val = param_spec.get('min', 0)
            max_val = param_spec.get('max', 100)
            new_value = max(min_val, min(max_val, new_value))
            
            self.current_state.parameters[param_name] = new_value
        
        # Occasionally introduce anomalies (5% chance)
        if random.random() < 0.05:
            await self._introduce_anomaly()
        
        # Occasionally fix anomalies (10% chance if in error state)
        if self.current_state.status == 'error' and random.random() < 0.1:
            await self._resolve_anomaly()
    
    async def _introduce_anomaly(self):
        """Introduce realistic anomalies based on documentation"""
        param_name = random.choice(list(self.device_spec.get('parameters', {}).keys()))
        param_spec = self.device_spec['parameters'][param_name]
        
        # Introduce different types of anomalies
        anomaly_type = random.choice(['drift', 'spike', 'noise', 'failure'])
        
        if anomaly_type == 'drift':
            # Gradual drift
            drift_amount = random.uniform(-0.1, 0.1) * param_spec['default']
            self.current_state.parameters[param_name] += drift_amount
            
        elif anomaly_type == 'spike':
            # Sudden spike
            spike_amount = random.uniform(-0.3, 0.3) * param_spec['default']
            self.current_state.parameters[param_name] += spike_amount
            
        elif anomaly_type == 'noise':
            # Add noise
            noise_amount = random.uniform(-0.05, 0.05) * param_spec['default']
            self.current_state.parameters[param_name] += noise_amount
            
        elif anomaly_type == 'failure':
            # Simulate sensor failure
            self.current_state.parameters[param_name] = random.uniform(
                param_spec.get('min', 0), 
                param_spec.get('max', 100)
            )
        
        # Update device status
        await self._update_device_status()
        
        logger.info(f"Introduced {anomaly_type} anomaly in {param_name}: {self.current_state.parameters[param_name]}")
    
    async def _resolve_anomaly(self):
        """Resolve anomalies (simulate maintenance)"""
        # Reset parameters to normal ranges
        for param_name, param_spec in self.device_spec.get('parameters', {}).items():
            normal_range = param_spec.get('normal_range', (param_spec['min'], param_spec['max']))
            self.current_state.parameters[param_name] = random.uniform(normal_range[0], normal_range[1])
        
        self.current_state.status = 'normal'
        self.current_state.last_maintenance = datetime.now()
        
        logger.info(f"Resolved anomalies for device {self.device_id}")
    
    async def _update_device_status(self):
        """Update device status based on current parameters"""
        status = 'normal'
        
        for param_name, value in self.current_state.parameters.items():
            param_spec = self.device_spec.get('parameters', {}).get(param_name, {})
            error_range = param_spec.get('error_range', (0, 100))
            
            if value < error_range[0] or value > error_range[1]:
                status = 'error'
                break
            elif status != 'error':
                warning_range = param_spec.get('warning_range', (0, 100))
                if value < warning_range[0] or value > warning_range[1]:
                    status = 'warning'
        
        self.current_state.status = status
    
    async def get_parameter_value(self, parameter_name: str) -> Dict[str, Any]:
        """Get specific parameter value with documentation context"""
        if parameter_name not in self.current_state.parameters:
            return {"error": f"Parameter {parameter_name} not found"}
        
        param_spec = self.device_spec.get('parameters', {}).get(parameter_name, {})
        value = self.current_state.parameters[parameter_name]
        
        return {
            "parameter": parameter_name,
            "value": value,
            "unit": param_spec.get('unit', ''),
            "description": param_spec.get('description', ''),
            "normal_range": param_spec.get('normal_range'),
            "warning_range": param_spec.get('warning_range'),
            "error_range": param_spec.get('error_range'),
            "status": self._get_parameter_status(value, param_spec),
            "troubleshooting": param_spec.get('troubleshooting', [])
        }
    
    def _get_parameter_status(self, value: float, param_spec: Dict[str, Any]) -> str:
        """Determine parameter status based on value and ranges"""
        error_range = param_spec.get('error_range', (0, 100))
        warning_range = param_spec.get('warning_range', (0, 100))
        
        if value < error_range[0] or value > error_range[1]:
            return 'error'
        elif value < warning_range[0] or value > warning_range[1]:
            return 'warning'
        else:
            return 'normal'


# Example usage and testing
async def main():
    """Test the documentation-driven simulator"""
    # Initialize AI engine
    ai_engine = LocalAIEngine()
    await ai_engine.initialize()
    
    # Create simulators for different device types
    simulators = {
        "hvac_01": DocumentationDrivenSimulator("hvac_01", "hvac_controller_manual.pdf", ai_engine),
        "sensor_01": DocumentationDrivenSimulator("sensor_01", "environmental_sensor_spec.pdf", ai_engine),
        "bacnet_01": DocumentationDrivenSimulator("bacnet_01", "bacnet_device_manual.pdf", ai_engine)
    }
    
    # Initialize all simulators
    for simulator in simulators.values():
        await simulator.initialize()
    
    # Simulate behavior for a few cycles
    for cycle in range(5):
        print(f"\n=== Simulation Cycle {cycle + 1} ===")
        
        for device_id, simulator in simulators.items():
            # Simulate realistic behavior
            await simulator.simulate_realistic_behavior()
            
            # Get device status
            status = await simulator.get_device_status()
            
            print(f"\n{device_id}:")
            print(f"  Status: {status['status']}")
            print(f"  Parameters: {status['parameters']}")
            
            if status['analysis']['recommendations']:
                print(f"  Recommendations: {status['analysis']['recommendations']}")
            
            if status['analysis']['maintenance_alerts']:
                print(f"  Maintenance: {status['analysis']['maintenance_alerts']}")
        
        await asyncio.sleep(1)  # Wait between cycles
    
    await ai_engine.close()


if __name__ == "__main__":
    asyncio.run(main())
