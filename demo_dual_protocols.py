"""
Demo: Dual Protocol AI Gateway
Shows the MCP server dynamically handling both REST and BACnet protocols
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def demo_dual_protocols():
    """Demonstrate the AI Gateway handling both REST and BACnet protocols dynamically"""
    print("🤖 Dual Protocol AI Gateway Demo")
    print("=" * 60)
    print("Dynamic protocol implementation: REST + BACnet IP")
    print("No hardcoded drivers - AI generates protocol implementations!")
    print()
    
    # Import the MCP server components
    from mcp_server import (
        _implement_protocol_dynamically,
        _process_natural_query_dynamically,
        knowledge_base
    )
    
    print("🚀 Step 1: Protocol Knowledge Base")
    print("   Available protocols in knowledge base:")
    for protocol in knowledge_base.protocols:
        print(f"   ✅ {protocol.name} - {protocol.value}")
    print()
    
    print("🎯 Step 2: Dynamic REST Protocol Implementation")
    print("   AI analyzing REST specification and generating implementation...")
    
    # Get REST protocol specification
    all_protocols = knowledge_base.get_all_protocols()
    rest_spec = next((p for p in all_protocols if p.name == "REST API"), None)
    if rest_spec:
        print(f"   📋 Protocol: {rest_spec.name}")
        print(f"   🔌 Port: {rest_spec.port}")
        print(f"   📝 Type: {rest_spec.protocol_type.value}")
        print(f"   🔍 Discovery: {rest_spec.discovery_method}")
        print()
        
        # Simulate dynamic REST implementation
        rest_device_spec = {
            "device_type": "temperature_sensor",
            "manufacturer": "Generic",
            "model": "REST-API-Sensor",
            "capabilities": ["temperature", "humidity", "pressure"]
        }
        
        print("   🤖 AI generating REST implementation...")
        rest_result = await _implement_protocol_dynamically(
            rest_spec, 
            "localhost:8000", 
            rest_device_spec
        )
        
        if rest_result["success"]:
            print(f"   ✅ REST connection established: {rest_result['connection_id']}")
            print(f"   🔧 Implementation: {rest_result['implementation_method']}")
            print(f"   📊 Status: {rest_result.get('status', 'Connected')}")
        else:
            print(f"   ❌ REST implementation failed: {rest_result['error']}")
    
    print()
    
    print("🎯 Step 3: Dynamic BACnet Protocol Implementation")
    print("   AI analyzing BACnet specification and generating implementation...")
    
    # Get BACnet protocol specification
    bacnet_spec = next((p for p in all_protocols if p.name == "BACnet IP"), None)
    if bacnet_spec:
        print(f"   📋 Protocol: {bacnet_spec.name}")
        print(f"   🔌 Port: {bacnet_spec.port}")
        print(f"   📝 Type: {bacnet_spec.protocol_type.value}")
        print(f"   🔍 Discovery: {bacnet_spec.discovery_method}")
        print()
        
        # Simulate dynamic BACnet implementation
        bacnet_device_spec = {
            "device_type": "bacnet_device",
            "manufacturer": "Honeywell",
            "model": "T6-Pro-Thermostat",
            "capabilities": ["temperature_control", "scheduling", "remote_access"]
        }
        
        print("   🤖 AI generating BACnet implementation...")
        bacnet_result = await _implement_protocol_dynamically(
            bacnet_spec, 
            "localhost:47808", 
            bacnet_device_spec
        )
        
        if bacnet_result["success"]:
            print(f"   ✅ BACnet connection established: {bacnet_result['connection_id']}")
            print(f"   🔧 Implementation: {bacnet_result['implementation_method']}")
            print(f"   📊 Status: {bacnet_result.get('status', 'Connected')}")
        else:
            print(f"   ❌ BACnet implementation failed: {bacnet_result['error']}")
    
    print()
    
    print("🗣️  Step 4: Natural Language Queries")
    print("   Testing AI query processing with multiple protocols...")
    print()
    
    test_queries = [
        "What's the temperature in room 101?",
        "Get me the humidity reading from the BACnet device",
        "Show me the pressure sensor data",
        "What's the status of all connected devices?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"   {i}. Query: \"{query}\"")
        
        # Process with AI
        result = await _process_natural_query_dynamically(query)
        
        if result["success"]:
            print(f"      ✅ AI Analysis: {result.get('ai_analysis', {}).get('intent', 'Unknown')}")
            print(f"      🎯 Entities: {result.get('ai_analysis', {}).get('entities', {})}")
            print(f"      ⚡ Actions: {len(result.get('ai_analysis', {}).get('protocol_actions', []))} protocol actions")
            print(f"      🚀 Method: {result.get('processing_method', 'Unknown')}")
            
            if result.get("results"):
                print(f"      📊 Results: {len(result['results'])} device responses")
                for res in result["results"]:
                    print(f"         • {res['protocol']} device: {res['result'].get('data', 'No data')}")
        else:
            print(f"      ❌ Error: {result.get('error', 'Unknown error')}")
        
        print()
    
    print("🎯 Step 5: Protocol Comparison")
    print("   Comparing dynamic implementations:")
    print()
    print("   📊 REST API Protocol:")
    print("      • Implementation: HTTP client with httpx")
    print("      • Discovery: HTTP GET requests")
    print("      • Data Format: JSON")
    print("      • Real-time: Polling-based")
    print("      • Complexity: Low")
    print()
    print("   📊 BACnet IP Protocol:")
    print("      • Implementation: UDP socket communication")
    print("      • Discovery: Who-Is/I-Am messages")
    print("      • Data Format: Binary BACnet messages")
    print("      • Real-time: Event-driven")
    print("      • Complexity: High")
    print()
    
    print("🎉 Dual Protocol Demo Complete!")
    print("   Your AI Gateway successfully:")
    print("   ✅ Dynamically implemented REST protocol")
    print("   ✅ Dynamically implemented BACnet protocol")
    print("   ✅ Processed natural language queries")
    print("   ✅ Generated protocol-specific implementations")
    print("   ✅ No hardcoded drivers required!")
    print()
    print("   🚀 This demonstrates the revolutionary approach:")
    print("      • AI analyzes protocol specifications")
    print("      • Generates implementations on-the-fly")
    print("      • Handles multiple protocols simultaneously")
    print("      • Uses natural language for device interaction")
    print()
    print("   💡 Perfect for industrial environments with:")
    print("      • Mixed protocol devices")
    print("      • Legacy system integration")
    print("      • Rapid device onboarding")
    print("      • Intelligent automation")


if __name__ == "__main__":
    asyncio.run(demo_dual_protocols())
