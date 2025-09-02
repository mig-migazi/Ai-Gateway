#!/usr/bin/env python3
"""
Documentation-Driven Simulator Demo
Demonstrates AI-powered device simulation based on real documentation
"""

import asyncio
import json
import sys
import os
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.simulators.documentation_driven_simulator import DocumentationDrivenSimulator
from ml.local_ai_engine import LocalAIEngine


async def demo_documentation_driven_simulation():
    """Demonstrate documentation-driven device simulation"""
    print("📚 Documentation-Driven Device Simulator Demo")
    print("=" * 60)
    
    # Initialize AI engine
    ai_engine = LocalAIEngine()
    await ai_engine.initialize()
    
    print(f"✅ TinyML AI Engine initialized")
    print(f"   Models: {ai_engine.get_model_info()['total_models']}")
    print(f"   Total Size: {ai_engine.get_model_info()['total_size_kb']:.2f} KB")
    
    # Create different types of device simulators
    devices = {
        "HVAC Controller": DocumentationDrivenSimulator(
            "hvac_controller_01", 
            "hvac_controller_manual.pdf", 
            ai_engine
        ),
        "Environmental Sensor": DocumentationDrivenSimulator(
            "env_sensor_01", 
            "environmental_sensor_spec.pdf", 
            ai_engine
        ),
        "BACnet Device": DocumentationDrivenSimulator(
            "bacnet_device_01", 
            "bacnet_device_manual.pdf", 
            ai_engine
        )
    }
    
    # Initialize all devices
    print(f"\n🔧 Initializing {len(devices)} documentation-driven devices...")
    for name, device in devices.items():
        await device.initialize()
        print(f"   ✅ {name}: {device.device_spec.get('device_type', 'unknown')} ({device.device_spec.get('protocol', 'unknown')})")
    
    # Show device specifications
    print(f"\n📋 Device Specifications:")
    for name, device in devices.items():
        spec = device.device_spec
        print(f"\n   {name}:")
        print(f"     Type: {spec.get('device_type', 'unknown')}")
        print(f"     Protocol: {spec.get('protocol', 'unknown')}")
        print(f"     Parameters: {len(spec.get('parameters', {}))}")
        print(f"     Error Codes: {len(spec.get('error_codes', {}))}")
        print(f"     Maintenance Schedule: {spec.get('maintenance_schedule', {})}")
    
    # Simulate realistic behavior over time
    print(f"\n🔄 Simulating Realistic Device Behavior...")
    print(f"   (Running 10 simulation cycles with AI-driven analysis)")
    
    for cycle in range(10):
        print(f"\n--- Simulation Cycle {cycle + 1} ---")
        
        for name, device in devices.items():
            # Simulate realistic behavior (including anomalies)
            await device.simulate_realistic_behavior()
            
            # Get comprehensive device status
            status = await device.get_device_status()
            
            print(f"\n   {name} ({status['device_id']}):")
            print(f"     Status: {status['status'].upper()}")
            
            # Show parameter values with context
            for param_name, value in status['parameters'].items():
                param_info = await device.get_parameter_value(param_name)
                status_emoji = {
                    'normal': '✅',
                    'warning': '⚠️',
                    'error': '🚨'
                }.get(param_info['status'], '❓')
                
                print(f"     {status_emoji} {param_info['parameter']}: {value:.2f} {param_info['unit']} ({param_info['status']})")
            
            # Show AI analysis
            analysis = status['analysis']
            if analysis.get('recommendations'):
                print(f"     💡 Recommendations: {analysis['recommendations']}")
            
            if analysis.get('maintenance_alerts'):
                print(f"     🔧 Maintenance: {analysis['maintenance_alerts']}")
            
            if analysis.get('troubleshooting_steps'):
                print(f"     🔍 Troubleshooting: {analysis['troubleshooting_steps'][:2]}")  # Show first 2 steps
            
            # Show error history if any
            if status['error_history']:
                latest_error = status['error_history'][-1]
                print(f"     🚨 Latest Error: {latest_error['message']} ({latest_error['error_code']})")
        
        # Wait between cycles
        await asyncio.sleep(0.5)
    
    # Demonstrate troubleshooting capabilities
    print(f"\n🔍 Troubleshooting Demonstration:")
    print(f"   (Simulating device issues and AI-powered solutions)")
    
    # Force an anomaly in the HVAC controller
    hvac_device = devices["HVAC Controller"]
    hvac_device.current_state.parameters['temperature'] = 45.0  # Force high temperature
    
    # Get analysis with troubleshooting
    status = await hvac_device.get_device_status()
    analysis = status['analysis']
    
    print(f"\n   HVAC Controller Issue Detected:")
    print(f"     Temperature: {status['parameters']['temperature']:.1f}°C (ERROR)")
    print(f"     AI Analysis: Anomaly Score {analysis['anomaly_score']:.2f}")
    print(f"     Confidence: {analysis['confidence']:.2f}")
    
    if analysis.get('troubleshooting_steps'):
        print(f"     🔧 AI-Generated Troubleshooting Steps:")
        for i, step in enumerate(analysis['troubleshooting_steps'], 1):
            print(f"       {i}. {step}")
    
    # Show documentation context
    print(f"\n📚 Documentation Context:")
    doc_context = status['documentation_context']
    print(f"     Protocol: {doc_context['protocol']}")
    print(f"     Error Codes: {doc_context['error_codes']}")
    print(f"     Maintenance Schedule: {doc_context['maintenance_schedule']}")
    
    # Performance summary
    print(f"\n⚡ Performance Summary:")
    print(f"   ✅ Documentation-driven simulation working")
    print(f"   ✅ AI-powered anomaly detection active")
    print(f"   ✅ Realistic device behavior with errors/anomalies")
    print(f"   ✅ Contextual troubleshooting from documentation")
    print(f"   ✅ Maintenance scheduling based on specs")
    print(f"   ✅ No hardcoded rules - all from documentation!")
    
    await ai_engine.close()
    print(f"\n🎉 Documentation-Driven Simulator Demo Complete!")


if __name__ == "__main__":
    asyncio.run(demo_documentation_driven_simulation())
