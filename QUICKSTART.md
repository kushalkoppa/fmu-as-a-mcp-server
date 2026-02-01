# Quick Start Guide

This guide will get you up and running with the FMU MCP Server in 5 minutes.

## Quick Setup

```bash
# 1. Clone and navigate to the project
git clone https://github.com/kushalkoppa/fmu-as-a-mcp-server.git
cd fmu-as-a-mcp-server

# 2. Install dependencies
npm install

# 3. Build the project
npm run build

# 4. Run the server
npm start
```

## Quick Test

Once the server is running, open a new terminal and test with the example client:

```bash
cd examples
node test-client.js
```

You should see output showing:
- Connected to FMU MCP Server
- List of available tools
- Test results for all ECU functions
- Addition operation results

## Quick Query Examples

If you have GitHub Copilot set up in VS Code:

1. Open the project in VS Code
2. Open Copilot Chat (Ctrl+Shift+I or Cmd+Shift+I)
3. Try these queries:

```
What software is running on the Virtual ECU?
```

```
Add 25 and 17 using the ECU
```

```
Show me all metadata for the Virtual ECU
```

## What's Next?

- Read [COPILOT_SETUP.md](COPILOT_SETUP.md) for detailed Copilot configuration
- Read [OPENAI_INTEGRATION.md](OPENAI_INTEGRATION.md) for OpenAI API integration
- Check [README.md](README.md) for complete documentation

## Troubleshooting

**Server won't start?**
- Check Node.js version: `node --version` (must be v18+)
- Rebuild: `npm run build`
- Check for errors in the build output

**Can't connect with client?**
- Ensure server is running in another terminal
- Check that dist/index.js exists
- Verify no other process is using the same port

**Need Help?**
Open an issue on GitHub with:
- Node.js version
- Operating system
- Error messages
- Steps to reproduce
