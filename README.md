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
- **Real PDF Parsing**: Extract device specs from actual PDF documentation using PyMuPDF, pdfplumber, and PyPDF2
- **Advanced Vector Search**: Sentence transformer embeddings (all-MiniLM-L6-v2) with 384-dimensional vectors
- **Documentation-Driven Simulators**: AI-powered device simulation from parsed PDF specs
- **Multi-Protocol Dashboard**: Dynamic device management across all protocols
- **Real MCP Integration**: Connected to actual MCP server and device simulators
- **Web Dashboard**: Real-time monitoring with status indicators and AI query interface
- **REST API Simulator**: Complete with real-time streaming and EventSource support
- **BACnet IP Simulator**: Basic UDP communication and device simulation
- **Modbus TCP Simulator**: Industrial automation protocol with Schneider Electric Modicon M580 PLC

### 🚧 **In Development**
- **OPC-UA Simulator**: Machine-to-machine communication
- **Device Discovery**: Automatic network scanning and device detection
- **MCP Server HTTP Interface**: Currently stdio-based, needs HTTP wrapper

### 🎯 **Key Features**
- **Hybrid Architecture**: Edge AI + Cloud context for optimal performance
- **Minimal Edge Resources**: 2.44 KB models, ~1ms inference time
- **Rich Cloud Context**: Full device documentation and troubleshooting
- **Vector Database Search**: Intelligent device matching from documentation using sentence transformers
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

### Real PDF Processing Demos
- **PDF to Vector Flow**: `python demo_real_pdf_vector_flow.py` - Complete PDF → parsing → vectorizing → search pipeline
- **Create Sample PDF**: `python create_sample_pdf.py` - Generate sample BACnet device manual
- **PDF Parser Test**: `python src/pdf/pdf_parser.py` - Test PDF parsing functionality
- **Vector Embedding Test**: `python src/vector/embedding_service.py` - Test sentence transformer embeddings

### Device Management Examples
- **Add Device Examples**: `python example_add_device.py` - Complete examples of adding devices to the gateway

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

## Adding Device Support

The AI Gateway is designed to support any industrial protocol through documentation-driven learning. Here's how to add support for new devices:

### Method 1: Using the Web Dashboard (Recommended)

1. **Access the Multi-Protocol Dashboard**:
   ```
   http://localhost:8081/multi-protocol
   ```

2. **Add Device Form**:
   - **Protocol**: Select from REST, BACnet IP, Modbus TCP, or OPC-UA
   - **Device Name**: Enter a descriptive name (e.g., "HVAC Controller")
   - **IP Address**: Device's network address (e.g., 192.168.1.100)
   - **Port**: Device's communication port (e.g., 502 for Modbus)
   - **Documentation**: Upload device manual PDF (optional but recommended)

3. **Click "Add Device"**: The system will automatically:
   - Parse device documentation (if provided)
   - Generate vector embeddings for intelligent matching
   - Create device fingerprint for identification
   - Establish connection and start monitoring

### Method 2: Using the API

```python
import httpx

# Add a new device via API
async def add_device():
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8081/api/devices", json={
            "protocol": "modbus",
            "name": "Schneider Electric PLC",
            "ip": "192.168.1.100",
            "port": 502,
            "docs": "plc_manual.pdf"  # Optional
        })
        return response.json()

# Usage
device = await add_device()
print(f"Added device: {device['device']['name']}")
```

### Method 3: Programmatic Integration

```python
from src.integration.mcp_dashboard_integration import MCPDashboardIntegration

# Initialize integration
integration = MCPDashboardIntegration()
await integration.initialize()

# Add device programmatically
device = await integration.add_device(
    protocol="bacnet",
    name="Honeywell Thermostat",
    ip="192.168.1.101",
    port=47808,
    docs="thermostat_manual.pdf"
)

print(f"Device added: {device['id']}")
```

### Supported Protocols

| Protocol | Port | Description | Documentation Required |
|----------|------|-------------|----------------------|
| **REST API** | 8000-8999 | HTTP/JSON APIs | Optional - API endpoints |
| **BACnet IP** | 47808 | Building automation | Recommended - Object definitions |
| **Modbus TCP** | 502 | Industrial automation | Recommended - Register maps |
| **OPC-UA** | 4840 | Machine-to-machine | Recommended - Node definitions |

### Documentation Requirements

#### For BACnet Devices:
- **Object Definitions**: Analog Inputs (AI), Analog Values (AV), Binary Inputs (BI)
- **Object Instances**: Instance numbers for each object
- **Units**: Engineering units for analog values
- **Error Codes**: Device-specific error codes and descriptions
- **Network Configuration**: Device ID, network number, MAC address

#### For Modbus Devices:
- **Register Maps**: Input registers, holding registers, coils, discrete inputs
- **Data Types**: Integer, float, boolean, string formats
- **Scaling Factors**: Engineering unit conversions
- **Error Codes**: Modbus exception codes and meanings
- **Communication Settings**: Baud rate, parity, stop bits (for RTU)

