"""
Demo: Local AI Engine on Industrial Gateway
Shows how lightweight ML models run directly on the gateway for fast, offline processing
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def demo_local_ai():
    """Demonstrate local AI engine on industrial gateway"""
    print("🤖 Local AI Engine Demo - Industrial Gateway")
    print("=" * 60)
    print("Lightweight ML models running directly on the gateway!")
    print("Fast, offline, private AI processing for industrial applications")
    print()
    
    # Import the local AI engine
    from ml.local_ai_engine import LocalAIEngine
    
    # Initialize the local AI engine
    print("🚀 Step 1: Initializing Local AI Engine")
    print("   Loading lightweight ML models...")
    
    ai_engine = LocalAIEngine()
    await ai_engine.initialize()
    
    # Show model information
    model_info = ai_engine.get_model_info()
    print(f"   ✅ Models loaded: {model_info['models_loaded']}")
    print(f"   📊 Total parameters: {model_info['total_parameters']:,}")
    print(f"   💾 Memory usage: {model_info['estimated_memory_mb']:.1f} MB")
    print()
    
    # Test natural language processing
    print("🗣️  Step 2: Natural Language Processing")
    print("   Processing queries locally (no internet required!)")
    print()
    
    test_queries = [
        "What's the temperature in room 101?",
        "Get me the humidity reading",
        "Show me the pressure sensor data",
        "What's the status of the HVAC system?",
        "Set the temperature to 75 degrees"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"   {i}. Query: \"{query}\"")
        
        # Process with local AI
        result = await ai_engine.process_natural_query(query)
        
        if result["success"]:
            print(f"      ✅ Intent: {result['intent']}")
            print(f"      🎯 Entities: {result['entities']}")
            print(f"      ⚡ Actions: {len(result['protocol_actions'])} protocol actions")
            print(f"      🚀 Method: {result['processing_method']}")
            if 'latency_ms' in result:
                print(f"      ⏱️  Latency: {result['latency_ms']:.1f}ms")
        else:
            print(f"      ❌ Error: {result.get('error', 'Unknown error')}")
        
        print()
    
    # Test device classification
    print("🔍 Step 3: Device Classification")
    print("   Classifying devices from network traffic...")
    print()
    
    test_devices = [
        {"port": 80, "protocol": "tcp", "response_time": 50, "data_size": 1024, "headers": {"content-type": "application/json"}},
        {"port": 47808, "protocol": "udp", "response_time": 10, "data_size": 256, "headers": {}},
        {"port": 502, "protocol": "tcp", "response_time": 20, "data_size": 512, "headers": {}},
        {"port": 4840, "protocol": "tcp", "response_time": 100, "data_size": 2048, "headers": {"content-type": "application/opcua"}}
    ]
    
    for i, device_data in enumerate(test_devices, 1):
        print(f"   {i}. Network data: Port {device_data['port']}, Protocol {device_data['protocol']}")
        
        # Classify with local AI
        result = await ai_engine.classify_device_type(device_data)
        
        if result["success"]:
            print(f"      ✅ Device type: {result['device_type']}")
            print(f"      🎯 Confidence: {result['confidence']:.2f}")
            print(f"      🔧 Features: {result['features']}")
            print(f"      🚀 Method: {result['processing_method']}")
        else:
            print(f"      ❌ Error: {result.get('error', 'Unknown error')}")
        
        print()
    
    # Show performance comparison
    print("⚡ Step 4: Performance Comparison")
    print("   Local AI vs Cloud AI for industrial gateways:")
    print()
    print("   🌐 Cloud AI (OpenAI API):")
    print("      • Latency: 100-500ms per query")
    print("      • Reliability: Depends on internet")
    print("      • Cost: $0.01-0.10 per query")
    print("      • Privacy: Data leaves facility")
    print()
    print("   🏭 Local AI (Your Gateway):")
    print("      • Latency: 1-10ms per query")
    print("      • Reliability: Works offline")
    print("      • Cost: One-time deployment")
    print("      • Privacy: Data stays local")
    print()
    
    # Show model optimization
    print("🔧 Step 5: Edge Optimization")
    print("   Optimizing models for industrial gateway deployment...")
    
    await ai_engine.optimize_for_edge()
    
    print("   ✅ Models optimized for edge deployment")
    print("   📦 Ready for industrial gateway deployment")
    print()
    
    # Cleanup
    await ai_engine.close()
    
    print("🎯 Local AI Demo Complete!")
    print("   Your industrial gateway now has:")
    print("   • Fast, offline AI processing")
    print("   • Lightweight ML models")
    print("   • Private data processing")
    print("   • Real-time device classification")
    print("   • Natural language understanding")
    print()
    print("   Perfect for industrial environments where:")
    print("   • Internet connectivity is unreliable")
    print("   • Data privacy is critical")
    print("   • Low latency is required")
    print("   • Cost optimization is important")


if __name__ == "__main__":
    asyncio.run(demo_local_ai())
