# OpenAI Integration Guide

This guide shows how to integrate the FMU MCP Server with OpenAI's API for direct LLM access.

## Overview

The FMU Virtual ECU can be queried using OpenAI's API with function calling capabilities. This allows you to build custom applications that interact with the Virtual ECU using natural language.

## Prerequisites

1. OpenAI API account
2. API key from OpenAI
3. FMU MCP Server running
4. Node.js environment for client code

## Setup

### 1. Get Your OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy and save it securely

### 2. Set Environment Variable

```bash
# Linux/macOS
export OPENAI_API_KEY="sk-your-api-key-here"

# Windows (Command Prompt)
set OPENAI_API_KEY=sk-your-api-key-here

# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-your-api-key-here"
```

Or create a `.env` file:
```
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. Install OpenAI SDK (if creating custom client)

```bash
npm install openai
```

## Using OpenAI with MCP Server

### Option 1: Direct API Calls

Here's an example Node.js script to interact with the Virtual ECU via OpenAI:

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
  }
  // Add other tools as needed
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
    model: "gpt-4-turbo-preview",
    messages: messages,
    tools: tools,
    tool_choice: "auto"
  });

  return response;
}

// Example usage
const result = await queryVirtualECU("What is the Virtual ECU software and version?");
console.log(result.choices[0].message);
```

### Option 2: Using MCP Bridge

The MCP SDK can bridge OpenAI API calls to the MCP server:

```javascript
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import OpenAI from 'openai';

// Connect to MCP server
const transport = new StdioClientTransport({
  command: 'node',
  args: ['./dist/index.js']
});

const client = new Client({
  name: 'openai-mcp-client',
  version: '1.0.0'
}, {
  capabilities: {}
});

await client.connect(transport);

// Get available tools from MCP server
const { tools } = await client.listTools();

// Use with OpenAI
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

async function askECU(question) {
  // Convert MCP tools to OpenAI function format
  const openaiTools = tools.map(tool => ({
    type: "function",
    function: {
      name: tool.name,
      description: tool.description,
      parameters: tool.inputSchema
    }
  }));

  // Make OpenAI request
  const response = await openai.chat.completions.create({
    model: "gpt-4-turbo-preview",
    messages: [{ role: "user", content: question }],
    tools: openaiTools
  });

  const message = response.choices[0].message;

  // If OpenAI wants to call a tool
  if (message.tool_calls) {
    for (const toolCall of message.tool_calls) {
      const result = await client.callTool({
        name: toolCall.function.name,
        arguments: JSON.parse(toolCall.function.arguments)
      });
      
      console.log(`Tool: ${toolCall.function.name}`);
      console.log(`Result:`, result.content);
    }
  }

  return message;
}

// Examples
await askECU("What software is running on the Virtual ECU?");
await askECU("What version is it?");
await askECU("Add 15 and 27 using the ECU");
```

## Example Queries and Responses

### Query 1: Get ECU Metadata

**Query**:
```javascript
await askECU("Tell me everything about the Virtual ECU");
```

**Response**:
```json
{
  "software": "Virtual ECU Addition Unit",
  "version": "1.0.0",
  "interfaces": ["addition", "metadata", "status"],
  "level": "L2 - Basic Arithmetic Functions",
  "description": "A virtual ECU FMU that provides basic addition functionality and queryable metadata"
}
```

### Query 2: Perform Addition

**Query**:
```javascript
await askECU("Can you add 42 and 58 using the Virtual ECU?");
```

**Response**:
```
Result: 42 + 58 = 100
```

### Query 3: Check Interfaces

**Query**:
```javascript
await askECU("What interfaces are available on the ECU?");
```

**Response**:
```json
["addition", "metadata", "status"]
```

## Complete Example Application

Create a file `openai-client.js`:

```javascript
#!/usr/bin/env node
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import OpenAI from 'openai';
import * as readline from 'readline';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

// Connect to MCP server
const transport = new StdioClientTransport({
  command: 'node',
  args: ['./dist/index.js']
});

const mcpClient = new Client({
  name: 'openai-ecu-client',
  version: '1.0.0'
}, {
  capabilities: {}
});

await mcpClient.connect(transport);
const { tools } = await mcpClient.listTools();

// Convert MCP tools to OpenAI format
const openaiTools = tools.map(tool => ({
  type: "function",
  function: {
    name: tool.name,
    description: tool.description,
    parameters: tool.inputSchema
  }
}));

console.log("Connected to Virtual ECU FMU!");
console.log("Ask questions about the ECU or use its functions.\n");

// Interactive prompt
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

async function processQuery(query) {
  const messages = [
    {
      role: "system",
      content: "You are an assistant helping users interact with a Virtual ECU FMU. Use the available tools to answer questions."
    },
    {
      role: "user",
      content: query
    }
  ];

  const response = await openai.chat.completions.create({
    model: "gpt-4-turbo-preview",
    messages: messages,
    tools: openaiTools,
    tool_choice: "auto"
  });

  const message = response.choices[0].message;

  // Handle tool calls
  if (message.tool_calls) {
    console.log("\nCalling Virtual ECU tools...\n");
    
    for (const toolCall of message.tool_calls) {
      console.log(`Using: ${toolCall.function.name}`);
      
      const result = await mcpClient.callTool({
        name: toolCall.function.name,
        arguments: JSON.parse(toolCall.function.arguments)
      });
      
      console.log("Result:", result.content[0].text);
      console.log();
    }
  } else if (message.content) {
    console.log("Assistant:", message.content);
    console.log();
  }
}

function askQuestion() {
  rl.question('You: ', async (answer) => {
    if (answer.toLowerCase() === 'exit' || answer.toLowerCase() === 'quit') {
      console.log("Goodbye!");
      rl.close();
      process.exit(0);
    }

    try {
      await processQuery(answer);
    } catch (error) {
      console.error("Error:", error.message);
    }

    askQuestion();
  });
}

askQuestion();
```

Run it:
```bash
node openai-client.js
```

## Best Practices

1. **API Key Security**: Never commit API keys to version control
2. **Rate Limiting**: Be aware of OpenAI API rate limits
3. **Error Handling**: Always handle API errors gracefully
4. **Token Usage**: Monitor token consumption for cost optimization
5. **Model Selection**: Choose appropriate model (GPT-4 for complex reasoning, GPT-3.5 for simple queries)

## Cost Optimization

- Use `gpt-3.5-turbo` for simple queries (cheaper)
- Use `gpt-4-turbo-preview` for complex reasoning
- Cache responses when possible
- Batch queries when appropriate

## Troubleshooting

### Issue: "Invalid API key"
**Solution**: Verify your OpenAI API key is correct and active

### Issue: "Rate limit exceeded"
**Solution**: Implement exponential backoff or reduce request frequency

### Issue: "Tool call failed"
**Solution**: Ensure MCP server is running and tools are properly configured

### Issue: "Connection refused"
**Solution**: Check that the MCP server is accessible and running

## Advanced Use Cases

1. **Dashboard Integration**: Build a web dashboard to visualize ECU data
2. **Automated Testing**: Use OpenAI to generate test cases for ECU functions
3. **Diagnostics**: Implement AI-assisted ECU diagnostics
4. **Documentation**: Auto-generate documentation from ECU metadata
5. **Voice Interface**: Add voice commands via OpenAI's Whisper API

## Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [MCP SDK Documentation](https://modelcontextprotocol.io/)

## Support

For issues with OpenAI integration:
1. Check OpenAI API status
2. Verify API key permissions
3. Review OpenAI usage dashboard
4. Check MCP server logs
5. Open an issue on GitHub
