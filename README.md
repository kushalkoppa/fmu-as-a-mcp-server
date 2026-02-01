# FMU as a MCP Server - Virtual ECU with AI Agent

**FaaMs** (FMU as a MCP Server) is an innovative project that combines Functional Mockup Units (FMU), Model Context Protocol (MCP), and AI Agent capabilities to create an intelligent Virtual ECU (Electronic Control Unit).

## 🌟 Overview

This project implements a Virtual ECU that:
- Acts as an MCP server exposing queryable tools
- Provides AI-powered natural language interface via OpenAI
- Demonstrates basic ECU functionality (addition operations)
- Supports standard automotive communication interfaces
- Integrates seamlessly with GitHub Copilot and VS Code

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│         User (VS Code + Copilot)            │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│          MCP Server (server.py)             │
│  ┌───────────────────────────────────────┐  │
│  │  Tools:                               │  │
│  │  - get_ecu_info                       │  │
│  │  - get_software_version               │  │
│  │  - get_interfaces                     │  │
│  │  - get_ecu_level                      │  │
│  │  - perform_addition                   │  │
│  │  - get_ecu_status                     │  │
│  └───────────────────────────────────────┘  │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│       Virtual ECU (fmu_model.py)            │
│  ┌───────────────────────────────────────┐  │
│  │  - Version: 1.0.0                     │  │
│  │  - Level: Level_2                     │  │
│  │  - Interfaces: CAN, LIN, Ethernet,    │  │
│  │    FlexRay                            │  │
│  │  - Operations: Addition, Processing   │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│       AI Agent (ai_agent.py)                │
│         OpenAI Integration                  │
└─────────────────────────────────────────────┘
```

## 📋 Features

### Virtual ECU Capabilities
- **Software Information**: Query software name, version, and manufacturer
- **Interface Support**: CAN, LIN, Ethernet, FlexRay communication protocols
- **ECU Level**: Configurable ECU level (Level_1, Level_2, etc.)
- **Arithmetic Operations**: Demonstration addition functionality
- **Real-time Status**: Monitor ECU operational status

### MCP Server Tools
1. **get_ecu_info**: Get comprehensive ECU information
2. **get_software_version**: Query software version
3. **get_interfaces**: List supported communication interfaces
4. **get_ecu_level**: Get the ECU level
5. **perform_addition**: Execute addition operations
6. **get_ecu_status**: Check ECU operational status

### AI Agent Features
- Natural language queries via OpenAI
- Context-aware responses about ECU specifications
- Intelligent command execution
- Integration with GitHub Copilot

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Visual Studio Code
- GitHub Copilot (optional but recommended)
- OpenAI API key (for AI agent features)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/kushalkoppa/fmu-as-a-mcp-server.git
cd fmu-as-a-mcp-server
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## 💻 Usage

### Running the MCP Server

```bash
python server.py
```

The MCP server will start and listen for requests via stdio.

### Using the AI Agent

```bash
python ai_agent.py
```

This will run example queries demonstrating the AI agent's capabilities.

### Example Queries

```python
from ai_agent import FMU_AI_Agent

agent = FMU_AI_Agent()

# Query software version
response = agent.query("What software version is running?")

# Query interfaces
response = agent.query("What interfaces does the ECU support?")

# Perform addition
response = agent.query_with_action("Can you add 25 and 17?")

