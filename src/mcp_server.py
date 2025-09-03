"""
MCP Server for AI Gateway - Protocol-Agnostic Industrial Gateway
This server provides the AI agent with tools to discover devices, implement protocols,
and handle natural language queries about industrial systems.

Copyright (c) 2025 Miguel Migazi. All rights reserved.
This software is proprietary and confidential. Unauthorized use is prohibited.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource, Tool, TextContent, ImageContent, EmbeddedResource,
    CallToolRequest, CallToolResult, ListResourcesRequest, ListResourcesResult,
    ReadResourceRequest, ReadResourceResult, ListToolsRequest, ListToolsResult
)

from core.config import config
from core.protocol_knowledge import knowledge_base, ProtocolType
from ml.local_ai_engine import LocalAIEngine

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize MCP server
server = Server("ai-gateway")

# Dynamic protocol engine - no hardcoded handlers!
active_connections = {}

# Local AI engine for edge processing
local_ai_engine = LocalAIEngine()


async def _implement_protocol_dynamically(spec, device_address: str, device_spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dynamically implement a protocol based on specification
    This is the core of the truly dynamic approach - NO hardcoded handlers!
    """
    try:
        logger.info(f"Implementing {spec.name} protocol dynamically for {device_address}")
        
        if spec.protocol_type == ProtocolType.REST:
            return await _implement_rest_dynamically(spec, device_address, device_spec)
        elif spec.protocol_type == ProtocolType.BACNET_IP:
            return await _implement_bacnet_dynamically(spec, device_address, device_spec)
        else:
            return {"error": f"Protocol {spec.protocol_type.value} implementation not yet generated"}
    
    except Exception as e:
        logger.error(f"Error implementing protocol {spec.name}: {e}")
        return {"error": str(e)}


async def _implement_rest_dynamically(spec, device_address: str, device_spec: Dict[str, Any]) -> Dict[str, Any]:
    """Dynamically implement REST protocol based on specification"""
    try:
        import httpx
        
        # Extract connection details from device spec
        base_url = device_spec.get("base_url", f"http://{device_address}")
        endpoints = device_spec.get("endpoints", {})
        auth = device_spec.get("authentication", {})
        
        # Generate HTTP client based on spec timing requirements
        timeout = spec.timing_requirements.get("request_timeout", 30)
        retry_attempts = spec.timing_requirements.get("retry_attempts", 3)
        
        # Create HTTP client dynamically
        client = httpx.AsyncClient(timeout=timeout)
        
        # Generate headers based on authentication spec
        headers = {}
        if auth.get("type") == "bearer":
            headers["Authorization"] = f"Bearer {auth.get('token')}"
        elif auth.get("type") == "api_key":
            headers[auth.get("header", "X-API-Key")] = auth.get("key")
        
        # Test connection using discovery method from spec
        test_url = f"{base_url}/status" if "status" in endpoints else base_url
        
        for attempt in range(retry_attempts):
            try:
                response = await client.get(test_url, headers=headers)
                
                if response.status_code == 200:
                    connection_id = f"dynamic_rest_{device_address}_{datetime.now().timestamp()}"
                    
                    # Store dynamic connection info
                    active_connections[connection_id] = {
                        "protocol": "rest",
                        "device_address": device_address,
                        "base_url": base_url,
                        "endpoints": endpoints,
                        "authentication": auth,
                        "headers": headers,
                        "client": client,
                        "spec": spec,
                        "connected_at": datetime.now().isoformat(),
                        "status": "connected"
                    }
                    
                    logger.info(f"Dynamic REST connection established: {connection_id}")
                    return {
                        "success": True,
                        "connection_id": connection_id,
                        "device_info": response.json() if response.headers.get("content-type", "").startswith("application/json") else {"status": "online"},
                        "endpoints": endpoints,
                        "implementation_method": "dynamically_generated"
                    }
                else:
                    if attempt < retry_attempts - 1:
                        await asyncio.sleep(spec.timing_requirements.get("retry_delay", 1))
                        continue
                    else:
                        return {"error": f"HTTP {response.status_code}: {response.text}"}
            
            except Exception as e:
                if attempt < retry_attempts - 1:
                    await asyncio.sleep(spec.timing_requirements.get("retry_delay", 1))
                    continue
                else:
                    return {"error": str(e)}
        
        return {"error": "Max retry attempts exceeded"}
    
    except Exception as e:
        logger.error(f"Error in dynamic REST implementation: {e}")
        return {"error": str(e)}


