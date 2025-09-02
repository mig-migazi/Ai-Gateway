# AI Gateway - Protocol-Agnostic Industrial Gateway

An AI-driven gateway that integrates with industrial protocols (BACnet IP, Modbus, OPC-UA, REST) without hardcoded integrations. Instead, it uses an MCP server with protocol knowledge to dynamically establish connections and handle queries.

## Concept

- **No dedicated protocol drivers** - AI agent implements protocols on-the-fly
- **Documentation-driven** - Protocol specs and device docs guide connections
- **Natural language queries** - Ask "what's the temperature in room 101?"
- **Dynamic discovery** - Agent finds and connects to devices automatically

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           AI GATEWAY ECOSYSTEM                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   REST API      │    │   BACnet IP     │    │   Modbus TCP    │    │   OPC-UA        │
│   Simulator     │    │   Simulator     │    │   Simulator     │    │   Simulator     │
│   Port: 8000    │    │   Port: 47808   │    │   Port: 502     │    │   Port: 4840    │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │                      │
          │ HTTP/JSON            │ UDP/BACnet           │ TCP/Modbus           │ TCP/OPC-UA
          │                      │                      │                      │
          └──────────────────────┼──────────────────────┼──────────────────────┘
                                 │                      │
                    ┌─────────────▼─────────────┐      │
                    │     AI GATEWAY CORE       │      │
                    │                           │      │
                    │  ┌─────────────────────┐  │      │
                    │  │   MCP SERVER        │  │      │
                    │  │   (Dynamic Engine)  │  │      │
                    │  └─────────┬───────────┘  │      │
                    │            │              │      │
                    │  ┌─────────▼───────────┐  │      │
                    │  │  LOCAL AI ENGINE    │  │      │
                    │  │  - NLP Processing   │  │      │
                    │  │  - Device Classify  │  │      │
                    │  │  - Anomaly Detect   │  │      │
                    │  └─────────┬───────────┘  │      │
                    │            │              │      │
                    │  ┌─────────▼───────────┐  │      │
                    │  │ PROTOCOL KNOWLEDGE  │  │      │
                    │  │      BASE           │  │      │
                    │  │ - BACnet Specs      │  │      │
                    │  │ - REST Docs         │  │      │
                    │  │ - Modbus Specs      │  │      │
                    │  │ - OPC-UA Specs      │  │      │
                    │  └─────────────────────┘  │      │
                    └─────────────┬─────────────┘      │
                                  │                    │
                    ┌─────────────▼─────────────┐      │
                    │    DASHBOARD SERVER       │      │
                    │    Port: 8081             │      │
                    │                           │      │
                    │  ┌─────────────────────┐  │      │
                    │  │  REAL-TIME UI       │  │      │
                    │  │  - Status Monitor   │  │      │
                    │  │  - Data Charts      │  │      │
                    │  │  - AI Decisions     │  │      │
                    │  │  - Query Interface  │  │      │
                    │  └─────────────────────┘  │      │
                    └───────────────────────────┘      │
                                                       │
                    ┌──────────────────────────────────▼──────────────────────────────────┐
                    │                    USER INTERFACE LAYER                              │
                    │                                                                     │
                    │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │
                    │  │  Web Dashboard  │  │  AI Query       │  │  Protocol       │     │
                    │  │  - Live Data    │  │  Dropdown       │  │  Status         │     │
                    │  │  - Charts       │  │  - 8 Query      │  │  - REST: ●      │     │
                    │  │  - Logs         │  │    Types        │  │  - BACnet: ●    │     │
                    │  │  - Controls     │  │  - Execute      │  │  - MCP: ●       │     │
                    │  └─────────────────┘  └─────────────────┘  └─────────────────┘     │
                    └─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA FLOW                                          │
└─────────────────────────────────────────────────────────────────────────────────┘

User Query → MCP Server → Local AI Engine → Protocol Knowledge Base → Dynamic Implementation
     ↓              ↓              ↓                    ↓                      ↓
