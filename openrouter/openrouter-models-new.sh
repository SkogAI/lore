#!/bin/bash
# OpenRouter Models Reference Script

# Set your API key from environment variable or fallback to prompt
OPENROUTER_API_KEY=${OPENROUTER_API_KEY:-""}

# If no API key is set, prompt for it
if [ -z "$OPENROUTER_API_KEY" ]; then
  echo "OpenRouter API key not found in environment variable."
  read -p "Please enter your OpenRouter API key: " OPENROUTER_API_KEY
  if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "No API key provided. Exiting."
    exit 1
  fi
fi

# Set path to virtual environment if it exists
VENV_PATH="/home/skogix/skogai/.venv"
if [ -d "$VENV_PATH" ]; then
  echo "Activating virtual environment at $VENV_PATH"
  source "$VENV_PATH/bin/activate"
fi

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print header
echo -e "${BLUE}OpenRouter Models Reference Tool${NC}"
echo "--------------------------------------"
echo -e "${BLUE}Using API Key:${NC} ${OPENROUTER_API_KEY:0:8}...${OPENROUTER_API_KEY: -4}"

# Function to check required commands
check_dependencies() {
  if ! command -v curl &> /dev/null; then
    echo -e "${RED}Error: curl is required but not installed.${NC}"
    exit 1
  fi

  if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 is required but not installed.${NC}"
    exit 1
  fi
}

# List models with simple view
list_models() {
  echo -e "\n${GREEN}Fetching Available Models from OpenRouter${NC}"
  
  # Create a temporary file for the raw JSON output
  curl -s -X GET "https://openrouter.ai/api/v1/models" \
    -H "Authorization: Bearer $OPENROUTER_API_KEY" > /tmp/openrouter_models.json
  
  # Create a Python script to parse and display the models
  cat > /tmp/parse_models.py << 'EOF'
import json

# Load the models data
with open('/tmp/openrouter_models.json', 'r') as f:
    data = json.load(f)

models = data.get('data', [])

# Sort models by provider
models_by_provider = {}
for model in models:
    model_id = model['id']
    provider = model_id.split('/')[0] if '/' in model_id else 'unknown'
    
    if provider not in models_by_provider:
        models_by_provider[provider] = []
    
    models_by_provider[provider].append(model)

# Print the models grouped by provider
print(f"{'=' * 100}")
print(f"{'PROVIDER':<20} {'MODEL ID':<50} {'CONTEXT LENGTH':<15} {'PRICING (INPUT/OUTPUT)'}")
print(f"{'-' * 100}")

for provider, provider_models in sorted(models_by_provider.items()):
    # Sort models within each provider by name
    for model in sorted(provider_models, key=lambda x: x['id']):
        model_id = model['id']
        context_length = f"{model['context_length']:,}"
        
        # Format pricing information
        pricing = model.get('pricing', {})
        prompt_price = float(pricing.get('prompt', 0))
        completion_price = float(pricing.get('completion', 0))
        pricing_str = f"${prompt_price:.8f} / ${completion_price:.8f}"
        
        print(f"{provider:<20} {model_id:<50} {context_length:<15} {pricing_str}")
    
    print(f"{'-' * 100}")

print("\nUSAGE EXAMPLES:")
print("1. In Python with OpenAI SDK:")
print('   client.chat.completions.create(model="anthropic/claude-3.5-sonnet", messages=[...])')
print("\n2. In API calls:")
print('   { "model": "anthropic/claude-3.5-sonnet", "messages": [...] }')