#### For REST APIs:
- **Endpoint Documentation**: Available URLs and methods
- **Request/Response Formats**: JSON schemas, data types
- **Authentication**: API keys, tokens, headers
- **Rate Limits**: Request frequency limitations
- **Error Responses**: HTTP status codes and error messages

### Adding Custom Protocols

To add support for a completely new protocol:

1. **Create Protocol Simulator**:
   ```python
   # simulators/custom_protocol_simulator.py
   class CustomProtocolSimulator:
       def __init__(self, port=9999):
           self.port = port
           self.devices = {}
       
       async def start(self):
           # Implement protocol server
           pass
   ```

2. **Add Protocol Knowledge**:
   ```python
   # src/core/protocol_knowledge.py
   CUSTOM_PROTOCOL_SPEC = {
       "name": "Custom Protocol",
       "port": 9999,
       "transport": "tcp",  # or "udp"
       "message_format": "binary",  # or "text", "json"
       "commands": {
           "read": "0x01",
           "write": "0x02",
           "status": "0x03"
       }
   }
   ```

3. **Update MCP Server**:
   ```python
   # src/mcp_server.py
   async def _implement_custom_protocol_dynamically(spec, device_address, device_spec):
       # Implement protocol-specific logic
       pass
   ```

4. **Add to Dashboard**:
   ```html
   <!-- dashboard/multi_protocol_dashboard.html -->
   <option value="custom">Custom Protocol</option>
   ```

### Device Discovery

The gateway can automatically discover devices on the network:

```python
# Automatic device discovery
discovered_devices = await integration.discover_devices(
    network_range="192.168.1.0/24",
    protocols=["bacnet", "modbus", "rest"]
)

for device in discovered_devices:
    print(f"Found {device['protocol']} device at {device['ip']}")
```

### Troubleshooting Device Connections

1. **Check Network Connectivity**:
   ```bash
   ping 192.168.1.100
   telnet 192.168.1.100 502  # For Modbus
   ```

2. **Verify Protocol Settings**:
   - Port numbers match device configuration
   - Protocol version compatibility
   - Network security settings

3. **Review Device Documentation**:
   - Ensure PDF is properly formatted
   - Check for required parameters
   - Verify error code mappings

4. **Check Gateway Logs**:
   ```bash
   # View MCP server logs
   python src/mcp_server.py
   
   # View dashboard logs
   python dashboard_server.py
   ```

### Best Practices

1. **Documentation Quality**:
   - Use high-quality PDFs with clear text
   - Include complete parameter definitions
   - Provide troubleshooting sections

2. **Network Configuration**:
   - Use static IP addresses for critical devices
   - Configure proper firewall rules
   - Monitor network latency

3. **Testing**:
   - Test with device simulators first
   - Verify all parameters are accessible
   - Check error handling scenarios

4. **Security**:
   - Use secure communication protocols
   - Implement proper authentication
   - Monitor for unauthorized access

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

### PDF Processing Capabilities
- **Multi-Library Support**: PyMuPDF, pdfplumber, PyPDF2 for comprehensive text extraction
- **Structured Data Extraction**: Device parameters, error codes, troubleshooting steps
- **BACnet Object Parsing**: Automatic extraction of object types, instances, and properties
- **Error Code Recognition**: Pattern-based extraction of error codes and descriptions
- **Maintenance Schedule Parsing**: Automatic extraction of maintenance intervals and tasks
- **Network Configuration**: IP addresses, ports, and protocol settings
- **Sentence Transformer Embeddings**: 384-dimensional vectors using all-MiniLM-L6-v2 model
- **Vector Similarity Search**: Cosine similarity for intelligent device matching
- **Embedding Persistence**: Save/load embeddings for offline operation

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

This is a revolutionary approach to industrial protocol integration. **All contributions require explicit written consent** from the copyright holder.

Potential contribution areas (subject to approval):
- Additional protocol simulators (Modbus, OPC-UA, etc.)
- Enhanced AI capabilities
- Device discovery algorithms
- Performance optimizations
- Documentation improvements

**Contact the copyright holder before making any contributions.**

## License

**Copyright (c) 2025 Miguel Migazi. All rights reserved.**

This software and associated documentation files (the "Software") are proprietary and confidential. The Software is protected by copyright laws and international copyright treaties, as well as other intellectual property laws and treaties.

### Terms of Use

**NO PERMISSION IS GRANTED** to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, or to permit persons to whom the Software is furnished to do so, **WITHOUT EXPRESS WRITTEN CONSENT** from the copyright holder.

### Restrictions

- **Commercial Use**: Prohibited without explicit written permission
- **Distribution**: Prohibited without explicit written permission  
- **Modification**: Prohibited without explicit written permission
- **Reverse Engineering**: Prohibited
- **Derivative Works**: Prohibited without explicit written permission

### Contact for Permission

To request permission to use this Software, please contact:
- **Email**: [Your Email Address]
- **Subject**: "AI Gateway Software License Request"

Include in your request:
- Intended use case
- Commercial or non-commercial purpose
- Duration of use
- Any modifications planned

### Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

**⚠️ IMPORTANT**: This is proprietary software. Any unauthorized use, copying, or distribution is strictly prohibited and may result in legal action.
