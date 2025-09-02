#!/usr/bin/env python3
"""
TinyML Demo - Test the ultra-lightweight ML models
Demonstrates real-time inference on edge hardware
"""

import asyncio
import json
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ml.local_ai_engine import LocalAIEngine


async def demo_tinyml_models():
    """Demonstrate TinyML capabilities"""
    print("🤖 TinyML AI Gateway Demo")
    print("=" * 50)
    
    # Initialize TinyML engine
    ai_engine = LocalAIEngine()
    await ai_engine.initialize()
    
    # Show model information
    model_info = ai_engine.get_model_info()
    print(f"\n📊 TinyML Model Information:")
    print(f"   Total Models: {model_info['total_models']}")
    print(f"   Total Size: {model_info['total_size_kb']:.2f} KB")
    print(f"   Estimated Latency: {model_info['estimated_latency_ms']} ms")
    print(f"   Capabilities: {', '.join(model_info['capabilities'])}")
    
    print(f"\n🔍 Individual Models:")
    for name, model in model_info['tinyml_models'].items():
        print(f"   {name}: {model['input_size']}→{model['output_size']} ({model['size_kb']:.2f} KB)")
    
    # Test natural language query processing
    print(f"\n💬 Testing Natural Language Query Processing:")
    test_queries = [
        "What is the temperature in room 101?",
        "Show me the humidity levels",
        "Get pressure readings from all sensors",
        "Set the HVAC temperature to 22 degrees",
        "Compare energy consumption between rooms"
    ]
    
    for query in test_queries:
        print(f"\n   Query: '{query}'")
        result = await ai_engine.process_natural_query(query)
        print(f"   Intent: {result['intent']}")
        print(f"   Confidence: {result.get('confidence', 'N/A')}")
        print(f"   Latency: {result['latency_ms']:.2f} ms")
        print(f"   Model Size: {result.get('model_size_kb', 'N/A')} KB")
        print(f"   Processing: {result['processing_method']}")
    
    # Test device classification
    print(f"\n🔌 Testing Device Type Classification:")
    test_devices = [
        {"port": 8000, "protocol": "tcp", "response_time": 50, "data_size": 1024, "http_headers": 8, "has_json": True},
        {"port": 47808, "protocol": "udp", "response_time": 10, "data_size": 128, "http_headers": 0, "has_json": False},
        {"port": 502, "protocol": "tcp", "response_time": 25, "data_size": 64, "http_headers": 0, "has_json": False},
        {"port": 4840, "protocol": "tcp", "response_time": 100, "data_size": 2048, "http_headers": 12, "has_json": True}
    ]
    
    for i, device_data in enumerate(test_devices):
        print(f"\n   Device {i+1}: Port {device_data['port']}, {device_data['protocol'].upper()}")
        result = await ai_engine.classify_device_type(device_data)
        print(f"   Type: {result['device_type']}")
        print(f"   Confidence: {result['confidence']:.3f}")
        print(f"   Processing: {result.get('processing_method', 'unknown')}")
        print(f"   Keys: {list(result.keys())}")
        if 'latency_ms' in result:
            print(f"   Latency: {result['latency_ms']:.2f} ms")
        else:
            print(f"   Latency: N/A")
        print(f"   Model Size: {result.get('model_size_kb', 'N/A')} KB")
    
    # Test anomaly detection
    print(f"\n🚨 Testing Real-time Anomaly Detection:")
    test_sensor_data = [
        {"temperature": 22.5, "humidity": 45.0, "pressure": 1013.2},  # Normal
        {"temperature": 45.0, "humidity": 15.0, "pressure": 850.0},   # Anomalous
        {"temperature": 18.0, "humidity": 60.0, "pressure": 1020.0},  # Normal
        {"temperature": 5.0, "humidity": 95.0, "pressure": 1200.0},   # Anomalous
    ]
    
    for i, sensor_data in enumerate(test_sensor_data):
        print(f"\n   Sensor Data {i+1}: {sensor_data}")
        result = await ai_engine.detect_anomalies(sensor_data)
        print(f"   Anomaly: {'🚨 YES' if result['is_anomaly'] else '✅ NO'}")
        print(f"   Score: {result['anomaly_score']:.3f}")
        print(f"   Confidence: {result['confidence']:.3f}")
        if result['affected_sensors']:
            print(f"   Affected: {', '.join(result['affected_sensors'])}")
        if 'latency_ms' in result:
            print(f"   Latency: {result['latency_ms']:.2f} ms")
        else:
            print(f"   Latency: N/A")
        print(f"   Model Size: {result.get('model_size_kb', 'N/A')} KB")
    
    # Performance comparison
    print(f"\n⚡ Performance Summary:")
    print(f"   TinyML Models: Ultra-lightweight, edge-optimized")
    print(f"   Total Memory: {model_info['total_size_kb']:.2f} KB (fits in L1 cache!)")
    print(f"   Inference Speed: ~1ms per model")
    print(f"   Power Consumption: Minimal (perfect for gateways)")
    print(f"   Offline Capable: No internet required")
    print(f"   Privacy: All processing stays local")
    
    await ai_engine.close()
    print(f"\n✅ TinyML Demo Complete!")


if __name__ == "__main__":
    asyncio.run(demo_tinyml_models())
