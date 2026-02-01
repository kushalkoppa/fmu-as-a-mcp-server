#!/usr/bin/env node

/**
 * FMU MCP Server - Model Context Protocol Server for Virtual ECU
 * 
 * This server exposes the Virtual ECU FMU through MCP protocol,
 * allowing AI agents and LLMs to query ECU information and perform operations.
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";
import { VirtualECU } from "./virtual-ecu.js";

// Initialize the Virtual ECU
const virtualECU = new VirtualECU();

// Create MCP server
const server = new Server(
  {
    name: "fmu-mcp-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define available tools
const tools: Tool[] = [
  {
    name: "get_ecu_metadata",
    description: "Get complete metadata about the Virtual ECU FMU including software, version, interfaces, level, and domain",
    inputSchema: {
      type: "object",
      properties: {},
      required: [],
    },
  },
  {
    name: "get_ecu_software",
    description: "Get the software name of the Virtual ECU",
    inputSchema: {
      type: "object",
      properties: {},
      required: [],
    },
  },
  {
    name: "get_ecu_version",
    description: "Get the version of the Virtual ECU",
    inputSchema: {
      type: "object",
      properties: {},
      required: [],
    },
  },
  {
    name: "get_ecu_interfaces",
    description: "Get the list of available interfaces in the Virtual ECU",
    inputSchema: {
      type: "object",
      properties: {},
      required: [],
    },
  },
  {
    name: "get_ecu_level",
    description: "Get the level/capability of the Virtual ECU",
    inputSchema: {
      type: "object",
      properties: {},
      required: [],
    },
  },
  {
    name: "get_ecu_status",
    description: "Get the current operational status of the Virtual ECU",
    inputSchema: {
      type: "object",
      properties: {},
      required: [],
    },
  },
  {
    name: "get_ecu_domain",
    description: "Get the domain/application area of the Virtual ECU (e.g., Automotive, Industrial, HVAC)",
    inputSchema: {
      type: "object",
      properties: {},
      required: [],
    },
  },
  {
    name: "list_ecu_functions",
    description: "List all available functions in the Virtual ECU with their descriptions, parameters, and return types",
    inputSchema: {
      type: "object",
      properties: {},
      required: [],
    },
  },
  {
    name: "add_numbers",
    description: "Perform addition operation using the Virtual ECU's arithmetic unit",
    inputSchema: {
      type: "object",
      properties: {
        a: {
          type: "number",
          description: "First number to add",
        },
        b: {
          type: "number",
          description: "Second number to add",
        },
      },
      required: ["a", "b"],
    },
  },
];

// Handle list tools request
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools,
  };
});

// Handle tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "get_ecu_metadata": {
        const metadata = virtualECU.getMetadata();
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(metadata, null, 2),
            },
          ],
        };
      }

      case "get_ecu_software": {
        const software = virtualECU.getSoftware();
        return {
          content: [
            {
              type: "text",
              text: software,
            },
          ],
        };
      }

      case "get_ecu_version": {
        const version = virtualECU.getVersion();
        return {
          content: [
            {
              type: "text",
              text: version,
            },
          ],
        };
      }

      case "get_ecu_interfaces": {
        const interfaces = virtualECU.getInterfaces();
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(interfaces, null, 2),
            },
          ],
        };
      }

      case "get_ecu_level": {
        const level = virtualECU.getLevel();
        return {
          content: [
            {
              type: "text",
              text: level,
            },
          ],
        };
      }

      case "get_ecu_status": {
        const status = virtualECU.getStatus();
        return {
          content: [
            {
              type: "text",
              text: status,
            },
          ],
        };
      }

      case "get_ecu_domain": {
        const domain = virtualECU.getDomain();
        return {
          content: [
            {
              type: "text",
              text: domain,
            },
          ],
        };
      }

      case "list_ecu_functions": {
        const functions = virtualECU.listFunctions();
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(functions, null, 2),
            },
          ],
        };
      }

      case "add_numbers": {
        if (!args || typeof args.a !== "number" || typeof args.b !== "number") {
          throw new Error("Both 'a' and 'b' must be numbers");
        }
        const result = virtualECU.add(args.a, args.b);
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
