#!/usr/bin/env python3
"""
Hybrid Edge-Cloud Architecture Demo
Demonstrates the complete flow: Device → Gateway → Cloud → Context
"""

import asyncio
import json
import sys
import os
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from gateway.hybrid_gateway import HybridGateway
from cloud.context_service import DeviceFingerprint


async def demo_complete_flow():
    """Demonstrate the complete hybrid architecture flow"""
    print("🌐 Hybrid Edge-Cloud Architecture Demo")
    print("=" * 60)
    print("Flow: BACnet Device → Gateway (TinyML) → Cloud (LLM + Vector DB) → Context")
    print()
    
    # Initialize hybrid gateway
    print("🔧 Initializing Hybrid Gateway...")
    gateway = HybridGateway()
    await gateway.initialize()
    
    gateway_info = gateway.get_gateway_info()
    print(f"✅ Gateway Ready:")
    print(f"   Type: {gateway_info['gateway_type']}")
    print(f"   Local AI Models: {gateway_info['local_ai_models']['total_models']}")
    print(f"   Model Size: {gateway_info['local_ai_models']['total_size_kb']:.2f} KB")
    print(f"   Capabilities: {len(gateway_info['capabilities'])}")
    
    # Simulate different device scenarios
    scenarios = [
        {
            "name": "HVAC Controller Discovery",
            "description": "BACnet HVAC controller starts talking to gateway",
            "device_data": {
                "port": 47808,
                "protocol": "udp",
                "response_time": 25,
                "data_size": 128,
                "device_id": "hvac_001",
                "vendor_id": "260",  # Johnson Controls
                "model_name": "Metasys NAE55",
                "firmware_version": "2.1.3",
                "request_frequency": 30,  # seconds
                "data_pattern": "bacnet_read_property"
            }
        },
        {
            "name": "Environmental Sensor Discovery", 
            "description": "REST API environmental sensor connects",
            "device_data": {
                "port": 8000,
                "protocol": "tcp",
                "response_time": 50,
                "data_size": 1024,
                "http_headers": 8,
                "has_json": True,
                "device_id": "sensor_001",
                "model_name": "SHT40",
                "request_frequency": 10,  # seconds
                "data_pattern": "rest_json"
            }
        },
        {
            "name": "Unknown BACnet Device",
            "description": "Unknown BACnet device with minimal info",
            "device_data": {
                "port": 47808,
                "protocol": "udp",
                "response_time": 15,
                "data_size": 64,
                "device_id": "unknown_001",
                "vendor_id": "999",  # Unknown vendor
                "model_name": "Unknown Model",
                "firmware_version": "1.0.0"
            }
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*60}")
        print(f"📱 Scenario {i}: {scenario['name']}")
        print(f"   {scenario['description']}")
        print(f"{'='*60}")
        
        device_data = scenario['device_data']
        
        # Show device fingerprint
        print(f"\n🔍 Step 1: Device Fingerprint")
        print(f"   Port: {device_data['port']}")
        print(f"   Device ID: {device_data.get('device_id', 'N/A')}")
        print(f"   Vendor ID: {device_data.get('vendor_id', 'N/A')}")
        print(f"   Model: {device_data.get('model_name', 'N/A')}")
        print(f"   Protocol: {device_data.get('protocol', 'N/A').upper()}")
        
        # Handle device connection
        print(f"\n🤖 Step 2: Gateway Processing")
        start_time = datetime.now()
        
        result = await gateway.handle_device_connection(device_data)
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds() * 1000
        
        if result.get("success"):
            print(f"✅ Device Successfully Handled ({processing_time:.1f}ms)")
            
            # Show protocol identification
            print(f"\n   🔍 Local AI Protocol Identification:")
            print(f"      Protocol: {result['protocol']}")
            print(f"      Confidence: {result['device_context']['confidence']:.3f}")
            
            # Show cloud context
            print(f"\n   ☁️ Cloud Context Retrieved:")
            context = result['device_context']
            print(f"      Manufacturer: {context['manufacturer']}")
            print(f"      Model: {context['model']}")
            print(f"      Device Type: {context['device_type']}")
            print(f"      Vector Similarity: {context['vector_similarity']:.3f}")
            
            # Show handling result
            handling = result['handling_result']
            print(f"\n   🔧 Device Handling Result:")
            print(f"      Parameters Available: {len(handling['parameters_available'])}")
            print(f"      Error Codes Known: {len(handling['error_codes_known'])}")
            print(f"      Troubleshooting Steps: {handling['troubleshooting_available']}")
            
            # Show sample parameters
            if handling.get('parameters'):
                print(f"\n   📋 Sample Parameters:")
                for param_name, param_desc in list(handling['parameters'].items())[:2]:
                    print(f"      - {param_name}: {param_desc}")
            
            # Show maintenance info
            if handling.get('maintenance'):
                print(f"\n   🔧 Maintenance Schedule:")
                for maintenance_type, interval in handling['maintenance'].items():
                    print(f"      - {maintenance_type.replace('_', ' ').title()}: {interval} days")
        
        else:
            print(f"❌ Device Handling Failed")
            print(f"   Error: {result.get('error', 'Unknown error')}")
        
        # Show processing method
        print(f"\n   ⚡ Processing Method: {result.get('processing_method', 'unknown')}")
    
    # Demonstrate troubleshooting
    print(f"\n{'='*60}")
    print(f"🔧 Troubleshooting Demonstration")
    print(f"{'='*60}")
    
    # Simulate device error
    print(f"\n📱 Simulating Device Error...")
    print(f"   Device: hvac_001")
    print(f"   Error Code: E001")
    
    # Get troubleshooting info
    troubleshoot_result = await gateway.troubleshoot_device("hvac_001", "E001")
    
    if troubleshoot_result.get("error_code"):
        print(f"✅ Troubleshooting Information Retrieved:")
        print(f"   Error: {troubleshoot_result['error_description']}")
        print(f"   Troubleshooting Steps:")
        for i, step in enumerate(troubleshoot_result['troubleshooting_steps'][:3], 1):
            print(f"      {i}. {step}")
        print(f"   Context Source: {troubleshoot_result['context_source']}")
    else:
        print(f"❌ Troubleshooting failed: {troubleshoot_result.get('error', 'Unknown error')}")
    
    # Show final gateway status
    print(f"\n{'='*60}")
    print(f"📊 Final Gateway Status")
    print(f"{'='*60}")
    
    final_info = gateway.get_gateway_info()
    print(f"   Gateway Type: {final_info['gateway_type']}")
    print(f"   Cached Devices: {final_info['cached_devices']}")
    print(f"   Local AI Models: {final_info['local_ai_models']['total_models']}")
    print(f"   Total Model Size: {final_info['local_ai_models']['total_size_kb']:.2f} KB")
    
    print(f"\n   🎯 Architecture Benefits:")
    print(f"      ✅ Minimal local processing (2.44 KB models)")
    print(f"      ✅ Fast protocol identification (~1ms)")
    print(f"      ✅ Rich device context from cloud")
    print(f"      ✅ Vector database search for device matching")
    print(f"      ✅ Free LLM integration for device identification")
    print(f"      ✅ Cached contexts for offline operation")
    print(f"      ✅ Comprehensive troubleshooting from documentation")
    
    print(f"\n🎉 Hybrid Edge-Cloud Architecture Demo Complete!")
    print(f"   This demonstrates how a gateway can use minimal local AI")
    print(f"   to identify protocols, then request rich context from the cloud")
    print(f"   to handle devices intelligently without hardcoded integrations!")


if __name__ == "__main__":
    asyncio.run(demo_complete_flow())