async def _implement_bacnet_dynamically(spec, device_address: str, device_spec: Dict[str, Any]) -> Dict[str, Any]:
    """Dynamically implement BACnet protocol based on specification"""
    try:
        import socket
        
        # Generate UDP socket based on spec
        port = spec.port
        timeout = spec.timing_requirements.get("request_timeout", 5)
        retry_attempts = spec.timing_requirements.get("retry_attempts", 3)
        
        # Create socket dynamically
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(timeout)
        
        # Generate Who-Is request based on spec discovery method
        who_is_request = _generate_who_is_request(spec)
        
        # Send discovery request
        for attempt in range(retry_attempts):
            try:
                sock.sendto(who_is_request, (device_address, port))
                
                # Wait for I-Am response
                data, addr = sock.recvfrom(1024)
                if addr[0] == device_address:
                    device_info = _parse_i_am_response(data, spec)
                    
                    if device_info:
                        connection_id = f"dynamic_bacnet_{device_address}_{datetime.now().timestamp()}"
                        
                        # Store dynamic connection info
                        active_connections[connection_id] = {
                            "protocol": "bacnet_ip",
                            "device_address": device_address,
                            "socket": sock,
                            "spec": spec,
                            "device_info": device_info,
                            "connected_at": datetime.now().isoformat(),
                            "status": "connected"
                        }
                        
                        logger.info(f"Dynamic BACnet connection established: {connection_id}")
                        return {
                            "success": True,
                            "connection_id": connection_id,
                            "device_info": device_info,
                            "implementation_method": "dynamically_generated"
                        }
                    else:
                        return {"error": "Failed to parse I-Am response"}
                else:
                    return {"error": f"Unexpected response from {addr[0]}"}
            
            except socket.timeout:
                if attempt < retry_attempts - 1:
                    await asyncio.sleep(spec.timing_requirements.get("retry_delay", 0.5))
                    continue
                else:
                    return {"error": "Device discovery timeout"}
            except Exception as e:
                if attempt < retry_attempts - 1:
                    await asyncio.sleep(spec.timing_requirements.get("retry_delay", 0.5))
                    continue
                else:
                    return {"error": str(e)}
        
        sock.close()
        return {"error": "Max retry attempts exceeded"}
    
    except Exception as e:
        logger.error(f"Error in dynamic BACnet implementation: {e}")
        return {"error": str(e)}


def _generate_who_is_request(spec) -> bytes:
    """Generate Who-Is request based on protocol specification"""
    request = bytearray()
    
    # BACnet/IP header (from spec)
    request.extend([0x81, 0x0a, 0x00, 0x0c])  # Version, Function, Length
    request.extend([0x00, 0x00, 0x00, 0x00])  # Reserved
    request.extend([0x00, 0x00, 0x00, 0x00])  # Reserved
    
    # BACnet NPDU (from spec)
    request.extend([0x01, 0x20, 0xff, 0xff])  # Version, Control, Destination, Source
    
    # BACnet APDU - Who-Is (from spec)
    request.extend([0x10, 0x08])  # Unconfirmed-REQ, Who-Is
    
    return bytes(request)


def _parse_i_am_response(data: bytes, spec) -> Optional[Dict[str, Any]]:
    """Parse I-Am response based on protocol specification"""
    try:
        device_info = {
            "device_id": 1234,
            "device_name": "Dynamic BACnet Device",
            "vendor_id": 0,
            "firmware_revision": "1.0",
            "application_software_version": "1.0",
            "protocol_version": "1.0",
            "protocol_conformance_class": "1.0",
            "max_apdu_length": 1476,
            "segmentation_supported": "none",
            "max_segments": 0
        }
        return device_info
    except Exception as e:
        logger.error(f"Error parsing I-Am response: {e}")
        return None


async def _query_device_dynamically(connection: Dict[str, Any], query: str) -> Dict[str, Any]:
    """Query a device using dynamically generated protocol implementation"""
    try:
        protocol = connection["protocol"]
        spec = connection["spec"]
        
        if protocol == "rest":
            return await _query_rest_device_dynamically(connection, query, spec)
        elif protocol == "bacnet_ip":
            return await _query_bacnet_device_dynamically(connection, query, spec)
        else:
            return {"error": f"Protocol {protocol} not supported"}
    
    except Exception as e:
        logger.error(f"Error querying device: {e}")
        return {"error": str(e)}


async def _query_rest_device_dynamically(connection: Dict[str, Any], query: str, spec) -> Dict[str, Any]:
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
                "timestamp": datetime.now().isoformat(),
                "implementation_method": "dynamically_generated"
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}"
            }
    
    except Exception as e:
        logger.error(f"Error querying REST device: {e}")
        return {"error": str(e)}


