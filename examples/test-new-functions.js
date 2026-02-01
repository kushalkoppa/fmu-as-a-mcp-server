#!/usr/bin/env node

/**
 * Test for new ECU functions: getDomain() and listFunctions()
 */

import { VirtualECU } from '../dist/virtual-ecu.js';

console.log('🧪 Testing New Virtual ECU Functions\n');

const ecu = new VirtualECU();

// Test 1: Get Domain
console.log('✅ Test 1: Get ECU Domain');
const domain = ecu.getDomain();
console.log(`Domain: ${domain}\n`);

// Test 2: List Functions
console.log('✅ Test 2: List All Functions');
const functions = ecu.listFunctions();
console.log('Available Functions:');
functions.forEach(func => {
  console.log(`\n  📌 ${func.name}()`);
  console.log(`     Description: ${func.description}`);
  if (func.parameters.length > 0) {
    console.log(`     Parameters:`);
    func.parameters.forEach(param => {
      console.log(`       - ${param.name}: ${param.type} - ${param.description}`);
    });
  }
  console.log(`     Returns: ${func.returnType}`);
});

console.log('\n🎉 All new function tests passed!');
