#!/usr/bin/env python3
"""
Simple script to find free OpenRouter models.
Run with: python3 or-free.py
"""

import json
import os
import requests
import sys

# Get API key from environment variable
api_key = os.environ.get("OPENROUTER_API_KEY")
print(f"API Key found: {'Yes' if api_key else 'No'}")
if not api_key:
    print("Error: OPENROUTER_API_KEY environment variable not set")
    sys.exit(1)

# Fetch models from OpenRouter
try:
    print(f"Fetching models from OpenRouter...")
    response = requests.get(
        "https://openrouter.ai/api/v1/models",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    print(f"Response status code: {response.status_code}")
    response.raise_for_status()
    data = response.json()
    print(f"Found {len(data.get('data', []))} models")
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
    
    print("\n=== BEST FREE MODEL ===")
    print(f"ID: {best_model['id']}")
    print(f"Name: {best_model['name']}")
    print(f"Context Length: {best_model['context_length']} tokens")
    
    print("\nPython Example:")
    print(f"client.chat.completions.create(")
    print(f"    model=\"{best_model['id']}\",")
    print(f"    messages=[{{\"role\": \"user\", \"content\": \"Hello\"}}]")
    print(f")")
    
    print("\n=== OTHER FREE MODELS ===")
    for model in sorted_models[1:10]:  # Top 10 other models
        print(f"- {model['id']} (Context: {model['context_length']})")
    
    if len(sorted_models) > 11:
        print(f"... and {len(sorted_models) - 11} more free models available")
else:
    print("No completely free models found.")