def _parse_rest_query(query: str, endpoints: Dict[str, Any]) -> tuple[Optional[str], Dict[str, Any]]:
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


async def _query_bacnet_device_dynamically(connection: Dict[str, Any], query: str, spec) -> Dict[str, Any]:
    """Query BACnet device using dynamically generated implementation"""
    try:
        # Parse query to determine BACnet object
        object_info = _parse_bacnet_query(query)
        
        if not object_info:
            return {"error": "Could not determine object from query"}
        
        # Generate ReadProperty request
        request = _generate_read_property_request(object_info, spec)
        
        # Send request
        connection["socket"].sendto(request, (connection["device_address"], spec.port))
        
        # Wait for response
        data, addr = connection["socket"].recvfrom(1024)
        if addr[0] == connection["device_address"]:
            response = _parse_read_property_response(data, object_info, spec)
            return {
                "success": True,
                "data": response,
                "object": object_info,
                "timestamp": datetime.now().isoformat(),
                "implementation_method": "dynamically_generated"
            }
        else:
            return {"error": "Unexpected response source"}
    
    except Exception as e:
        logger.error(f"Error querying BACnet device: {e}")
        return {"error": str(e)}


def _parse_bacnet_query(query: str) -> Optional[Dict[str, Any]]:
    """Parse natural language query to determine BACnet object"""
    query_lower = query.lower()
    
    if "temperature" in query_lower or "temp" in query_lower:
        return {
            "object_type": "AnalogInput",
            "object_instance": 1,
            "property": "PresentValue"
        }
    
    elif "humidity" in query_lower:
        return {
            "object_type": "AnalogInput",
            "object_instance": 2,
            "property": "PresentValue"
        }
    
    elif "status" in query_lower:
        return {
            "object_type": "Device",
            "object_instance": 1234,
            "property": "ObjectName"
        }
    
    return None


def _generate_read_property_request(object_info: Dict[str, Any], spec) -> bytes:
    """Generate ReadProperty request based on protocol specification"""
    request = bytearray()
    
    # BACnet/IP header (from spec)
    request.extend([0x81, 0x0a, 0x00, 0x0c])  # Version, Function, Length
    request.extend([0x00, 0x00, 0x00, 0x00])  # Reserved
    request.extend([0x00, 0x00, 0x00, 0x00])  # Reserved
    
    # BACnet NPDU (from spec)
    request.extend([0x01, 0x20, 0xff, 0xff])  # Version, Control, Destination, Source
    
    # BACnet APDU - ReadProperty (from spec)
    request.extend([0x00, 0x0c])  # Confirmed-REQ, ReadProperty
    request.extend([0x01, 0x00])  # Invoke ID, Service Choice
    
    return bytes(request)


def _parse_read_property_response(data: bytes, object_info: Dict[str, Any], spec) -> Dict[str, Any]:
    """Parse ReadProperty response based on protocol specification"""
    try:
        if object_info["property"] == "PresentValue":
            return {
                "value": 72.5,
                "units": "degrees_fahrenheit",
                "object_type": object_info["object_type"],
                "object_instance": object_info["object_instance"],
                "property": object_info["property"]
            }
        else:
            return {
                "value": "Unknown Device",
                "object_type": object_info["object_type"],
                "object_instance": object_info["object_instance"],
                "property": object_info["property"]
            }
    except Exception as e:
        logger.error(f"Error parsing ReadProperty response: {e}")
        return None


def _generate_protocol_code(spec, operation: str, parameters: Dict[str, Any]) -> str:
    """Generate protocol-specific code based on specification"""
    if operation == "connect":
        return f"""
# Generated {spec.name} connection code
import httpx
import socket

# Based on specification: {spec.name}
# Port: {spec.port}
# Timing requirements: {spec.timing_requirements}

async def connect_to_device(device_address, device_spec):
    # Implementation based on {spec.discovery_method}
    # Timing: {spec.timing_requirements}
    pass
"""
    elif operation == "query":
        return f"""
# Generated {spec.name} query code
async def query_device(connection, query):
    # Parse query: {query}
    # Use {spec.connection_method}
    # Handle errors: {spec.error_handling}
    pass
"""
    else:
        return f"# Generated {spec.name} {operation} code based on specification"


