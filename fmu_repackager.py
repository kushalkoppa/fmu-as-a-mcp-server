"""
FMU Repackager - Tool to add MCP Server to existing FMUs

This tool takes an existing FMU (created by tools like Synopsys/Vector/dSPACE/ETAS)
and repackages it with an MCP Server wrapper, making it compatible with FMPy
and enabling AI agent integration.

Usage:
    python fmu_repackager.py --input existing.fmu --output repackaged.fmu

Features:
- Extracts existing FMU structure
- Preserves original FMU binaries and resources
- Adds MCP Server wrapper layer
- Updates modelDescription.xml with new variables
- Repackages as FMI 2.0/3.0 compatible FMU
- Compatible with FMPy for loading and simulation
"""

import os
import sys
import zipfile
import shutil
import xml.etree.ElementTree as ET
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import tempfile
from datetime import datetime, timezone


class FMURepackager:
    """
    Main class for repackaging existing FMUs with MCP Server capabilities
    """
    
    def __init__(self, input_fmu: str, output_fmu: str, mcp_config: Optional[Dict] = None):
        """
        Initialize the FMU repackager
        
        Args:
            input_fmu: Path to the existing FMU file
            output_fmu: Path where the repackaged FMU will be saved
            mcp_config: Optional MCP server configuration
        """
        self.input_fmu = Path(input_fmu)
        self.output_fmu = Path(output_fmu)
        self.mcp_config = mcp_config or {}
        self.temp_dir = None
        self.model_description = None
        self.fmi_version = None
        
        if not self.input_fmu.exists():
            raise FileNotFoundError(f"Input FMU not found: {input_fmu}")
    
    def extract_fmu(self) -> Path:
        """
        Extract the FMU to a temporary directory
        
        Returns:
            Path to the extracted FMU directory
        """
        print(f"[1/6] Extracting FMU: {self.input_fmu.name}")
        
        self.temp_dir = Path(tempfile.mkdtemp(prefix="fmu_repackage_"))
        
        try:
            with zipfile.ZipFile(self.input_fmu, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
            print(f"  ✓ Extracted to: {self.temp_dir}")
            return self.temp_dir
        except Exception as e:
            print(f"  ✗ Error extracting FMU: {e}")
            raise
    
    def parse_model_description(self) -> ET.ElementTree:
        """
        Parse the modelDescription.xml file
        
        Returns:
            ElementTree of the model description
        """
        print("[2/6] Parsing modelDescription.xml")
        
        model_desc_path = self.temp_dir / "modelDescription.xml"
        
        if not model_desc_path.exists():
            raise FileNotFoundError("modelDescription.xml not found in FMU")
        
        try:
            tree = ET.parse(model_desc_path)
            root = tree.getroot()
            
            # Detect FMI version
            self.fmi_version = root.get('fmiVersion', '2.0')
            model_name = root.get('modelName', 'Unknown')
            guid = root.get('guid', 'Unknown')
            
            print(f"  ✓ FMI Version: {self.fmi_version}")
            print(f"  ✓ Model Name: {model_name}")
            print(f"  ✓ GUID: {guid}")
            
            self.model_description = tree
            return tree
        except Exception as e:
            print(f"  ✗ Error parsing modelDescription.xml: {e}")
            raise
    
    def add_mcp_variables(self):
        """
        Add MCP-related variables to the model description
        """
        print("[3/6] Adding MCP Server variables")
        
        root = self.model_description.getroot()
        
        # Find or create ModelVariables section
        model_vars = root.find('ModelVariables')
        if model_vars is None:
            model_vars = ET.SubElement(root, 'ModelVariables')
        
        # Get the highest existing value reference
        max_value_ref = 0
        for var in model_vars.findall('ScalarVariable'):
            vr = var.get('valueReference', '0')
            max_value_ref = max(max_value_ref, int(vr))
        
        # Add MCP status variable
        mcp_status_var = ET.SubElement(model_vars, 'ScalarVariable')
        mcp_status_var.set('name', 'mcp_server_status')
        mcp_status_var.set('valueReference', str(max_value_ref + 1))
        mcp_status_var.set('description', 'MCP Server operational status')
        mcp_status_var.set('causality', 'output')
        mcp_status_var.set('variability', 'discrete')
        
        string_type = ET.SubElement(mcp_status_var, 'String')
        string_type.set('start', 'active')
        
        # Add MCP version variable
        mcp_version_var = ET.SubElement(model_vars, 'ScalarVariable')
        mcp_version_var.set('name', 'mcp_server_version')
        mcp_version_var.set('valueReference', str(max_value_ref + 2))
        mcp_version_var.set('description', 'MCP Server version')
        mcp_version_var.set('causality', 'parameter')
        mcp_version_var.set('variability', 'fixed')
        
        string_type = ET.SubElement(mcp_version_var, 'String')
        string_type.set('start', '1.0.0')
        
        print(f"  ✓ Added MCP status variable (valueReference: {max_value_ref + 1})")
        print(f"  ✓ Added MCP version variable (valueReference: {max_value_ref + 2})")
    
    def add_mcp_wrapper(self):
        """
        Add MCP server wrapper files to the FMU
        """
        print("[4/6] Adding MCP Server wrapper")
        
        # Create resources directory if it doesn't exist
        resources_dir = self.temp_dir / "resources"
        resources_dir.mkdir(exist_ok=True)
        
        # Create MCP configuration file
        mcp_config_path = resources_dir / "mcp_config.json"
        mcp_config_data = {
            "enabled": True,
            "version": "1.0.0",
            "server_name": "fmu-mcp-wrapper",
            "capabilities": {
                "tools": True,
                "resources": False,
                "prompts": False
            },
            "original_fmu": str(self.input_fmu.name),
            "repackaged_timestamp": datetime.now(timezone.utc).isoformat()
        }
        mcp_config_data.update(self.mcp_config)
        
        with open(mcp_config_path, 'w') as f:
            json.dump(mcp_config_data, f, indent=2)
        
        print(f"  ✓ Created MCP config: {mcp_config_path.name}")
        
        # Create MCP wrapper script
        wrapper_script_path = resources_dir / "mcp_wrapper.py"
        wrapper_script = '''"""
MCP Server Wrapper for FMU
This script provides MCP server functionality for the FMU
"""

import json
import sys
from pathlib import Path

class MCPWrapper:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
    
    def get_status(self):
        return {
            "status": "active",
            "version": self.config.get("version", "1.0.0"),
            "server_name": self.config.get("server_name", "fmu-mcp-wrapper")
        }
    
    def list_tools(self):
        return [
            {
                "name": "get_fmu_info",
                "description": "Get information about the FMU",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        ]

if __name__ == "__main__":
    config_path = Path(__file__).parent / "mcp_config.json"
    wrapper = MCPWrapper(config_path)
    print(json.dumps(wrapper.get_status(), indent=2))
'''
        
        with open(wrapper_script_path, 'w') as f:
            f.write(wrapper_script)
        
        print(f"  ✓ Created MCP wrapper: {wrapper_script_path.name}")
        
        # Create README for the MCP integration
        readme_path = resources_dir / "MCP_README.txt"
        readme_content = f"""MCP Server Integration for FMU

This FMU has been repackaged with MCP (Model Context Protocol) Server capabilities.

Original FMU: {self.input_fmu.name}
Repackaged: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC
FMI Version: {self.fmi_version}

MCP Server Features:
- Query FMU metadata through natural language
- AI agent integration via MCP protocol
- Compatible with FMPy and other FMI tools

Loading in FMPy:
```python
from fmpy import simulate_fmu

result = simulate_fmu('{self.output_fmu.name}')
```

MCP Server Usage:
The MCP server wrapper is located in resources/mcp_wrapper.py
Configuration is in resources/mcp_config.json

For more information, visit:
https://github.com/kushalkoppa/fmu-as-a-mcp-server
"""
        
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        print(f"  ✓ Created MCP README: {readme_path.name}")
    
    def update_model_description(self):
        """
        Update modelDescription.xml with MCP information
        """
        print("[5/6] Updating modelDescription.xml")
        
        root = self.model_description.getroot()
        
        # Update description to indicate MCP integration
        orig_description = root.get('description', '')
        new_description = f"{orig_description} [MCP-Enhanced]"
        root.set('description', new_description)
        
        # Add generation tool annotation
        root.set('generationTool', 'FMU-MCP-Repackager v1.0.0')
        root.set('generationDateAndTime', datetime.now(timezone.utc).isoformat())
        
        # Save updated modelDescription.xml
        model_desc_path = self.temp_dir / "modelDescription.xml"
        
        # Pretty print XML with proper indentation
        self._indent_xml(root)
        
        tree = ET.ElementTree(root)
        tree.write(model_desc_path, encoding='utf-8', xml_declaration=True)
        
        print(f"  ✓ Updated modelDescription.xml")
    
    def _indent_xml(self, elem, level=0):
        """
        Add pretty-print indentation to XML elements
        """
        indent = "\n" + "  " * level
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = indent + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = indent
            for child in elem:
                self._indent_xml(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = indent
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = indent
    
    def repackage_fmu(self) -> Path:
        """
        Repackage the FMU with MCP components
        
        Returns:
            Path to the repackaged FMU
        """
        print(f"[6/6] Repackaging FMU: {self.output_fmu.name}")
        
        # Create output directory if it doesn't exist
        self.output_fmu.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Create a zip file with the FMU contents
            with zipfile.ZipFile(self.output_fmu, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(self.temp_dir):
                    for file in files:
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(self.temp_dir)
                        zipf.write(file_path, arcname)
            
            print(f"  ✓ Created repackaged FMU: {self.output_fmu}")
            print(f"  ✓ Size: {self.output_fmu.stat().st_size / 1024:.2f} KB")
            return self.output_fmu
            
        except Exception as e:
            print(f"  ✗ Error repackaging FMU: {e}")
            raise
    
    def cleanup(self):
        """
        Clean up temporary files
        """
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            print(f"  ✓ Cleaned up temporary files")
    
    def repackage(self) -> Path:
        """
        Main method to perform the complete repackaging process
        
        Returns:
            Path to the repackaged FMU
        """
        try:
            print("=" * 60)
            print("FMU MCP Server Repackaging Tool")
            print("=" * 60)
            
            # Step 1: Extract FMU
            self.extract_fmu()
            
            # Step 2: Parse model description
            self.parse_model_description()
            
            # Step 3: Add MCP variables
            self.add_mcp_variables()
            
            # Step 4: Add MCP wrapper files
            self.add_mcp_wrapper()
            
            # Step 5: Update model description
            self.update_model_description()
            
            # Step 6: Repackage FMU
            output_path = self.repackage_fmu()
            
            print("=" * 60)
            print("✓ Repackaging completed successfully!")
            print("=" * 60)
            print(f"Input FMU:  {self.input_fmu}")
            print(f"Output FMU: {self.output_fmu}")
            print(f"\nThe repackaged FMU can now be loaded in FMPy:")
            print(f"  from fmpy import simulate_fmu")
            print(f"  simulate_fmu('{self.output_fmu}')")
            
            return output_path
            
        except Exception as e:
            print(f"\n✗ Repackaging failed: {e}")
            raise
        finally:
            self.cleanup()


def create_sample_fmu(output_path: str = "sample_vendor.fmu"):
    """
    Create a sample FMU for testing purposes
    This simulates an FMU created by vendor tools like Synopsys/Vector/dSPACE/ETAS
    """
    print("\nCreating sample vendor FMU for testing...")
    
    temp_dir = Path(tempfile.mkdtemp(prefix="sample_fmu_"))
    
    try:
        # Create modelDescription.xml
        model_desc = f'''<?xml version="1.0" encoding="UTF-8"?>
<fmiModelDescription
    fmiVersion="2.0"
    modelName="VendorECU_Controller"
    guid="{{12345678-1234-1234-1234-123456789abc}}"
    description="Sample ECU Controller from Vendor Tools"
    generationTool="Vendor FMU Export Tool v3.2.1"
    generationDateAndTime="2024-01-15T10:30:00Z"
    variableNamingConvention="structured"
    numberOfEventIndicators="0">
    
    <CoSimulation
        modelIdentifier="VendorECU_Controller"
        canHandleVariableCommunicationStepSize="true"
        canInterpolateInputs="false"
        maxOutputDerivativeOrder="0"
        canGetAndSetFMUstate="false"
        canSerializeFMUstate="false"/>
    
    <ModelVariables>
        <ScalarVariable name="input_voltage" valueReference="0" description="Input voltage signal" causality="input" variability="continuous">
            <Real start="0.0" unit="V"/>
        </ScalarVariable>
        <ScalarVariable name="output_current" valueReference="1" description="Output current" causality="output" variability="continuous">
            <Real start="0.0" unit="A"/>
        </ScalarVariable>
        <ScalarVariable name="controller_mode" valueReference="2" description="Controller operating mode" causality="parameter" variability="fixed">
            <Integer start="1"/>
        </ScalarVariable>
    </ModelVariables>
    
    <ModelStructure>
        <Outputs>
            <Unknown index="2"/>
        </Outputs>
    </ModelStructure>
    
</fmiModelDescription>'''
        
        model_desc_path = temp_dir / "modelDescription.xml"
        with open(model_desc_path, 'w') as f:
            f.write(model_desc)
        
        # Create binaries directory structure
        binaries_dir = temp_dir / "binaries" / "linux64"
        binaries_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a placeholder binary file
        placeholder_binary = binaries_dir / "VendorECU_Controller.so"
        with open(placeholder_binary, 'w') as f:
            f.write("# Placeholder binary - replace with actual FMU binary\n")
        
        # Create resources directory
        resources_dir = temp_dir / "resources"
        resources_dir.mkdir(exist_ok=True)
        
        # Package as FMU
        output = Path(output_path)
        with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(temp_dir)
                    zipf.write(file_path, arcname)
        
        print(f"✓ Created sample FMU: {output}")
        return output
        
    finally:
        shutil.rmtree(temp_dir)


def main():
    """
    Command-line interface for the FMU repackager
    """
    parser = argparse.ArgumentParser(
        description="FMU MCP Server Repackaging Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Repackage an existing FMU
  python fmu_repackager.py --input vendor.fmu --output vendor_mcp.fmu
  
  # Create a sample FMU for testing
  python fmu_repackager.py --create-sample sample_vendor.fmu
  
  # Repackage with custom MCP configuration
  python fmu_repackager.py --input vendor.fmu --output vendor_mcp.fmu --mcp-config config.json
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        help='Path to the existing FMU file',
        type=str
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Path where the repackaged FMU will be saved',
        type=str
    )
    
    parser.add_argument(
        '--mcp-config',
        help='Path to MCP configuration JSON file',
        type=str
    )
    
    parser.add_argument(
        '--create-sample',
        help='Create a sample vendor FMU for testing',
        type=str,
        metavar='OUTPUT_PATH'
    )
    
    args = parser.parse_args()
    
    # Handle sample FMU creation
    if args.create_sample:
        create_sample_fmu(args.create_sample)
        return 0
    
    # Validate required arguments
    if not args.input or not args.output:
        parser.print_help()
        print("\nError: --input and --output are required (or use --create-sample)")
        return 1
    
    # Load MCP config if provided
    mcp_config = {}
    if args.mcp_config:
        try:
            with open(args.mcp_config, 'r') as f:
                mcp_config = json.load(f)
        except Exception as e:
            print(f"Error loading MCP config: {e}")
            return 1
    
    # Perform repackaging
    try:
        repackager = FMURepackager(args.input, args.output, mcp_config)
        repackager.repackage()
        return 0
    except Exception as e:
        print(f"\nFatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
