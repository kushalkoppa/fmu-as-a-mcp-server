# FMU Virtual ECU - How to Use with Copilot

This guide shows you how to query the Virtual ECU using GitHub Copilot in VS Code.

## Prerequisites

1. ✅ Project opened in VS Code
2. ✅ GitHub Copilot extension installed
3. ✅ Dependencies installed (`pip install -r requirements.txt`)
4. ✅ MCP server configured (see SETUP_GUIDE.md)

## Example Copilot Queries

Once your MCP server is running, you can ask Copilot questions about your Virtual ECU:

### 1. Get ECU Information

**Question:**
```
@workspace What is the Virtual ECU information?
```

**Expected Answer:**
Copilot will use the `get_ecu_info` tool and return:
- Software: Virtual ECU - Addition Module
- Version: 1.0.0
- ECU Level: Level_2
- Supported Interfaces: CAN, LIN, Ethernet, FlexRay
- Capabilities: Addition, Data Processing, Real-time Response

### 2. Query Software Version

**Question:**
```
@workspace What software version is the Virtual ECU running?
```

**Expected Answer:**
Version 1.0.0

### 3. List Communication Interfaces

**Question:**
```
@workspace What communication interfaces does the ECU support?
```

**Expected Answer:**
- CAN
- LIN
- Ethernet
- FlexRay

### 4. Check ECU Level

**Question:**
```
@workspace What is the ECU level?
```

**Expected Answer:**
Level_2

### 5. Perform Addition

**Question:**
```
@workspace Can you add 42 and 58 using the Virtual ECU?
```

**Expected Answer:**
Addition Result: 42 + 58 = 100

### 6. Check Status

**Question:**
```
@workspace What's the current status of the Virtual ECU?
```

**Expected Answer:**
ECU Status: Active
Timestamp: [current timestamp]

### 7. Complex Queries

**Question:**
```
@workspace Can you show me all the capabilities of the ECU and then add 123 and 456?
```

**Expected Answer:**
Copilot will use multiple tools to:
1. Get ECU capabilities
2. Perform the addition operation

## Tips for Best Results

1. **Use @workspace**: This tells Copilot to use workspace context and MCP tools
2. **Be specific**: Ask clear, direct questions
3. **Natural language**: Phrase questions conversationally
4. **Check server**: Ensure MCP server is running in the background

## Troubleshooting

### Copilot doesn't use the MCP tools

**Solution:**
1. Verify MCP server is running: `python server.py`
2. Check MCP configuration in settings
3. Restart VS Code

### Server not responding

**Solution:**
1. Check virtual environment is activated
2. Verify dependencies are installed
3. Look for error messages in terminal

### No OpenAI responses

**Solution:**
1. Set OPENAI_API_KEY in `.env` file
2. Verify API key is valid
3. Check internet connection

## Advanced Usage

### Writing Code with Copilot

You can also ask Copilot to write code that interacts with the ECU:

**Question:**
```
Write a Python script that queries the ECU version and performs addition
```

Copilot will generate code like:
```python
from fmu_model import VirtualECU

ecu = VirtualECU()
version = ecu.get_version()
print(f"Version: {version}")

result = ecu.add(10, 20)
print(f"Result: {result}")
```

### Code Completion

As you type, Copilot will suggest completions based on the ECU API:

```python
ecu = VirtualECU()
# Start typing "ecu." and Copilot will suggest methods:
# - ecu.add()
# - ecu.get_info()
# - ecu.get_version()
# etc.
```

## Next Steps

1. Experiment with different queries
2. Try combining multiple ECU operations
3. Use Copilot to extend the ECU functionality
4. Create custom scripts with Copilot's help

---

**Happy coding with your AI-powered Virtual ECU! 🤖🚗**
