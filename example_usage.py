"""
Example usage of the FMU Virtual ECU
This script demonstrates how to use the Virtual ECU and AI Agent
"""

from fmu_model import VirtualECU
import os

def main():
    """
    Demonstrate Virtual ECU functionality.
    """
    print("=" * 60)
    print("FMU Virtual ECU - Example Usage")
    print("=" * 60)
    
    # Initialize the Virtual ECU
    ecu = VirtualECU()
    
    # 1. Get comprehensive ECU information
    print("\n1. Virtual ECU Information:")
    print("-" * 60)
    info = ecu.get_info()
    print(f"Software: {info['software']}")
    print(f"Version: {info['version']}")
    print(f"ECU Level: {info['ecu_level']}")
    print(f"Manufacturer: {info['manufacturer']}")
    print(f"Build Date: {info['build_date']}")
    print(f"Status: {info['status']}")
    
    # 2. Get software version
    print("\n2. Software Version:")
    print("-" * 60)
    version = ecu.get_version()
    print(f"Version: {version}")
    
    # 3. Get supported interfaces
    print("\n3. Supported Communication Interfaces:")
    print("-" * 60)
    interfaces = ecu.get_interfaces()
    for idx, interface in enumerate(interfaces, 1):
        print(f"  {idx}. {interface}")
    
    # 4. Get ECU level
    print("\n4. ECU Level:")
    print("-" * 60)
    level = ecu.get_ecu_level()
    print(f"ECU Level: {level}")
    
    # 5. Demonstrate addition capability
    print("\n5. Addition Operations:")
    print("-" * 60)
    
    test_cases = [
        (10, 20),
        (42, 58),
        (100.5, 200.3),
        (-15, 25),
        (0, 0)
    ]
    
    for a, b in test_cases:
        result = ecu.add(a, b)
        print(f"  {a} + {b} = {result}")
    
    # 6. Get ECU status
    print("\n6. ECU Status:")
    print("-" * 60)
    status = ecu.get_status()
    print(f"Status: {status['status']}")
    print(f"Timestamp: {status['timestamp']}")
    
    # 7. Display capabilities
    print("\n7. ECU Capabilities:")
    print("-" * 60)
    for idx, capability in enumerate(info['capabilities'], 1):
        print(f"  {idx}. {capability}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)
    
    # 8. Try AI Agent if OpenAI key is configured
    print("\n8. Testing AI Agent (Optional):")
    print("-" * 60)
    
    if os.getenv("OPENAI_API_KEY"):
        try:
            from ai_agent import FMU_AI_Agent
            
            print("Initializing AI Agent...")
            agent = FMU_AI_Agent()
            
            # Example query
            query = "What are the main capabilities of this ECU?"
            print(f"\nQuery: {query}")
            response = agent.query(query)
            print(f"Response: {response}")
            
            print("\n✅ AI Agent is working!")
            
        except Exception as e:
            print(f"⚠️ AI Agent not available: {e}")
            print("Set OPENAI_API_KEY in .env to enable AI features")
    else:
        print("⚠️ OPENAI_API_KEY not set in environment")
        print("AI Agent features are disabled")
        print("To enable: Set OPENAI_API_KEY in your .env file")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
