#!/bin/bash
# Find the best free model on OpenRouter

# API Key from environment variable
API_KEY=${OPENROUTER_API_KEY}

# Make the API request
curl -s \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  "https://openrouter.ai/api/v1/models" > /tmp/models.json

# Process the data with Python
python3 <<END_PYTHON
import json

# Load models data
with open("/tmp/models.json") as f:
    data = json.load(f)
models = data.get("data", [])

# Find free models
free_models = []
for model in models:
    pricing = model.get("pricing", {})
    
    is_free = True
    for price_type, price in pricing.items():
        if float(price) > 0:
            is_free = False
            break
    
    if is_free and pricing and "tool-calling" in model.get("capabilities", []):
        free_models.append(model)

# Sort free models by context length (highest first)
if free_models:
    sorted_models = sorted(free_models, 
                        key=lambda x: (x.get("context_length", 0), x.get("created", 0)),
                        reverse=True)
    
    best_model = sorted_models[0]
    
    print("BEST FREE MODEL FOUND:")
    print("---------------------")
    print("ID:", best_model["id"])
    print("Name:", best_model["name"])
    print("Context Length:", best_model["context_length"], "tokens")
    
    print("\nPython Example:")
    print("client.chat.completions.create(")
    print("    model=\"" + best_model["id"] + "\",")
    print("    messages=[{\"role\": \"user\", \"content\": \"Hello\"}]")
    print(")")
    
    # Show other free models
    if len(sorted_models) > 1:
        print("\nOTHER FREE MODELS:")
        for model in sorted_models[1:]:
            print("- " + model["id"] + " (Context: " + str(model["context_length"]) + ")")
else:
    # Find cheapest models instead
    def get_combined_cost(model):
        pricing = model.get("pricing", {})
        prompt_cost = float(pricing.get("prompt", 0))
        completion_cost = float(pricing.get("completion", 0))
        return prompt_cost + completion_cost
    
    cheap_models = sorted(models, key=get_combined_cost)[:5]
    
    print("No free models found. Here are the cheapest models:")
    print("-------------------------------------------------")
    
    for model in cheap_models:
        pricing = model.get("pricing", {})
        prompt_cost = float(pricing.get("prompt", 0))
        completion_cost = float(pricing.get("completion", 0))
        
        print(model["id"], "- Input: $" + "{:.8f}".format(prompt_cost), "Output: $" + "{:.8f}".format(completion_cost))
END_PYTHON

# Clean up
rm /tmp/models.json
EOFSCRIPT 2>&1
