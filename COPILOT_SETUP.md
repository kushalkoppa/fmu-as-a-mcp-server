# Setting Up GitHub Copilot with FMU MCP Server

This guide provides detailed steps to configure GitHub Copilot in Visual Studio Code to work with the FMU MCP Server.

## Prerequisites

1. Visual Studio Code installed
2. GitHub Copilot subscription
3. Node.js v18+ installed
4. FMU MCP Server project cloned and built

## Step-by-Step Setup

### 1. Install Required VS Code Extensions

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
3. Install:
   - **GitHub Copilot**
   - **GitHub Copilot Chat**

### 2. Sign in to GitHub Copilot

1. Click on the Copilot icon in the VS Code sidebar
2. Sign in with your GitHub account
3. Verify your Copilot subscription is active

### 3. Build the FMU MCP Server

```bash
cd fmu-as-a-mcp-server
npm install
npm run build
```

### 4. Configure MCP in VS Code

#### Option A: Using Settings UI

1. Open Settings: `File > Preferences > Settings` (or `Ctrl+,`)
2. Search for "MCP" or "Model Context Protocol"
3. Click "Edit in settings.json"
4. Add the following configuration:

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

#### Option B: Using Claude Desktop Configuration

If you're using Claude Desktop app, configure in:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

Add:
```json
{
  "mcpServers": {
    "fmu-virtual-ecu": {
      "command": "node",
      "args": ["/path/to/fmu-as-a-mcp-server/dist/index.js"]
    }
  }
}
```

### 5. Restart VS Code

After configuration, restart VS Code to load the MCP server.

### 6. Verify MCP Server is Running

Open VS Code Terminal and check:
```bash
ps aux | grep "index.js"
```

You should see the Node.js process running the MCP server.

## Using Copilot to Query the Virtual ECU

### Basic Queries

Open Copilot Chat (Ctrl+Shift+I / Cmd+Shift+I) and try:

1. **Get Metadata**:
   ```
   Can you get the metadata for the FMU Virtual ECU?
   ```

2. **Check Software**:
   ```
   What software is running on the Virtual ECU?
   ```

3. **Check Version**:
   ```
   What version is the Virtual ECU?
   ```

4. **List Interfaces**:
   ```
   What interfaces are available on the ECU?
   ```

5. **Check Level**:
   ```
   What is the ECU level?
   ```

6. **Perform Addition**:
   ```
   Use the ECU to add 42 and 58
   ```

### Advanced Queries

1. **Comparative Analysis**:
   ```
   Compare the interfaces available on the Virtual ECU with standard automotive ECU interfaces
   ```

2. **Status Check**:
   ```
   What is the current operational status of the Virtual ECU?
   ```

3. **Multiple Operations**:
   ```
   First, get the ECU version, then use it to add 10 and 20, and finally check its status
   ```

## Expected Responses

### Example 1: Metadata Query
**Query**: "Show me the complete metadata for the Virtual ECU"

**Expected Response**:
```json
{
  "software": "Virtual ECU Addition Unit",
  "version": "1.0.0",
  "interfaces": ["addition", "metadata", "status"],
  "level": "L2 - Basic Arithmetic Functions",
  "description": "A virtual ECU FMU that provides basic addition functionality and queryable metadata"
}
```

### Example 2: Addition Operation
**Query**: "Add 25 and 17 using the Virtual ECU"

**Expected Response**:
```
Result: 25 + 17 = 42
```

### Example 3: Interface List
**Query**: "What interfaces does the Virtual ECU provide?"

**Expected Response**:
```json
["addition", "metadata", "status"]
```

## Troubleshooting

### Issue: Copilot doesn't recognize MCP tools

**Solution**:
1. Verify MCP server is built: `npm run build`
2. Check configuration in settings.json
3. Restart VS Code completely
4. Check VS Code Output panel for MCP server logs

### Issue: "Command not found" error

**Solution**:
1. Ensure Node.js is in your PATH
2. Use absolute path to node executable in configuration
3. Verify dist/index.js exists after build

### Issue: MCP server crashes on startup

**Solution**:
1. Check for syntax errors: `npm run build`
2. Verify all dependencies are installed: `npm install`
3. Check Node.js version: `node --version` (must be v18+)
4. Review error logs in VS Code Output panel

### Issue: No response from queries

**Solution**:
1. Ensure MCP server is running (check process list)
2. Try restarting the MCP server
3. Check if Copilot is connected (look for green indicator)
4. Try a simple query first: "What is the ECU version?"

## Tips for Effective Querying

1. **Be Specific**: Instead of "tell me about the ECU", ask "What is the software version of the Virtual ECU?"

2. **Use Context**: Reference the tool name: "Use the get_ecu_metadata tool to show me the ECU information"

3. **Chain Operations**: "First check the ECU version, then add 10 and 20"

4. **Natural Language**: Copilot understands natural language, so you can ask conversationally

## Next Steps

Once you have the basic setup working:

1. Explore all available MCP tools
2. Try complex multi-step queries
3. Extend the Virtual ECU with more functions
4. Create custom queries for your use case
5. Integrate with your own ECU implementations

## Additional Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [GitHub Copilot Documentation](https://docs.github.com/copilot)
- [FMU Standard](https://fmi-standard.org/)

## Support

If you encounter issues:
1. Check the main README.md for general troubleshooting
2. Review VS Code Output panel logs
3. Open an issue on GitHub with error details
