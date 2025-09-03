# AI Gateway - Protocol-Agnostic Industrial Gateway

An AI-driven gateway that integrates with industrial protocols (BACnet IP, Modbus, OPC-UA, REST) without hardcoded integrations. Instead, it uses an MCP server with protocol knowledge to dynamically establish connections and handle queries.

## Concept

- **No dedicated protocol drivers** - AI agent implements protocols on-the-fly
- **Documentation-driven** - Protocol specs and device docs guide connections
- **Natural language queries** - Ask "what's the temperature in room 101?"
- **Dynamic discovery** - Agent finds and connects to devices automatically

## Architecture

### Hybrid Edge-Cloud System Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    HYBRID EDGE-CLOUD AI GATEWAY ECOSYSTEM                      │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   REST API      │    │   BACnet IP     │    │   Modbus TCP    │    │   OPC-UA        │
│   Simulator     │    │   Simulator     │    │   Simulator     │    │   Simulator     │
│   Port: 8001    │    │   Port: 47808   │    │   Port: 502     │    │   Port: 4840    │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │                      │
          │ HTTP/JSON            │ UDP/BACnet           │ TCP/Modbus           │ TCP/OPC-UA
          │                      │                      │                      │
          └──────────────────────┼──────────────────────┼──────────────────────┘
                                 │                      │
                    ┌─────────────▼─────────────┐      │
                    │     EDGE GATEWAY          │      │
                    │   (Minimal Resources)     │      │
                    │                           │      │
                    │  ┌─────────────────────┐  │      │
                    │  │   TINYML ENGINE     │  │      │
                    │  │   (2.44 KB Models)  │  │      │
                    │  │  - Protocol ID      │  │      │
                    │  │  - Device Classify  │  │      │
                    │  │  - Anomaly Detect   │  │      │
                    │  │  - Fast Inference   │  │      │
                    │  └─────────┬───────────┘  │      │
                    │            │              │      │
                    │  ┌─────────▼───────────┐  │      │
                    │  │ DEVICE FINGERPRINT  │  │      │
                    │  │ - Network Features  │  │      │
                    │  │ - Protocol Data     │  │      │
                    │  │ - Communication     │  │      │
                    │  └─────────┬───────────┘  │      │
                    └─────────────┬─────────────┘      │
                                  │                    │
                    ┌─────────────▼─────────────┐      │
                    │    CLOUD CONTEXT SERVICE  │      │
                    │                           │      │
                    │  ┌─────────────────────┐  │      │
                    │  │   FREE LLM SERVICE  │  │      │
                    │  │  - Device ID        │  │      │
                    │  │  - Model Detection  │  │      │
                    │  │  - Context Extract  │  │      │
                    │  └─────────┬───────────┘  │      │
                    │            │              │      │
                    │  ┌─────────▼───────────┐  │      │
                    │  │  VECTOR DATABASE    │  │      │
                    │  │  - Device Docs      │  │      │
                    │  │  - Embeddings       │  │      │
                    │  │  - Similarity Search│  │      │
                    │  │  - Troubleshooting  │  │      │
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
│                        HYBRID EDGE-CLOUD DATA FLOW                             │
└─────────────────────────────────────────────────────────────────────────────────┘

Device → Edge Gateway (TinyML) → Cloud (LLM + Vector DB) → Context Response
   ↓              ↓                      ↓                        ↓
Network → Protocol ID → Device Fingerprint → Device Context → Intelligent Handling
   ↓              ↓                      ↓                        ↓
