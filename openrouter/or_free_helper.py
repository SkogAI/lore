#!/usr/bin/env python3
import os
import requests
import sys

# Get API key from environment variable
api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    print("Error: OPENROUTER_API_KEY environment variable not set")
    print("Please set it with: export OPENROUTER_API_KEY=your_key_here")
    sys.exit(1)

# Fetch models from OpenRouter
try:
    response = requests.get(
        "https://openrouter.ai/api/v1/models",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    response.raise_for_status()
    data = response.json()
except Exception as e:
    print(f"Error fetching models: {e}")
    sys.exit(1)

# Find free models
free_models = []
for model in data.get("data", []):
    pricing = model.get("pricing", {})
    
    is_free = True
    for price_type, price in pricing.items():
        if float(price) > 0:
            is_free = False
            break
    
    if is_free and pricing:
        free_models.append(model)

# Sort by context length
if free_models:
    sorted_models = sorted(free_models, 
                       key=lambda x: (x.get("context_length", 0), x.get("created", 0)),
                       reverse=True)
    
    best_model = sorted_models[0]
    
    print("\n=== BEST FREE OPENROUTER MODEL ===")
    print(f"ID: {best_model['id']}")
    print(f"Name: {best_model['name']}")
    print(f"Context Length: {best_model['context_length']} tokens")
    
    print("\nPython Example:")
    print(f"client.chat.completions.create(")
    print(f"    model=\"{best_model['id']}\",")
    print(f"    messages=[{{\"role\": \"user\", \"content\": \"Hello\"}}]")
    print(f")")
    
    # Optional: show more models
    if len(sorted_models) > 1 and "--all" in sys.argv:
        print("\n=== OTHER FREE MODELS ===")
        for model in sorted_models[1:]:
            print(f"- {model['id']} (Context: {model['context_length']})")
    elif len(sorted_models) > 1:
        print("\n=== OTHER FREE MODELS (TOP 5) ===")
        for model in sorted_models[1:6]:
            print(f"- {model['id']} (Context: {model['context_length']})")
        if len(sorted_models) > 6:
            print(f"... and {len(sorted_models) - 6} more free models available")
            print(f"Use --all to see all free models")
else:
    print("No completely free models found.")
