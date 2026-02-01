#!/usr/bin/env node

/**
 * Simple Test Client for FMU MCP Server
 * 
 * This client demonstrates how to connect to and interact with
 * the Virtual ECU FMU through the MCP protocol.
 */

import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

async function main() {
  console.log("🚗 Starting FMU MCP Client...\n");

  // Create transport to connect to MCP server
  const transport = new StdioClientTransport({
    command: 'node',
    args: ['../dist/index.js']
  });

  // Create client
  const client = new Client({
    name: 'fmu-test-client',
    version: '1.0.0'
  }, {
    capabilities: {}
  });

  try {
    // Connect to server
    await client.connect(transport);
    console.log("✅ Connected to FMU MCP Server\n");

    // List available tools
    console.log("📋 Available Tools:");
    const { tools } = await client.listTools();
    tools.forEach(tool => {
      console.log(`  - ${tool.name}: ${tool.description}`);
    });
    console.log();

    // Test 1: Get ECU Metadata
    console.log("🔍 Test 1: Getting ECU Metadata");
    const metadataResult = await client.callTool({
      name: 'get_ecu_metadata',
      arguments: {}
    });
    console.log("Result:", metadataResult.content[0].text);
    console.log();

    // Test 2: Get ECU Software
    console.log("🔍 Test 2: Getting ECU Software");
    const softwareResult = await client.callTool({
      name: 'get_ecu_software',
      arguments: {}
    });
    console.log("Software:", softwareResult.content[0].text);
    console.log();

    // Test 3: Get ECU Version
    console.log("🔍 Test 3: Getting ECU Version");
    const versionResult = await client.callTool({
      name: 'get_ecu_version',
      arguments: {}
    });
    console.log("Version:", versionResult.content[0].text);
    console.log();

    // Test 4: Get ECU Interfaces
    console.log("🔍 Test 4: Getting ECU Interfaces");
    const interfacesResult = await client.callTool({
      name: 'get_ecu_interfaces',
      arguments: {}
    });
    console.log("Interfaces:", interfacesResult.content[0].text);
    console.log();

    // Test 5: Get ECU Level
    console.log("🔍 Test 5: Getting ECU Level");
    const levelResult = await client.callTool({
      name: 'get_ecu_level',
      arguments: {}
    });
    console.log("Level:", levelResult.content[0].text);
    console.log();

    // Test 6: Get ECU Status
    console.log("🔍 Test 6: Getting ECU Status");
    const statusResult = await client.callTool({
      name: 'get_ecu_status',
      arguments: {}
    });
    console.log("Status:", statusResult.content[0].text);
    console.log();

    // Test 7: Addition Operation
    console.log("🔍 Test 7: Testing Addition Operation");
    const addResult1 = await client.callTool({
      name: 'add_numbers',
      arguments: { a: 10, b: 20 }
    });
    console.log(addResult1.content[0].text);

    const addResult2 = await client.callTool({
      name: 'add_numbers',
      arguments: { a: 42, b: 58 }
    });
    console.log(addResult2.content[0].text);

    const addResult3 = await client.callTool({
      name: 'add_numbers',
      arguments: { a: 123.45, b: 67.89 }
    });
    console.log(addResult3.content[0].text);
    console.log();

    console.log("✨ All tests completed successfully!");

  } catch (error) {
    console.error("❌ Error:", error);
    process.exit(1);
  } finally {
    // Close connection
    await client.close();
    console.log("\n👋 Disconnected from FMU MCP Server");
  }
}

main();
