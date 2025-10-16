#!/usr/bin/env python3

import gradio as gr
import requests
import json
import os
import time
import subprocess
from typing import Dict, Any, List, Optional

# Configuration
OLLAMA_BASE_URL = "http://localhost:11434/api"
CONFIG_DIR = os.path.expanduser("~/.config/skogai-chat")
HISTORY_DIR = os.path.join(CONFIG_DIR, "history")

# Ensure directories exist
os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(HISTORY_DIR, exist_ok=True)

# Get available models
def get_local_models():
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [model["name"] for model in models]
        return ["llama3"]
    except Exception as e:
        print(f"Error getting local models: {e}")
        return ["llama3"]

def get_api_models():
    return ["claude-3.7-reasoning", "claude-3.5-sonnet", "gpt-4o", "gpt-4-turbo"]

# Chat functions
def format_chat_history(history: List) -> List:
    """Format chat history for display."""
    return history

def generate_response(message: str, history: List, model: str, temperature: float, 
                     system_prompt: str, api_key: str) -> str:
    """Generate a response from the selected model."""
    if not message.strip():
        return "Please enter a message."
    
    # Add thinking indicator
    thinking = "Thinking..."
    
    # Check if it's a local model (Ollama)
    if model in get_local_models():
        try:
            # Format the prompt
            prompt = format_prompt_for_ollama(message, history, system_prompt)
            
            # Call Ollama API
            response = requests.post(
                f"{OLLAMA_BASE_URL}/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "temperature": temperature,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                return response.json().get("response", "No response from model")
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error generating response: {e}"
    
    # Handle API-based models
    else:
        try:
            if not api_key and model.startswith(("claude", "gpt")):
                return "API key required for this model. Please enter it in the settings tab."
            
            if model.startswith("claude"):
                return call_anthropic_api(message, history, model, temperature, system_prompt, api_key)
            elif model.startswith("gpt"):
                return call_openai_api(message, history, model, temperature, system_prompt, api_key)
            else:
                return f"Model {model} not supported yet."
                
        except Exception as e:
            return f"Error calling API: {e}"

def format_prompt_for_ollama(message: str, history: List, system_prompt: str) -> str:
    """Format the prompt for Ollama models."""
    # Simple formatting for Ollama
    formatted_history = ""
    
    # Add system prompt if provided
    if system_prompt:
        formatted_history = f"<s>[INST] {system_prompt} [/INST]</s>\n\n"
    
    # Add chat history
    for entry in history:
        user_message = entry[0]
        ai_message = entry[1]
        formatted_history += f"<s>[INST] {user_message} [/INST] {ai_message}</s>\n\n"
    
    # Add current message
    full_prompt = f"{formatted_history}<s>[INST] {message} [/INST]"
    return full_prompt

def call_anthropic_api(message: str, history: List, model: str, temperature: float, 
                     system_prompt: str, api_key: str) -> str:
    """Call Anthropic API (Claude)."""
    # Format messages in Anthropic format
    messages = []
    
    # Add history
    for entry in history:
        messages.append({"role": "user", "content": entry[0]})
        messages.append({"role": "assistant", "content": entry[1]})
    
    # Add current message
    messages.append({"role": "user", "content": message})
    
    # Make API call
    headers = {
        "x-api-key": api_key,
        "content-type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 4000
    }
    
    if system_prompt:
        data["system"] = system_prompt
    
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        return response.json()["content"][0]["text"]
    else:
        return f"Error: {response.status_code} - {response.text}"

def call_openai_api(message: str, history: List, model: str, temperature: float, 
                  system_prompt: str, api_key: str) -> str:
    """Call OpenAI API."""
    # Format messages in OpenAI format
    messages = []
    
    # Add system message if provided
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    # Add history
    for entry in history:
        messages.append({"role": "user", "content": entry[0]})
        messages.append({"role": "assistant", "content": entry[1]})
    
    # Add current message
    messages.append({"role": "user", "content": message})
    
    # Make API call
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 4000
    }
    
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

def save_chat_history(history: List, model: str) -> None:
    """Save chat history to file."""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{model}-{timestamp}.json"
    filepath = os.path.join(HISTORY_DIR, filename)
    
    with open(filepath, "w") as f:
        json.dump(history, f, indent=2)
    
    return filepath

def save_settings(settings: Dict[str, Any]) -> None:
    """Save user settings."""
    settings_path = os.path.join(CONFIG_DIR, "settings.json")
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=2)

def load_settings() -> Dict[str, Any]:
    """Load user settings."""
    settings_path = os.path.join(CONFIG_DIR, "settings.json")
    
    default_settings = {
        "temperature": 0.7,
        "model": "llama3",
        "system_prompt": "",
        "theme": "dark",
        "api_keys": {}
    }
    
    if os.path.exists(settings_path):
        try:
            with open(settings_path, "r") as f:
                settings = json.load(f)
                # Merge with defaults in case some settings are missing
                return {**default_settings, **settings}
        except:
            return default_settings
    
    return default_settings

