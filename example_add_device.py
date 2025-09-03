#!/usr/bin/env python3
"""
Example: Adding Device Support to AI Gateway
Demonstrates different methods to add devices to the gateway
"""

import asyncio
import httpx
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.integration.mcp_dashboard_integration import MCPDashboardIntegration


async def example_web_dashboard_method():
    """Example: Add device using web dashboard API"""
    print("🌐 Method 1: Using Web Dashboard API")
    print("-" * 50)
    
    # Example device configurations
    devices_to_add = [
        {
            "protocol": "modbus",
            "name": "Schneider Electric PLC",
            "ip": "192.168.1.100",
            "port": 502,
            "docs": "schneider_plc_manual.pdf"
        },
        {
            "protocol": "bacnet",
            "name": "Honeywell Thermostat",
            "ip": "192.168.1.101",
            "port": 47808,
            "docs": "honeywell_thermostat_manual.pdf"
        },
        {
            "protocol": "rest",
            "name": "Environmental Sensor",
            "ip": "192.168.1.102",
            "port": 8001,
            "docs": "sensor_api_docs.pdf"
        }
    ]
    
    try:
        async with httpx.AsyncClient() as client:
            for device_config in devices_to_add:
                print(f"Adding {device_config['name']}...")
                
                response = await client.post(
                    "http://localhost:8081/api/devices",
                    json=device_config,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    device = result['device']
                    print(f"✅ Successfully added: {device['name']} (ID: {device['id']})")
                    print(f"   Protocol: {device['protocol'].upper()}")
                    print(f"   Address: {device['ip']}:{device['port']}")
                    print(f"   Status: {device['status']}")
                else:
                    print(f"❌ Failed to add {device_config['name']}: {response.text}")
                
                print()
                
    except httpx.ConnectError:
        print("❌ Cannot connect to dashboard server. Make sure it's running on port 8081")
    except Exception as e:
        print(f"❌ Error: {e}")


async def example_programmatic_method():
    """Example: Add device using programmatic integration"""
    print("🔧 Method 2: Using Programmatic Integration")
    print("-" * 50)
    
    try:
        # Initialize integration
        integration = MCPDashboardIntegration()
        await integration.initialize()
        
        # Add devices programmatically
        devices_to_add = [
            ("bacnet", "Johnson Controls VAV", "192.168.1.103", 47808, "johnson_vav_manual.pdf"),
            ("modbus", "Siemens S7 PLC", "192.168.1.104", 502, "siemens_s7_manual.pdf"),
            ("rest", "Weather Station API", "192.168.1.105", 8080, "weather_api_docs.pdf")
        ]
        
        for protocol, name, ip, port, docs in devices_to_add:
            print(f"Adding {name}...")
            
            device = await integration.add_device(
                protocol=protocol,
                name=name,
                ip=ip,
                port=port,
                docs=docs
            )
            
            print(f"✅ Successfully added: {device['name']} (ID: {device['id']})")
            print(f"   Protocol: {device['protocol'].upper()}")
            print(f"   Address: {device['ip']}:{device['port']}")
            print(f"   Created: {device['created']}")
            print()
            
        # Get all devices
        all_devices = integration.get_devices()
        print(f"📊 Total devices in system: {len(all_devices)}")
        
        for device in all_devices:
            print(f"   • {device['name']} ({device['protocol'].upper()}) - {device['status']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


async def example_device_discovery():
    """Example: Automatic device discovery"""
    print("🔍 Method 3: Automatic Device Discovery")
    print("-" * 50)
    
    try:
        integration = MCPDashboardIntegration()
        await integration.initialize()
        
        # Simulate device discovery (in real implementation, this would scan the network)
        print("Scanning network for devices...")
        
        # Mock discovered devices
        discovered_devices = [
            {
                "protocol": "bacnet",
                "ip": "192.168.1.200",
                "port": 47808,
                "device_id": 1001,
                "device_name": "Auto-discovered BACnet Device"
            },
            {
                "protocol": "modbus",
                "ip": "192.168.1.201",
                "port": 502,
                "unit_id": 1,
                "device_name": "Auto-discovered Modbus Device"
            },
            {
                "protocol": "rest",
                "ip": "192.168.1.202",
                "port": 8000,
                "endpoints": ["/api/status", "/api/data"],
                "device_name": "Auto-discovered REST API"
            }
        ]
        
        for discovered in discovered_devices:
            print(f"Found {discovered['protocol'].upper()} device:")
            print(f"   IP: {discovered['ip']}")
            print(f"   Port: {discovered['port']}")
            print(f"   Name: {discovered['device_name']}")
            
            # Add discovered device
            device = await integration.add_device(
                protocol=discovered['protocol'],
                name=discovered['device_name'],
                ip=discovered['ip'],
                port=discovered['port']
            )
            
            print(f"✅ Added to system: {device['id']}")
            print()
            
    except Exception as e:
        print(f"❌ Error: {e}")


async def example_custom_protocol():
    """Example: Adding a custom protocol"""
    print("🛠️ Method 4: Adding Custom Protocol")
    print("-" * 50)
    
    print("To add a custom protocol, you need to:")
    print()
    print("1. Create a protocol simulator:")
    print("   simulators/custom_protocol_simulator.py")
    print()
    print("2. Add protocol knowledge:")
    print("   src/core/protocol_knowledge.py")
    print()
    print("3. Update MCP server:")
    print("   src/mcp_server.py")
    print()
    print("4. Add to dashboard:")
    print("   dashboard/multi_protocol_dashboard.html")
    print()
    print("Example custom protocol specification:")
    print("""
CUSTOM_PROTOCOL_SPEC = {
    "name": "Custom Industrial Protocol",
    "port": 9999,
    "transport": "tcp",
    "message_format": "binary",
    "commands": {
        "read": "0x01",
        "write": "0x02",
        "status": "0x03",
        "alarm": "0x04"
    },
    "data_types": {
        "analog": "float32",
        "digital": "boolean",
        "string": "utf8"
    }
}
    """)


async def example_device_management():
    """Example: Device management operations"""
    print("📋 Method 5: Device Management Operations")
    print("-" * 50)
    
    try:
        integration = MCPDashboardIntegration()
        await integration.initialize()
        
        # Get all devices
        devices = integration.get_devices()
        print(f"Current devices: {len(devices)}")
        
        if devices:
            # Get first device
            device_id = list(devices.keys())[0]
            device = devices[device_id]
            
            print(f"Managing device: {device['name']}")
            print()
            
            # Read device data
            print("Reading device data...")
            try:
                data = await integration.read_device(device_id)
                print(f"✅ Read successful: {data}")
            except Exception as e:
                print(f"❌ Read failed: {e}")
            
            print()
            
            # Troubleshoot device
            print("Troubleshooting device...")
            try:
                troubleshooting = await integration.troubleshoot_device(device_id)
                print(f"✅ Troubleshooting: {troubleshooting}")
            except Exception as e:
                print(f"❌ Troubleshooting failed: {e}")
            
            print()
            
            # Remove device
            print("Removing device...")
            try:
                result = await integration.remove_device(device_id)
                print(f"✅ Device removed: {result}")
            except Exception as e:
                print(f"❌ Remove failed: {e}")
        else:
            print("No devices to manage. Add some devices first.")
            
    except Exception as e:
        print(f"❌ Error: {e}")


async def main():
    """Run all examples"""
    print("🚀 AI Gateway - Adding Device Support Examples")
    print("=" * 60)
    print()
    
    # Run examples
    await example_web_dashboard_method()
    print()
    
    await example_programmatic_method()
    print()
    
    await example_device_discovery()
    print()
    
    await example_custom_protocol()
    print()
    
    await example_device_management()
    print()
    
    print("🎉 All examples completed!")
    print()
    print("Next steps:")
    print("1. Start the dashboard server: python dashboard_server.py")
    print("2. Access the web interface: http://localhost:8081/multi-protocol")
    print("3. Add your own devices using the methods shown above")
    print("4. Upload device documentation PDFs for best results")


if __name__ == "__main__":
    asyncio.run(main())
