"""
FMU (Functional Mockup Unit) Virtual ECU Model
This module implements a simple virtual ECU with addition functionality
"""

from typing import Dict, Any, Optional
from datetime import datetime


class VirtualECU:
    """
    Virtual ECU implementation with basic arithmetic operations.
    This simulates a simple electronic control unit for demonstration.
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.ecu_level = "Level_2"
        self.software_name = "Virtual ECU - Addition Module"
        self.manufacturer = "FMU-MCP-Server"
        self.build_date = datetime.now().isoformat()
        self.interfaces = [
            "CAN",
            "LIN",
            "Ethernet",
            "FlexRay"
        ]
        self.capabilities = [
            "Addition",
            "Data Processing",
            "Real-time Response"
        ]
        self.status = "Active"
        
    def add(self, a: float, b: float) -> float:
        """
        Perform addition operation.
        
        Args:
            a: First operand
            b: Second operand
            
        Returns:
            Sum of a and b
        """
        result = a + b
        return result
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get comprehensive information about the virtual ECU.
        
        Returns:
            Dictionary containing ECU information
        """
        return {
            "software": self.software_name,
            "version": self.version,
            "ecu_level": self.ecu_level,
            "manufacturer": self.manufacturer,
            "build_date": self.build_date,
            "interfaces": self.interfaces,
            "capabilities": self.capabilities,
            "status": self.status
        }
    
    def get_version(self) -> str:
        """Get the software version."""
        return self.version
    
    def get_interfaces(self) -> list:
        """Get the list of supported interfaces."""
        return self.interfaces
    
    def get_ecu_level(self) -> str:
        """Get the ECU level."""
        return self.ecu_level
    
    def get_status(self) -> Dict[str, str]:
        """Get the current status of the ECU."""
        return {
            "status": self.status,
            "timestamp": datetime.now().isoformat()
        }
