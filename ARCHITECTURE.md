# FMU Virtual ECU Architecture

## System Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                         USER LAYER                                │
│                                                                    │
│  ┌───────────────┐        ┌──────────────┐                       │
│  │  VS Code      │        │   Terminal   │                       │
│  │  + Copilot    │        │   Scripts    │                       │
│  └───────┬───────┘        └──────┬───────┘                       │
│          │                       │                                │
└──────────┼───────────────────────┼────────────────────────────────┘
           │                       │
           │  MCP Protocol         │  Direct Python
           │  (stdio/JSON-RPC)     │  Import
           ▼                       ▼
┌──────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                            │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                MCP Server (server.py)                     │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │  MCP Tools:                                        │  │   │
│  │  │  • get_ecu_info                                    │  │   │
│  │  │  • get_software_version                            │  │   │
│  │  │  • get_interfaces                                  │  │   │
│  │  │  • get_ecu_level                                   │  │   │
│  │  │  • perform_addition                                │  │   │
│  │  │  • get_ecu_status                                  │  │   │
│  │  └────────────┬───────────────────────────────────────┘  │   │
│  └───────────────┼──────────────────────────────────────────┘   │
│                  │                                               │
│  ┌───────────────┼──────────────────────────────────────────┐   │
│  │               │       AI Agent (ai_agent.py)             │   │
│  │               │       ┌──────────────────┐               │   │
│  │               │       │  OpenAI Client   │               │   │
│  │               │       │   GPT-3.5/GPT-4  │               │   │
│  │               │       └────────┬─────────┘               │   │
│  │               │                │                          │   │
│  │               │       Natural Language                    │   │
│  │               │       Query Processing                    │   │
│  │               │                │                          │   │
│  └───────────────┼────────────────┼──────────────────────────┘   │
│                  │                │                               │
└──────────────────┼────────────────┼───────────────────────────────┘
                   │                │
                   ▼                ▼
┌──────────────────────────────────────────────────────────────────┐
│                       DOMAIN LAYER                                │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           Virtual ECU (fmu_model.py)                      │   │
│  │                                                            │   │
│  │  ECU Attributes:                                          │   │
│  │  • Software: Virtual ECU - Addition Module                │   │
│  │  • Version: 1.0.0                                         │   │
│  │  • ECU Level: Level_2                                     │   │
│  │  • Manufacturer: FMU-MCP-Server                           │   │
│  │                                                            │   │
│  │  Supported Interfaces:                                    │   │
│  │  ┌──────┐ ┌──────┐ ┌──────────┐ ┌──────────┐            │   │
│  │  │ CAN  │ │ LIN  │ │ Ethernet │ │ FlexRay  │            │   │
│  │  └──────┘ └──────┘ └──────────┘ └──────────┘            │   │
│  │                                                            │   │
│  │  ECU Operations:                                          │   │
│  │  • add(a, b) → a + b                                      │   │
│  │  • get_info() → ECU metadata                              │   │
│  │  • get_version() → version string                         │   │
│  │  • get_interfaces() → interface list                      │   │
│  │  • get_ecu_level() → ECU level                            │   │
│  │  • get_status() → operational status                      │   │
│  │                                                            │   │
│  │  Capabilities:                                            │   │
│  │  • Addition                                               │   │
│  │  • Data Processing                                        │   │
│  │  • Real-time Response                                     │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
                           ▲
                           │
                  Internal State & Logic
```

## Data Flow

### 1. MCP Query Flow

```
User (Copilot)
    │
    │ "What is the ECU version?"
    ▼
MCP Server
    │
    │ parse request → call tool
    ▼
Virtual ECU
    │
    │ get_version()
    │
    │ return "1.0.0"
    ▼
MCP Server
    │
    │ format response
    ▼
User (Copilot)
    │
    │ Display: "Version: 1.0.0"
```

### 2. AI Agent Query Flow

```
User (Python script)
    │
    │ "What can this ECU do?"
    ▼
AI Agent
    │
    │ get ECU context → build prompt
    ▼