Dashboard ← API Response ← Protocol Handler ← Device Communication ← Network Protocol
```

### Component Details

#### 🤖 **AI Gateway Core**
- **MCP Server**: Central orchestrator that handles all protocol interactions
- **Local AI Engine**: Fast, offline AI processing for NLP and device classification
- **Protocol Knowledge Base**: Repository of protocol specifications and device documentation

#### 🌐 **Protocol Simulators**
- **REST API Simulator**: HTTP/JSON-based device simulation with real-time streaming
- **BACnet IP Simulator**: UDP-based building automation protocol simulation
- **Modbus TCP Simulator**: Industrial automation protocol simulation (planned)
- **OPC-UA Simulator**: Machine-to-machine communication simulation (planned)

#### 📊 **Dashboard & Monitoring**
- **Real-time Dashboard**: Live data visualization and system monitoring
- **AI Query Interface**: Dropdown-based query selection with 8 predefined options
- **Status Monitoring**: Visual indicators for all system components
- **Activity Logging**: Comprehensive system activity and decision tracking

#### 🔄 **Dynamic Protocol Implementation**
- **On-demand Generation**: Protocol handlers created dynamically based on specifications
- **Real-time Adaptation**: Automatic protocol selection and optimization
- **Error Recovery**: Intelligent handling of connection issues and protocol errors
- **Multi-protocol Support**: Simultaneous handling of multiple industrial protocols

## Protocols Supported

- **REST APIs** - Simple HTTP-based device communication
- **BACnet IP** - Building automation and control networks
- **Modbus TCP** - Industrial automation protocol
- **OPC-UA** - Machine-to-machine communication

## Current Implementation Status

### ✅ **Fully Implemented**
- **REST API Simulator**: Complete with real-time streaming and EventSource support
- **BACnet IP Simulator**: Basic UDP communication and device simulation
- **MCP Server**: Dynamic protocol engine with local AI integration
- **Web Dashboard**: Real-time monitoring with status indicators and AI query interface
- **Local AI Engine**: NLP processing, device classification, and anomaly detection
- **Protocol Knowledge Base**: BACnet and REST specifications with dynamic implementation

### 🚧 **In Development**
- **Modbus TCP Simulator**: Industrial automation protocol support
- **OPC-UA Simulator**: Machine-to-machine communication
- **Advanced AI Features**: Predictive maintenance and energy optimization
- **Device Discovery**: Automatic network scanning and device detection

### 🎯 **Key Features**
- **Real-time Data Streaming**: Live sensor data with 5-second intervals
- **Dual Protocol Support**: Simultaneous REST and BACnet communication
- **AI Query Interface**: 8 predefined query types with dropdown selection
- **Status Monitoring**: Visual indicators for all system components
- **Dynamic Protocol Implementation**: No hardcoded drivers, all protocols generated on-demand
- **Local AI Processing**: Fast, offline AI with 0.1ms latency
- **Professional Dashboard**: Modern UI with charts, logs, and controls

## Getting Started

### Quick Start
1. **Clone the repository**: `git clone https://github.com/mig-migazi/Ai-Gateway.git`
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Set up environment**: Copy `env.example` to `.env` and add your OpenAI API key
4. **Start all services**: `python demo_full_system.py`

### Manual Setup
1. **Start REST Simulator**: `python simulators/rest_simulator.py`
2. **Start BACnet Simulator**: `python simulators/bacnet_simulator.py`
3. **Start Dashboard Server**: `python dashboard_server.py`
4. **Access Dashboard**: Open http://localhost:8081 in your browser

### Testing
- **Test API Key**: `python test_api_key.py`
- **Demo Local AI**: `python demo_local_ai.py`
- **Demo Dual Protocols**: `python demo_dual_protocols.py`
- **Interactive Demo**: `python interactive_demo.py`

## Technical Specifications

### Port Configuration
- **REST Simulator**: `http://localhost:8000`
- **BACnet Simulator**: `udp://localhost:47808`
- **Dashboard Server**: `http://localhost:8081`
- **MCP Server**: Integrated with Dashboard Server

### API Endpoints
- **REST Simulator**: `/api/temperature`, `/api/humidity`, `/api/stream`
- **Dashboard Server**: `/api/mcp/status`, `/api/mcp/query`, `/api/analytics`
- **BACnet Simulator**: UDP-based BACnet IP protocol

### AI Query Types
1. **Temperature**: "What's the current temperature?"
2. **Energy**: "Is the energy usage optimal?"
3. **HVAC**: "Should I adjust the HVAC settings?"
4. **Humidity**: "What's the humidity trend?"
5. **Anomalies**: "Are there any anomalies in the data?"
6. **BACnet**: "Test BACnet connection and get device information"
7. **Protocols**: "Compare REST vs BACnet data"
8. **Optimization**: "Suggest energy optimization strategies"

## Example Queries

### Natural Language Queries
- "What's the temperature in room 101?"
- "Show me all devices on the network"
- "What's the status of the HVAC system?"
- "Get the value of sensor ID 1234"
- "Compare data from REST and BACnet devices"
- "Are there any energy optimization opportunities?"

### Programmatic Queries
```python
# Test MCP query
response = await mcp_server.call_tool("query_device", {
    "query": "What's the current temperature?",
    "protocol": "REST"
})

# Dynamic protocol implementation
result = await mcp_server._implement_protocol_dynamically(
    "BACnet IP", "read_property", {"object_id": 1234}
)
```

## Contributing

This is a revolutionary approach to industrial protocol integration. Contributions are welcome for:
- Additional protocol simulators (Modbus, OPC-UA, etc.)
- Enhanced AI capabilities
- Device discovery algorithms
- Performance optimizations
- Documentation improvements

## License

This project demonstrates a novel approach to industrial protocol integration using AI-driven dynamic implementation.
