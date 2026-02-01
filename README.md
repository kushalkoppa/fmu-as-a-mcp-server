# FMU as MCP Server (FaaMs)

A Functional Mock-up Unit (FMU) virtual ECU embedded with AI agent capabilities, acting as a Model Context Protocol (MCP) server. This allows users to query ECU information like software version, interfaces, and capabilities using LLMs such as GitHub Copilot or OpenAI.

**NEW:** Now includes automated FMU repackaging tool for adding MCP capabilities to existing FMUs from Synopsys, Vector, dSPACE, ETAS, and other vendors!

[![CI/CD Pipeline](https://github.com/kushalkoppa/fmu-as-a-mcp-server/actions/workflows/ci.yml/badge.svg)](https://github.com/kushalkoppa/fmu-as-a-mcp-server/actions/workflows/ci.yml)

## 📚 Documentation

For comprehensive documentation, see **[DOCUMENTATION.md](DOCUMENTATION.md)** which includes:
- Complete setup and installation guide
- GitHub Copilot and OpenAI integration
- **Automated FMU repackaging tool guide** (NEW!)
- **Working with vendor FMUs** (Synopsys/Vector/dSPACE/ETAS)
- **FMPy compatibility and loading guide**
- C implementation details
- Architecture and design patterns
- Troubleshooting and best practices

## Overview

This project demonstrates a Virtual ECU FMU with:
- **Basic arithmetic operations** (addition example with C source code)
- **Queryable metadata** (software, version, interfaces, level)
- **MCP server interface** for AI agent integration
- **OpenAI/Copilot compatibility** for natural language queries
- **CI/CD pipeline** with GitHub Actions
- **FMU repackaging tool** for adding MCP to existing FMUs
- **FMPy compatibility** for simulation and testing

## Features

- 🚗 **Virtual ECU Implementation**: Simulates an Electronic Control Unit with addition functionality
- 🤖 **AI Agent Integration**: MCP server enables LLM-based queries
- 📊 **Metadata Exposure**: Query SW version, interfaces, ECU level via natural language
- 🔌 **OpenAI Compatible**: Works with OpenAI API and GitHub Copilot
- 💻 **VS Code Integration**: First-class support for Visual Studio Code
- ⚙️ **C Source Code**: Includes addition.c and addition.h for native implementation
- 🔧 **Extensible**: Easy to integrate with existing FMUs
- 📦 **FMU Repackaging Tool**: Automated tool to add MCP to vendor FMUs (NEW!)
- 🔄 **FMPy Compatible**: Repackaged FMUs work with FMPy for simulation (NEW!)

## Architecture

```
┌─────────────────────────────────────────┐
│         User (via LLM/Copilot)          │
└────────────────┬────────────────────────┘
                 │ Natural Language Query
                 ↓
┌─────────────────────────────────────────┐
│         MCP Server Interface            │
│  (Model Context Protocol)               │
└────────────────┬────────────────────────┘
                 │ Tool Calls
                 ↓
┌─────────────────────────────────────────┐
│         Virtual ECU (FMU)               │
│  - Addition Unit                        │
│  - Metadata (SW, Version, Interfaces)   │
│  - Status Monitoring                    │
└─────────────────────────────────────────┘
```

## Prerequisites

- Node.js (v18 or higher)
- npm (Node Package Manager)
- Visual Studio Code (recommended)
- GitHub Copilot extension (for VS Code integration)
- OpenAI API key (optional, for direct OpenAI integration)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kushalkoppa/fmu-as-a-mcp-server.git
   cd fmu-as-a-mcp-server
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Build the project**:
   ```bash
   npm run build
   ```

## Quick Start: Repackaging Existing FMUs

Have an existing FMU from Synopsys, Vector, dSPACE, or ETAS? Add MCP capabilities in 3 steps:

### Step 1: Install Python Dependencies
```bash
pip install fmpy lxml
```

### Step 2: Repackage Your FMU
```bash
# Repackage an existing FMU with MCP capabilities
python fmu_repackager.py --input your_vendor.fmu --output your_vendor_mcp.fmu
```

### Step 3: Load in FMPy
```python
from fmpy import simulate_fmu

# Your repackaged FMU now has MCP capabilities
result = simulate_fmu('your_vendor_mcp.fmu')
```

**Output Example:**
```
===========================================================
FMU MCP Server Repackaging Tool
===========================================================
[1/6] Extracting FMU: your_vendor.fmu
  ✓ Extracted to: /tmp/fmu_repackage_xyz
[2/6] Parsing modelDescription.xml
  ✓ FMI Version: 2.0
  ✓ Model Name: VendorECU_Controller
[3/6] Adding MCP Server variables
  ✓ Added MCP status variable
  ✓ Added MCP version variable
[4/6] Adding MCP Server wrapper
  ✓ Created MCP config
  ✓ Created MCP wrapper
[5/6] Updating modelDescription.xml
  ✓ Updated modelDescription.xml
[6/6] Repackaging FMU: your_vendor_mcp.fmu
  ✓ Created repackaged FMU
===========================================================
✓ Repackaging completed successfully!
===========================================================
```

For detailed instructions, see [DOCUMENTATION.md](DOCUMENTATION.md#approach-1-repackaging-existing-fmus-automated).

## Setup in Visual Studio Code

### Step 1: Open the Project

1. Launch Visual Studio Code
2. Open the project folder: `File > Open Folder...`
3. Select the `fmu-as-a-mcp-server` directory

### Step 2: Configure GitHub Copilot for MCP

1. **Install GitHub Copilot extension** if not already installed:
   - Open Extensions (`Ctrl+Shift+X` or `Cmd+Shift+X` on Mac)
   - Search for "GitHub Copilot"
   - Click "Install"

2. **Configure MCP Settings**:
   - Open VS Code Settings (`Ctrl+,` or `Cmd+,` on Mac)
   - Search for "MCP" or "Model Context Protocol"
   - Add the FMU MCP server configuration

3. **Alternative: Use the provided MCP config**:
   - The project includes `.vscode/mcp-config.json`
   - Copy this to your VS Code user settings or workspace settings

### Step 3: Set Up OpenAI API Key (Optional)

If you want to use OpenAI directly:

1. Create a `.env` file in the project root:
   ```bash
   OPENAI_API_KEY=your-api-key-here
   ```

2. Or set it as an environment variable:
   ```bash
   export OPENAI_API_KEY=your-api-key-here
   ```

## Running the MCP Server

### Option 1: Direct Execution
```bash
npm run dev
```

### Option 2: Using VS Code Debugger
1. Press `F5` or go to `Run > Start Debugging`
2. Select "Launch FMU MCP Server"
3. The server will start and listen for MCP connections

### Option 3: As a Background Service
```bash
npm start
```

## Querying with GitHub Copilot

Once the MCP server is running and configured in VS Code, you can ask Copilot natural language questions:

### Example Queries:

1. **Query ECU Software**:
   ```
   @workspace What software is running on the Virtual ECU?
   ```

2. **Query ECU Version**:
   ```
   @workspace What version is the Virtual ECU FMU?
   ```

3. **Query Available Interfaces**:
   ```
   @workspace What interfaces does the Virtual ECU provide?
   ```

4. **Query ECU Level**:
   ```
   @workspace What is the level of the Virtual ECU?
   ```

5. **Use the Addition Function**:
   ```
   @workspace Can you add 15 and 27 using the Virtual ECU?
   ```

6. **Get Complete Metadata**:
   ```
   @workspace Show me all the metadata for the Virtual ECU
   ```

## Available MCP Tools

The FMU MCP server exposes the following tools:

| Tool Name | Description |
|-----------|-------------|
| `get_ecu_metadata` | Get complete metadata (SW, version, interfaces, level) |
| `get_ecu_software` | Get the software name |
| `get_ecu_version` | Get the version number |
| `get_ecu_interfaces` | Get available interfaces list |
| `get_ecu_level` | Get the ECU capability level |
| `get_ecu_status` | Get current operational status |
| `add_numbers` | Perform addition operation (a + b) |

## Using with OpenAI API Directly

You can also interact with the FMU MCP server using OpenAI's API:

```javascript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

// Example: Query ECU metadata
const response = await openai.chat.completions.create({
  model: "gpt-4",
  messages: [
    {
      role: "user",
      content: "What is the software and version of the Virtual ECU?"
    }
  ],
  tools: [
    // MCP tools would be registered here
  ]
});
```

## Project Structure

```
fmu-as-a-mcp-server/
├── src/
│   ├── index.ts              # MCP server implementation
│   └── virtual-ecu.ts        # Virtual ECU FMU implementation
├── .vscode/
│   ├── launch.json           # VS Code debug configuration
│   └── mcp-config.json       # MCP server configuration
├── dist/                     # Compiled JavaScript output
├── package.json              # Project dependencies
├── tsconfig.json             # TypeScript configuration
└── README.md                 # This file
```

## Development

### Building
```bash
npm run build
```

### Development Mode (auto-rebuild)
```bash
npm run dev
```

## Example Interaction

```
User: "What software is running on the ECU?"
Response: "Virtual ECU Addition Unit"

User: "What version?"
Response: "1.0.0"

User: "What domain is this ECU for?"
Response: "Automotive - Basic Arithmetic Control Unit"

User: "What functions are available in the FMU?"
Response: Lists all functions with descriptions:
  - add(a, b): Perform addition operation
  - getMetadata(): Get complete ECU metadata
  - getSoftware(): Get software name
  - getVersion(): Get version number
  - getInterfaces(): Get available interfaces
  - getLevel(): Get capability level
  - getStatus(): Get operational status
  - getDomain(): Get domain/application area
  - listFunctions(): List all available functions

User: "What interfaces are available?"
Response: ["addition", "metadata", "status"]

User: "What level is this ECU?"
Response: "L2 - Basic Arithmetic Functions"

User: "Add 25 and 17"
Response: "Result: 25 + 17 = 42"
```

## ECU Metadata Details

The Virtual ECU FMU provides the following metadata:

- **Software**: Virtual ECU Addition Unit
- **Version**: 1.0.0
- **Interfaces**: addition, metadata, status
- **Level**: L2 - Basic Arithmetic Functions
- **Domain**: Automotive - Basic Arithmetic Control Unit
- **Description**: A virtual ECU FMU that provides basic addition functionality and queryable metadata

### Available Functions

Query the ECU with `@workspace What functions are available?` to get a complete list of:
- Core arithmetic operations (addition)
- Metadata query functions
- Status and domain information
- Function introspection capabilities

## Use Cases

1. **Development & Testing**: Test ECU interfaces without physical hardware
2. **AI-Assisted Diagnostics**: Query ECU information using natural language
3. **Documentation**: Automatically document ECU capabilities via AI
4. **Training**: Learn about ECU systems with interactive AI queries
5. **Integration Testing**: Validate MCP server integration with various LLMs

## Troubleshooting

### MCP Server Not Connecting
- Ensure the server is built: `npm run build`
- Check that Node.js v18+ is installed: `node --version`
- Verify the server is running: `npm start`

### Copilot Not Recognizing MCP Tools
- Restart VS Code after configuring MCP settings
- Check that GitHub Copilot extension is up to date
- Verify MCP configuration in `.vscode/mcp-config.json`

### OpenAI API Issues
- Verify your API key is set correctly
- Check API key permissions and quotas
- Ensure you have a valid OpenAI account

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Model Context Protocol (MCP) by Anthropic
- FMU (Functional Mock-up Interface) standards
- OpenAI for LLM capabilities
- GitHub Copilot for AI-assisted development

## Contact

For questions or support, please open an issue on GitHub.

---

**Note**: This is a demonstration project showing how FMU virtual ECUs can be integrated with AI agents through MCP. The addition operation is a simple example - real ECUs would have more complex functionality.
