# FMU Repackaging Examples

This directory contains examples demonstrating how to use the FMU repackaging tool to add MCP Server capabilities to existing FMUs.

## Available Examples

### `repackage_example.py`

Comprehensive examples showing:

1. **Basic FMU Repackaging**
   - Create a sample vendor FMU
   - Repackage with MCP capabilities
   - Verify the repackaged FMU structure

2. **FMPy Integration**
   - Load repackaged FMU with FMPy
   - Query FMU metadata and variables
   - Access MCP-specific variables

3. **Custom MCP Configuration**
   - Define custom MCP settings
   - Apply configuration during repackaging
   - Verify custom configuration in output

## Running the Examples

### Prerequisites

```bash
# Install Python dependencies
pip install fmpy lxml

# Optional: For full FMPy functionality
pip install numpy matplotlib
```

### Run All Examples

```bash
python examples/repackage_example.py
```

### Expected Output

```
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║        FMU Repackaging Tool - Complete Usage Examples               ║
║                                                                      ║
║  Demonstrates how to add MCP Server capabilities to existing FMUs   ║
║  from vendors like Synopsys, Vector, dSPACE, ETAS                   ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

======================================================================
Example 1: Basic FMU Repackaging
======================================================================

[Step 1] Creating sample vendor FMU...
✓ Created: example_vendor_ecu.fmu

[Step 2] Repackaging with MCP Server...
✓ Repackaged FMU saved to: example_vendor_ecu_mcp.fmu

[Step 3] Verifying repackaged FMU...
✓ FMU contains 5 files:
  - modelDescription.xml
  - resources/MCP_README.txt
  - resources/mcp_wrapper.py
  - resources/mcp_config.json
  - binaries/linux64/VendorECU_Controller.so

======================================================================
Example 1 completed successfully!
======================================================================
```

## Using Your Own FMU

To repackage your own vendor FMU:

```python
from fmu_repackager import FMURepackager

# Basic repackaging
repackager = FMURepackager(
    input_fmu="your_vendor_fmu.fmu",
    output_fmu="your_vendor_fmu_mcp.fmu"
)
repackager.repackage()

# With custom configuration
repackager = FMURepackager(
    input_fmu="your_vendor_fmu.fmu",
    output_fmu="your_vendor_fmu_mcp.fmu",
    mcp_config={
        "server_name": "your-custom-name",
        "description": "Custom description",
        "custom_metadata": {
            "vendor": "Your Company",
            "model": "YourModel"
        }
    }
)
repackager.repackage()
```

## Command Line Usage

You can also use the tool directly from command line:

```bash
# Create a sample FMU for testing
python fmu_repackager.py --create-sample test.fmu

# Repackage an existing FMU
python fmu_repackager.py --input vendor.fmu --output vendor_mcp.fmu

# Repackage with custom config
python fmu_repackager.py \
    --input vendor.fmu \
    --output vendor_mcp.fmu \
    --mcp-config custom_config.json
```

## Vendor-Specific Examples

### Synopsys Platform Architect

```bash
# Export your model from Synopsys as FMU
# Then repackage:
python fmu_repackager.py \
    --input synopsys_model.fmu \
    --output synopsys_model_mcp.fmu
```

### Vector CANoe

```bash
# Export RT model from CANoe as FMU
# Then repackage:
python fmu_repackager.py \
    --input vector_rt_model.fmu \
    --output vector_rt_model_mcp.fmu
```

### dSPACE TargetLink

```bash
# Export TargetLink model as FMU
# Then repackage:
python fmu_repackager.py \
    --input dspace_controller.fmu \
    --output dspace_controller_mcp.fmu
```

### ETAS ASCET

```bash
# Export ASCET model as FMU
# Then repackage:
python fmu_repackager.py \
    --input etas_component.fmu \
    --output etas_component_mcp.fmu
```

## Loading Repackaged FMUs

### With FMPy

```python
from fmpy import read_model_description, simulate_fmu

# Read model description
model_desc = read_model_description('your_vendor_mcp.fmu')
print(f"Model: {model_desc.modelName}")
print(f"FMI Version: {model_desc.fmiVersion}")

# List variables including MCP variables
for var in model_desc.modelVariables:
    if 'mcp' in var.name.lower():
        print(f"MCP Variable: {var.name}")

# Simulate the FMU
result = simulate_fmu('your_vendor_mcp.fmu')
```

### Verifying MCP Integration

```python
import zipfile
import json

# Check MCP components in repackaged FMU
with zipfile.ZipFile('your_vendor_mcp.fmu', 'r') as z:
    # Read MCP configuration
    mcp_config = json.loads(z.read('resources/mcp_config.json'))
    print(f"MCP Server: {mcp_config['server_name']}")
    print(f"Version: {mcp_config['version']}")
    
    # Verify MCP variables in modelDescription.xml
    model_desc = z.read('modelDescription.xml').decode('utf-8')
    assert 'mcp_server_status' in model_desc
    assert 'mcp_server_version' in model_desc
    print("✓ MCP integration verified")
```

## Troubleshooting

### Issue: Import Error

```
ModuleNotFoundError: No module named 'fmu_repackager'
```

**Solution**: Run examples from the repository root:
```bash
cd /path/to/fmu-as-a-mcp-server
python examples/repackage_example.py
```

### Issue: FMPy Not Found

```
⚠ FMPy not installed. Install with: pip install fmpy
```

**Solution**: Install FMPy:
```bash
pip install fmpy
```

### Issue: Invalid FMU

```
Error: modelDescription.xml not found in FMU
```

**Solution**: Ensure your input file is a valid FMU (ZIP file with modelDescription.xml at root)

## Next Steps

1. Review the [complete documentation](../DOCUMENTATION.md) for detailed information
2. Try repackaging your own vendor FMUs
3. Load repackaged FMUs in FMPy for simulation
4. Integrate with AI agents via MCP protocol
5. Query FMU metadata using GitHub Copilot or OpenAI

## Support

For issues or questions:
- Open an issue on GitHub
- Check the [troubleshooting guide](../DOCUMENTATION.md#troubleshooting)
- Review the [CI/CD pipeline](.github/workflows/ci.yml) for automated testing examples
