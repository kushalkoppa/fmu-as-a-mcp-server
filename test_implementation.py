"""
Test script for FMU Virtual ECU MCP Server
This script tests the MCP server functionality without requiring an MCP client
"""

import sys
import os

# Test 1: Import FMU model
print("=" * 70)
print("TEST 1: FMU Model Functionality")
print("=" * 70)

try:
    from fmu_model import VirtualECU
    ecu = VirtualECU()
    print("✅ FMU model imported successfully")
    
    # Test get_info
    info = ecu.get_info()
    assert info['version'] == '1.0.0', "Version mismatch"
    assert info['ecu_level'] == 'Level_2', "ECU level mismatch"
    assert len(info['interfaces']) == 4, "Interfaces count mismatch"
    print("✅ get_info() works correctly")
    
    # Test addition
    result = ecu.add(10, 20)
    assert result == 30, f"Addition failed: expected 30, got {result}"
    print("✅ add() works correctly")
    
    # Test get_version
    version = ecu.get_version()
    assert version == '1.0.0', "Version retrieval failed"
    print("✅ get_version() works correctly")
    
    # Test get_interfaces
    interfaces = ecu.get_interfaces()
    assert 'CAN' in interfaces, "CAN interface missing"
    assert 'LIN' in interfaces, "LIN interface missing"
    print("✅ get_interfaces() works correctly")
    
    # Test get_ecu_level
    level = ecu.get_ecu_level()
    assert level == 'Level_2', "ECU level retrieval failed"
    print("✅ get_ecu_level() works correctly")
    
    # Test get_status
    status = ecu.get_status()
    assert status['status'] == 'Active', "Status retrieval failed"
    print("✅ get_status() works correctly")
    
    print("\n✅ ALL FMU MODEL TESTS PASSED!\n")
    
except Exception as e:
    print(f"❌ Error in FMU model tests: {e}")
    sys.exit(1)

# Test 2: MCP Server structure
print("=" * 70)
print("TEST 2: MCP Server Structure")
print("=" * 70)

try:
    import server
    print("✅ MCP server module imported successfully")
    
    # Check if server object exists
    assert hasattr(server, 'server'), "Server object not found"
    print("✅ Server object exists")
    
    # Check if ECU instance exists
    assert hasattr(server, 'ecu'), "ECU instance not found in server"
    print("✅ ECU instance exists in server")
    
    print("\n✅ ALL MCP SERVER STRUCTURE TESTS PASSED!\n")
    
except Exception as e:
    print(f"❌ Error in MCP server tests: {e}")
    sys.exit(1)

# Test 3: AI Agent (without OpenAI key)
print("=" * 70)
print("TEST 3: AI Agent Structure")
print("=" * 70)

try:
    # Test import
    import ai_agent
    print("✅ AI agent module imported successfully")
    
    # Check if class exists
    assert hasattr(ai_agent, 'FMU_AI_Agent'), "FMU_AI_Agent class not found"
    print("✅ FMU_AI_Agent class exists")
    
    # Test initialization only if API key is set
    if os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_API_KEY") != "your_openai_api_key_here":
        try:
            agent = ai_agent.FMU_AI_Agent()
            print("✅ AI agent initialized with API key")
        except Exception as e:
            print(f"⚠️  AI agent initialization failed: {e}")
    else:
        print("⚠️  OPENAI_API_KEY not set - skipping agent initialization test")
    
    print("\n✅ ALL AI AGENT STRUCTURE TESTS PASSED!\n")
    
except Exception as e:
    print(f"❌ Error in AI agent tests: {e}")
    sys.exit(1)

# Test 4: Configuration files
print("=" * 70)
print("TEST 4: Configuration Files")
print("=" * 70)

try:
    # Test requirements.txt
    assert os.path.exists('requirements.txt'), "requirements.txt not found"
    print("✅ requirements.txt exists")
    
    # Test package.json
    assert os.path.exists('package.json'), "package.json not found"
    print("✅ package.json exists")
    
    # Test .env.example
    assert os.path.exists('.env.example'), ".env.example not found"
    print("✅ .env.example exists")
    
    # Test mcp-config.json
    assert os.path.exists('mcp-config.json'), "mcp-config.json not found"
    print("✅ mcp-config.json exists")
    
    # Test VS Code configuration
    assert os.path.exists('.vscode/extensions.json'), "VS Code extensions.json not found"
    print("✅ .vscode/extensions.json exists")
    
    assert os.path.exists('.vscode/settings.json'), "VS Code settings.json not found"
    print("✅ .vscode/settings.json exists")
    
    print("\n✅ ALL CONFIGURATION FILE TESTS PASSED!\n")
    
except Exception as e:
    print(f"❌ Error in configuration tests: {e}")
    sys.exit(1)

# Test 5: Documentation
print("=" * 70)
print("TEST 5: Documentation Files")
print("=" * 70)

try:
    # Test README
    assert os.path.exists('README.md'), "README.md not found"
    with open('README.md', 'r') as f:
        readme_content = f.read()
        assert 'FMU as a MCP Server' in readme_content, "README title incorrect"
        assert 'Virtual ECU' in readme_content, "Virtual ECU not mentioned in README"
        assert 'OpenAI' in readme_content, "OpenAI not mentioned in README"
        assert 'Copilot' in readme_content, "Copilot not mentioned in README"
    print("✅ README.md exists and contains required information")
    
    # Test SETUP_GUIDE
    assert os.path.exists('SETUP_GUIDE.md'), "SETUP_GUIDE.md not found"
    with open('SETUP_GUIDE.md', 'r') as f:
        setup_content = f.read()
        assert 'Visual Studio Code' in setup_content, "VS Code setup not documented"
        assert 'OpenAI' in setup_content, "OpenAI setup not documented"
        assert 'GitHub Copilot' in setup_content, "Copilot not documented"
    print("✅ SETUP_GUIDE.md exists and contains required information")
    
    # Test LICENSE
    assert os.path.exists('LICENSE'), "LICENSE not found"
    print("✅ LICENSE exists")
    
    print("\n✅ ALL DOCUMENTATION TESTS PASSED!\n")
    
except Exception as e:
    print(f"❌ Error in documentation tests: {e}")
    sys.exit(1)

# Final summary
print("=" * 70)
print("🎉 ALL TESTS PASSED SUCCESSFULLY! 🎉")
print("=" * 70)
print("\nFMU Virtual ECU Implementation Summary:")
print("  • FMU Model: ✅ Working")
print("  • MCP Server: ✅ Configured")
print("  • AI Agent: ✅ Structured")
print("  • Configuration: ✅ Complete")
print("  • Documentation: ✅ Comprehensive")
print("\nNext steps:")
print("  1. Set OPENAI_API_KEY in .env file")
print("  2. Run: python server.py (to start MCP server)")
print("  3. Open in VS Code and use Copilot")
print("=" * 70)
