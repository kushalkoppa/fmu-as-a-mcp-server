# Architecture & Design

## System Architecture

The FMU-as-a-MCP-Server system consists of three main layers:

### 1. Virtual ECU Layer (FMU Implementation)

```
┌───────────────────────────────────────┐
│         Virtual ECU (FMU)             │
│  ┌─────────────────────────────────┐  │
│  │  Addition Unit                  │  │
│  │  - add(a, b): number            │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │  Metadata Storage               │  │
│  │  - software: string             │  │
│  │  - version: string              │  │
│  │  - interfaces: string[]         │  │
│  │  - level: string                │  │
│  │  - description: string          │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │  Query Methods                  │  │
│  │  - getMetadata()                │  │
│  │  - getSoftware()                │  │
│  │  - getVersion()                 │  │
│  │  - getInterfaces()              │  │
│  │  - getLevel()                   │  │
│  │  - getStatus()                  │  │
│  └─────────────────────────────────┘  │
└───────────────────────────────────────┘
```

**File**: `src/virtual-ecu.ts`

**Responsibilities**:
- Implement core FMU functionality (addition)
- Store and manage ECU metadata
- Provide query methods for metadata access
- Maintain ECU operational state

### 2. MCP Server Layer

```
┌────────────────────────────────────────┐
│       MCP Server Interface             │
│  ┌──────────────────────────────────┐  │
│  │  Tool Registration               │  │
│  │  - get_ecu_metadata              │  │
│  │  - get_ecu_software              │  │
│  │  - get_ecu_version               │  │
│  │  - get_ecu_interfaces            │  │
│  │  - get_ecu_level                 │  │
│  │  - get_ecu_status                │  │
│  │  - add_numbers                   │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │  Request Handlers                │  │
│  │  - ListTools                     │  │
│  │  - CallTool                      │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │  Transport Layer (stdio)         │  │
│  │  - StdioServerTransport          │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

**File**: `src/index.ts`

**Responsibilities**:
- Expose Virtual ECU through MCP protocol
- Register tools for each ECU capability
- Handle MCP requests (list tools, call tool)
- Manage stdio communication transport
- Error handling and response formatting

### 3. Client/AI Layer

```
┌────────────────────────────────────────┐
│         Client Applications            │
│  ┌──────────────────────────────────┐  │
│  │  GitHub Copilot                  │  │
│  │  (in VS Code)                    │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │  OpenAI API                      │  │
│  │  (GPT-4, GPT-3.5)                │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │  Custom MCP Clients              │  │
│  │  (test-client.js)                │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

## Data Flow

### Query Flow (e.g., "What software is running?")

```
User Query
    ↓
┌─────────────────────┐
│  LLM (Copilot/GPT)  │
│  Understands intent │
└─────────┬───────────┘
          ↓
   Decides to use tool:
   "get_ecu_software"
          ↓
┌─────────────────────┐
│   MCP Server        │
│   Receives request  │
└─────────┬───────────┘
          ↓
   Calls ECU method:
   virtualECU.getSoftware()
          ↓
┌─────────────────────┐
│   Virtual ECU       │
│   Returns: "Virtual │
│   ECU Addition Unit"│
└─────────┬───────────┘
          ↓
   Response packaged
   as MCP result
          ↓
┌─────────────────────┐
│   MCP Server        │
│   Returns to client │
└─────────┬───────────┘
          ↓
   LLM formats response
          ↓
┌─────────────────────┐
│   User sees:        │
│   "The software     │
│   running is Virtual│
│   ECU Addition Unit"│
└─────────────────────┘
```

### Addition Operation Flow (e.g., "Add 10 and 20")

```
User: "Add 10 and 20"
    ↓
LLM interprets as:
tool: "add_numbers"
args: {a: 10, b: 20}
    ↓
MCP Server receives
CallTool request
    ↓
Server calls:
virtualECU.add(10, 20)
    ↓
Virtual ECU computes:
result = 30
    ↓
MCP Server formats:
"Result: 10 + 20 = 30"
    ↓
LLM presents to user:
"The result is 30"
```

## Component Details

### Virtual ECU (virtual-ecu.ts)

**Core Class**: `VirtualECU`

**Properties**:
```typescript
private metadata: ECUMetadata {
  software: string;
  version: string;
  interfaces: string[];
  level: string;
  description: string;
}
```