# UI Creation
def create_ui():
    settings = load_settings()
    
    with gr.Blocks(theme=gr.themes.Soft(primary_hue=gr.themes.colors.blue, neutral_hue=gr.themes.colors.gray, font=["Source Sans Pro", "ui-sans-serif", "system-ui", "sans-serif"])) as demo:
        gr.Markdown("# SkogAI Chat")
        
        with gr.Tab("Chat"):
            chatbot = gr.Chatbot(height=700, value=[], label="Conversation")
            
            with gr.Row():
                with gr.Column(scale=4):
                    msg = gr.Textbox(
                        label="Your message",
                        placeholder="Type your message here...",
                        container=False,
                        scale=4,
                        show_label=False
                    )
                
                with gr.Column(scale=1):
                    submit_btn = gr.Button("Send", variant="primary")
            
            with gr.Row():
                clear_btn = gr.Button("Clear")
                save_btn = gr.Button("Save Chat")
                
            with gr.Row():
                model_dropdown = gr.Dropdown(
                    choices=get_local_models() + get_api_models(),
                    value=settings.get("model", "llama3"),
                    label="Model"
                )
                temperature_slider = gr.Slider(
                    minimum=0, 
                    maximum=1.5, 
                    value=settings.get("temperature", 0.7),
                    step=0.1,
                    label="Temperature"
                )
            
            gr.Markdown("### Quick System Prompts")
            
            with gr.Row():
                default_system = gr.Button("Default")
                creative_system = gr.Button("Creative")
                technical_system = gr.Button("Technical Expert")
            
            # Event handlers
            def user_input(message, history):
                return "", history + [[message, ""]]
            
            def bot_response(history, model, temperature, system_prompt, api_key):
                user_message = history[-1][0]
                bot_message = generate_response(
                    user_message, 
                    history[:-1], 
                    model, 
                    temperature, 
                    system_prompt,
                    api_key
                )
                history[-1][1] = bot_message
                return history
            
            def save_history(history, model):
                if not history:
                    return "No messages to save."
                
                filepath = save_chat_history(history, model)
                return f"Chat saved to {filepath}"
            
            def set_system_prompt(prompt_type):
                if prompt_type == "default":
                    return "You are a helpful AI assistant. Answer questions accurately, completely, and helpfully."
                elif prompt_type == "creative":
                    return "You are a creative assistant focused on generating innovative ideas and content. Be imaginative, unique, and inspiring in your responses."
                elif prompt_type == "technical":
                    return "You are an expert technical assistant with deep knowledge of software development, engineering, and computer science. Provide detailed, accurate, and technical responses."
            
            # Connect event handlers
            submit_btn.click(
                user_input, 
                [msg, chatbot], 
                [msg, chatbot]
            ).then(
                bot_response, 
                [chatbot, model_dropdown, temperature_slider, system_prompt, api_key],
                [chatbot]
            )
            
            msg.submit(
                user_input, 
                [msg, chatbot], 
                [msg, chatbot]
            ).then(
                bot_response, 
                [chatbot, model_dropdown, temperature_slider, system_prompt, api_key],
                [chatbot]
            )
            
            clear_btn.click(lambda: [], None, chatbot)
            save_btn.click(save_history, [chatbot, model_dropdown], gr.Textbox())
            
            default_system.click(lambda: set_system_prompt("default"), None, system_prompt)
            creative_system.click(lambda: set_system_prompt("creative"), None, system_prompt)
            technical_system.click(lambda: set_system_prompt("technical"), None, system_prompt)
        
        with gr.Tab("Settings"):
            system_prompt = gr.Textbox(
                label="System Prompt",
                placeholder="Instructions for the AI assistant",
                value=settings.get("system_prompt", ""),
                lines=4
            )
            
            with gr.Accordion("API Keys", open=False):
                api_key = gr.Textbox(
                    label="API Key (for Claude/OpenAI)",
                    placeholder="Enter your API key here",
                    value=settings.get("api_keys", {}).get("default", ""),
                    type="password"
                )
            
            with gr.Row():
                save_settings_btn = gr.Button("Save Settings")
            
            # Settings event handlers
            def update_settings(system_prompt, api_key, model, temperature):
                settings = {
                    "system_prompt": system_prompt,
                    "api_keys": {"default": api_key},
                    "model": model,
                    "temperature": temperature
                }
                save_settings(settings)
                return "Settings saved successfully!"
            
            save_settings_btn.click(
                update_settings,
                [system_prompt, api_key, model_dropdown, temperature_slider],
                gr.Textbox(label="Status")
            )
        
        with gr.Tab("History"):
            def list_history_files():
                files = os.listdir(HISTORY_DIR)
                files = [f for f in files if f.endswith('.json')]
                files.sort(reverse=True)
                return files
            
            history_files = gr.Dropdown(
                choices=list_history_files(),
                label="Select chat history",
                value=None
            )
            
            refresh_btn = gr.Button("Refresh")
            
            def load_history_file(filename):
                if not filename:
                    return "Please select a file."
                
                filepath = os.path.join(HISTORY_DIR, filename)
                try:
                    with open(filepath, 'r') as f:
                        history = json.load(f)
                    return history
                except:
                    return []
            
            load_btn = gr.Button("Load Selected Chat")
            
            refresh_btn.click(list_history_files, None, history_files)
            load_btn.click(load_history_file, [history_files], chatbot)
    
    return demo

# Main
if __name__ == "__main__":
    demo = create_ui()
    demo.launch(server_name="0.0.0.0", share=False)