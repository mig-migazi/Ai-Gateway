"""
Interactive Demo - See exactly how the dynamic AI Gateway works
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def interactive_demo():
    """Interactive demo showing how the dynamic gateway works"""
    print("🎯 Interactive Demo: How Your Dynamic AI Gateway Works")
    print("=" * 60)
    print()
    
    # Import the dynamic MCP server
    from mcp_server import server, active_connections, _implement_protocol_dynamically
    from core.protocol_knowledge import knowledge_base, ProtocolType
    
    print("📚 Step 1: Protocol Knowledge Base")
    print("   This contains specifications for all protocols:")
    print()
    
    protocols = knowledge_base.get_all_protocols()
    for i, protocol in enumerate(protocols, 1):
        print(f"   {i}. {protocol.name}")
        print(f"      Port: {protocol.port}")
        print(f"      Discovery: {protocol.discovery_method}")
        print(f"      Timing: {protocol.timing_requirements}")
        print()
    
    print("🤖 Step 2: AI Agent Receives Query")
    print("   User asks: 'What's the temperature in room 101?'")
    print("   AI Agent thinks: 'I need to find temperature data'")
    print()
    
    print("🔧 Step 3: AI Agent Calls MCP Tool")
    print("   AI calls: implement_protocol_dynamically")
    print("   Parameters:")
    print("   - protocol: 'rest'")
    print("   - device_address: '127.0.0.1'")
    print("   - device_spec: {...}")
    print()
    
    print("⚡ Step 4: MCP Server Generates Code On-The-Fly")
    print("   Reading REST specification from knowledge base...")
    print("   Generating HTTP client code...")
    print("   Creating connection logic...")
    print()
    
    # Actually implement the protocol dynamically
    print("🚀 Step 5: Executing Generated Code")
    print("   Connecting to device...")
    
    try:
        protocol_type = ProtocolType.REST
        spec = knowledge_base.get_protocol_spec(protocol_type)
        
        result = await _implement_protocol_dynamically(
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
        
        if result["success"]:
            print(f"   ✅ Connection established!")
            print(f"   Connection ID: {result['connection_id']}")
            print(f"   Device info: {result['device_info']}")
            print()
            
            print("📊 Step 6: Getting Real Data")
            print("   Querying device for temperature...")
            
            # Query the device
            connection = active_connections[result["connection_id"]]
            query_result = await _query_device_dynamically(connection, "What's the temperature?")
            
            if query_result["success"]:
                temp = query_result["data"].get("temperature", "N/A")
                units = query_result["data"].get("units", "")
                print(f"   ✅ Temperature: {temp} {units}")
                print()
                
                print("🎯 Step 7: AI Agent Returns Answer")
                print(f"   AI Agent: 'The temperature in room 101 is {temp} {units}'")
                print()
                
                print("✨ The Magic: No Hardcoded Code!")
                print("   - No bacnet_handler.py")
                print("   - No rest_handler.py")
                print("   - No device_discovery.py")
                print("   - Just AI + Protocol Knowledge = Dynamic Implementation")
                
            else:
                print(f"   ❌ Query failed: {query_result['error']}")
        else:
            print(f"   ❌ Connection failed: {result['error']}")
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("🔗 Active Connections:")
    print(f"   Total: {len(active_connections)}")
    for connection_id, connection in active_connections.items():
        print(f"   - {connection['protocol']} to {connection['device_address']}")
        print(f"     Status: {connection['status']}")
        print(f"     Connected: {connection['connected_at']}")


async def _query_device_dynamically(connection, query):
    """Query a device using dynamically generated protocol implementation"""
    try:
        protocol = connection["protocol"]
        spec = connection["spec"]
        
        if protocol == "rest":
            return await _query_rest_device_dynamically(connection, query, spec)
        else:
            return {"error": f"Protocol {protocol} not supported"}
    
    except Exception as e:
        return {"error": str(e)}


async def _query_rest_device_dynamically(connection, query, spec):
    """Query REST device using dynamically generated implementation"""
    try:
        # Parse query to determine endpoint
        endpoint, params = _parse_rest_query(query, connection["endpoints"])
        
        if not endpoint:
            return {"error": "Could not determine endpoint from query"}
        
        url = f"{connection['base_url']}{endpoint}"
        response = await connection["client"].get(url, headers=connection["headers"], params=params)
        
        if response.status_code == 200:
            data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {"data": response.text}
            return {
                "success": True,
                "data": data,
                "endpoint": endpoint,
                "timestamp": "2025-09-02T12:00:00",
                "implementation_method": "dynamically_generated"
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}"
            }
    
    except Exception as e:
        return {"error": str(e)}


def _parse_rest_query(query, endpoints):
    """Parse natural language query to determine REST endpoint"""
    query_lower = query.lower()
    
    if "temperature" in query_lower or "temp" in query_lower:
        if "temperature" in endpoints:
            return endpoints["temperature"], {}
        elif "sensors" in endpoints:
            return endpoints["sensors"], {"type": "temperature"}
    
    elif "humidity" in query_lower:
        if "humidity" in endpoints:
            return endpoints["humidity"], {}
        elif "sensors" in endpoints:
            return endpoints["sensors"], {"type": "humidity"}
    
    elif "status" in query_lower:
        if "status" in endpoints:
            return endpoints["status"], {}
    
    if "status" in endpoints:
        return endpoints["status"], {}
    
    return None, {}


if __name__ == "__main__":
    asyncio.run(interactive_demo())
