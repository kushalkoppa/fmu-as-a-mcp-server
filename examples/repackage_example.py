#!/usr/bin/env python3
"""
Example: How to repackage an existing vendor FMU with MCP Server capabilities

This example demonstrates the complete workflow of:
1. Creating or using an existing vendor FMU
2. Repackaging it with MCP capabilities
3. Loading the repackaged FMU with FMPy
4. Accessing MCP variables

Compatible with FMUs from:
- Synopsys Platform Architect
- Vector CANoe/PREEvision
- dSPACE TargetLink/SystemDesk
- ETAS ASCET/COSYM
- Other FMI 2.0/3.0 compliant tools
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import fmu_repackager
sys.path.insert(0, str(Path(__file__).parent.parent))

from fmu_repackager import FMURepackager, create_sample_fmu


def example_basic_repackaging():
    """
    Example 1: Basic FMU repackaging
    """
    print("=" * 70)
    print("Example 1: Basic FMU Repackaging")
    print("=" * 70)
    
    # Step 1: Create a sample vendor FMU (simulate existing FMU)
    print("\n[Step 1] Creating sample vendor FMU...")
    vendor_fmu = "example_vendor_ecu.fmu"
    create_sample_fmu(vendor_fmu)
    print(f"✓ Created: {vendor_fmu}")
    
    # Step 2: Repackage the FMU with MCP capabilities
    print("\n[Step 2] Repackaging with MCP Server...")
    output_fmu = "example_vendor_ecu_mcp.fmu"
    
    repackager = FMURepackager(
        input_fmu=vendor_fmu,
        output_fmu=output_fmu,
        mcp_config={
            "description": "Example ECU with MCP integration",
            "capabilities": {
                "tools": True,
                "resources": True
            }
        }
    )
    
    repackaged_path = repackager.repackage()
    print(f"✓ Repackaged FMU saved to: {repackaged_path}")
    
    # Step 3: Verify the repackaged FMU
    print("\n[Step 3] Verifying repackaged FMU...")
    import zipfile
    with zipfile.ZipFile(output_fmu, 'r') as z:
        files = z.namelist()
        print(f"✓ FMU contains {len(files)} files:")
        for f in files:
            print(f"  - {f}")
    
    # Cleanup
    print("\n[Cleanup] Removing example files...")
    os.remove(vendor_fmu)
    os.remove(output_fmu)
    print("✓ Cleanup complete")
    
    print("\n" + "=" * 70)
    print("Example 1 completed successfully!")
    print("=" * 70)


def example_fmpy_integration():
    """
    Example 2: Load repackaged FMU with FMPy
    """
    print("\n\n" + "=" * 70)
    print("Example 2: FMPy Integration")
    print("=" * 70)
    
    try:
        from fmpy import read_model_description
        fmpy_available = True
    except ImportError:
        print("\n⚠ FMPy not installed. Install with: pip install fmpy")
        fmpy_available = False
    
    if not fmpy_available:
        print("Skipping FMPy integration example")
        return
    
    # Create and repackage FMU
    print("\n[Step 1] Creating and repackaging FMU...")
    vendor_fmu = "example_fmpy_test.fmu"
    output_fmu = "example_fmpy_test_mcp.fmu"
    
    create_sample_fmu(vendor_fmu)
    repackager = FMURepackager(vendor_fmu, output_fmu)
    repackager.repackage()
    
    # Load with FMPy
    print("\n[Step 2] Loading repackaged FMU with FMPy...")
    model_desc = read_model_description(output_fmu)
    
    print(f"✓ Model Name: {model_desc.modelName}")
    print(f"✓ FMI Version: {model_desc.fmiVersion}")
    print(f"✓ GUID: {model_desc.guid}")
    
    print(f"\n✓ Model Variables ({len(model_desc.modelVariables)} total):")
    for var in model_desc.modelVariables:
        print(f"  - {var.name} ({var.type}): {var.description or 'No description'}")
    
    # Find MCP variables
    print("\n[Step 3] Checking MCP variables...")
    mcp_vars = [v for v in model_desc.modelVariables if 'mcp' in v.name.lower()]
    if mcp_vars:
        print(f"✓ Found {len(mcp_vars)} MCP variables:")
        for var in mcp_vars:
            print(f"  - {var.name}: {var.description}")
    else:
        print("⚠ No MCP variables found")
    
    # Cleanup
    print("\n[Cleanup] Removing example files...")
    os.remove(vendor_fmu)
    os.remove(output_fmu)
    print("✓ Cleanup complete")
    
    print("\n" + "=" * 70)
    print("Example 2 completed successfully!")
    print("=" * 70)


def example_custom_configuration():
    """
    Example 3: Repackaging with custom MCP configuration
    """
    print("\n\n" + "=" * 70)
    print("Example 3: Custom MCP Configuration")
    print("=" * 70)
    
    # Create custom MCP configuration
    print("\n[Step 1] Creating custom MCP configuration...")
    custom_config = {
        "server_name": "automotive-ecu-mcp",
        "description": "Automotive ECU with advanced MCP capabilities",
        "capabilities": {
            "tools": True,
            "resources": True,
            "prompts": True
        },
        "custom_metadata": {
            "vendor": "Example Automotive",
            "model": "ECU-2024",
            "application": "Engine Control"
        }
    }
    
    print("✓ Custom configuration:")
    import json
    print(json.dumps(custom_config, indent=2))
    
    # Repackage with custom config
    print("\n[Step 2] Repackaging with custom configuration...")
    vendor_fmu = "example_custom_config.fmu"
    output_fmu = "example_custom_config_mcp.fmu"
    
    create_sample_fmu(vendor_fmu)
    repackager = FMURepackager(
        input_fmu=vendor_fmu,
        output_fmu=output_fmu,
        mcp_config=custom_config
    )
    repackager.repackage()
    
    # Verify custom config was applied
    print("\n[Step 3] Verifying custom configuration...")
    import zipfile
    with zipfile.ZipFile(output_fmu, 'r') as z:
        config_content = z.read('resources/mcp_config.json').decode('utf-8')
        loaded_config = json.loads(config_content)
        
        print("✓ MCP configuration in repackaged FMU:")
        print(f"  - Server Name: {loaded_config.get('server_name')}")
        print(f"  - Description: {loaded_config.get('description')}")
        print(f"  - Custom Metadata: {loaded_config.get('custom_metadata')}")
    
    # Cleanup
    print("\n[Cleanup] Removing example files...")
    os.remove(vendor_fmu)
    os.remove(output_fmu)
    print("✓ Cleanup complete")
    
    print("\n" + "=" * 70)
    print("Example 3 completed successfully!")
    print("=" * 70)


def main():
    """
    Run all examples
    """
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║        FMU Repackaging Tool - Complete Usage Examples               ║
║                                                                      ║
║  Demonstrates how to add MCP Server capabilities to existing FMUs   ║
║  from vendors like Synopsys, Vector, dSPACE, ETAS                   ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Run all examples
        example_basic_repackaging()
        example_fmpy_integration()
        example_custom_configuration()
        
        print("\n\n" + "=" * 70)
        print("🎉 All examples completed successfully!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Use your own vendor FMU instead of the sample")
        print("2. Load the repackaged FMU in FMPy for simulation")
        print("3. Query the FMU using MCP tools via AI agents")
        print("4. Integrate with GitHub Copilot or OpenAI")
        print("\nFor more information, see DOCUMENTATION.md")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