Dashboard ← API Response ← Cached Context ← Troubleshooting ← Maintenance Schedule
```

### Component Details

#### 🔗 **Edge Gateway (Minimal Resources)**
- **TinyML Engine**: Ultra-lightweight ML models (2.44 KB total) for fast edge processing
- **Device Fingerprinting**: Creates unique device signatures from network data
- **Protocol Identification**: Fast protocol classification (~1ms inference time)
- **Local Caching**: Stores device contexts for offline operation

#### ☁️ **Cloud Context Service**
- **Free LLM Service**: Uses Hugging Face models for device identification and context extraction
- **Vector Database**: Stores device documentation with embeddings for similarity search
- **Device Matching**: Finds similar devices using vector similarity algorithms
- **Rich Context**: Returns parameters, error codes, troubleshooting guides, and maintenance schedules

#### 🌐 **Protocol Simulators**
- **REST API Simulator**: HTTP/JSON-based device simulation with real-time streaming
- **BACnet IP Simulator**: UDP-based building automation protocol simulation
- **Modbus TCP Simulator**: Industrial automation protocol simulation with Schneider Electric Modicon M580 PLC
- **OPC-UA Simulator**: Machine-to-machine communication simulation (planned)

#### 📊 **Dashboard & Monitoring**
- **Multi-Protocol Dashboard**: Dynamic device management across all protocols
- **Real-time Dashboard**: Live data visualization and system monitoring
- **AI Query Interface**: Dropdown-based query selection with 8 predefined options
- **Status Monitoring**: Visual indicators for all system components
- **Activity Logging**: Comprehensive system activity and decision tracking
- **Real MCP Integration**: Connected to actual MCP server and device simulators

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
- **Hybrid Edge-Cloud Architecture**: Complete edge gateway with cloud context service
- **TinyML Engine**: Ultra-lightweight models (2.44 KB) for fast edge processing
- **Cloud Context Service**: Free LLM integration with vector database
- **Device Fingerprinting**: Network-based device identification and classification
- **Vector Database**: Device documentation storage with similarity search
- **Documentation-Driven Simulators**: AI-powered device simulation from specs
- **Multi-Protocol Dashboard**: Dynamic device management across all protocols
- **Real MCP Integration**: Connected to actual MCP server and device simulators
- **Web Dashboard**: Real-time monitoring with status indicators and AI query interface
- **REST API Simulator**: Complete with real-time streaming and EventSource support
- **BACnet IP Simulator**: Basic UDP communication and device simulation
- **Modbus TCP Simulator**: Industrial automation protocol with Schneider Electric Modicon M580 PLC

### 🚧 **In Development**
- **Real PDF Parsing**: Extract device specs from actual PDF documentation
- **Advanced Vector Search**: Improved similarity algorithms and embeddings
- **OPC-UA Simulator**: Machine-to-machine communication
- **Device Discovery**: Automatic network scanning and device detection
- **MCP Server HTTP Interface**: Currently stdio-based, needs HTTP wrapper

### 🎯 **Key Features**
- **Hybrid Architecture**: Edge AI + Cloud context for optimal performance
- **Minimal Edge Resources**: 2.44 KB models, ~1ms inference time
- **Rich Cloud Context**: Full device documentation and troubleshooting
- **Vector Database Search**: Intelligent device matching from documentation
- **Free LLM Integration**: No expensive API costs for device identification
- **Offline Operation**: Cached contexts work without internet
- **Real-time Data Streaming**: Live sensor data with 5-second intervals
- **AI Query Interface**: 8 predefined query types with dropdown selection
- **Status Monitoring**: Visual indicators for all system components
- **No Hardcoded Rules**: All behavior learned from documentation

## Getting Started

### Quick Start
1. **Clone the repository**: `git clone https://github.com/mig-migazi/Ai-Gateway.git`
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Set up environment**: Copy `env.example` to `.env` and add your OpenAI API key
4. **Start all services**: `python demo_full_system.py`

### Hybrid Architecture Demos
- **TinyML Demo**: `python demo_tinyml.py` - Test ultra-lightweight edge AI models
- **Documentation-Driven Simulator**: `python demo_documentation_driven.py` - AI-powered device simulation
- **Hybrid Edge-Cloud**: `python demo_hybrid_architecture.py` - Complete hybrid architecture flow
- **Cloud Context Service**: `python src/cloud/context_service.py` - Test cloud context retrieval

### Manual Setup
1. **Start REST Simulator**: `python simulators/rest_simulator.py`
2. **Start BACnet Simulator**: `python simulators/bacnet_simulator.py`
3. **Start Modbus Simulator**: `python simulators/modbus_simulator.py`
4. **Start Dashboard Server**: `python dashboard_server.py`
5. **Access Dashboards**: 
   - Multi-Protocol Dashboard: http://localhost:8081/multi-protocol
   - Hybrid Dashboard: http://localhost:8081/hybrid
   - Legacy Dashboard: http://localhost:8081/legacy

### Testing
- **Test API Key**: `python test_api_key.py`
- **Demo Local AI**: `python demo_local_ai.py`
- **Demo Dual Protocols**: `python demo_dual_protocols.py`
- **Interactive Demo**: `python interactive_demo.py`

## Hybrid Architecture Benefits

### 🚀 **Edge Gateway Advantages**
- **Ultra-Low Latency**: ~1ms protocol identification with TinyML models
- **Minimal Resources**: 2.44 KB total model size (fits in L1 cache!)
- **Offline Operation**: Cached device contexts work without internet
- **Low Power**: Perfect for battery-powered industrial gateways
- **Real-Time**: Sub-millisecond inference for time-critical applications

### ☁️ **Cloud Context Advantages**
- **Rich Device Knowledge**: Full documentation, error codes, troubleshooting
- **Free LLM Integration**: No expensive API costs for device identification
- **Vector Search**: Intelligent device matching from documentation
- **Scalable**: Easy to add new devices via cloud updates
- **Maintenance**: Centralized device knowledge management

### 🔄 **Hybrid Flow**
1. **Device connects** → Gateway uses TinyML to identify protocol (~1ms)
2. **Gateway creates fingerprint** → Sends to cloud for context lookup
3. **Cloud LLM identifies device** → Searches vector database for documentation
4. **Cloud returns context** → Gateway caches and handles device intelligently
5. **Future requests** → Use cached context for offline operation

## Technical Specifications

### Port Configuration
- **REST Simulator**: `http://localhost:8001`
- **BACnet Simulator**: `udp://localhost:47808`
- **Modbus Simulator**: `tcp://localhost:502`
- **Dashboard Server**: `http://localhost:8081`
- **MCP Server**: stdio-based (integrated with Dashboard Server)

### API Endpoints
- **REST Simulator**: `/api/temperature`, `/api/humidity`, `/api/stream`
- **Dashboard Server**: `/api/mcp/status`, `/api/mcp/query`, `/api/analytics`
- **Multi-Protocol Dashboard**: `/api/devices`, `/api/ai/query`, `/api/mcp/real-status`
- **BACnet Simulator**: UDP-based BACnet IP protocol
- **Modbus Simulator**: TCP-based Modbus protocol

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
