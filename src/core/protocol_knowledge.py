"""
Protocol Knowledge Base - Contains specifications and documentation for supported protocols.
This is the "brain" that the AI agent uses to understand how to implement protocols dynamically.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json
import yaml


class ProtocolType(Enum):
    REST = "rest"
    BACNET_IP = "bacnet_ip"
    MODBUS_TCP = "modbus_tcp"
    OPC_UA = "opc_ua"


@dataclass
class ProtocolSpec:
    """Specification for a protocol implementation"""
    name: str
    protocol_type: ProtocolType
    port: int
    description: str
    timing_requirements: Dict[str, Any]
    connection_method: str
    discovery_method: str
    error_handling: Dict[str, Any]
    examples: List[Dict[str, Any]]


class ProtocolKnowledgeBase:
    """Knowledge base containing protocol specifications and implementation details"""
    
    def __init__(self):
        self.protocols: Dict[ProtocolType, ProtocolSpec] = {}
        self._load_protocol_specs()
    
    def _load_protocol_specs(self):
        """Load protocol specifications from knowledge base"""
        
        # REST API Protocol Specification
        self.protocols[ProtocolType.REST] = ProtocolSpec(
            name="REST API",
            protocol_type=ProtocolType.REST,
            port=80,
            description="HTTP-based RESTful API for device communication",
            timing_requirements={
                "request_timeout": 30,
                "retry_attempts": 3,
                "retry_delay": 1
            },
            connection_method="HTTP GET/POST/PUT/DELETE",
            discovery_method="Network scan for HTTP endpoints",
            error_handling={
                "http_codes": {
                    "200": "Success",
                    "404": "Resource not found",
                    "500": "Server error"
                },
                "retry_logic": "Exponential backoff"
            },
            examples=[
                {
                    "description": "Get device status",
                    "method": "GET",
                    "url": "http://192.168.1.100/api/status",
                    "response": {"status": "online", "temperature": 72.5}
                },
                {
                    "description": "Set device value",
                    "method": "POST",
                    "url": "http://192.168.1.100/api/set",
                    "payload": {"value": 25.0},
                    "response": {"success": True}
                }
            ]
        )
        
        # BACnet IP Protocol Specification
        self.protocols[ProtocolType.BACNET_IP] = ProtocolSpec(
            name="BACnet IP",
            protocol_type=ProtocolType.BACNET_IP,
            port=47808,
            description="Building Automation and Control Networks over IP",
            timing_requirements={
                "request_timeout": 5,
                "retry_attempts": 3,
                "retry_delay": 0.5,
                "frame_timing": "3.5 character times between frames"
            },
            connection_method="UDP broadcast/multicast",
            discovery_method="Who-Is broadcast for device discovery",
            error_handling={
                "error_codes": {
                    "0": "Success",
                    "1": "Abort",
                    "2": "Reject",
                    "3": "Error"
                },
                "retry_logic": "Immediate retry with backoff"
            },
            examples=[
                {
                    "description": "Read property value",
                    "service": "ReadProperty",
                    "object_type": "AnalogInput",
                    "object_instance": 1,
                    "property": "PresentValue",
                    "response": {"value": 72.5, "units": "degrees_fahrenheit"}
                },
                {
                    "description": "Write property value",
                    "service": "WriteProperty",
                    "object_type": "AnalogOutput",
                    "object_instance": 1,
                    "property": "PresentValue",
                    "value": 75.0
                }
            ]
        )
    
    def get_protocol_spec(self, protocol_type: ProtocolType) -> Optional[ProtocolSpec]:
        """Get specification for a specific protocol"""
        return self.protocols.get(protocol_type)
    
    def get_all_protocols(self) -> List[ProtocolSpec]:
        """Get all available protocol specifications"""
        return list(self.protocols.values())
    
    def get_protocol_by_port(self, port: int) -> Optional[ProtocolSpec]:
        """Find protocol by port number"""
        for spec in self.protocols.values():
            if spec.port == port:
                return spec
        return None
    
    def get_discovery_methods(self) -> Dict[ProtocolType, str]:
        """Get discovery methods for all protocols"""
        return {spec.protocol_type: spec.discovery_method for spec in self.protocols.values()}
    
    def get_timing_requirements(self, protocol_type: ProtocolType) -> Dict[str, Any]:
        """Get timing requirements for a specific protocol"""
        spec = self.get_protocol_spec(protocol_type)
        return spec.timing_requirements if spec else {}
    
    def get_examples(self, protocol_type: ProtocolType) -> List[Dict[str, Any]]:
        """Get implementation examples for a protocol"""
        spec = self.get_protocol_spec(protocol_type)
        return spec.examples if spec else []
    
    def to_json(self) -> str:
        """Export knowledge base to JSON"""
        data = {}
        for protocol_type, spec in self.protocols.items():
            data[protocol_type.value] = {
                "name": spec.name,
                "port": spec.port,
                "description": spec.description,
                "timing_requirements": spec.timing_requirements,
                "connection_method": spec.connection_method,
                "discovery_method": spec.discovery_method,
                "error_handling": spec.error_handling,
                "examples": spec.examples
            }
        return json.dumps(data, indent=2)
    
    def from_json(self, json_data: str):
        """Import knowledge base from JSON"""
        data = json.loads(json_data)
        for protocol_name, spec_data in data.items():
            protocol_type = ProtocolType(protocol_name)
            self.protocols[protocol_type] = ProtocolSpec(
                name=spec_data["name"],
                protocol_type=protocol_type,
                port=spec_data["port"],
                description=spec_data["description"],
                timing_requirements=spec_data["timing_requirements"],
                connection_method=spec_data["connection_method"],
                discovery_method=spec_data["discovery_method"],
                error_handling=spec_data["error_handling"],
                examples=spec_data["examples"]
            )


# Global knowledge base instance
knowledge_base = ProtocolKnowledgeBase()
