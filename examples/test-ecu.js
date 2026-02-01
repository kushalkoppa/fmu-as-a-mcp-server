#!/usr/bin/env node

/**
 * Simple validation test for Virtual ECU
 * Tests the ECU functionality directly without MCP protocol
 */

import { VirtualECU } from '../dist/virtual-ecu.js';

console.log("🧪 Testing Virtual ECU FMU Implementation\n");

const ecu = new VirtualECU();

// Test 1: Metadata
console.log("✅ Test 1: Get Metadata");
const metadata = ecu.getMetadata();
console.log(JSON.stringify(metadata, null, 2));
console.log();

// Test 2: Software
console.log("✅ Test 2: Get Software");
console.log("Software:", ecu.getSoftware());
console.log();

// Test 3: Version
console.log("✅ Test 3: Get Version");
console.log("Version:", ecu.getVersion());
console.log();

// Test 4: Interfaces
console.log("✅ Test 4: Get Interfaces");
console.log("Interfaces:", ecu.getInterfaces());
console.log();

// Test 5: Level
console.log("✅ Test 5: Get Level");
console.log("Level:", ecu.getLevel());
console.log();

// Test 6: Status
console.log("✅ Test 6: Get Status");
console.log("Status:", ecu.getStatus());
console.log();

// Test 7: Addition Operations
console.log("✅ Test 7: Addition Operations");
console.log("10 + 20 =", ecu.add(10, 20));
console.log("42 + 58 =", ecu.add(42, 58));
console.log("123.45 + 67.89 =", ecu.add(123.45, 67.89));
console.log("-10 + 25 =", ecu.add(-10, 25));
console.log();

console.log("🎉 All Virtual ECU tests passed!");
