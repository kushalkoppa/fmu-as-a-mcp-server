# FMU as MCP Server - Complete Documentation

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Quick Start](#quick-start)
5. [Installation](#installation)
6. [Setup and Configuration](#setup-and-configuration)
7. [GitHub Copilot Integration](#github-copilot-integration)
8. [OpenAI API Integration](#openai-api-integration)
9. [Available MCP Tools](#available-mcp-tools)
10. [C Implementation Details](#c-implementation-details)
11. [Integrating MCP Server into Existing FMUs](#integrating-mcp-server-into-existing-fmus)
12. [Project Structure](#project-structure)
13. [Development Guide](#development-guide)
14. [Testing](#testing)
15. [Troubleshooting](#troubleshooting)
16. [Use Cases](#use-cases)
17. [Contributing](#contributing)
18. [License](#license)

---

## Overview

**FMU as MCP Server (FaaMs)** is a Functional Mock-up Unit (FMU) virtual ECU embedded with AI agent capabilities, acting as a Model Context Protocol (MCP) server. This enables users to query ECU information like software version, interfaces, and capabilities using Large Language Models (LLMs) such as GitHub Copilot or OpenAI.

### What is This Project?

This project demonstrates how to:
- Create a Virtual ECU with queryable capabilities
- Expose FMU functionality through MCP protocol
- Enable natural language queries to ECU systems
- Integrate existing FMUs with AI agents

### Key Concepts

- **FMU (Functional Mock-up Unit)**: A standardized interface for model exchange and co-simulation
- **Virtual ECU**: A software simulation of an Electronic Control Unit
- **MCP (Model Context Protocol)**: A protocol for enabling AI agents to interact with external tools
- **AI Agent Integration**: Using LLMs to query and control systems through natural language

---

## Features

- 🚗 **Virtual ECU Implementation**: Simulates an Electronic Control Unit with addition functionality
- 🤖 **AI Agent Integration**: MCP server enables LLM-based queries
- 📊 **Metadata Exposure**: Query SW version, interfaces, ECU level via natural language
- 🔌 **OpenAI Compatible**: Works with OpenAI API and GitHub Copilot
- 💻 **VS Code Integration**: First-class support for Visual Studio Code
- ⚙️ **C/C++ Source Available**: Includes native C implementation of core functions
- 🔧 **Extensible Architecture**: Easy to add new FMU capabilities
- 🌐 **MCP Protocol Standard**: Compatible with any MCP-compliant client

---

## Architecture

### System Architecture

The FMU-as-a-MCP-Server system consists of three main layers:

```
┌─────────────────────────────────────────┐
│         User (via LLM/Copilot)          │
└────────────────┬────────────────────────┘
                 │ Natural Language Query
                 ↓
┌─────────────────────────────────────────┐
│         MCP Server Interface            │
│  (Model Context Protocol)               │
│  - Tool Registration                    │
│  - Request Handling                     │
│  - Response Formatting                  │
└────────────────┬────────────────────────┘
                 │ Tool Calls
                 ↓
┌─────────────────────────────────────────┐
│         Virtual ECU (FMU)               │
│  ┌───────────────────────────────────┐  │
│  │  Addition Unit (C/TypeScript)     │  │
│  │  - add(a, b): number              │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │  Metadata Storage                 │  │
│  │  - software: string               │  │
│  │  - version: string                │  │
│  │  - interfaces: string[]           │  │
│  │  - level: string                  │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │  Status & Query Methods           │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Component Details

#### 1. Virtual ECU Layer (`src/virtual-ecu.ts`)

**Responsibilities**:
- Implement core FMU functionality (addition operations)
- Store and manage ECU metadata
- Provide query methods for metadata access
- Maintain ECU operational state

**Key Methods**:
- `add(a, b)`: Perform addition operation
- `getMetadata()`: Return complete ECU metadata
- `getSoftware()`, `getVersion()`, `getInterfaces()`, `getLevel()`: Query specific metadata
- `getStatus()`: Get operational status

#### 2. MCP Server Layer (`src/index.ts`)

**Responsibilities**:
- Register MCP tools with descriptions
- Handle incoming MCP requests
- Route requests to Virtual ECU
- Format responses according to MCP protocol
- Handle errors gracefully

**Tool Registration**:
- Each ECU function is exposed as an MCP tool
- Tools have clear descriptions for LLM understanding
- Input schemas define required parameters
- Standard MCP response format

#### 3. AI Agent Layer

**Capabilities**:
- Natural language query interpretation
- Tool selection based on user intent
- Parameter extraction from natural language
- Response formatting for human readability

---

## Quick Start

Get up and running in 5 minutes:

```bash
# 1. Clone the repository
git clone https://github.com/kushalkoppa/fmu-as-a-mcp-server.git
cd fmu-as-a-mcp-server

# 2. Install dependencies
npm install

# 3. Build the project
npm run build

# 4. Run the server
npm start
```

### Quick Test

Test with the example client:

```bash
cd examples
node test-client.js
```

You should see:
- Connected to FMU MCP Server
- List of available tools
- Test results for all ECU functions
- Addition operation results

---

## Installation

### Prerequisites

#### Required Software

1. **Node.js v18 or higher**
   ```bash
   node --version  # Should be v18+
   ```
   Download from: https://nodejs.org/

2. **npm (Node Package Manager)**
   - Comes with Node.js
   ```bash
   npm --version
   ```

3. **Git**
   ```bash
   git --version
   ```
   Download from: https://git-scm.com/

4. **Visual Studio Code** (recommended)
   - Download from: https://code.visualstudio.com/
   - Version 1.75 or higher

#### Optional Software

1. **GCC Compiler** (for C source compilation)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install gcc
   
   # macOS (Xcode Command Line Tools)
   xcode-select --install
   
   # Windows (MinGW or MSYS2)
   # Download from: https://www.mingw-w64.org/
   ```

2. **GitHub Copilot License**
   - Sign up at: https://github.com/features/copilot
   - Available for individuals, students, and enterprise

3. **OpenAI API Account** (optional)
   - Create account at: https://platform.openai.com/
   - Get API key from: https://platform.openai.com/api-keys

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/kushalkoppa/fmu-as-a-mcp-server.git
   cd fmu-as-a-mcp-server
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Build the Project**
   ```bash
   npm run build
   ```
   
   This compiles TypeScript to JavaScript in the `dist/` directory.

4. **Verify Installation**
   ```bash
   # Check that build output exists
   ls dist/index.js
   
   # Run tests
   npm test
   ```

---

## Setup and Configuration

### Visual Studio Code Setup

#### Step 1: Open the Project

1. Launch Visual Studio Code
2. Open the project folder: `File > Open Folder...`
3. Select the `fmu-as-a-mcp-server` directory

#### Step 2: Install Required Extensions

1. Open Extensions (`Ctrl+Shift+X` or `Cmd+Shift+X`)
2. Install:
   - **GitHub Copilot**
   - **GitHub Copilot Chat**

#### Step 3: Configure MCP Settings

**Option A: VS Code Settings**

1. Open Settings: `File > Preferences > Settings` (`Ctrl+,`)
2. Search for "MCP" or "Model Context Protocol"
3. Click "Edit in settings.json"
4. Add:

```json
{
  "mcp.servers": {
    "fmu-virtual-ecu": {
      "command": "node",
      "args": ["${workspaceFolder}/dist/index.js"],
      "env": {
        "NODE_ENV": "production"
      }
    }
  }
}
```

**Option B: Claude Desktop Configuration**

For Claude Desktop app:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "fmu-virtual-ecu": {
      "command": "node",
      "args": ["/absolute/path/to/fmu-as-a-mcp-server/dist/index.js"]
    }
  }
}
```

#### Step 4: Set Up OpenAI API Key (Optional)

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=sk-your-api-key-here
```

Or set as environment variable:

```bash
# Linux/macOS
export OPENAI_API_KEY="sk-your-api-key-here"

# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-your-api-key-here"
```

#### Step 5: Restart VS Code

After configuration, restart VS Code to load the MCP server.

---

## GitHub Copilot Integration

### Running the MCP Server

**Option 1: Direct Execution**
```bash
npm run dev
```

**Option 2: Using VS Code Debugger**
1. Press `F5` or go to `Run > Start Debugging`
2. Select "Launch FMU MCP Server"
3. The server will start and listen for MCP connections

**Option 3: As a Background Service**
```bash
npm start
```

### Example Queries with Copilot

Once the MCP server is running and configured in VS Code, you can ask Copilot natural language questions:

#### Query ECU Software
```
@workspace What software is running on the Virtual ECU?
```
**Expected Response**: "Virtual ECU Addition Unit"

#### Query ECU Version
```
@workspace What version is the Virtual ECU FMU?
```
**Expected Response**: "1.0.0"

#### Query Available Interfaces
```
@workspace What interfaces does the Virtual ECU provide?
```
**Expected Response**: `["addition", "metadata", "status"]`

#### Query ECU Level
```
@workspace What is the level of the Virtual ECU?
```
**Expected Response**: "L2 - Basic Arithmetic Functions"

#### Use the Addition Function
```
@workspace Can you add 15 and 27 using the Virtual ECU?
```
**Expected Response**: "Result: 15 + 27 = 42"

#### Get Complete Metadata
```
@workspace Show me all the metadata for the Virtual ECU
```
**Expected Response**: Complete JSON metadata object including domain information

#### Query ECU Domain
```
@workspace What domain is the Virtual ECU for?
```
**Expected Response**: "Automotive - Basic Arithmetic Control Unit"

#### List All Functions
```
@workspace What functions are available in the Virtual ECU?
```
**Expected Response**: Detailed list of all functions with descriptions, parameters, and return types

```
@workspace List all the functions in the FMU
```
**Expected Response**: JSON array of ECUFunction objects

### Advanced Queries

```
@workspace What capabilities does the Virtual ECU have?
@workspace Demonstrate the addition functionality with numbers 100 and 250
@workspace Is the Virtual ECU operational?
@workspace List all available functions in the Virtual ECU
@workspace What is the domain of this ECU?
@workspace Show me the function signatures for all ECU operations
```

---

## OpenAI API Integration

### Setup

1. **Get OpenAI API Key**
   - Visit [OpenAI Platform](https://platform.openai.com/)
   - Sign up or log in
   - Navigate to API Keys section
   - Create and copy your API key

2. **Set Environment Variable**
   ```bash
   export OPENAI_API_KEY="sk-your-api-key-here"
   ```

3. **Install OpenAI SDK** (if building custom client)
   ```bash
   npm install openai
   ```

### Example: Direct API Integration

```javascript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

// Define MCP tools for OpenAI function calling
const tools = [
  {
    type: "function",
    function: {
      name: "get_ecu_metadata",
      description: "Get complete metadata about the Virtual ECU FMU",
      parameters: {
        type: "object",
        properties: {},
        required: []
      }
    }
  },
  {
    type: "function",
    function: {
      name: "add_numbers",
      description: "Perform addition using the Virtual ECU",
      parameters: {
        type: "object",
        properties: {
          a: { type: "number", description: "First number" },
          b: { type: "number", description: "Second number" }
        },
        required: ["a", "b"]
      }
    }
  },
  {
    type: "function",
    function: {
      name: "get_ecu_software",
      description: "Get the software name of the Virtual ECU",
      parameters: { type: "object", properties: {}, required: [] }
    }
  },
  {
    type: "function",
    function: {
      name: "get_ecu_version",
      description: "Get the version of the Virtual ECU",
      parameters: { type: "object", properties: {}, required: [] }
    }
  }
];

async function queryVirtualECU(userQuery) {
  const messages = [
    {
      role: "system",
      content: "You are an assistant that helps users interact with a Virtual ECU FMU through MCP tools."
    },
    {
      role: "user",
      content: userQuery
    }
  ];

  const response = await openai.chat.completions.create({
    model: "gpt-4",
    messages: messages,
    tools: tools,
    tool_choice: "auto"
  });

  return response.choices[0].message;
}

// Example usage
async function main() {
  const result = await queryVirtualECU("What software is running on the ECU?");
  console.log(result);
  
  const addResult = await queryVirtualECU("Add 25 and 17");
  console.log(addResult);
}

main();
```

### Handling Tool Calls

```javascript
async function handleToolCall(toolCall) {
  const { name, arguments: args } = toolCall.function;
  
  // In a real implementation, this would call the MCP server
  // For this example, we simulate the responses
  
  switch(name) {
    case "get_ecu_metadata":
      return {
        software: "Virtual ECU Addition Unit",
        version: "1.0.0",
        interfaces: ["addition", "metadata", "status"],
        level: "L2 - Basic Arithmetic Functions"
      };
    
    case "add_numbers":
      const a = JSON.parse(args).a;
      const b = JSON.parse(args).b;
      return { result: a + b };
    
    case "get_ecu_software":
      return "Virtual ECU Addition Unit";
    
    case "get_ecu_version":
      return "1.0.0";
    
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
}
```

---

## Available MCP Tools

The FMU MCP server exposes the following tools:

| Tool Name | Description | Parameters | Return Type |
|-----------|-------------|------------|-------------|
| `get_ecu_metadata` | Get complete metadata (SW, version, interfaces, level, domain) | None | JSON Object |
| `get_ecu_software` | Get the software name | None | String |
| `get_ecu_version` | Get the version number | None | String |
| `get_ecu_interfaces` | Get available interfaces list | None | Array<String> |
| `get_ecu_level` | Get the ECU capability level | None | String |
| `get_ecu_status` | Get current operational status | None | String |
| `get_ecu_domain` | Get the domain/application area of the ECU | None | String |
| `list_ecu_functions` | List all available functions with descriptions and signatures | None | Array<ECUFunction> |
| `add_numbers` | Perform addition operation (a + b) | a: number, b: number | Number |

### Tool Usage Examples

#### Get Complete Metadata

**MCP Tool Call**:
```json
{
  "name": "get_ecu_metadata",
  "arguments": {}
}
```

**Response**:
```json
{
  "software": "Virtual ECU Addition Unit",
  "version": "1.0.0",
  "interfaces": ["addition", "metadata", "status"],
  "level": "L2 - Basic Arithmetic Functions",
  "description": "A virtual ECU FMU that provides basic addition functionality and queryable metadata",
  "domain": "Automotive - Basic Arithmetic Control Unit"
}
```

#### 2. List All Functions

**MCP Tool Call**:
```json
{
  "name": "list_ecu_functions",
  "arguments": {}
}
```

**Response**:
```json
[
  {
    "name": "add",
    "description": "Perform addition operation on two numbers",
    "parameters": [
      {
        "name": "a",
        "type": "number",
        "description": "First number to add"
      },
      {
        "name": "b",
        "type": "number",
        "description": "Second number to add"
      }
    ],
    "returnType": "number"
  },
  {
    "name": "getMetadata",
    "description": "Get complete metadata about the Virtual ECU",
    "parameters": [],
    "returnType": "ECUMetadata"
  }
  // ... more functions
]
```

#### 3. Get ECU Domain

**MCP Tool Call**:
```json
{
  "name": "get_ecu_domain",
  "arguments": {}
}
```

**Response**:
```
Automotive - Basic Arithmetic Control Unit
```

#### 4. Add Numbers

**MCP Tool Call**:
```json
{
  "name": "add_numbers",
  "arguments": {
    "a": 25,
    "b": 17
  }
}
```

**Response**:
```
Result: 25 + 17 = 42
```

---

## C Implementation Details

The project includes C source and header files for the core addition function, demonstrating how to integrate native C code with the FMU MCP server.

### Files

- **src/addition.h**: Header file with function declaration
- **src/addition.c**: Implementation file with function definition

### addition.h

```c
/**
 * addition.h - Header file for addition function
 * 
 * This header file declares the addition function used in the Virtual ECU FMU.
 */

#ifndef ADDITION_H
#define ADDITION_H

/**
 * Add two numbers
 * 
 * @param a First number to add
 * @param b Second number to add
 * @return The sum of a and b
 */
double add(double a, double b);

#endif // ADDITION_H
```

### addition.c

```c
/**
 * addition.c - Implementation of addition function
 * 
 * This file implements the addition function for the Virtual ECU FMU.
 */

#include "addition.h"

/**
 * Add two numbers
 * 
 * @param a First number to add
 * @param b Second number to add
 * @return The sum of a and b
 */
double add(double a, double b) {
    return a + b;
}
```

### Compiling the C Code

```bash
# Navigate to src directory
cd src

# Compile to object file
gcc -c addition.c -o addition.o

# Create shared library (optional)
gcc -shared -o libadd.so addition.c

# Compile with debugging symbols
gcc -g -c addition.c -o addition.o
```

### Integrating C Code with Node.js

To use the C code in Node.js, you can use Node.js native addons or FFI (Foreign Function Interface):

#### Option 1: Using node-ffi-napi

```bash
npm install ffi-napi ref-napi
```

```javascript
import ffi from 'ffi-napi';
import path from 'path';

// Load the shared library
const lib = ffi.Library(path.join(__dirname, 'libadd.so'), {
  'add': ['double', ['double', 'double']]
});

// Use the C function
const result = lib.add(25.5, 17.3);
console.log(`Result: ${result}`); // 42.8
```

#### Option 2: Using N-API (Node.js Native Addon)

Create a binding file that wraps the C function for Node.js (more complex but better performance).

---

## Integrating MCP Server into Existing FMUs

This section explains how to add MCP server capabilities to an existing FMU, enabling AI agent integration.

### Overview

There are two main approaches to add MCP server capabilities to existing FMUs:

**Approach 1: Repackaging (Recommended for Vendor FMUs)**
- Use the automated FMU repackaging tool
- Preserves original FMU binaries and structure
- Adds MCP wrapper as resource files
- Compatible with FMPy and other FMI tools
- Best for FMUs from Synopsys, Vector, dSPACE, ETAS, etc.

**Approach 2: Creating a Custom Wrapper**
- Build a new MCP server that wraps your FMU
- Requires programming the FMI interface
- Offers more customization options
- Best for programmatic control and custom integration

---

## Approach 1: Repackaging Existing FMUs (Automated)

### Introduction

The FMU Repackaging Tool automatically adds MCP Server capabilities to existing FMUs created by industry-standard tools like:
- **Synopsys** - Platform Architect
- **Vector** - CANoe, PREEvision
- **dSPACE** - TargetLink, SystemDesk
- **ETAS** - ASCET, COSYM
- Other FMI 2.0/3.0 compliant tools

### Key Features

✅ **Non-invasive**: Preserves original FMU binaries and functionality  
✅ **FMPy Compatible**: Repackaged FMUs work with FMPy for simulation  
✅ **MCP Enhanced**: Adds AI agent query capabilities  
✅ **Standards Compliant**: Maintains FMI 2.0/3.0 compatibility  
✅ **Automated**: Simple command-line tool, no manual editing  

### Installation

The repackaging tool is included in this repository. Ensure you have Python 3.9+ installed:

```bash
# Install required Python packages
pip install fmpy lxml

# The tool is ready to use
python fmu_repackager.py --help
```

### Quick Start Guide

#### Step 1: Create a Sample FMU (for testing)

```bash
# Create a sample vendor FMU for testing
python fmu_repackager.py --create-sample my_vendor.fmu
```

This creates a sample FMU that simulates an ECU from vendor tools.

#### Step 2: Repackage Your FMU

```bash
# Repackage an existing FMU with MCP capabilities
python fmu_repackager.py --input my_vendor.fmu --output my_vendor_mcp.fmu
```

The tool will:
1. Extract the existing FMU structure
2. Parse `modelDescription.xml`
3. Add MCP server variables
4. Inject MCP wrapper scripts
5. Repackage as a new FMU

Output:
```
===========================================================
FMU MCP Server Repackaging Tool
===========================================================
[1/6] Extracting FMU: my_vendor.fmu
  ✓ Extracted to: /tmp/fmu_repackage_xyz
[2/6] Parsing modelDescription.xml
  ✓ FMI Version: 2.0
  ✓ Model Name: VendorECU_Controller
  ✓ GUID: {12345678-1234-1234-1234-123456789abc}
[3/6] Adding MCP Server variables
  ✓ Added MCP status variable (valueReference: 3)
  ✓ Added MCP version variable (valueReference: 4)
[4/6] Adding MCP Server wrapper
  ✓ Created MCP config: mcp_config.json
  ✓ Created MCP wrapper: mcp_wrapper.py
  ✓ Created MCP README: MCP_README.txt
[5/6] Updating modelDescription.xml
  ✓ Updated modelDescription.xml
[6/6] Repackaging FMU: my_vendor_mcp.fmu
  ✓ Created repackaged FMU: my_vendor_mcp.fmu
  ✓ Size: 3.45 KB
===========================================================
✓ Repackaging completed successfully!
===========================================================
Input FMU:  my_vendor.fmu
Output FMU: my_vendor_mcp.fmu

The repackaged FMU can now be loaded in FMPy:
  from fmpy import simulate_fmu
  simulate_fmu('my_vendor_mcp.fmu')
```

#### Step 3: Load in FMPy

```python
from fmpy import read_model_description, simulate_fmu

# Read the repackaged FMU
model_desc = read_model_description('my_vendor_mcp.fmu')
print(f"Model: {model_desc.modelName}")
print(f"FMI Version: {model_desc.fmiVersion}")

# List all variables (including MCP variables)
for var in model_desc.modelVariables:
    print(f"  - {var.name}: {var.type}")

# Simulate the FMU
result = simulate_fmu('my_vendor_mcp.fmu')
```

### What Gets Added to Your FMU

When you repackage an FMU, the following components are added:

#### 1. MCP Server Variables (in modelDescription.xml)

```xml
<ScalarVariable 
    name="mcp_server_status" 
    valueReference="N+1"
    description="MCP Server operational status"
    causality="output" 
    variability="discrete">
    <String start="active"/>
</ScalarVariable>

<ScalarVariable 
    name="mcp_server_version" 
    valueReference="N+2"
    description="MCP Server version"
    causality="parameter" 
    variability="fixed">
    <String start="1.0.0"/>
</ScalarVariable>
```

#### 2. MCP Configuration (resources/mcp_config.json)

```json
{
  "enabled": true,
  "version": "1.0.0",
  "server_name": "fmu-mcp-wrapper",
  "capabilities": {
    "tools": true,
    "resources": false,
    "prompts": false
  },
  "original_fmu": "my_vendor.fmu",
  "repackaged_timestamp": "2024-01-15T10:30:00Z"
}
```

#### 3. MCP Wrapper Script (resources/mcp_wrapper.py)

A Python script that provides MCP server functionality for querying the FMU.

#### 4. Documentation (resources/MCP_README.txt)

Instructions on how to use the MCP-enhanced FMU.

### Advanced Usage

#### Custom MCP Configuration

Create a custom configuration file:

```json
{
  "server_name": "custom-ecu-server",
  "description": "Custom ECU with MCP capabilities",
  "tools": {
    "custom_tool_1": {
      "enabled": true,
      "description": "Custom functionality"
    }
  }
}
```

Apply it during repackaging:

```bash
python fmu_repackager.py \
    --input my_vendor.fmu \
    --output my_vendor_mcp.fmu \
    --mcp-config custom_mcp_config.json
```

#### Batch Repackaging

Repackage multiple FMUs:

```bash
#!/bin/bash
# batch_repackage.sh

for fmu in vendor_fmus/*.fmu; do
    basename=$(basename "$fmu" .fmu)
    echo "Repackaging $basename..."
    python fmu_repackager.py \
        --input "$fmu" \
        --output "repackaged/${basename}_mcp.fmu"
done
```

### Vendor-Specific Considerations

#### Synopsys Platform Architect

- Export FMUs using FMI 2.0 for Co-Simulation
- Ensure all required binaries are included
- Test MCP integration with Platform Architect models

```bash
# Typical Synopsys FMU structure
synopsys_model.fmu
├── modelDescription.xml
├── binaries/
│   ├── linux64/libmodel.so
│   └── win64/model.dll
└── resources/
    └── model_data.xml

# After repackaging
synopsys_model_mcp.fmu
├── modelDescription.xml (MCP-enhanced)
├── binaries/ (unchanged)
├── resources/
│   ├── model_data.xml (original)
│   ├── mcp_config.json (new)
│   ├── mcp_wrapper.py (new)
│   └── MCP_README.txt (new)
```

#### Vector CANoe/PREEvision

- Export RT models as FMUs
- MCP integration works with CAN/LIN signals
- Repackaged FMUs maintain Vector's signal database

```python
# Example: Query Vector CAN signals via MCP
from fmpy import read_model_description

model = read_model_description('vector_ecu_mcp.fmu')

# Find CAN signals (now queryable via MCP)
can_signals = [v for v in model.modelVariables 
               if 'CAN' in v.description]
print(f"Found {len(can_signals)} CAN signals")
```

#### dSPACE TargetLink/SystemDesk

- Export production code models
- MCP enables querying of model structure
- Compatible with dSPACE real-time systems

```bash
# Repackage dSPACE FMU
python fmu_repackager.py \
    --input dspace_controller.fmu \
    --output dspace_controller_mcp.fmu
```

#### ETAS ASCET/COSYM

- ETAS ASCET models export to FMI 2.0
- MCP integration for component queries
- Maintains ETAS calibration parameters

### Verification and Testing

#### 1. Verify FMU Structure

```bash
# Check the repackaged FMU structure
unzip -l my_vendor_mcp.fmu

# Should show:
# - modelDescription.xml
# - binaries/...
# - resources/mcp_config.json
# - resources/mcp_wrapper.py
# - resources/MCP_README.txt
```

#### 2. Validate with FMPy

```python
from fmpy import read_model_description
from fmpy.validation import validate_fmu

# Validate FMU structure
problems = validate_fmu('my_vendor_mcp.fmu')
if not problems:
    print("✓ FMU is valid")
else:
    for problem in problems:
        print(f"⚠ {problem}")

# Read model description
model = read_model_description('my_vendor_mcp.fmu')
print(f"✓ Model: {model.modelName}")
print(f"✓ Variables: {len(model.modelVariables)}")

# Check for MCP variables
mcp_vars = [v.name for v in model.modelVariables 
            if 'mcp' in v.name.lower()]
print(f"✓ MCP variables: {mcp_vars}")
```

#### 3. Test MCP Functionality

```python
# Test MCP wrapper directly
import sys
import json
sys.path.insert(0, './extracted_fmu/resources')

from mcp_wrapper import MCPWrapper

wrapper = MCPWrapper('./extracted_fmu/resources/mcp_config.json')
status = wrapper.get_status()
print(json.dumps(status, indent=2))

tools = wrapper.list_tools()
print(f"Available MCP tools: {len(tools)}")
```

### Troubleshooting

#### Issue: FMU extraction fails

**Solution**: Ensure the input file is a valid ZIP-based FMU:
```bash
file my_vendor.fmu
# Should output: Zip archive data
```

#### Issue: Missing modelDescription.xml

**Solution**: The input FMU must contain a valid modelDescription.xml at the root level.

#### Issue: FMPy cannot load repackaged FMU

**Solution**: Check that original FMU binaries are present:
```bash
unzip -l my_vendor_mcp.fmu | grep binaries
```

#### Issue: MCP variables not found

**Solution**: Verify the modelDescription.xml was updated:
```bash
unzip -p my_vendor_mcp.fmu modelDescription.xml | grep mcp_server
```

### CI/CD Integration

The repackaging tool is integrated into the CI/CD pipeline for automated testing:

```yaml
# .github/workflows/ci.yml
fmu-repackaging-test:
  runs-on: ubuntu-latest
  steps:
    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: pip install fmpy lxml
    
    - name: Create sample FMU
      run: python fmu_repackager.py --create-sample test.fmu
    
    - name: Repackage FMU
      run: python fmu_repackager.py --input test.fmu --output test_mcp.fmu
    
    - name: Validate repackaged FMU
      run: |
        python -c "from fmpy.validation import validate_fmu; \
                   problems = validate_fmu('test_mcp.fmu'); \
                   exit(1 if problems else 0)"
```

---

## Approach 2: Creating a Custom MCP Wrapper

For developers who want more control, you can create a custom MCP server wrapper around your FMU.

### Overview

Adding MCP server to an existing FMU via custom wrapper involves:
1. Creating an MCP server wrapper
2. Mapping FMU functions to MCP tools
3. Handling FMU-specific data types and protocols
4. Setting up communication between MCP and FMU

### Integration Architecture

```
┌─────────────────────────────────────────┐
│         AI Agent / LLM Client           │
└────────────────┬────────────────────────┘
                 │ MCP Protocol
                 ↓
┌─────────────────────────────────────────┐
│         MCP Server Wrapper              │
│  - Tool Registration                    │
│  - Type Conversion                      │
│  - Error Handling                       │
└────────────────┬────────────────────────┘
                 │ Adapter Layer
                 ↓
┌─────────────────────────────────────────┐
│         Your Existing FMU               │
│  - FMI Interface                        │
│  - Model Variables                      │
│  - Simulation Functions                 │
└─────────────────────────────────────────┘
```

### Step-by-Step Integration Guide

#### Step 1: Analyze Your Existing FMU

First, identify what capabilities your FMU provides:

```bash
# For FMI 2.0/3.0 FMUs, extract modelDescription.xml
unzip your-fmu.fmu modelDescription.xml

# Review the model description
cat modelDescription.xml
```

Key information to extract:
- **Model Variables**: Input/output parameters
- **Functions**: Available simulation functions
- **Metadata**: Name, version, GUID, capabilities

#### Step 2: Create MCP Server Wrapper

Create a new Node.js project that wraps your FMU:

```bash
mkdir fmu-mcp-wrapper
cd fmu-mcp-wrapper
npm init -y
npm install @modelcontextprotocol/sdk
npm install --save-dev typescript @types/node
```

#### Step 3: Set Up TypeScript Configuration

**tsconfig.json**:
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

#### Step 4: Create FMU Adapter Class

**src/fmu-adapter.ts**:

```typescript
/**
 * FMU Adapter - Wraps existing FMU functionality
 * 
 * This adapter provides a clean interface to your existing FMU,
 * handling FMI protocol communication and data conversion.
 */

import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export interface FMUMetadata {
  name: string;
  version: string;
  guid: string;
  description: string;
  author: string;
  fmiVersion: string;
}

export interface FMUVariable {
  name: string;
  valueReference: number;
  type: 'Real' | 'Integer' | 'Boolean' | 'String';
  causality: 'input' | 'output' | 'parameter';
  variability: 'constant' | 'fixed' | 'tunable' | 'discrete' | 'continuous';
  description?: string;
}

export class FMUAdapter {
  private fmuPath: string;
  private metadata: FMUMetadata | null = null;
  private variables: Map<string, FMUVariable> = new Map();

  constructor(fmuPath: string) {
    this.fmuPath = fmuPath;
  }

  /**
   * Initialize the FMU adapter by reading modelDescription.xml
   */
  async initialize(): Promise<void> {
    // Extract and parse modelDescription.xml from FMU
    await this.loadMetadata();
    await this.loadVariables();
  }

  /**
   * Load FMU metadata from modelDescription.xml
   */
  private async loadMetadata(): Promise<void> {
    // Implementation depends on your FMU format
    // This is a simplified example
    this.metadata = {
      name: "Existing FMU Model",
      version: "1.0.0",
      guid: "unique-guid-here",
      description: "Your existing FMU description",
      author: "Your Name",
      fmiVersion: "2.0"
    };
  }

  /**
   * Load FMU variables from modelDescription.xml
   */
  private async loadVariables(): Promise<void> {
    // Parse modelDescription.xml and extract ScalarVariable elements
    // This is a simplified example
    const variable: FMUVariable = {
      name: "input1",
      valueReference: 0,
      type: "Real",
      causality: "input",
      variability: "continuous",
      description: "First input parameter"
    };
    this.variables.set(variable.name, variable);
  }

  /**
   * Get FMU metadata
   */
  getMetadata(): FMUMetadata {
    if (!this.metadata) {
      throw new Error("FMU not initialized. Call initialize() first.");
    }
    return { ...this.metadata };
  }

  /**
   * Get all FMU variables
   */
  getVariables(): FMUVariable[] {
    return Array.from(this.variables.values());
  }

  /**
   * Get a specific variable by name
   */
  getVariable(name: string): FMUVariable | undefined {
    return this.variables.get(name);
  }

  /**
   * Set FMU input variable
   */
  async setVariable(name: string, value: number | boolean | string): Promise<void> {
    const variable = this.variables.get(name);
    if (!variable) {
      throw new Error(`Variable ${name} not found`);
    }
    
    // Call your FMU's fmi2SetXXX function
    // Implementation depends on your FMU interface
    console.log(`Setting ${name} = ${value}`);
  }

  /**
   * Get FMU output variable
   */
  async getVariableValue(name: string): Promise<number | boolean | string> {
    const variable = this.variables.get(name);
    if (!variable) {
      throw new Error(`Variable ${name} not found`);
    }
    
    // Call your FMU's fmi2GetXXX function
    // Implementation depends on your FMU interface
    return 0; // Placeholder
  }

  /**
   * Execute FMU simulation step
   */
  async doStep(stepSize: number): Promise<void> {
    // Call fmi2DoStep or equivalent
    console.log(`Executing step with size ${stepSize}`);
  }

  /**
   * Custom function: Example of calling FMU-specific functionality
   */
  async calculateSum(a: number, b: number): Promise<number> {
    // Set input variables
    await this.setVariable("input1", a);
    await this.setVariable("input2", b);
    
    // Execute simulation step
    await this.doStep(0.01);
    
    // Get output variable
    const result = await this.getVariableValue("output");
    return result as number;
  }
}
```

#### Step 5: Create MCP Server with FMU Integration

**src/index.ts**:

```typescript
#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";
import { FMUAdapter } from "./fmu-adapter.js";
import path from "path";

// Initialize FMU Adapter
const fmuPath = process.env.FMU_PATH || "./your-fmu.fmu";
const fmuAdapter = new FMUAdapter(fmuPath);

// Initialize FMU
await fmuAdapter.initialize();

// Create MCP server
const server = new Server(
  {
    name: "existing-fmu-mcp-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define MCP tools based on FMU capabilities
const tools: Tool[] = [
  {
    name: "get_fmu_metadata",
    description: "Get metadata about the FMU including name, version, and description",
    inputSchema: {
      type: "object",
      properties: {},
      required: [],
    },
  },
  {
    name: "list_fmu_variables",
    description: "List all variables (inputs/outputs) available in the FMU",
    inputSchema: {
      type: "object",
      properties: {},
      required: [],
    },
  },
  {
    name: "get_variable_value",
    description: "Get the current value of an FMU variable",
    inputSchema: {
      type: "object",
      properties: {
        name: {
          type: "string",
          description: "Name of the variable",
        },
      },
      required: ["name"],
    },
  },
  {
    name: "set_variable_value",
    description: "Set the value of an FMU input variable",
    inputSchema: {
      type: "object",
      properties: {
        name: {
          type: "string",
          description: "Name of the variable",
        },
        value: {
          type: ["number", "boolean", "string"],
          description: "Value to set",
        },
      },
      required: ["name", "value"],
    },
  },
  {
    name: "calculate_sum",
    description: "Calculate sum using FMU (example custom function)",
    inputSchema: {
      type: "object",
      properties: {
        a: { type: "number", description: "First number" },
        b: { type: "number", description: "Second number" },
      },
      required: ["a", "b"],
    },
  },
];

// Handle list tools request
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools };
});

// Handle tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "get_fmu_metadata": {
        const metadata = fmuAdapter.getMetadata();
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(metadata, null, 2),
            },
          ],
        };
      }

      case "list_fmu_variables": {
        const variables = fmuAdapter.getVariables();
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(variables, null, 2),
            },
          ],
        };
      }

      case "get_variable_value": {
        if (!args || typeof args.name !== "string") {
          throw new Error("Variable name is required");
        }
        const value = await fmuAdapter.getVariableValue(args.name);
        return {
          content: [
            {
              type: "text",
              text: `${args.name} = ${value}`,
            },
          ],
        };
      }

      case "set_variable_value": {
        if (!args || typeof args.name !== "string") {
          throw new Error("Variable name is required");
        }
        await fmuAdapter.setVariable(args.name, args.value);
        return {
          content: [
            {
              type: "text",
              text: `Set ${args.name} = ${args.value}`,
            },
          ],
        };
      }

      case "calculate_sum": {
        if (!args || typeof args.a !== "number" || typeof args.b !== "number") {
          throw new Error("Both 'a' and 'b' must be numbers");
        }
        const result = await fmuAdapter.calculateSum(args.a, args.b);
        return {
          content: [
            {
              type: "text",
              text: `Result: ${args.a} + ${args.b} = ${result}`,
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    return {
      content: [
        {
          type: "text",
          text: `Error: ${errorMessage}`,
        },
      ],
      isError: true,
    };
  }
});

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("FMU MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error in main():", error);
  process.exit(1);
});
```

#### Step 6: Update Package Configuration

**package.json**:
```json
{
  "name": "existing-fmu-mcp-wrapper",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsc && node dist/index.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.25.2"
  },
  "devDependencies": {
    "@types/node": "^20.10.0",
    "typescript": "^5.3.0"
  }
}
```

### Integration Examples

#### Example 1: Automotive ECU FMU

```typescript
// Automotive ECU with engine control
export class EngineECUAdapter extends FMUAdapter {
  async getEngineRPM(): Promise<number> {
    return await this.getVariableValue("engine_rpm") as number;
  }

  async setThrottlePosition(position: number): Promise<void> {
    await this.setVariable("throttle_position", position);
  }

  async calculateFuelInjection(rpm: number, load: number): Promise<number> {
    await this.setVariable("engine_rpm", rpm);
    await this.setVariable("engine_load", load);
    await this.doStep(0.01);
    return await this.getVariableValue("fuel_injection") as number;
  }
}

// MCP tools for engine ECU
const engineTools: Tool[] = [
  {
    name: "get_engine_rpm",
    description: "Get current engine RPM",
    inputSchema: { type: "object", properties: {}, required: [] }
  },
  {
    name: "set_throttle",
    description: "Set throttle position (0-100%)",
    inputSchema: {
      type: "object",
      properties: {
        position: { type: "number", minimum: 0, maximum: 100 }
      },
      required: ["position"]
    }
  },
  {
    name: "calculate_fuel_injection",
    description: "Calculate required fuel injection based on RPM and load",
    inputSchema: {
      type: "object",
      properties: {
        rpm: { type: "number" },
        load: { type: "number" }
      },
      required: ["rpm", "load"]
    }
  }
];
```

#### Example 2: Industrial Control FMU

```typescript
// Industrial temperature controller
export class TemperatureControllerAdapter extends FMUAdapter {
  async getCurrentTemperature(): Promise<number> {
    return await this.getVariableValue("current_temperature") as number;
  }

  async setTargetTemperature(target: number): Promise<void> {
    await this.setVariable("target_temperature", target);
  }

  async getPIDParameters(): Promise<{ kp: number; ki: number; kd: number }> {
    const kp = await this.getVariableValue("pid_kp") as number;
    const ki = await this.getVariableValue("pid_ki") as number;
    const kd = await this.getVariableValue("pid_kd") as number;
    return { kp, ki, kd };
  }
}
```

#### Example 3: Building HVAC FMU

```typescript
// HVAC system controller
export class HVACAdapter extends FMUAdapter {
  async getRoomTemperature(roomId: string): Promise<number> {
    return await this.getVariableValue(`room_${roomId}_temp`) as number;
  }

  async setHVACMode(mode: 'heat' | 'cool' | 'auto' | 'off'): Promise<void> {
    await this.setVariable("hvac_mode", mode);
  }

  async optimizeEnergyUsage(targetTemp: number): Promise<{ savings: number }> {
    await this.setVariable("target_temp", targetTemp);
    await this.setVariable("optimize_energy", true);
    await this.doStep(0.1);
    const savings = await this.getVariableValue("energy_savings") as number;
    return { savings };
  }
}
```

### Best Practices for Integration

1. **Error Handling**: Wrap all FMU calls with try-catch blocks
2. **Type Safety**: Use TypeScript interfaces for FMU data structures
3. **Validation**: Validate input parameters before calling FMU functions
4. **Documentation**: Document all MCP tools with clear descriptions
5. **Testing**: Create test clients to verify MCP tool functionality
6. **Logging**: Add logging for debugging FMU communication
7. **Performance**: Cache FMU metadata and variable definitions
8. **Security**: Validate access permissions for sensitive FMU operations

### Testing Your Integration

Create a test script to verify the integration:

**test-integration.js**:
```javascript
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

async function testMCPServer() {
  console.log("Testing FMU MCP Server Integration...\n");

  // Test 1: Get Metadata
  console.log("Test 1: Get FMU Metadata");
  // Call your MCP server and verify response

  // Test 2: List Variables
  console.log("Test 2: List FMU Variables");
  // Verify all expected variables are present

  // Test 3: Set and Get Variable
  console.log("Test 3: Set and Get Variable");
  // Set a variable value and read it back

  // Test 4: Custom Function
  console.log("Test 4: Execute Custom Function");
  // Call a custom FMU function through MCP

  console.log("\nAll tests passed!");
}

testMCPServer().catch(console.error);
```

---

## Project Structure

```
fmu-as-a-mcp-server/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD pipeline
├── .vscode/
│   ├── launch.json             # VS Code debug configuration
│   └── mcp-config.json         # MCP server configuration
├── src/
│   ├── index.ts                # MCP server implementation
│   ├── virtual-ecu.ts          # Virtual ECU FMU implementation
│   ├── addition.h              # C header file for addition
│   └── addition.c              # C implementation of addition
├── examples/
│   ├── test-client.js          # Example MCP client
│   └── test-ecu.js             # ECU functionality tests
├── dist/                       # Compiled JavaScript output (generated)
├── node_modules/               # Node.js dependencies (generated)
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore rules
├── DOCUMENTATION.md            # This file - complete documentation
├── README.md                   # Project overview and quick start
├── LICENSE                     # MIT License
├── package.json                # Node.js project configuration
├── tsconfig.json               # TypeScript configuration
└── requirements.txt            # Python dependencies (if any)
```

---

## Development Guide

### Building the Project

```bash
# Clean build
rm -rf dist
npm run build

# Development mode (auto-rebuild on changes)
npm run dev

# Watch mode (continuous compilation)
npx tsc --watch
```

### Running Tests

```bash
# Run all tests
npm test

# Run specific test
node examples/test-ecu.js
```

### Code Style

The project follows standard TypeScript conventions:
- Use camelCase for variables and functions
- Use PascalCase for classes and interfaces
- Use UPPER_CASE for constants
- Add JSDoc comments for public functions
- Keep functions small and focused

### Adding New ECU Functions

1. **Add method to Virtual ECU class** (`src/virtual-ecu.ts`):
   ```typescript
   multiply(a: number, b: number): number {
     return a * b;
   }
   ```

2. **Register MCP tool** (`src/index.ts`):
   ```typescript
   {
     name: "multiply_numbers",
     description: "Multiply two numbers using the Virtual ECU",
     inputSchema: {
       type: "object",
       properties: {
         a: { type: "number", description: "First number" },
         b: { type: "number", description: "Second number" }
       },
       required: ["a", "b"]
     }
   }
   ```

3. **Add tool handler** (`src/index.ts`):
   ```typescript
   case "multiply_numbers": {
     if (!args || typeof args.a !== "number" || typeof args.b !== "number") {
       throw new Error("Both 'a' and 'b' must be numbers");
     }
     const result = virtualECU.multiply(args.a, args.b);
     return {
       content: [{
         type: "text",
         text: `Result: ${args.a} × ${args.b} = ${result}`
       }]
     };
   }
   ```

4. **Rebuild and test**:
   ```bash
   npm run build
   npm test
   ```

### Debugging

#### VS Code Debugging

1. Set breakpoints in TypeScript files
2. Press `F5` to start debugging
3. Use Debug Console to inspect variables

#### Command Line Debugging

```bash
# Enable Node.js debugging
node --inspect dist/index.js

# Or use Node.js inspector
node --inspect-brk dist/index.js
```

Connect with Chrome DevTools: `chrome://inspect`

### Logging

Add logging for debugging:

```typescript
// In src/index.ts or src/virtual-ecu.ts
console.error("Debug info:", { variable: value });

// Log to file
import fs from 'fs';
fs.appendFileSync('debug.log', `${new Date().toISOString()}: ${message}\n`);
```

---

## Testing

### Running Tests

```bash
# Run all tests
npm test

# Run with verbose output
npm test -- --verbose
```

### Test Files

#### examples/test-ecu.js

Tests Virtual ECU functionality:
- Addition operations
- Metadata queries
- Status checks

#### examples/test-client.js

Tests MCP server communication:
- Tool registration
- Tool execution
- Error handling

### Writing New Tests

Create a new test file:

```javascript
// test-my-feature.js
import { VirtualECU } from '../dist/virtual-ecu.js';

function testMyFeature() {
  const ecu = new VirtualECU();
  
  // Test setup
  const result = ecu.myFunction(input);
  
  // Assertion
  if (result !== expected) {
    throw new Error(`Test failed: expected ${expected}, got ${result}`);
  }
  
  console.log("✓ Test passed");
}

testMyFeature();
```

### Continuous Integration

Tests run automatically on:
- Push to main/develop branches
- Pull requests
- Manual workflow dispatch

See `.github/workflows/ci.yml` for CI configuration.

---

## Troubleshooting

### Common Issues

#### 1. MCP Server Not Connecting

**Symptoms**: Copilot can't find the MCP server

**Solutions**:
- Ensure the server is built: `npm run build`
- Check Node.js version: `node --version` (must be v18+)
- Verify server is running: `ps aux | grep index.js`
- Check MCP configuration in VS Code settings
- Restart VS Code after configuration changes

#### 2. Build Fails

**Symptoms**: `npm run build` errors

**Solutions**:
```bash
# Clean and reinstall
rm -rf node_modules package-lock.json dist
npm install
npm run build

# Check TypeScript version
npx tsc --version

# Verify tsconfig.json is correct
cat tsconfig.json
```

#### 3. Import Errors

**Symptoms**: `Cannot find module` errors

**Solutions**:
- Ensure `"type": "module"` is in package.json
- Use `.js` extension in imports (even for `.ts` files)
- Check file paths are correct

#### 4. C Compilation Errors

**Symptoms**: GCC compilation fails

**Solutions**:
```bash
# Install GCC
# Ubuntu/Debian
sudo apt-get install build-essential

# macOS
xcode-select --install

# Verify GCC
gcc --version

# Compile with verbose output
gcc -v -c src/addition.c
```

#### 5. Copilot Not Recognizing MCP Tools

**Symptoms**: Copilot doesn't respond to queries

**Solutions**:
- Restart VS Code
- Check GitHub Copilot extension is up to date
- Verify MCP configuration: check `settings.json`
- Enable Copilot Chat extension
- Check MCP server logs for errors

#### 6. OpenAI API Issues

**Symptoms**: API calls fail or return errors

**Solutions**:
- Verify API key: `echo $OPENAI_API_KEY`
- Check API key permissions
- Verify account has credits
- Check rate limits
- Test with curl:
  ```bash
  curl https://api.openai.com/v1/models \
    -H "Authorization: Bearer $OPENAI_API_KEY"
  ```

### Getting Help

If you encounter issues not covered here:

1. **Check GitHub Issues**: https://github.com/kushalkoppa/fmu-as-a-mcp-server/issues
2. **Open a New Issue** with:
   - Node.js version (`node --version`)
   - Operating system
   - Error messages (full stack trace)
   - Steps to reproduce
   - Expected vs actual behavior
3. **Community Support**: Ask in GitHub Discussions

### Debug Mode

Enable debug logging:

```bash
# Set debug environment variable
export DEBUG=mcp:*

# Run with debug output
npm run dev
```

---

## Use Cases

### 1. Development & Testing
- Test ECU interfaces without physical hardware
- Rapid prototyping of ECU functionality
- Integration testing with other systems

### 2. AI-Assisted Diagnostics
- Query ECU information using natural language
- Troubleshoot issues with LLM assistance
- Generate diagnostic reports automatically

### 3. Documentation
- Automatically document ECU capabilities
- Generate API documentation from metadata
- Create user guides with AI assistance

### 4. Training & Education
- Learn about ECU systems interactively
- Demonstrate FMU concepts
- Practice with virtual hardware

### 5. Integration Testing
- Validate MCP server integration
- Test with various LLMs
- Verify tool calling functionality

### 6. Research & Development
- Experiment with AI-ECU integration
- Develop new interaction patterns
- Prototype future automotive systems

---

## Contributing

Contributions are welcome! Here's how to contribute:

### Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/fmu-as-a-mcp-server.git
   cd fmu-as-a-mcp-server
   ```
3. **Create a branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Making Changes

1. **Install dependencies**: `npm install`
2. **Make your changes**
3. **Test your changes**: `npm test`
4. **Build the project**: `npm run build`
5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request**

### Contribution Guidelines

- Follow existing code style
- Add tests for new functionality
- Update documentation as needed
- Keep commits focused and atomic
- Write clear commit messages
- Ensure all tests pass before submitting PR

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

---

## License

MIT License

Copyright (c) 2024 Kushal Koppa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Acknowledgments

- **Model Context Protocol (MCP)** by Anthropic - for the MCP specification
- **FMI Standard** (Functional Mock-up Interface) - for FMU standards
- **OpenAI** - for LLM capabilities and API
- **GitHub Copilot** - for AI-assisted development
- **TypeScript Community** - for excellent tooling and support
- **Node.js** - for the runtime environment

---

## Contact & Support

- **GitHub Repository**: https://github.com/kushalkoppa/fmu-as-a-mcp-server
- **Issues**: https://github.com/kushalkoppa/fmu-as-a-mcp-server/issues
- **Discussions**: https://github.com/kushalkoppa/fmu-as-a-mcp-server/discussions

For questions or support, please open an issue on GitHub.

---

## Version History

### v1.0.0 (Current)
- Initial release
- Virtual ECU with addition functionality
- MCP server implementation
- GitHub Copilot integration
- OpenAI API support
- C source code for addition function
- Comprehensive documentation
- CI/CD pipeline with GitHub Actions
- Integration guide for existing FMUs

---

**Note**: This is a demonstration project showing how FMU virtual ECUs can be integrated with AI agents through MCP. The addition operation is a simple example - real ECUs would have more complex functionality. The integration guide provides a framework for adding MCP capabilities to your existing FMU implementations.
