# AI Gateway - Protocol-Agnostic Industrial Gateway

An AI-driven gateway that integrates with industrial protocols (BACnet IP, Modbus, OPC-UA, REST) without hardcoded integrations. Instead, it uses an MCP server with protocol knowledge to dynamically establish connections and handle queries.

## Concept

- **No dedicated protocol drivers** - AI agent implements protocols on-the-fly
- **Documentation-driven** - Protocol specs and device docs guide connections
- **Natural language queries** - Ask "what's the temperature in room 101?"
- **Dynamic discovery** - Agent finds and connects to devices automatically

## Architecture

```
AI Agent (MCP Server)
├── Protocol Knowledge Base
│   ├── BACnet IP specifications
│   ├── REST API documentation
│   └── Device specifications
├── Dynamic Protocol Implementer
│   ├── Generates protocol handlers on-demand
│   ├── Manages timing and state
│   └── Handles error recovery
└── Natural Language Interface
    ├── Query understanding
    ├── Device discovery
    └── Response generation
```

## Protocols Supported

- **REST APIs** - Simple HTTP-based device communication
- **BACnet IP** - Building automation and control networks
- **Modbus TCP** - Industrial automation protocol
- **OPC-UA** - Machine-to-machine communication

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Start the MCP server: `python src/mcp_server.py`
3. Run simulators: `python simulators/rest_simulator.py` and `python simulators/bacnet_simulator.py`
4. Test with queries: `python examples/test_queries.py`

## Example Queries

- "What's the temperature in room 101?"
- "Show me all devices on the network"
- "What's the status of the HVAC system?"
- "Get the value of sensor ID 1234"
