#!/usr/bin/env python3
"""
Documentation-Driven Anomaly Detection
Uses device documentation to detect and classify anomalies with contextual troubleshooting
"""

import asyncio
import json
import logging
import random
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ml.local_ai_engine import LocalAIEngine

logger = logging.getLogger(__name__)


class AnomalyType(Enum):
    """Types of anomalies that can be detected"""
    SENSOR_DRIFT = "sensor_drift"
    SENSOR_FAILURE = "sensor_failure"
    COMMUNICATION_ERROR = "communication_error"
    VALUE_OUT_OF_RANGE = "value_out_of_range"
    TREND_ANOMALY = "trend_anomaly"
    PATTERN_ANOMALY = "pattern_anomaly"
    MAINTENANCE_OVERDUE = "maintenance_overdue"
    ENVIRONMENTAL_ANOMALY = "environmental_anomaly"


class AnomalySeverity(Enum):
    """Anomaly severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AnomalyDetection:
    """Anomaly detection result with documentation context"""
    anomaly_id: str
    anomaly_type: AnomalyType
    severity: AnomalySeverity
    parameter: str
    current_value: float
    expected_range: Tuple[float, float]
    deviation_percentage: float
    description: str
    root_cause: str
    troubleshooting_steps: List[str]
    maintenance_required: bool
    estimated_impact: str
    detection_confidence: float
    timestamp: datetime
    device_context: Dict[str, Any]


class DocumentationAnomalyDetector:
    """Anomaly detector that uses device documentation for contextual analysis"""
    
    def __init__(self, ai_engine: LocalAIEngine):
        self.ai_engine = ai_engine
        self.anomaly_history = []
        self.device_baselines = {}
        self.pattern_history = {}
    
    async def detect_anomalies(self, device_id: str, device_spec: Dict[str, Any], 
                             current_data: Dict[str, Any]) -> List[AnomalyDetection]:
        """Detect anomalies using documentation context"""
        anomalies = []
        
        try:
            # 1. Range-based anomaly detection
            range_anomalies = await self._detect_range_anomalies(device_id, device_spec, current_data)
            anomalies.extend(range_anomalies)
            
            # 2. Trend-based anomaly detection
            trend_anomalies = await self._detect_trend_anomalies(device_id, device_spec, current_data)
            anomalies.extend(trend_anomalies)
            
            # 3. Pattern-based anomaly detection
            pattern_anomalies = await self._detect_pattern_anomalies(device_id, device_spec, current_data)
            anomalies.extend(pattern_anomalies)
            
            # 4. Maintenance-based anomaly detection
            maintenance_anomalies = await self._detect_maintenance_anomalies(device_id, device_spec, current_data)
            anomalies.extend(maintenance_anomalies)
            
            # 5. Environmental anomaly detection
            env_anomalies = await self._detect_environmental_anomalies(device_id, device_spec, current_data)
            anomalies.extend(env_anomalies)
            
            # 6. Use TinyML for additional anomaly detection
            ml_anomalies = await self._detect_ml_anomalies(device_id, current_data)
            anomalies.extend(ml_anomalies)
            
            # Store anomalies in history
            for anomaly in anomalies:
                self.anomaly_history.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting anomalies: {e}")
            return []
    
    async def _detect_range_anomalies(self, device_id: str, device_spec: Dict[str, Any], 
                                    current_data: Dict[str, Any]) -> List[AnomalyDetection]:
        """Detect anomalies based on parameter ranges from documentation"""
        anomalies = []
        
        parameters = device_spec.get('parameters', {})
        
        for param_name, param_spec in parameters.items():
            if param_name not in current_data:
                continue
            
            current_value = current_data[param_name]
            normal_range = param_spec.get('normal_range', (0, 100))
            warning_range = param_spec.get('warning_range', (0, 100))
            error_range = param_spec.get('error_range', (0, 100))
            
            # Check for critical errors
            if current_value < error_range[0] or current_value > error_range[1]:
                anomaly = AnomalyDetection(
                    anomaly_id=f"{device_id}_{param_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    anomaly_type=AnomalyType.VALUE_OUT_OF_RANGE,
                    severity=AnomalySeverity.CRITICAL,
                    parameter=param_name,
                    current_value=current_value,
                    expected_range=normal_range,
                    deviation_percentage=self._calculate_deviation(current_value, normal_range),
                    description=f"{param_spec.get('name', param_name)} reading {current_value} {param_spec.get('unit', '')} is outside critical range",
                    root_cause=self._determine_root_cause(param_name, current_value, param_spec),
                    troubleshooting_steps=param_spec.get('troubleshooting', []),
                    maintenance_required=True,
                    estimated_impact="Device may malfunction or fail",
                    detection_confidence=0.95,
                    timestamp=datetime.now(),
                    device_context=param_spec
                )
                anomalies.append(anomaly)
            
            # Check for warnings
            elif current_value < warning_range[0] or current_value > warning_range[1]:
                anomaly = AnomalyDetection(
                    anomaly_id=f"{device_id}_{param_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    anomaly_type=AnomalyType.VALUE_OUT_OF_RANGE,
                    severity=AnomalySeverity.MEDIUM,
                    parameter=param_name,
                    current_value=current_value,
                    expected_range=normal_range,
                    deviation_percentage=self._calculate_deviation(current_value, normal_range),
                    description=f"{param_spec.get('name', param_name)} reading {current_value} {param_spec.get('unit', '')} is outside normal range",
                    root_cause=self._determine_root_cause(param_name, current_value, param_spec),
                    troubleshooting_steps=param_spec.get('troubleshooting', []),
                    maintenance_required=False,
                    estimated_impact="Performance may be affected",
                    detection_confidence=0.85,
                    timestamp=datetime.now(),
                    device_context=param_spec
                )
                anomalies.append(anomaly)
        
        return anomalies
    
    async def _detect_trend_anomalies(self, device_id: str, device_spec: Dict[str, Any], 
                                    current_data: Dict[str, Any]) -> List[AnomalyDetection]:
        """Detect anomalies based on parameter trends"""
        anomalies = []
        
        # Initialize baseline if not exists
        if device_id not in self.device_baselines:
            self.device_baselines[device_id] = current_data.copy()
            return anomalies
        
        baseline = self.device_baselines[device_id]
        parameters = device_spec.get('parameters', {})
        
        for param_name, param_spec in parameters.items():
            if param_name not in current_data or param_name not in baseline:
                continue
            
            current_value = current_data[param_name]
            baseline_value = baseline[param_name]
            
            # Calculate trend
            trend_percentage = ((current_value - baseline_value) / baseline_value) * 100
            
            # Detect significant drift
            if abs(trend_percentage) > 20:  # 20% drift threshold
                anomaly = AnomalyDetection(
                    anomaly_id=f"{device_id}_{param_name}_trend_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    anomaly_type=AnomalyType.SENSOR_DRIFT,
                    severity=AnomalySeverity.MEDIUM if abs(trend_percentage) < 50 else AnomalySeverity.HIGH,
                    parameter=param_name,
                    current_value=current_value,
                    expected_range=(baseline_value * 0.8, baseline_value * 1.2),
                    deviation_percentage=trend_percentage,
                    description=f"{param_spec.get('name', param_name)} showing {trend_percentage:.1f}% drift from baseline",
                    root_cause="Possible sensor drift or environmental change",
                    troubleshooting_steps=[
                        "Check sensor calibration",
                        "Verify environmental conditions",
                        "Compare with other sensors",
                        "Schedule sensor maintenance"
                    ],
                    maintenance_required=abs(trend_percentage) > 50,
                    estimated_impact="Measurement accuracy may be compromised",
                    detection_confidence=0.80,
                    timestamp=datetime.now(),
                    device_context=param_spec
                )
                anomalies.append(anomaly)
        
        return anomalies
    
    async def _detect_pattern_anomalies(self, device_id: str, device_spec: Dict[str, Any], 
                                      current_data: Dict[str, Any]) -> List[AnomalyDetection]:
        """Detect anomalies based on parameter patterns"""
        anomalies = []
        
        # Initialize pattern history
        if device_id not in self.pattern_history:
            self.pattern_history[device_id] = []
        
        # Add current data to history
        self.pattern_history[device_id].append({
            'timestamp': datetime.now(),
            'data': current_data.copy()
        })
        
        # Keep only last 10 readings
        if len(self.pattern_history[device_id]) > 10:
            self.pattern_history[device_id] = self.pattern_history[device_id][-10:]
        
        # Need at least 3 readings for pattern analysis
        if len(self.pattern_history[device_id]) < 3:
            return anomalies
        
        # Analyze patterns for each parameter
        parameters = device_spec.get('parameters', {})
        history = self.pattern_history[device_id]
        
        for param_name, param_spec in parameters.items():
            if param_name not in current_data:
                continue
            
            # Extract parameter values over time
            values = [reading['data'].get(param_name, 0) for reading in history]
            
            # Detect unusual patterns
            if self._detect_unusual_pattern(values):
                anomaly = AnomalyDetection(
                    anomaly_id=f"{device_id}_{param_name}_pattern_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    anomaly_type=AnomalyType.PATTERN_ANOMALY,
                    severity=AnomalySeverity.MEDIUM,
                    parameter=param_name,
                    current_value=current_data[param_name],
                    expected_range=param_spec.get('normal_range', (0, 100)),
                    deviation_percentage=0,  # Pattern-based, not value-based
                    description=f"{param_spec.get('name', param_name)} showing unusual pattern",
                    root_cause="Possible sensor noise or communication issues",
                    troubleshooting_steps=[
                        "Check sensor stability",
                        "Verify communication quality",
                        "Look for environmental interference",
                        "Test sensor response time"
                    ],
                    maintenance_required=False,
                    estimated_impact="Data quality may be affected",
                    detection_confidence=0.75,
                    timestamp=datetime.now(),
                    device_context=param_spec
                )
                anomalies.append(anomaly)
        
        return anomalies
    
    async def _detect_maintenance_anomalies(self, device_id: str, device_spec: Dict[str, Any], 
                                          current_data: Dict[str, Any]) -> List[AnomalyDetection]:
        """Detect anomalies related to maintenance schedules"""
        anomalies = []
        
        maintenance_schedule = device_spec.get('maintenance_schedule', {})
        last_maintenance = current_data.get('last_maintenance')
        
        if not last_maintenance or not maintenance_schedule:
            return anomalies
        
        # Parse last maintenance date
        try:
            if isinstance(last_maintenance, str):
                last_maintenance_date = datetime.fromisoformat(last_maintenance.replace('Z', '+00:00'))
            else:
                last_maintenance_date = last_maintenance
        except:
            return anomalies
        
        days_since_maintenance = (datetime.now() - last_maintenance_date).days
        
        for maintenance_type, interval_days in maintenance_schedule.items():
            if days_since_maintenance >= interval_days:
                anomaly = AnomalyDetection(
                    anomaly_id=f"{device_id}_maintenance_{maintenance_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    anomaly_type=AnomalyType.MAINTENANCE_OVERDUE,
                    severity=AnomalySeverity.MEDIUM if days_since_maintenance < interval_days * 2 else AnomalySeverity.HIGH,
                    parameter="maintenance",
                    current_value=days_since_maintenance,
                    expected_range=(0, interval_days),
                    deviation_percentage=((days_since_maintenance - interval_days) / interval_days) * 100,
                    description=f"{maintenance_type.replace('_', ' ').title()} overdue by {days_since_maintenance - interval_days} days",
                    root_cause="Maintenance schedule not followed",
                    troubleshooting_steps=[
                        f"Schedule {maintenance_type.replace('_', ' ')} immediately",
                        "Check device performance",
                        "Review maintenance logs",
                        "Update maintenance schedule"
                    ],
                    maintenance_required=True,
                    estimated_impact="Device reliability may be compromised",
                    detection_confidence=0.90,
                    timestamp=datetime.now(),
                    device_context={"maintenance_type": maintenance_type, "interval_days": interval_days}
                )
                anomalies.append(anomaly)
        
        return anomalies
    
    async def _detect_environmental_anomalies(self, device_id: str, device_spec: Dict[str, Any], 
                                            current_data: Dict[str, Any]) -> List[AnomalyDetection]:
        """Detect environmental anomalies"""
        anomalies = []
        
        # Check for environmental parameter correlations
        parameters = device_spec.get('parameters', {})
        
        # Temperature-Humidity correlation check
        if 'temperature' in current_data and 'humidity' in current_data:
            temp = current_data['temperature']
            humidity = current_data['humidity']
            
            # Unusual temperature-humidity combination
            if temp > 30 and humidity > 80:  # High temp + high humidity
                anomaly = AnomalyDetection(
                    anomaly_id=f"{device_id}_env_high_temp_humidity_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    anomaly_type=AnomalyType.ENVIRONMENTAL_ANOMALY,
                    severity=AnomalySeverity.MEDIUM,
                    parameter="environmental",
                    current_value=temp * humidity / 100,  # Combined index
                    expected_range=(15, 25),  # Comfortable range
                    deviation_percentage=50,
                    description="High temperature and humidity combination detected",
                    root_cause="Environmental conditions outside comfort range",
                    troubleshooting_steps=[
                        "Check HVAC system operation",
                        "Verify ventilation",
                        "Monitor for condensation",
                        "Adjust environmental controls"
                    ],
                    maintenance_required=False,
                    estimated_impact="Comfort and equipment performance may be affected",
                    detection_confidence=0.85,
                    timestamp=datetime.now(),
                    device_context={"temperature": temp, "humidity": humidity}
                )
                anomalies.append(anomaly)
        
        return anomalies
    
    async def _detect_ml_anomalies(self, device_id: str, current_data: Dict[str, Any]) -> List[AnomalyDetection]:
        """Use TinyML for additional anomaly detection"""
        anomalies = []
        
        try:
            # Use the existing TinyML anomaly detection
            ml_result = await self.ai_engine.detect_anomalies(current_data)
            
            if ml_result.get('is_anomaly', False):
                anomaly_score = ml_result.get('anomaly_score', 0.5)
                affected_sensors = ml_result.get('affected_sensors', [])
                
                for sensor in affected_sensors:
                    anomaly = AnomalyDetection(
                        anomaly_id=f"{device_id}_ml_{sensor}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        anomaly_type=AnomalyType.PATTERN_ANOMALY,
                        severity=self._score_to_severity(anomaly_score),
                        parameter=sensor,
                        current_value=current_data.get(sensor, 0),
                        expected_range=(0, 100),  # Generic range
                        deviation_percentage=anomaly_score * 100,
                        description=f"ML-detected anomaly in {sensor} (score: {anomaly_score:.3f})",
                        root_cause="AI-detected unusual pattern",
                        troubleshooting_steps=[
                            "Review sensor data patterns",
                            "Check for environmental changes",
                            "Verify sensor calibration",
                            "Compare with historical data"
                        ],
                        maintenance_required=anomaly_score > 0.8,
                        estimated_impact="Potential sensor or system issue",
                        detection_confidence=ml_result.get('confidence', 0.7),
                        timestamp=datetime.now(),
                        device_context={"ml_score": anomaly_score, "affected_sensors": affected_sensors}
                    )
                    anomalies.append(anomaly)
        
        except Exception as e:
            logger.error(f"Error in ML anomaly detection: {e}")
        
        return anomalies
    
    def _calculate_deviation(self, value: float, expected_range: Tuple[float, float]) -> float:
        """Calculate percentage deviation from expected range"""
        range_center = (expected_range[0] + expected_range[1]) / 2
        range_size = expected_range[1] - expected_range[0]
        
        if range_size == 0:
            return 0
        
        deviation = abs(value - range_center) / range_size * 100
        return deviation
    
    def _determine_root_cause(self, param_name: str, value: float, param_spec: Dict[str, Any]) -> str:
        """Determine likely root cause based on parameter and value"""
        param_type = param_spec.get('type', 'unknown')
        
        if 'temperature' in param_name.lower():
            if value > 40:
                return "Possible sensor overheating or environmental issue"
            elif value < 0:
                return "Possible sensor failure or extreme cold"
        elif 'humidity' in param_name.lower():
            if value > 90:
                return "Possible condensation or sensor contamination"
            elif value < 10:
                return "Possible sensor drift or dry environment"
        elif 'pressure' in param_name.lower():
            if value > 1100:
                return "Possible sensor calibration issue"
            elif value < 900:
                return "Possible altitude change or sensor failure"
        
        return "Parameter outside normal operating range"
    
    def _detect_unusual_pattern(self, values: List[float]) -> bool:
        """Detect unusual patterns in parameter values"""
        if len(values) < 3:
            return False
        
        # Check for excessive noise (high variance)
        mean_val = sum(values) / len(values)
        variance = sum((x - mean_val) ** 2 for x in values) / len(values)
        
        # High variance indicates noise
        if variance > mean_val * 0.1:  # 10% of mean value
            return True
        
        # Check for sudden jumps
        for i in range(1, len(values)):
            if abs(values[i] - values[i-1]) > mean_val * 0.2:  # 20% jump
                return True
        
        return False
    
    def _score_to_severity(self, score: float) -> AnomalySeverity:
        """Convert anomaly score to severity level"""
        if score > 0.9:
            return AnomalySeverity.CRITICAL
        elif score > 0.7:
            return AnomalySeverity.HIGH
        elif score > 0.5:
            return AnomalySeverity.MEDIUM
        else:
            return AnomalySeverity.LOW
    
    def get_anomaly_summary(self, device_id: str) -> Dict[str, Any]:
        """Get summary of anomalies for a device"""
        device_anomalies = [a for a in self.anomaly_history if device_id in a.anomaly_id]
        
        if not device_anomalies:
            return {"total_anomalies": 0}
        
        severity_counts = {}
        type_counts = {}
        
        for anomaly in device_anomalies:
            severity_counts[anomaly.severity.value] = severity_counts.get(anomaly.severity.value, 0) + 1
            type_counts[anomaly.anomaly_type.value] = type_counts.get(anomaly.anomaly_type.value, 0) + 1
        
        return {
            "total_anomalies": len(device_anomalies),
            "severity_breakdown": severity_counts,
            "type_breakdown": type_counts,
            "latest_anomaly": device_anomalies[-1].timestamp.isoformat() if device_anomalies else None,
            "critical_anomalies": len([a for a in device_anomalies if a.severity == AnomalySeverity.CRITICAL])
        }


# Demo function
async def main():
    """Demo the documentation-driven anomaly detection"""
    print("🚨 Documentation-Driven Anomaly Detection Demo")
    print("=" * 60)
    
    # Initialize AI engine
    ai_engine = LocalAIEngine()
    await ai_engine.initialize()
    
    # Initialize anomaly detector
    detector = DocumentationAnomalyDetector(ai_engine)
    
    # Sample device specification
    device_spec = {
        "device_type": "hvac_controller",
        "parameters": {
            "temperature": {
                "name": "Room Temperature",
                "type": "float",
                "unit": "°C",
                "normal_range": (18.0, 26.0),
                "warning_range": (15.0, 30.0),
                "error_range": (10.0, 40.0),
                "troubleshooting": [
                    "Check temperature sensor calibration",
                    "Verify HVAC system is running",
                    "Check for air flow obstructions"
                ]
            },
            "humidity": {
                "name": "Relative Humidity",
                "type": "float",
                "unit": "%",
                "normal_range": (30.0, 60.0),
                "warning_range": (20.0, 70.0),
                "error_range": (10.0, 90.0),
                "troubleshooting": [
                    "Check humidity sensor for condensation",
                    "Verify HVAC dehumidification settings",
                    "Check for water leaks"
                ]
            }
        },
        "maintenance_schedule": {
            "sensor_calibration": 90,
            "filter_replacement": 30
        }
    }
    
    # Test different anomaly scenarios
    test_scenarios = [
        {
            "name": "Normal Operation",
            "data": {"temperature": 22.0, "humidity": 45.0, "last_maintenance": "2024-01-01T00:00:00"}
        },
        {
            "name": "High Temperature",
            "data": {"temperature": 35.0, "humidity": 45.0, "last_maintenance": "2024-01-01T00:00:00"}
        },
        {
            "name": "High Humidity",
            "data": {"temperature": 22.0, "humidity": 85.0, "last_maintenance": "2024-01-01T00:00:00"}
        },
        {
            "name": "Environmental Anomaly",
            "data": {"temperature": 32.0, "humidity": 85.0, "last_maintenance": "2024-01-01T00:00:00"}
        },
        {
            "name": "Maintenance Overdue",
            "data": {"temperature": 22.0, "humidity": 45.0, "last_maintenance": "2023-06-01T00:00:00"}
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n--- {scenario['name']} ---")
        print(f"Data: {scenario['data']}")
        
        # Detect anomalies
        anomalies = await detector.detect_anomalies("hvac_001", device_spec, scenario['data'])
        
        if anomalies:
            print(f"🚨 {len(anomalies)} Anomalies Detected:")
            for anomaly in anomalies:
                print(f"   {anomaly.severity.value.upper()}: {anomaly.description}")
                print(f"   Type: {anomaly.anomaly_type.value}")
                print(f"   Confidence: {anomaly.detection_confidence:.2f}")
                print(f"   Troubleshooting: {anomaly.troubleshooting_steps[0] if anomaly.troubleshooting_steps else 'N/A'}")
        else:
            print("✅ No anomalies detected")
    
    # Show anomaly summary
    print(f"\n📊 Anomaly Summary:")
    summary = detector.get_anomaly_summary("hvac_001")
    print(f"   Total Anomalies: {summary['total_anomalies']}")
    print(f"   Severity Breakdown: {summary['severity_breakdown']}")
    print(f"   Type Breakdown: {summary['type_breakdown']}")
    
    await ai_engine.close()
    print(f"\n🎉 Documentation-Driven Anomaly Detection Demo Complete!")


if __name__ == "__main__":
    asyncio.run(main())
