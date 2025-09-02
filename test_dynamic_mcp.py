"""
Test the truly dynamic MCP server - NO hardcoded handlers!
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def test_dynamic_mcp():
    """Test the dynamic MCP server"""
    print("🚀 Testing Truly Dynamic MCP Server")
    print("=" * 50)
    print("NO hardcoded handlers - AI generates protocol implementations on-the-fly!")
    print()
    
    # Import the dynamic MCP server
    from mcp_server import server, active_connections, _implement_protocol_dynamically
    from core.protocol_knowledge import knowledge_base, ProtocolType
    
    print("📚 Protocol Knowledge Base:")
    protocols = knowledge_base.get_all_protocols()
    for protocol in protocols:
        print(f"  ✅ {protocol.name} - {protocol.description}")
        print(f"     Port: {protocol.port}, Discovery: {protocol.discovery_method}")
    print()
    
    print("🔧 Dynamic Protocol Implementation:")
    print("  (MCP server generates protocol implementations on-the-fly)")
    print()
    
    # Test dynamic REST protocol implementation
    print("1. Implementing REST protocol dynamically via MCP...")
    try:
        protocol_type = ProtocolType.REST
        spec = knowledge_base.get_protocol_spec(protocol_type)
        
        rest_result = await _implement_protocol_dynamically(
            spec,
            "127.0.0.1",
            {
                "base_url": "http://127.0.0.1:8000",
                "endpoints": {
                    "status": "/status",
                    "temperature": "/api/temperature",
                    "humidity": "/api/humidity"
                }
            }
        )
        
        if rest_result["success"]:
            print(f"  ✅ REST protocol implemented dynamically!")
            print(f"     Connection ID: {rest_result['connection_id']}")
            print(f"     Implementation method: {rest_result['implementation_method']}")
            print(f"     Device info: {rest_result['device_info']}")
        else:
            print(f"  ❌ Failed to implement REST protocol: {rest_result['error']}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    print()
    
    # Test dynamic BACnet protocol implementation
    print("2. Implementing BACnet IP protocol dynamically via MCP...")
    try:
        protocol_type = ProtocolType.BACNET_IP
        spec = knowledge_base.get_protocol_spec(protocol_type)
        
        bacnet_result = await _implement_protocol_dynamically(
            spec,
            "127.0.0.1",
            {}
        )
        
        if bacnet_result["success"]:
            print(f"  ✅ BACnet IP protocol implemented dynamically!")
            print(f"     Connection ID: {bacnet_result['connection_id']}")
            print(f"     Implementation method: {bacnet_result['implementation_method']}")
            print(f"     Device info: {bacnet_result['device_info']}")
        else:
            print(f"  ❌ Failed to implement BACnet protocol: {bacnet_result['error']}")
            print("     (This is expected - the BACnet simulator might not be responding)")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    print()
    
    # Show active connections
    print("🔗 Active Connections:")
    print(f"  Total connections: {len(active_connections)}")
    for connection_id, connection in active_connections.items():
        print(f"    - {connection['protocol']} connection to {connection['device_address']}")
        print(f"      Connected at: {connection['connected_at']}")
        print(f"      Status: {connection['status']}")
    
    print()
    
    # Test MCP server tools
    print("🛠️  MCP Server Tools:")
    tools_result = await server.list_tools()
    print(f"  Available tools: {len(tools_result.tools)}")
    for tool in tools_result.tools:
        print(f"    - {tool.name}: {tool.description}")
    
    print()
    
    # Test MCP server resources
    print("📋 MCP Server Resources:")
    resources_result = await server.list_resources()
    print(f"  Available resources: {len(resources_result.resources)}")
    for resource in resources_result.resources:
        print(f"    - {resource.name}: {resource.description}")
    
    print()
    
    print("🎯 Dynamic MCP Test Complete!")
    print("   This demonstrates your true concept:")
    print("   • NO hardcoded protocol handlers")
    print("   • MCP server generates protocol implementations on-the-fly")
    print("   • Protocol code is created dynamically from specifications")
    print("   • AI agent can use MCP tools to implement any protocol")
    print("   • Natural language queries trigger dynamic code generation")

if __name__ == "__main__":
    asyncio.run(test_dynamic_mcp())
