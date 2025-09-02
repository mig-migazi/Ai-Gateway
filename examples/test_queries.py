"""
Test Queries - Example queries to test the AI Gateway
"""

import asyncio
import json
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Example queries to test the AI Gateway
TEST_QUERIES = [
    "What's the temperature in room 101?",
    "Show me all devices on the network",
    "What's the status of the HVAC system?",
    "Get the value of sensor ID 1234",
    "What's the humidity in the building?",
    "Is the temperature sensor working?",
    "Show me all temperature readings",
    "What's the pressure in room 205?",
    "Are there any devices offline?",
    "Get the latest sensor data",
    "What's the temperature and humidity?",
    "Show me device information",
    "Is the system healthy?",
    "What protocols are available?",
    "Discover new devices"
]


async def test_query_processing():
    """Test the query processing functionality"""
    try:
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
        from src.ai.query_processor import QueryProcessor
        
        processor = QueryProcessor()
        await processor.initialize()
        
        print("Testing AI Gateway Query Processing")
        print("=" * 50)
        
        for i, query in enumerate(TEST_QUERIES, 1):
            print(f"\n{i}. Query: {query}")
            print("-" * 30)
            
            try:
                result = await processor.process_query(query)
                print(f"Result: {json.dumps(result, indent=2)}")
            except Exception as e:
                print(f"Error: {e}")
            
            # Small delay between queries
            await asyncio.sleep(1)
        
        await processor.close()
    
    except Exception as e:
        logger.error(f"Error testing query processing: {e}")


async def test_device_discovery():
    """Test device discovery functionality"""
    try:
        from src.discovery.device_discovery import DeviceDiscovery
        
        discovery = DeviceDiscovery()
        await discovery.initialize()
        
        print("Testing Device Discovery")
        print("=" * 30)
        
        # Test REST device discovery
        print("\n1. Discovering REST devices...")
        rest_devices = await discovery.discover_devices(["rest"], timeout=5)
        print(f"Found {len(rest_devices)} REST devices")
        for device in rest_devices:
            print(f"  - {device['name']} at {device['address']}:{device['port']}")
        
        # Test BACnet device discovery
        print("\n2. Discovering BACnet devices...")
        bacnet_devices = await discovery.discover_devices(["bacnet_ip"], timeout=5)
        print(f"Found {len(bacnet_devices)} BACnet devices")
        for device in bacnet_devices:
            print(f"  - {device['name']} at {device['address']}:{device['port']}")
        
        # Test combined discovery
        print("\n3. Discovering all devices...")
        all_devices = await discovery.discover_devices(["rest", "bacnet_ip"], timeout=10)
        print(f"Found {len(all_devices)} total devices")
        
        await discovery.close()
    
    except Exception as e:
        logger.error(f"Error testing device discovery: {e}")


async def test_protocol_handlers():
    """Test protocol handler functionality"""
    try:
        from src.protocols.rest_handler import RESTHandler
        from src.protocols.bacnet_handler import BACnetHandler
        
        print("Testing Protocol Handlers")
        print("=" * 30)
        
        # Test REST handler
        print("\n1. Testing REST handler...")
        rest_handler = RESTHandler()
        await rest_handler.initialize()
        
        # Try to connect to local REST simulator
        connection_result = await rest_handler.connect("127.0.0.1", {
            "base_url": "http://127.0.0.1:8000",
            "endpoints": {
                "status": "/status",
                "temperature": "/api/temperature",
                "humidity": "/api/humidity"
            }
        })
        
        if connection_result["success"]:
            print(f"Connected to REST device: {connection_result['connection_id']}")
            
            # Test querying
            query_result = await rest_handler.query(connection_result["connection_id"], "temperature")
            print(f"Query result: {json.dumps(query_result, indent=2)}")
        else:
            print(f"Failed to connect: {connection_result['error']}")
        
        await rest_handler.close()
        
        # Test BACnet handler
        print("\n2. Testing BACnet handler...")
        bacnet_handler = BACnetHandler()
        await bacnet_handler.initialize()
        
        # Try to connect to local BACnet simulator
        connection_result = await bacnet_handler.connect("127.0.0.1", {})
        
        if connection_result["success"]:
            print(f"Connected to BACnet device: {connection_result['connection_id']}")
            
            # Test querying
            query_result = await bacnet_handler.query(connection_result["connection_id"], "temperature")
            print(f"Query result: {json.dumps(query_result, indent=2)}")
        else:
            print(f"Failed to connect: {connection_result['error']}")
        
        await bacnet_handler.close()
    
    except Exception as e:
        logger.error(f"Error testing protocol handlers: {e}")


async def test_mcp_server():
    """Test MCP server functionality"""
    try:
        from src.mcp_server import server
        
        print("Testing MCP Server")
        print("=" * 20)
        
        # Test listing tools
        tools_result = await server.list_tools()
        print(f"Available tools: {len(tools_result.tools)}")
        for tool in tools_result.tools:
            print(f"  - {tool.name}: {tool.description}")
        
        # Test listing resources
        resources_result = await server.list_resources()
        print(f"Available resources: {len(resources_result.resources)}")
        for resource in resources_result.resources:
            print(f"  - {resource.name}: {resource.description}")
    
    except Exception as e:
        logger.error(f"Error testing MCP server: {e}")


async def run_all_tests():
    """Run all tests"""
    print("AI Gateway Test Suite")
    print("=" * 50)
    
    # Test device discovery first
    await test_device_discovery()
    
    # Test protocol handlers
    await test_protocol_handlers()
    
    # Test MCP server
    await test_mcp_server()
    
    # Test query processing
    await test_query_processing()
    
    print("\n" + "=" * 50)
    print("All tests completed!")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
