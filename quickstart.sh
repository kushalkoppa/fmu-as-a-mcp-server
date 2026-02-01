#!/bin/bash

# Quick Start Script for FMU Virtual ECU
# This script helps you get started quickly

echo "================================================"
echo "FMU Virtual ECU - Quick Start"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OpenAI API key"
else
    echo "✅ .env file already exists"
fi
echo ""

# Run example
echo "Running example usage..."
echo "================================================"
python example_usage.py
echo ""
echo "================================================"
echo "Quick start completed!"
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your OpenAI API key"
echo "  2. Run: python server.py (to start MCP server)"
echo "  3. Run: python ai_agent.py (to test AI agent)"
echo "  4. Open in VS Code: code ."
echo ""
echo "See SETUP_GUIDE.md for detailed instructions"
echo "================================================"