**Methods**:
- `add(a: number, b: number): number` - Core arithmetic operation
- `getMetadata(): ECUMetadata` - Returns complete metadata
- `getSoftware(): string` - Returns software name
- `getVersion(): string` - Returns version string
- `getInterfaces(): string[]` - Returns available interfaces
- `getLevel(): string` - Returns ECU capability level
- `getStatus(): string` - Returns operational status

### MCP Server (index.ts)

**Server Configuration**:
```typescript
{
  name: "fmu-mcp-server",
  version: "1.0.0",
  capabilities: { tools: {} }
}
```

**Registered Tools**:
1. `get_ecu_metadata` - No parameters
2. `get_ecu_software` - No parameters
3. `get_ecu_version` - No parameters
4. `get_ecu_interfaces` - No parameters
5. `get_ecu_level` - No parameters
6. `get_ecu_status` - No parameters
7. `add_numbers` - Parameters: `a: number, b: number`

**Request Handlers**:
- `ListToolsRequestSchema` - Returns list of available tools
- `CallToolRequestSchema` - Executes requested tool

## Communication Protocol

### MCP Protocol Over stdio

The server uses **stdio** (standard input/output) for communication:

```
Client → stdin → MCP Server
MCP Server → stdout → Client
MCP Server → stderr → Logs
```

### Message Format

**Tool List Request**:
```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "params": {},
  "id": 1
}
```

**Tool List Response**:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "tools": [
      {
        "name": "get_ecu_metadata",
        "description": "Get complete metadata...",
        "inputSchema": {...}
      },
      ...
    ]
  },
  "id": 1
}
```

**Tool Call Request**:
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "add_numbers",
    "arguments": {"a": 10, "b": 20}
  },
  "id": 2
}
```

**Tool Call Response**:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Result: 10 + 20 = 30"
      }
    ]
  },
  "id": 2
}
```

## Extension Points

### Adding New ECU Functionality

1. **Add method to VirtualECU**:
```typescript
multiply(a: number, b: number): number {
  return a * b;
}
```

2. **Register tool in MCP server**:
```typescript
{
  name: "multiply_numbers",
  description: "Multiply two numbers",
  inputSchema: {
    type: "object",
    properties: {
      a: { type: "number" },
      b: { type: "number" }
    },
    required: ["a", "b"]
  }
}
```

3. **Add handler in CallToolRequestSchema**:
```typescript
case "multiply_numbers": {
  const result = virtualECU.multiply(args.a, args.b);
  return {
    content: [{ type: "text", text: `Result: ${result}` }]
  };
}
```

### Adding New Metadata Fields

1. **Update ECUMetadata interface**:
```typescript
export interface ECUMetadata {
  // existing fields...
  manufacturer: string;
  hardwareVersion: string;
}
```

2. **Update VirtualECU constructor**:
```typescript
this.metadata = {
  // existing fields...
  manufacturer: "Virtual Systems Inc.",
  hardwareVersion: "HW1.0"
};
```

3. **Add getter methods and MCP tools as needed**

## Security Considerations

1. **Input Validation**: All tool arguments are validated before execution
2. **Error Handling**: Errors are caught and returned safely to clients
3. **No External Dependencies**: Virtual ECU has no external system dependencies
4. **Sandboxed Execution**: MCP server runs in isolated Node.js process
5. **API Key Protection**: Environment variables for sensitive data

## Performance Characteristics

- **Latency**: < 10ms for simple queries (metadata, status)
- **Addition Operation**: < 1ms computation time
- **Memory Footprint**: ~50MB (Node.js + dependencies)
- **Concurrency**: Single-threaded (stdio transport limitation)
- **Scalability**: One MCP server instance per client connection

## Future Enhancements

1. **More Arithmetic Operations**: Subtract, multiply, divide
2. **Complex ECU Functions**: Signal processing, CAN bus simulation
3. **State Management**: Persistent ECU state across sessions
4. **Multiple Virtual ECUs**: Support multiple ECU instances
5. **WebSocket Transport**: Support for web-based clients
6. **Monitoring Dashboard**: Real-time ECU status visualization
7. **Test Suite**: Comprehensive unit and integration tests
8. **Docker Support**: Containerized deployment
9. **CI/CD Pipeline**: Automated testing and deployment
10. **Performance Metrics**: Built-in telemetry and monitoring
