#!/bin/bash

echo "🚀 Setting up Slide Presentation Generator environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To use this environment in the future:"
echo "  source venv/bin/activate"
echo ""
echo "To generate a presentation:"
echo "  python generate_from_schema.py <your_schema.json>"
echo ""
echo "To validate a schema:"
echo "  python validate_schema.py <your_schema.json>"