# Query ECU level
response = agent.query("What is the ECU level?")
```

## 📝 VS Code Integration

### Step 1: Open in VS Code

1. Open Visual Studio Code
2. Go to **File** > **Open Folder**
3. Select the `fmu-as-a-mcp-server` directory
4. VS Code will recommend installing extensions (Python, Copilot)

### Step 2: Install Recommended Extensions

When you open the project, VS Code will prompt you to install recommended extensions:
- **GitHub Copilot** - AI pair programmer
- **GitHub Copilot Chat** - Chat interface for Copilot
- **Python** - Python language support
- **Pylance** - Python language server

Click **Install All** to set up your environment.

### Step 3: Configure Python Interpreter

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type "Python: Select Interpreter"
3. Choose the virtual environment: `./venv/bin/python`

### Step 4: Set up MCP Server for Copilot

1. Open VS Code settings (`Ctrl+,` or `Cmd+,`)
2. Search for "MCP"
3. Add the MCP server configuration from `mcp-config.json`

Alternatively, you can configure it in your Copilot settings:

**For Claude Desktop or MCP-compatible clients:**
Add to your MCP configuration file:

```json
{
  "mcpServers": {
    "fmu-virtual-ecu": {
      "command": "python",
      "args": [
        "/path/to/fmu-as-a-mcp-server/server.py"
      ],
      "env": {
        "PYTHONPATH": "/path/to/fmu-as-a-mcp-server"
      }
    }
  }
}
```

## 🤖 Using with GitHub Copilot

### Querying the Virtual ECU via Copilot

Once the MCP server is configured, you can use GitHub Copilot Chat to query your Virtual ECU:

1. **Open Copilot Chat** (Click the chat icon in the sidebar or press `Ctrl+Alt+I`)

2. **Ask questions about the ECU:**

```
@workspace What software version is the Virtual ECU running?
```

```
@workspace What interfaces does the Virtual ECU support?
```

```
@workspace Can you use the ECU to add 42 and 58?
```

```
@workspace What is the ECU level of this virtual unit?
```

3. **Copilot will use the MCP server tools to:**
   - Query ECU information
   - Execute operations
   - Provide contextual responses

### Example Copilot Interactions

**Query 1: Get ECU Information**
```
User: @workspace Show me the Virtual ECU information
Copilot: [Uses get_ecu_info tool]
Response: The Virtual ECU is running software version 1.0.0 
at Level_2. It supports CAN, LIN, Ethernet, and FlexRay 
interfaces...
```

**Query 2: Perform Calculation**
```
User: @workspace Add 123 and 456 using the ECU
Copilot: [Uses perform_addition tool]
Response: Addition Result: 123 + 456 = 579
```

**Query 3: Check Status**
```
User: @workspace What's the status of the Virtual ECU?
Copilot: [Uses get_ecu_status tool]
Response: ECU Status: Active
Timestamp: 2026-02-01T14:55:00...
```

## 🔗 OpenAI Integration

### Setting up OpenAI Connection

1. **Get an OpenAI API Key**
   - Visit https://platform.openai.com/api-keys
   - Create a new API key
   - Copy the key

2. **Configure the API Key**
   - Edit the `.env` file
   - Add your API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

3. **Choose Your Model**
   - Default: GPT-4 (more accurate, slower)
   - Alternative: GPT-3.5-turbo (faster, cheaper)
   
   Edit `ai_agent.py` to change the model:
   ```python
   self.model = "gpt-3.5-turbo"  # Or "gpt-4"
   ```

### Using the AI Agent

The AI agent provides a natural language interface to the Virtual ECU:

```python
from ai_agent import FMU_AI_Agent

# Initialize the agent
agent = FMU_AI_Agent()

# Ask questions in natural language
response = agent.query("What can this ECU do?")
print(response)

# The AI will respond based on ECU context:
# "This Virtual ECU (Level_2) can perform addition operations,
#  process data in real-time, and communicate via CAN, LIN,
#  Ethernet, and FlexRay interfaces..."
```

### AI Agent Features

- **Context-Aware**: The AI knows all ECU specifications
- **Natural Language**: Ask questions conversationally
- **Action Execution**: Can trigger ECU operations
- **Educational**: Explains ECU concepts and capabilities

## 📚 Project Structure

```
fmu-as-a-mcp-server/
├── .vscode/                    # VS Code configuration
│   ├── extensions.json         # Recommended extensions
│   └── settings.json           # Workspace settings
├── fmu_model.py               # Virtual ECU implementation
├── server.py                  # MCP server
├── ai_agent.py               # OpenAI integration
├── requirements.txt          # Python dependencies
├── package.json             # Project metadata
├── .env.example            # Environment variables template
├── mcp-config.json        # MCP server configuration
├── SETUP_GUIDE.md         # Detailed setup instructions
└── README.md             # This file
```

## 🔧 API Reference

### Virtual ECU Methods

```python
ecu = VirtualECU()

# Get comprehensive information
info = ecu.get_info()

# Get software version
version = ecu.get_version()  # Returns: "1.0.0"

# Get supported interfaces
interfaces = ecu.get_interfaces()  # Returns: ["CAN", "LIN", ...]

# Get ECU level
level = ecu.get_ecu_level()  # Returns: "Level_2"

# Perform addition
result = ecu.add(10, 20)  # Returns: 30.0

# Get status
status = ecu.get_status()
```

### MCP Server Tools

All tools are accessible via the MCP protocol:

1. `get_ecu_info` - No parameters
2. `get_software_version` - No parameters
3. `get_interfaces` - No parameters
4. `get_ecu_level` - No parameters
5. `perform_addition` - Parameters: `a` (number), `b` (number)
6. `get_ecu_status` - No parameters

## 🎯 Use Cases

1. **Educational**: Learn about ECU architecture and automotive software
2. **Development**: Prototype and test ECU functionality
3. **Integration**: Test MCP server capabilities
4. **AI Research**: Explore AI-enhanced automotive systems
5. **Simulation**: Virtual ECU for testing without hardware

## 🛠️ Development

### Running Tests

```bash
# Run the AI agent examples
python ai_agent.py

# Test the MCP server (in another terminal)
python server.py
```

### Extending the ECU

To add new capabilities:

1. **Add methods to `fmu_model.py`**
```python
def multiply(self, a: float, b: float) -> float:
    return a * b
```

2. **Add MCP tools in `server.py`**
```python
types.Tool(
    name="perform_multiplication",
    description="Multiply two numbers",
    inputSchema={...}
)
```

3. **Update AI agent context in `ai_agent.py`**

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Model Context Protocol (MCP) by Anthropic
- OpenAI for AI capabilities
- GitHub Copilot for development assistance
- FMI Standard for inspiration

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check the SETUP_GUIDE.md for detailed instructions
- Review example queries in ai_agent.py

---

**Built with ❤️ using Python, MCP, and OpenAI**