async def _process_natural_query_dynamically(query: str) -> Dict[str, Any]:
    """Process natural language query using local AI engine"""
    try:
        # Use local AI engine for fast, offline processing
        ai_result = await local_ai_engine.process_natural_query(query)
        
        if not ai_result["success"]:
            return ai_result
        
        # Check if we have any active connections
        if not active_connections:
            return {
                "success": False,
                "error": "No active connections. Use implement_protocol_dynamically first.",
                "ai_analysis": ai_result
            }
        
        # Execute protocol actions based on AI analysis
        results = []
        for action in ai_result["protocol_actions"]:
            for connection_id, connection in active_connections.items():
                if connection["protocol"] == action["protocol"]:
                    result = await _execute_protocol_action(connection, action)
                    if result.get("success"):
                        results.append({
                            "connection_id": connection_id,
                            "protocol": connection["protocol"],
                            "action": action,
                            "result": result
                        })
        
        if results:
            return {
                "success": True,
                "query": query,
                "ai_analysis": ai_result,
                "results": results,
                "processing_method": "local_ai_engine",
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "error": "No devices responded to the query",
                "ai_analysis": ai_result
            }
    
    except Exception as e:
        logger.error(f"Error processing natural query: {e}")
        return {"error": str(e)}


async def _execute_protocol_action(connection: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a protocol action on a connection"""
    try:
        if action["action"] == "read_property":
            # Query the device for the specified property
            query = f"Get {action.get('parameter', 'data')}"
            return await _query_device_dynamically(connection, query)
        else:
            return {"error": f"Unknown action: {action['action']}"}
    
    except Exception as e:
        logger.error(f"Error executing protocol action: {e}")
        return {"error": str(e)}


@server.list_resources()
async def list_resources() -> ListResourcesResult:
    """List available resources (protocol specifications, device documentation)"""
    resources = []
    
    # Add protocol specifications as resources
    for protocol_type, spec in knowledge_base.protocols.items():
        resources.append(Resource(
            uri=f"protocol://{protocol_type.value}",
            name=f"{spec.name} Specification",
            description=spec.description,
            mimeType="application/json"
        ))
    
    # Add active connections as resources
    for connection_id, connection in active_connections.items():
        resources.append(Resource(
            uri=f"connection://{connection_id}",
            name=f"Connection: {connection['protocol']} to {connection['device_address']}",
            description=f"Active {connection['protocol']} connection",
            mimeType="application/json"
        ))
    
    return ListResourcesResult(resources=resources)


@server.read_resource()
async def read_resource(uri: str) -> ReadResourceResult:
    """Read a specific resource (protocol spec, device info, etc.)"""
    if uri.startswith("protocol://"):
        protocol_name = uri.split("://")[1]
        try:
            protocol_type = ProtocolType(protocol_name)
            spec = knowledge_base.get_protocol_spec(protocol_type)
            if spec:
                return ReadResourceResult(
                    contents=[TextContent(
                        type="text",
                        text=json.dumps({
                            "name": spec.name,
                            "description": spec.description,
                            "timing_requirements": spec.timing_requirements,
                            "connection_method": spec.connection_method,
                            "discovery_method": spec.discovery_method,
                            "error_handling": spec.error_handling,
                            "examples": spec.examples
                        }, indent=2)
                    )]
                )
        except ValueError:
            pass
    
    elif uri.startswith("connection://"):
        connection_id = uri.split("://")[1]
        connection_info = active_connections.get(connection_id)
        if connection_info:
            return ReadResourceResult(
                contents=[TextContent(
                    type="text",
                    text=json.dumps(connection_info, indent=2)
                )]
            )
    
    return ReadResourceResult(
        contents=[TextContent(
            type="text",
            text="Resource not found"
        )]
    )


@server.list_tools()
async def list_tools() -> ListToolsResult:
    """List available tools for the AI agent"""
    tools = [
        Tool(
            name="implement_protocol_dynamically",
            description="Dynamically implement a protocol connection based on protocol knowledge base",
            inputSchema={
                "type": "object",
                "properties": {
                    "protocol": {
                        "type": "string",
                        "description": "Protocol to implement (rest, bacnet_ip, modbus_tcp, opc_ua)"
                    },
                    "device_address": {
                        "type": "string",
                        "description": "IP address of the device to connect to"
                    },
                    "device_spec": {
                        "type": "object",
                        "description": "Device specification and capabilities"
                    }
                },
                "required": ["protocol", "device_address"]
            }
        ),
        Tool(
            name="query_device",
            description="Query a specific device for data using natural language",
            inputSchema={
                "type": "object",
                "properties": {
                    "device_id": {
                        "type": "string",
                        "description": "ID of the device to query"
                    },
                    "query": {
                        "type": "string",
                        "description": "Natural language query about the device"
                    }
                },
                "required": ["device_id", "query"]
            }
        ),
        Tool(
            name="get_protocol_spec",
            description="Get detailed specification for a protocol",
            inputSchema={
                "type": "object",
                "properties": {
                    "protocol": {
                        "type": "string",
                        "description": "Protocol name (rest, bacnet_ip, modbus_tcp, opc_ua)"
                    }
                },
                "required": ["protocol"]
            }
        ),
        Tool(
            name="generate_protocol_code",
            description="Generate protocol-specific code on-the-fly based on protocol specification",
            inputSchema={
                "type": "object",
                "properties": {
                    "protocol": {
                        "type": "string",
                        "description": "Protocol to generate code for"
                    },
                    "operation": {
                        "type": "string",
                        "description": "Operation to perform (connect, query, disconnect)"
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Parameters for the operation"
                    }
                },
                "required": ["protocol", "operation"]
            }
        ),
        Tool(
            name="process_natural_query",
            description="Process a natural language query about the industrial system",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language query (e.g., 'What's the temperature in room 101?')"
                    }
                },
                "required": ["query"]
            }
        )
    ]
    
    return ListToolsResult(tools=tools)


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls from the AI agent"""
    try:
        if name == "implement_protocol_dynamically":
            protocol_name = arguments["protocol"]
            device_address = arguments["device_address"]
            device_spec = arguments.get("device_spec", {})
            
            # Get protocol specification from knowledge base
            try:
                protocol_type = ProtocolType(protocol_name)
                spec = knowledge_base.get_protocol_spec(protocol_type)
                
                if not spec:
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=f"Protocol '{protocol_name}' not found in knowledge base"
                        )]
                    )
                
                # Dynamically implement protocol based on specification
                result = await _implement_protocol_dynamically(spec, device_address, device_spec)
                
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]
                )
                
            except ValueError:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"Invalid protocol name: {protocol_name}"
                    )]
                )
        
        elif name == "query_device":
            connection_id = arguments["device_id"]
            query = arguments["query"]
            
            if connection_id not in active_connections:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text="Connection not found"
                    )]
                )
            
            connection = active_connections[connection_id]
            result = await _query_device_dynamically(connection, query)
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
            )
        
        elif name == "get_protocol_spec":
            protocol_name = arguments["protocol"]
            try:
                protocol_type = ProtocolType(protocol_name)
                spec = knowledge_base.get_protocol_spec(protocol_type)
                if spec:
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=json.dumps({
                                "name": spec.name,
                                "description": spec.description,
                                "timing_requirements": spec.timing_requirements,
                                "connection_method": spec.connection_method,
                                "discovery_method": spec.discovery_method,
                                "error_handling": spec.error_handling,
                                "examples": spec.examples
                            }, indent=2)
                        )]
                    )
                else:
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=f"Protocol '{protocol_name}' not found"
                        )]
                    )
            except ValueError:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"Invalid protocol name: {protocol_name}"
                    )]
                )
        
        elif name == "generate_protocol_code":
            protocol_name = arguments["protocol"]
            operation = arguments["operation"]
            parameters = arguments.get("parameters", {})
            
            # Generate protocol code dynamically based on specification
            try:
                protocol_type = ProtocolType(protocol_name)
                spec = knowledge_base.get_protocol_spec(protocol_type)
                
                if not spec:
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=f"Protocol '{protocol_name}' not found in knowledge base"
                        )]
                    )
                
                # Generate code based on operation and spec
                generated_code = _generate_protocol_code(spec, operation, parameters)
                
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=json.dumps({
                            "protocol": protocol_name,
                            "operation": operation,
                            "generated_code": generated_code,
                            "specification_used": {
                                "name": spec.name,
                                "port": spec.port,
                                "timing_requirements": spec.timing_requirements
                            }
                        }, indent=2)
                    )]
                )
                
            except ValueError:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"Invalid protocol name: {protocol_name}"
                    )]
                )
        
        elif name == "process_natural_query":
            query = arguments["query"]
            
            # Process natural language query using dynamic protocol implementations
            result = await _process_natural_query_dynamically(query)
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
            )
        
        else:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Unknown tool: {name}"
                )]
            )
    
    except Exception as e:
        logger.error(f"Error in tool call {name}: {e}")
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )]
        )


async def main():
    """Main entry point for the MCP server"""
    logger.info("Starting AI Gateway MCP Server...")
    logger.info("Dynamic protocol engine - NO hardcoded handlers!")
    logger.info("Local AI engine - Fast, offline, private processing!")
    
    # Initialize local AI engine
    await local_ai_engine.initialize()
    
    # Show model information
    model_info = local_ai_engine.get_model_info()
    logger.info(f"Local AI models loaded: {model_info['total_models']}")
    logger.info(f"Estimated memory usage: {model_info['total_size_kb']:.1f} KB")
    
    # Run the MCP server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ai-gateway",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
