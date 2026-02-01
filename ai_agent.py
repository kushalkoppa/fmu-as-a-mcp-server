"""
AI Agent integration using OpenAI
This module provides AI-powered responses about the Virtual ECU
"""

import os
from typing import Optional, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
from fmu_model import VirtualECU

# Load environment variables
load_dotenv()


class FMU_AI_Agent:
    """
    AI Agent for the Virtual ECU using OpenAI.
    Provides natural language interface to query ECU information.
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=self.api_key)
        self.ecu = VirtualECU()
        self.model = "gpt-4"  # You can change to "gpt-3.5-turbo" for faster/cheaper responses
        
    def get_system_prompt(self) -> str:
        """
        Generate system prompt with ECU context.
        """
        ecu_info = self.ecu.get_info()
        return f"""You are an AI assistant for a Virtual ECU (Electronic Control Unit) implemented as an FMU (Functional Mockup Unit).

Current ECU Information:
- Software: {ecu_info['software']}
- Version: {ecu_info['version']}
- ECU Level: {ecu_info['ecu_level']}
- Manufacturer: {ecu_info['manufacturer']}
- Build Date: {ecu_info['build_date']}
- Supported Interfaces: {', '.join(ecu_info['interfaces'])}
- Capabilities: {', '.join(ecu_info['capabilities'])}
- Status: {ecu_info['status']}

You can help users:
1. Query information about the software, version, interfaces, and ECU level
2. Perform addition operations using the ECU
3. Check the status of the ECU
4. Understand the capabilities and specifications

Always provide clear, concise, and accurate responses based on the ECU information above."""
    
    def query(self, user_question: str) -> str:
        """
        Process a user query using OpenAI.
        
        Args:
            user_question: The question from the user
            
        Returns:
            AI-generated response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.get_system_prompt()},
                    {"role": "user", "content": user_question}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error querying AI agent: {str(e)}"
    
    def query_with_action(self, user_question: str) -> Dict[str, Any]:
        """
        Process a query and potentially execute ECU actions.
        
        Args:
            user_question: The question from the user
            
        Returns:
            Dictionary with response and any action results
        """
        # Check if query involves addition
        if "add" in user_question.lower() or "+" in user_question:
            # Try to extract numbers (simple parsing)
            words = user_question.split()
            numbers = []
            for word in words:
                try:
                    numbers.append(float(word))
                except ValueError:
                    continue
            
            if len(numbers) >= 2:
                result = self.ecu.add(numbers[0], numbers[1])
                return {
                    "response": f"Performing addition: {numbers[0]} + {numbers[1]} = {result}",
                    "action": "addition",
                    "result": result
                }
        
        # Otherwise, just query the AI
        response = self.query(user_question)
        return {
            "response": response,
            "action": "query",
            "result": None
        }


def main():
    """
    Example usage of the AI agent.
    """
    print("FMU Virtual ECU - AI Agent")
    print("=" * 50)
    
    try:
        agent = FMU_AI_Agent()
        
        # Example queries
        queries = [
            "What software version is running?",
            "What interfaces does the ECU support?",
            "What is the ECU level?",
            "Can you add 25 and 17?",
            "What capabilities does this ECU have?"
        ]
        
        for query in queries:
            print(f"\nQ: {query}")
            result = agent.query_with_action(query)
            print(f"A: {result['response']}")
            
    except ValueError as e:
        print(f"\nError: {e}")
        print("Please set OPENAI_API_KEY in your .env file")


if __name__ == "__main__":
    main()
