#!/usr/bin/env python3
"""
Comprehensive Anomaly Detection Demo
Shows how anomalies are detected using documentation context and TinyML
"""

import asyncio
import json
import sys
import os
from datetime import datetime, timedelta

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from anomaly.documentation_anomaly_detector import DocumentationAnomalyDetector, AnomalyType, AnomalySeverity
from ml.local_ai_engine import LocalAIEngine


async def demo_comprehensive_anomaly_detection():
    """Demonstrate comprehensive anomaly detection with documentation context"""
    print("🚨 Comprehensive Anomaly Detection Demo")
    print("=" * 60)
    print("Shows how anomalies are detected using:")
    print("  📚 Device documentation context")
    print("  🤖 TinyML anomaly detection")
    print("  📊 Parameter range analysis")
    print("  📈 Trend and pattern analysis")
    print("  🔧 Maintenance schedule monitoring")
    print("  🌡️ Environmental correlation analysis")
    print()
    
    # Initialize AI engine and anomaly detector
    ai_engine = LocalAIEngine()
    await ai_engine.initialize()
    
    detector = DocumentationAnomalyDetector(ai_engine)
    
    print(f"✅ AI Engine initialized")
    print(f"   TinyML Models: {ai_engine.get_model_info()['total_models']}")
    print(f"   Model Size: {ai_engine.get_model_info()['total_size_kb']:.2f} KB")
    
    # Define realistic device specifications
    device_specs = {
        "hvac_controller": {
            "device_type": "hvac_controller",
            "manufacturer": "Honeywell",
            "model": "T6 Pro Smart Thermostat",
            "parameters": {
                "temperature": {
                    "name": "Room Temperature",
                    "type": "analog_input",
                    "unit": "°C",
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
                    "type": "analog_input",
                    "unit": "%",
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
                    "type": "analog_value",
                    "unit": "°C",
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
            "maintenance_schedule": {
                "sensor_calibration": 90,  # days
                "filter_replacement": 30,  # days
                "system_inspection": 180   # days
            }
        },
        "environmental_sensor": {
            "device_type": "environmental_sensor",
            "manufacturer": "Sensirion",
            "model": "SHT40 Temperature/Humidity Sensor",
            "parameters": {
                "temperature": {
                    "name": "Temperature",
                    "type": "float",
                    "unit": "°C",
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
                    "unit": "%",
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
                    "unit": "hPa",
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
            "maintenance_schedule": {
                "calibration": 180,  # days
                "cleaning": 90,      # days
                "replacement": 365   # days
            }
        }
    }
    
    # Define realistic anomaly scenarios
    anomaly_scenarios = [
        {
            "name": "Normal Operation",
            "description": "All parameters within normal ranges",
            "hvac_data": {
                "temperature": 22.0,
                "humidity": 45.0,
                "setpoint": 22.0,
                "last_maintenance": (datetime.now() - timedelta(days=30)).isoformat()
            },
            "sensor_data": {
                "temperature": 21.5,
                "humidity": 48.0,
                "pressure": 1013.2,
                "last_maintenance": (datetime.now() - timedelta(days=60)).isoformat()
            }
        },
        {
            "name": "Temperature Sensor Drift",
            "description": "Temperature sensor showing gradual drift",
            "hvac_data": {
                "temperature": 28.5,  # Outside normal range
                "humidity": 45.0,
                "setpoint": 22.0,
                "last_maintenance": (datetime.now() - timedelta(days=30)).isoformat()
            },
            "sensor_data": {
                "temperature": 28.0,  # Correlated drift
                "humidity": 48.0,
                "pressure": 1013.2,
                "last_maintenance": (datetime.now() - timedelta(days=60)).isoformat()
            }
        },
        {
            "name": "High Humidity Environment",
            "description": "High humidity causing environmental issues",
            "hvac_data": {
                "temperature": 24.0,
                "humidity": 75.0,  # Outside normal range
                "setpoint": 22.0,
                "last_maintenance": (datetime.now() - timedelta(days=30)).isoformat()
            },
            "sensor_data": {
                "temperature": 23.5,
                "humidity": 78.0,  # Correlated high humidity
                "pressure": 1005.0,  # Slightly low pressure
                "last_maintenance": (datetime.now() - timedelta(days=60)).isoformat()
            }
        },
        {
            "name": "Critical Sensor Failure",
            "description": "Temperature sensor completely failed",
            "hvac_data": {
                "temperature": 5.0,  # Critical error range
                "humidity": 45.0,
                "setpoint": 22.0,
                "last_maintenance": (datetime.now() - timedelta(days=30)).isoformat()
            },
            "sensor_data": {
                "temperature": 4.5,  # Correlated failure
                "humidity": 48.0,
                "pressure": 1013.2,
                "last_maintenance": (datetime.now() - timedelta(days=60)).isoformat()
            }
        },
        {
            "name": "Maintenance Overdue",
            "description": "Multiple maintenance tasks overdue",
            "hvac_data": {
                "temperature": 22.0,
                "humidity": 45.0,
                "setpoint": 22.0,
                "last_maintenance": (datetime.now() - timedelta(days=120)).isoformat()  # Overdue
            },
            "sensor_data": {
                "temperature": 21.5,
                "humidity": 48.0,
                "pressure": 1013.2,
                "last_maintenance": (datetime.now() - timedelta(days=200)).isoformat()  # Overdue
            }
        },
        {
            "name": "Environmental Anomaly",
            "description": "Unusual environmental conditions",
            "hvac_data": {
                "temperature": 32.0,  # High temperature
                "humidity": 85.0,     # High humidity
                "setpoint": 22.0,
                "last_maintenance": (datetime.now() - timedelta(days=30)).isoformat()
            },
            "sensor_data": {
                "temperature": 31.5,  # Correlated high temperature
                "humidity": 88.0,     # Correlated high humidity
                "pressure": 980.0,    # Low pressure (storm conditions)
                "last_maintenance": (datetime.now() - timedelta(days=60)).isoformat()
            }
        }
    ]
    
    # Test each scenario
    for i, scenario in enumerate(anomaly_scenarios, 1):
        print(f"\n{'='*60}")
        print(f"📱 Scenario {i}: {scenario['name']}")
        print(f"   {scenario['description']}")
        print(f"{'='*60}")
        
        # Test HVAC Controller
        print(f"\n🏠 HVAC Controller Analysis:")
        hvac_anomalies = await detector.detect_anomalies(
            "hvac_001", 
            device_specs["hvac_controller"], 
            scenario["hvac_data"]
        )
        
        if hvac_anomalies:
            print(f"   🚨 {len(hvac_anomalies)} Anomalies Detected:")
            
            # Group by severity
            by_severity = {}
            for anomaly in hvac_anomalies:
                severity = anomaly.severity.value
                if severity not in by_severity:
                    by_severity[severity] = []
                by_severity[severity].append(anomaly)
            
            # Display by severity (critical first)
            for severity in ['critical', 'high', 'medium', 'low']:
                if severity in by_severity:
                    print(f"\n   {severity.upper()} SEVERITY:")
                    for anomaly in by_severity[severity]:
                        print(f"      🔸 {anomaly.description}")
                        print(f"         Type: {anomaly.anomaly_type.value}")
                        print(f"         Confidence: {anomaly.detection_confidence:.2f}")
                        print(f"         Troubleshooting: {anomaly.troubleshooting_steps[0] if anomaly.troubleshooting_steps else 'N/A'}")
                        if anomaly.maintenance_required:
                            print(f"         ⚠️  Maintenance Required")
        else:
            print(f"   ✅ No anomalies detected")
        
        # Test Environmental Sensor
        print(f"\n🌡️ Environmental Sensor Analysis:")
        sensor_anomalies = await detector.detect_anomalies(
            "sensor_001", 
            device_specs["environmental_sensor"], 
            scenario["sensor_data"]
        )
        
        if sensor_anomalies:
            print(f"   🚨 {len(sensor_anomalies)} Anomalies Detected:")
            
            # Group by severity
            by_severity = {}
            for anomaly in sensor_anomalies:
                severity = anomaly.severity.value
                if severity not in by_severity:
                    by_severity[severity] = []
                by_severity[severity].append(anomaly)
            
            # Display by severity
            for severity in ['critical', 'high', 'medium', 'low']:
                if severity in by_severity:
                    print(f"\n   {severity.upper()} SEVERITY:")
                    for anomaly in by_severity[severity]:
                        print(f"      🔸 {anomaly.description}")
                        print(f"         Type: {anomaly.anomaly_type.value}")
                        print(f"         Confidence: {anomaly.detection_confidence:.2f}")
                        print(f"         Troubleshooting: {anomaly.troubleshooting_steps[0] if anomaly.troubleshooting_steps else 'N/A'}")
        else:
            print(f"   ✅ No anomalies detected")
    
    # Show comprehensive anomaly summary
    print(f"\n{'='*60}")
    print(f"📊 Comprehensive Anomaly Summary")
    print(f"{'='*60}")
    
    for device_id in ["hvac_001", "sensor_001"]:
        summary = detector.get_anomaly_summary(device_id)
        print(f"\n🔧 {device_id.upper()}:")
        print(f"   Total Anomalies: {summary['total_anomalies']}")
        print(f"   Critical Anomalies: {summary['critical_anomalies']}")
        print(f"   Severity Breakdown: {summary['severity_breakdown']}")
        print(f"   Type Breakdown: {summary['type_breakdown']}")
    
    # Show anomaly detection capabilities
    print(f"\n🎯 Anomaly Detection Capabilities:")
    print(f"   ✅ Range-based detection (normal/warning/error ranges)")
    print(f"   ✅ Trend analysis (sensor drift detection)")
    print(f"   ✅ Pattern analysis (unusual data patterns)")
    print(f"   ✅ Maintenance monitoring (overdue tasks)")
    print(f"   ✅ Environmental correlation (temp/humidity/pressure)")
    print(f"   ✅ TinyML integration (AI-powered anomaly detection)")
    print(f"   ✅ Documentation-driven troubleshooting")
    print(f"   ✅ Severity classification (low/medium/high/critical)")
    print(f"   ✅ Confidence scoring for each detection")
    print(f"   ✅ Contextual root cause analysis")
    
    await ai_engine.close()
    print(f"\n🎉 Comprehensive Anomaly Detection Demo Complete!")
    print(f"   This shows how the system uses device documentation")
    print(f"   to detect various types of anomalies with contextual")
    print(f"   troubleshooting and maintenance recommendations!")


if __name__ == "__main__":
    asyncio.run(demo_comprehensive_anomaly_detection())