OpenAI API
    │
    │ GPT-4 processing
    │
    │ return AI response
    ▼
AI Agent
    │
    │ format & return
    ▼
User
    │
    │ Display: "The ECU can perform addition,
    │           process data, and communicate
    │           via CAN, LIN, Ethernet..."
```

### 3. Addition Operation Flow

```
User
    │
    │ "Add 42 and 58"
    ▼
MCP Server / AI Agent
    │
    │ perform_addition(42, 58)
    ▼
Virtual ECU
    │
    │ add(42, 58)
    │
    │ Calculate: 42 + 58 = 100
    │
    │ return 100
    ▼
MCP Server / AI Agent
    │
    │ format result
    ▼
User
    │
    │ Display: "Result: 100"
```

## Component Details

### Virtual ECU (fmu_model.py)
- **Purpose**: Core ECU simulation
- **Type**: Python class
- **State**: Maintains ECU configuration and status
- **Operations**: Addition, info queries, status checks

### MCP Server (server.py)
- **Purpose**: Expose ECU via MCP protocol
- **Protocol**: JSON-RPC over stdio
- **Tools**: 6 queryable tools
- **Integration**: Works with Copilot, Claude, etc.

### AI Agent (ai_agent.py)
- **Purpose**: Natural language interface
- **Backend**: OpenAI GPT-3.5/GPT-4
- **Features**: Context-aware responses, action execution
- **Use Case**: Conversational ECU interaction

## File Structure

```
fmu-as-a-mcp-server/
├── fmu_model.py           # Domain Layer - ECU implementation
├── server.py              # Application Layer - MCP server
├── ai_agent.py            # Application Layer - AI integration
├── example_usage.py       # Examples - Direct usage
├── test_implementation.py # Testing - Validation
├── requirements.txt       # Dependencies
├── .env.example           # Configuration template
├── mcp-config.json        # MCP client configuration
├── quickstart.sh          # Quick setup script
├── README.md              # Main documentation
├── SETUP_GUIDE.md         # Detailed setup
├── COPILOT_USAGE.md       # Copilot examples
├── ARCHITECTURE.md        # This file
├── LICENSE                # MIT License
├── .vscode/               # VS Code configuration
│   ├── extensions.json    # Recommended extensions
│   └── settings.json      # Workspace settings
└── .gitignore            # Git ignore rules
```

## Technology Stack

### Core Technologies
- **Python 3.8+**: Programming language
- **MCP (Model Context Protocol)**: Server framework
- **OpenAI API**: AI capabilities
- **pydantic**: Data validation

### Development Tools
- **VS Code**: IDE
- **GitHub Copilot**: AI pair programming
- **Git**: Version control

### Communication Protocols
- **JSON-RPC**: MCP communication
- **stdio**: Standard input/output
- **REST**: OpenAI API calls

## Extension Points

### Adding New ECU Operations

1. **Update fmu_model.py**:
```python
def multiply(self, a: float, b: float) -> float:
    return a * b
```

2. **Add MCP Tool in server.py**:
```python
types.Tool(
    name="perform_multiplication",
    description="Multiply two numbers",
    inputSchema={...}
)
```

3. **Update AI Agent context** in ai_agent.py

### Supporting New Interfaces

1. Add to interfaces list in `VirtualECU.__init__()`
2. Document in README
3. Update tests

### Adding ECU Capabilities

1. Extend capabilities list
2. Implement new methods
3. Expose via MCP tools
4. Update documentation

## Security Considerations

- ✅ API keys stored in `.env` (not committed)
- ✅ Input validation via pydantic
- ✅ No direct system access from MCP
- ✅ Read-only operations (safe queries)

## Performance Characteristics

- **MCP Server**: Lightweight, stdio-based
- **ECU Operations**: O(1) for all current operations
- **AI Agent**: Network-dependent (OpenAI API)
- **Memory**: Minimal (~10MB for Python + dependencies)

---

**Design Philosophy**: Simple, extensible, well-documented
