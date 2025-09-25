#!/usr/bin/env python3

import streamlit as st
import requests
import json
import os
import time
import datetime
from typing import Dict, Any, List, Optional
import anthropic
import openai

# Configuration
OLLAMA_BASE_URL = "http://localhost:11434/api"
CONFIG_DIR = os.path.expanduser("~/.config/skogai-chat")
HISTORY_DIR = os.path.join(CONFIG_DIR, "history")

# Ensure directories exist
os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(HISTORY_DIR, exist_ok=True)

# Page Configuration
PAGE_TITLE = "SkogAI Chat"
PAGE_ICON = "🤖"

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Functions
def get_local_models():
    """Get list of locally available Ollama models"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [model["name"] for model in models]
        return ["llama3"]
    except Exception as e:
        st.error(f"Error getting local models: {e}")
        return ["llama3"]

def get_api_models():
    """Get list of available API-based models"""
    return [
        "claude-3.7-reasoning", 
        "claude-3.5-sonnet", 
        "gpt-4o", 
        "gpt-4-turbo"
    ]

def save_settings(settings: Dict[str, Any]):
    """Save user settings to file"""
    settings_path = os.path.join(CONFIG_DIR, "settings.json")
    try:
        with open(settings_path, "w") as f:
            json.dump(settings, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving settings: {e}")
        return False

def load_settings() -> Dict[str, Any]:
    """Load user settings from file"""
    settings_path = os.path.join(CONFIG_DIR, "settings.json")
    
    default_settings = {
        "temperature": 0.7,
        "model": "llama3",
        "system_prompt": "",
        "theme": "dark",
        "openai_api_key": "",
        "anthropic_api_key": ""
    }
    
    if os.path.exists(settings_path):
        try:
            with open(settings_path, "r") as f:
                settings = json.load(f)
                # Merge with defaults for any missing settings
                return {**default_settings, **settings}
        except Exception as e:
            st.error(f"Error loading settings: {e}")
            return default_settings
    
    return default_settings

def save_chat_history(history: List, model: str):
    """Save chat history to JSON file"""
    if not history:
        return None
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{model}_{timestamp}.json"
    filepath = os.path.join(HISTORY_DIR, filename)
    
    formatted_history = []
    for message in history:
        formatted_history.append({
            "role": message["role"],
            "content": message["content"],
            "timestamp": message.get("timestamp", timestamp)
        })
    
    try:
        with open(filepath, "w") as f:
            json.dump(formatted_history, f, indent=2)
        return filepath
    except Exception as e:
        st.error(f"Error saving chat history: {e}")
        return None

def load_chat_history(filename: str):
    """Load chat history from file"""
    filepath = os.path.join(HISTORY_DIR, filename)
    try:
        with open(filepath, "r") as f:
            history = json.load(f)
        return history
    except Exception as e:
        st.error(f"Error loading chat history: {e}")
        return []

def list_chat_histories():
    """List all saved chat histories"""
    try:
        files = os.listdir(HISTORY_DIR)
        files = [f for f in files if f.endswith('.json')]
        files.sort(reverse=True)  # Most recent first
        return files
    except Exception as e:
        st.error(f"Error listing chat histories: {e}")
        return []

def format_messages_for_ollama(messages: List[Dict], system_prompt: str = ""):
    """Format messages for Ollama API"""
    # Extract just user and assistant messages
    prompt = ""
    
    # Add system prompt if provided
    if system_prompt:
        prompt = f"<s>[INST] {system_prompt} [/INST]</s>\n\n"
    
    # Add conversation history
    for message in messages:
        if message["role"] == "user":
            user_message = message["content"]
            if prompt and not prompt.endswith("\n\n"):
                prompt += "\n\n"
            prompt += f"<s>[INST] {user_message} [/INST] "
        elif message["role"] == "assistant":
            ai_message = message["content"]
            prompt += f"{ai_message}</s>"
    
    # If the last message is from a user, format it properly
    if messages and messages[-1]["role"] == "user":
        return prompt
    
    return prompt

def call_ollama(messages: List[Dict], model: str, temperature: float, system_prompt: str = ""):
    """Call Ollama API to generate response"""
    try:
        prompt = format_messages_for_ollama(messages, system_prompt)
                
        response = requests.post(
            f"{OLLAMA_BASE_URL}/generate",
            json={
                "model": model,
                "prompt": prompt,
                "temperature": temperature,
                "stream": False
            },
            timeout=120  # 2-minute timeout
        )
        
        if response.status_code == 200:
            return {
                "role": "assistant",
                "content": response.json().get("response", ""),
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            return {
                "role": "assistant",
                "content": f"Error: {response.status_code} - {response.text}",
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
    except Exception as e:
        return {
            "role": "assistant",
            "content": f"Error: {str(e)}",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def call_anthropic(messages: List[Dict], model: str, temperature: float, system_prompt: str = "", api_key: str = ""):
    """Call Anthropic API to generate response"""
    try:
        formatted_messages = []
        for message in messages:
            if message["role"] in ["user", "assistant"]:
                formatted_messages.append({
                    "role": message["role"],
                    "content": message["content"]
                })
        
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model,
            messages=formatted_messages,
            temperature=temperature,
            max_tokens=4096,
            system=system_prompt if system_prompt else None
        )
        
        return {
            "role": "assistant",
            "content": response.content[0].text,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    except Exception as e:
        return {
            "role": "assistant", 
            "content": f"Error calling Anthropic API: {str(e)}",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def call_openai(messages: List[Dict], model: str, temperature: float, system_prompt: str = "", api_key: str = ""):
    """Call OpenAI API to generate response"""
    try:
        formatted_messages = []
        
        # Add system message if provided
        if system_prompt:
            formatted_messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # Add conversation history
        for message in messages:
            if message["role"] in ["user", "assistant"]:
                formatted_messages.append({
                    "role": message["role"],
                    "content": message["content"]
                })
        
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=formatted_messages,
            temperature=temperature,
            max_tokens=4096
        )
        
        return {
            "role": "assistant",
            "content": response.choices[0].message.content,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "role": "assistant",
            "content": f"Error calling OpenAI API: {str(e)}",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def generate_response(messages: List[Dict], model: str, temperature: float, 
                     system_prompt: str, api_keys: Dict[str, str]) -> Dict:
    """Generate a response from the selected model"""
    # Last message should be from user
    if not messages or messages[-1]["role"] != "user":
        return {
            "role": "assistant",
            "content": "Error: Last message must be from user.",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    # Check if it's a local model (Ollama)
    if model in get_local_models():
        return call_ollama(messages, model, temperature, system_prompt)
    
    # Handle API-based models
    elif model.startswith("claude"):
        api_key = api_keys.get("anthropic", "")
        if not api_key:
            return {
                "role": "assistant",
                "content": "Anthropic API key is required. Please enter it in the settings tab.",
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        return call_anthropic(messages, model, temperature, system_prompt, api_key)
    
    elif model.startswith("gpt"):
        api_key = api_keys.get("openai", "")
        if not api_key:
            return {
                "role": "assistant",
                "content": "OpenAI API key is required. Please enter it in the settings tab.",
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        return call_openai(messages, model, temperature, system_prompt, api_key)
    
    else:
        return {
            "role": "assistant",
            "content": f"Model {model} not supported yet.",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

# Initialize session state
def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "settings" not in st.session_state:
        st.session_state.settings = load_settings()
    
    if "current_model" not in st.session_state:
        st.session_state.current_model = st.session_state.settings.get("model", "llama3")
    
    if "temperature" not in st.session_state:
        st.session_state.temperature = st.session_state.settings.get("temperature", 0.7)
    
    if "system_prompt" not in st.session_state:
        st.session_state.system_prompt = st.session_state.settings.get("system_prompt", "")

# Helper functions for UI
def add_user_message(message: str):
    """Add a user message to the chat history"""
    if not message.strip():
        return
    
    st.session_state.messages.append({
        "role": "user",
        "content": message,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

def add_ai_response():
    """Generate and add AI response to the chat history"""
    api_keys = {
        "anthropic": st.session_state.settings.get("anthropic_api_key", ""),
        "openai": st.session_state.settings.get("openai_api_key", "")
    }
    
    with st.spinner("AI is thinking..."):
        response = generate_response(
            st.session_state.messages,
            st.session_state.current_model,
            st.session_state.temperature,
            st.session_state.system_prompt,
            api_keys
        )
        
        st.session_state.messages.append(response)

def clear_chat():
    """Clear the chat history"""
    st.session_state.messages = []

def handle_submit():
    """Handle message submission"""
    message = st.session_state.user_input
    st.session_state.user_input = ""
    
    add_user_message(message)
    add_ai_response()

def apply_custom_css():
    """Apply custom CSS for improved UI aesthetics"""
    st.markdown("""
    <style>
        .stTextInput > div > div > input {
            padding: 15px;
            font-size: 16px;
            border-radius: 10px;
        }
        
        .user-bubble {
            background-color: #e6f7ff;
            padding: 12px 15px;
            border-radius: 15px;
            margin-bottom: 10px;
            position: relative;
            max-width: 80%;
            float: right;
            clear: both;
            color: #333;
        }
        
        .ai-bubble {
            background-color: #f2f2f2;
            padding: 12px 15px;
            border-radius: 15px;
            margin-bottom: 10px;
            position: relative;
            max-width: 80%;
            float: left;
            clear: both;
        }
        
        .chat-header {
            text-align: center;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
            margin-bottom: 20px;
        }
        
        .timestamp {
            font-size: 10px;
            color: #999;
            margin-top: 5px;
        }
        
        .chat-container {
            height: calc(100vh - 300px);
            overflow-y: auto;
            padding: 20px;
            background-color: #fafafa;
            border-radius: 10px;
        }
        
        .message-container {
            overflow: hidden;
            margin-bottom: 15px;
        }
        
        .stButton button {
            border-radius: 8px;
            font-weight: 500;
            height: 46px;
        }
    </style>
    """, unsafe_allow_html=True)

# Custom message display
def display_messages():
    """Display chat messages with custom styling"""
    message_container = st.container()
    
    with message_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="message-container">
                    <div class="user-bubble">
                        {message["content"]}
                        <div class="timestamp">{message.get("timestamp", "")}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="message-container">
                    <div class="ai-bubble">
                        {message["content"]}
                        <div class="timestamp">{message.get("timestamp", "")}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Main UI function
def main():
    init_session_state()
    apply_custom_css()
    
    # Sidebar configuration
    st.sidebar.title("SkogAI Chat")
    st.sidebar.image("https://placehold.co/200x100?text=SkogAI", width=200)
    
    sidebar_tab = st.sidebar.radio("Menu", ["Chat", "Settings", "History"])
    
    if sidebar_tab == "Chat":
        # MODEL SELECTION
        models_col1, models_col2 = st.sidebar.columns(2)
        
        with models_col1:
            model_type = st.radio(
                "Model Type",
                ["Local (Ollama)", "API"],
                index=0 if st.session_state.current_model in get_local_models() else 1
            )
        
        with models_col2:
            if model_type == "Local (Ollama)":
                selected_model = st.selectbox(
                    "Select Model",
                    get_local_models(),
                    index=get_local_models().index(st.session_state.current_model) 
                    if st.session_state.current_model in get_local_models() else 0
                )
            else:
                selected_model = st.selectbox(
                    "Select Model",
                    get_api_models(),
                    index=get_api_models().index(st.session_state.current_model)
                    if st.session_state.current_model in get_api_models() else 0
                )
        
        st.session_state.current_model = selected_model
        
        # TEMPERATURE CONTROL
        st.sidebar.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.5,
            value=st.session_state.temperature,
            step=0.1,
            key="temperature"
        )
        
        # SYSTEM PROMPT
        st.sidebar.text_area(
            "System Prompt",
            value=st.session_state.system_prompt,
            height=100,
            key="system_prompt"
        )
        
        # PRESET SYSTEM PROMPTS
        st.sidebar.markdown("### Quick System Prompts")
        system_preset_cols = st.sidebar.columns(3)
        
        with system_preset_cols[0]:
            if st.button("General Assistant"):
                st.session_state.system_prompt = "You are a helpful, harmless, and honest AI assistant. Answer the user's questions accurately and concisely."
                st.experimental_rerun()
        
        with system_preset_cols[1]:
            if st.button("Creative"):
                st.session_state.system_prompt = "You are a creative and imaginative AI assistant. Generate innovative ideas, stories, and content that's engaging and original."
                st.experimental_rerun()
                
        with system_preset_cols[2]:
            if st.button("Technical"):
                st.session_state.system_prompt = "You are an expert technical assistant with deep knowledge of software, programming, and computer science. Provide detailed, accurate technical answers with code examples when relevant."
                st.experimental_rerun()
        
        # SAVE/CLEAR BUTTONS
        st.sidebar.markdown("### Chat Actions")
        save_clear_cols = st.sidebar.columns(2)
        
        with save_clear_cols[0]:
            if st.button("Save Chat"):
                if st.session_state.messages:
                    filepath = save_chat_history(st.session_state.messages, st.session_state.current_model)
                    if filepath:
                        st.sidebar.success(f"Chat saved!")
                else:
                    st.sidebar.error("Nothing to save")
        
        with save_clear_cols[1]:
            if st.button("Clear Chat"):
                clear_chat()
                st.experimental_rerun()
        
        # Main chat interface
        st.header("Chat Interface")
        
        # Display messages
        display_messages()
        
        # Message input
        st.text_input(
            "Message",
            key="user_input",
            on_change=handle_submit,
            placeholder="Type your message here...",
            label_visibility="collapsed"
        )
    
    elif sidebar_tab == "Settings":
        st.header("Settings")
        
        settings_form = st.form("settings_form")
        
        with settings_form:
            # General settings
            st.subheader("General Settings")
            default_model = settings_form.selectbox(
                "Default Model",
                get_local_models() + get_api_models(),
                index=(get_local_models() + get_api_models()).index(st.session_state.settings.get("model", "llama3"))
                if st.session_state.settings.get("model", "llama3") in get_local_models() + get_api_models() else 0
            )
            
            default_temperature = settings_form.slider(
                "Default Temperature",
                min_value=0.0,
                max_value=1.5,
                value=st.session_state.settings.get("temperature", 0.7),
                step=0.1
            )
            
            default_system_prompt = settings_form.text_area(
                "Default System Prompt",
                value=st.session_state.settings.get("system_prompt", "")
            )
            
            # API Keys
            st.subheader("API Keys")
            
            openai_api_key = settings_form.text_input(
                "OpenAI API Key",
                value=st.session_state.settings.get("openai_api_key", ""),
                type="password"
            )
            
            anthropic_api_key = settings_form.text_input(
                "Anthropic API Key",
                value=st.session_state.settings.get("anthropic_api_key", ""),
                type="password"
            )
            
            if settings_form.form_submit_button("Save Settings"):
                new_settings = {
                    "model": default_model,
                    "temperature": default_temperature,
                    "system_prompt": default_system_prompt,
                    "openai_api_key": openai_api_key,
                    "anthropic_api_key": anthropic_api_key
                }
                
                # Update session state
                st.session_state.settings = new_settings
                st.session_state.current_model = default_model
                st.session_state.temperature = default_temperature
                st.session_state.system_prompt = default_system_prompt
                
                # Save to file
                if save_settings(new_settings):
                    st.success("Settings saved successfully!")
                    time.sleep(1)
                    st.experimental_rerun()
    
    elif sidebar_tab == "History":
        st.header("Chat History")
        
        refreshed_histories = list_chat_histories()
        
        if not refreshed_histories:
            st.info("No saved chat histories found")
        else:
            selected_history = st.selectbox(
                "Select a saved chat to load",
                refreshed_histories
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Load Selected Chat"):
                    if selected_history:
                        loaded_history = load_chat_history(selected_history)
                        if loaded_history:
                            st.session_state.messages = loaded_history
                            st.success("Chat history loaded!")
                            time.sleep(1)
                            st.experimental_rerun()
            
            with col2:
                if st.button("Refresh List"):
                    st.experimental_rerun()
            
            # Preview selected history
            if selected_history:
                with st.expander("Preview Selected Chat", expanded=False):
                    history_preview = load_chat_history(selected_history)
                    
                    for message in history_preview:
                        role = message.get("role", "unknown")
                        content = message.get("content", "")
                        timestamp = message.get("timestamp", "")
                        
                        if role == "user":
                            st.markdown(f"**User** ({timestamp}):")
                            st.markdown(f"> {content}")
                        elif role == "assistant":
                            st.markdown(f"**AI** ({timestamp}):")
                            st.markdown(f"> {content}")
                        st.markdown("---")

if __name__ == "__main__":
    main()