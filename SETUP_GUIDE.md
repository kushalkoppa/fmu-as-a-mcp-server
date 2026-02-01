# FMU as MCP Server - Detailed Setup Guide

This guide provides step-by-step instructions for setting up and using the FMU Virtual ECU with MCP server and AI agent capabilities.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Opening in Visual Studio Code](#opening-in-visual-studio-code)
5. [Using with GitHub Copilot](#using-with-github-copilot)
6. [Connecting to OpenAI](#connecting-to-openai)
7. [Testing the Installation](#testing-the-installation)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - Verify installation:
     ```bash
     python --version
     # or
     python3 --version
     ```

2. **Visual Studio Code**
   - Download from: https://code.visualstudio.com/
   - Version 1.75 or higher recommended

3. **Git**
   - Download from: https://git-scm.com/downloads
   - Verify installation:
     ```bash
     git --version
     ```

### Optional but Recommended

1. **GitHub Copilot License**
   - Sign up at: https://github.com/features/copilot
   - Available for individuals, students, and enterprise

2. **OpenAI API Account**
   - Create account at: https://platform.openai.com/
   - Get API key from: https://platform.openai.com/api-keys

## Installation

### Step 1: Clone the Repository

```bash
# Navigate to your desired directory
cd ~/projects  # or any directory you prefer

# Clone the repository
git clone https://github.com/kushalkoppa/fmu-as-a-mcp-server.git

# Navigate into the project
cd fmu-as-a-mcp-server
```

### Step 2: Create a Virtual Environment

Creating a virtual environment isolates project dependencies:

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt, indicating the virtual environment is active.

### Step 3: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- `mcp` - Model Context Protocol library
- `openai` - OpenAI API client
- `python-dotenv` - Environment variable management
- `pydantic` - Data validation

### Step 4: Verify Installation

```bash
python -c "import mcp, openai; print('Dependencies installed successfully!')"
```

If no errors appear, the installation was successful!

## Configuration

### Step 1: Create Environment File

```bash
# Copy the example environment file
cp .env.example .env
```

### Step 2: Configure OpenAI API Key

1. **Obtain an API key** from https://platform.openai.com/api-keys

2. **Edit the .env file:**
   ```bash
   # On macOS/Linux
   nano .env
   
   # On Windows
   notepad .env
   ```

3. **Add your API key:**
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   FMU_VERSION=1.0.0
   FMU_ECU_LEVEL=Level_2
   ```

4. **Save and close the file**

**Important:** Never commit the `.env` file to version control. It's already in `.gitignore`.

## Opening in Visual Studio Code

### Step 1: Open the Project

**Method 1: From VS Code**
1. Open Visual Studio Code
2. Click **File** → **Open Folder**
3. Navigate to `fmu-as-a-mcp-server` directory
4. Click **Select Folder** (or **Open** on macOS)

**Method 2: From Terminal**
```bash
cd fmu-as-a-mcp-server
code .
```

### Step 2: Install Recommended Extensions

When you open the project, VS Code will show a notification:

> "This workspace has extension recommendations."

Click **Install All** to install:
- **GitHub Copilot** (`github.copilot`)
- **GitHub Copilot Chat** (`github.copilot-chat`)
- **Python** (`ms-python.python`)
- **Pylance** (`ms-python.vscode-pylance`)

**Manual Installation** (if notification doesn't appear):
1. Press `Ctrl+Shift+X` (or `Cmd+Shift+X` on macOS)
2. Search for each extension
3. Click **Install**

### Step 3: Configure Python Interpreter

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) to open Command Palette
2. Type: `Python: Select Interpreter`
3. Choose: `./venv/bin/python` (or `.\venv\Scripts\python.exe` on Windows)

**Verify:**
- Look at the bottom-left corner of VS Code
- You should see: `Python 3.x.x ('venv': venv)`

### Step 4: Open Integrated Terminal

1. Press `` Ctrl+` `` (backtick) to open the terminal
2. Ensure the virtual environment is activated (you should see `(venv)` in the prompt)
3. If not activated:
   ```bash
   # macOS/Linux
   source venv/bin/activate
   
   # Windows
   venv\Scripts\activate
   ```

## Using with GitHub Copilot

### Step 1: Authenticate GitHub Copilot

1. Click the **Copilot icon** in the VS Code status bar (bottom-right)
2. Or press `Ctrl+Shift+P` and type `GitHub Copilot: Sign In`
3. Follow the authentication flow
4. Authorize VS Code to access GitHub

### Step 2: Configure MCP Server for Copilot

**For Claude Desktop or MCP-compatible clients:**

1. **Locate your MCP config file:**
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. **Add the FMU server configuration:**
   ```json
   {
     "mcpServers": {
       "fmu-virtual-ecu": {
         "command": "python",
         "args": [
           "/absolute/path/to/fmu-as-a-mcp-server/server.py"
         ],
         "env": {
           "PYTHONPATH": "/absolute/path/to/fmu-as-a-mcp-server"
         }
       }
     }
   }
   ```

   **Important:** Replace `/absolute/path/to/` with your actual path!

3. **Save the file and restart Claude Desktop** (if applicable)

### Step 3: Using Copilot Chat to Query the ECU

1. **Open Copilot Chat:**
   - Click the chat icon in the Activity Bar (left sidebar)
   - Or press `Ctrl+Alt+I` (Windows/Linux) or `Cmd+Alt+I` (macOS)

2. **Example Queries:**

   **Query 1: Get ECU Information**
   ```
   @workspace Can you show me the Virtual ECU information?
   ```
   
   Expected response: Information about software version, interfaces, ECU level, etc.

   **Query 2: Check Software Version**
   ```
   @workspace What software version is the Virtual ECU running?
   ```
   
   Expected response: "Version 1.0.0"

   **Query 3: List Interfaces**
   ```
   @workspace What communication interfaces does the ECU support?
   ```
   
   Expected response: CAN, LIN, Ethernet, FlexRay

   **Query 4: Perform Addition**
   ```
   @workspace Can you use the ECU to add 42 and 58?
   ```
   
   Expected response: "Addition Result: 42 + 58 = 100"

   **Query 5: Check ECU Level**
   ```
   @workspace What is the ECU level?
   ```
   
   Expected response: "Level_2"

### Step 4: Direct Code Assistance

Copilot can also help you write code that interacts with the ECU:

1. Create a new file: `test_ecu.py`
2. Start typing a comment:
   ```python
   # Query the Virtual ECU and print the version
   ```
3. Copilot will suggest code to complete the task

## Connecting to OpenAI

### Step 1: Get OpenAI API Key

1. **Sign up or log in** to OpenAI:
   - Go to: https://platform.openai.com/
   - Create an account or sign in

2. **Navigate to API keys:**
   - Go to: https://platform.openai.com/api-keys
   - Click **"Create new secret key"**

3. **Copy the API key:**
   - Name it: "FMU Virtual ECU"
   - Copy the key (starts with `sk-`)
   - **Important:** Save it securely; you won't see it again!

### Step 2: Configure the API Key

1. **Edit the .env file:**
   ```bash
   nano .env  # or use your preferred editor
   ```

2. **Add your API key:**
   ```
   OPENAI_API_KEY=sk-proj-your-actual-key-here
   ```

3. **Save the file**

### Step 3: Test OpenAI Connection

Run the AI agent test:

```bash
python ai_agent.py
```

**Expected Output:**
```
FMU Virtual ECU - AI Agent
==================================================

Q: What software version is running?
A: The Virtual ECU is currently running version 1.0.0...

Q: What interfaces does the ECU support?
A: This ECU supports the following communication interfaces: CAN, LIN, Ethernet, and FlexRay...

Q: What is the ECU level?
A: The Virtual ECU is configured at Level_2...

Q: Can you add 25 and 17?
A: Performing addition: 25.0 + 17.0 = 42.0

Q: What capabilities does this ECU have?
A: The Virtual ECU has the following capabilities: Addition, Data Processing, and Real-time Response...
```

If you see this output, OpenAI is connected successfully! ✅

### Step 4: Customize AI Model (Optional)

Edit `ai_agent.py` to change the model:

```python
# Line 30-31 in ai_agent.py
self.model = "gpt-3.5-turbo"  # Faster and cheaper
# OR
self.model = "gpt-4"  # More accurate and capable
```

**Model Comparison:**
- **GPT-3.5-turbo**: Faster, cheaper (~$0.002/1K tokens), good for simple queries
- **GPT-4**: More accurate, better reasoning (~$0.03/1K tokens), recommended for complex queries

## Testing the Installation

### Test 1: MCP Server

**Terminal 1:**
```bash
python server.py
```

The server should start and wait for connections.

**Terminal 2:**
```bash
# Send a test request (example using stdio)
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python server.py
```

### Test 2: FMU Model Directly

```bash
python -c "from fmu_model import VirtualECU; ecu = VirtualECU(); print(ecu.get_info())"
```

**Expected Output:**
```python
{
  'software': 'Virtual ECU - Addition Module',
  'version': '1.0.0',
  'ecu_level': 'Level_2',
  ...
}
```

### Test 3: AI Agent

```bash
python ai_agent.py
```

Should run example queries without errors.

### Test 4: Addition Operation

```bash
python -c "from fmu_model import VirtualECU; ecu = VirtualECU(); print(f'25 + 17 = {ecu.add(25, 17)}')"
```

**Expected Output:**
```
25 + 17 = 42.0
```

## Troubleshooting

### Issue 1: Module Not Found

**Error:**
```
ModuleNotFoundError: No module named 'mcp'
```

**Solution:**
1. Ensure virtual environment is activated
2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Issue 2: OpenAI API Error

**Error:**
```
Error querying AI agent: Incorrect API key provided
```

**Solution:**
1. Verify API key in `.env` file
2. Ensure no extra spaces in the key
3. Check API key is valid at https://platform.openai.com/api-keys

### Issue 3: Python Interpreter Not Found in VS Code

**Solution:**
1. Press `Ctrl+Shift+P`
2. Type `Python: Select Interpreter`
3. Choose the venv interpreter
4. If not listed, click "Enter interpreter path" and browse to `venv/bin/python`

### Issue 4: MCP Server Won't Start

**Error:**
```
Error: Cannot find module 'mcp'
```

**Solution:**
1. Check Python version: `python --version` (should be 3.8+)
2. Ensure dependencies are installed
3. Try running with full path:
   ```bash
   /path/to/venv/bin/python server.py
   ```

### Issue 5: Copilot Not Seeing MCP Server

**Solution:**
1. Verify MCP config file path is correct
2. Use absolute paths, not relative paths
3. Restart Claude Desktop or VS Code
4. Check server runs manually: `python server.py`

### Issue 6: Permission Denied

**On macOS/Linux:**
```bash
chmod +x venv/bin/activate
```

### Issue 7: Rate Limit from OpenAI

**Error:**
```
Rate limit exceeded
```

**Solution:**
1. Wait a moment and try again
2. Consider upgrading OpenAI plan
3. Use GPT-3.5-turbo instead of GPT-4

## Next Steps

After successful setup:

1. **Explore the code:**
   - `fmu_model.py` - Virtual ECU implementation
   - `server.py` - MCP server
   - `ai_agent.py` - OpenAI integration

2. **Try custom queries:**
   - Use Copilot Chat to ask questions
   - Create custom scripts to interact with the ECU

3. **Extend functionality:**
   - Add new operations (multiply, subtract)
   - Add more ECU capabilities
   - Create custom MCP tools

4. **Read the main README:**
   - See `README.md` for detailed API reference
   - Check use cases and examples

## Support

If you encounter issues not covered here:

1. Check the main `README.md`
2. Review the code comments
3. Open an issue on GitHub
4. Check OpenAI and MCP documentation

---

**Happy coding with your Virtual ECU! 🚗⚡**
