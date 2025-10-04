# SkogAI Chat Interface

A modern, elegant chat interface for interacting with AI models, supporting both local Ollama models and API-based services like Claude and GPT.

![SkogAI Chat](https://placehold.co/800x400?text=SkogAI+Chat)

## Features

- **Multiple Model Support**: Seamlessly switch between local Ollama models and API-based services
- **Full Conversation History**: Save, load, and manage chat conversations
- **Customizable Settings**: Adjust temperature, system prompts, and other parameters
- **Clean, Responsive UI**: Works on desktop and mobile devices
- **Quick System Prompt Templates**: Switch between different AI personas with one click

## Requirements

- Python 3.10+
- Streamlit
- Ollama (for local models)
- API keys for Claude and/or GPT (for API-based services)

## Installation

1. Make sure Python is installed
2. Install required Python packages:
   ```bash
   pip install streamlit toml requests anthropic openai
   ```
3. Make sure Ollama is running locally (for local models)
4. Launch the application:
   ```bash
   ./start-chat-ui.sh
   ```

## Usage

1. **Select a Model**: Choose between local Ollama models or API-based services
2. **Set Parameters**: Adjust temperature and system prompts to control the AI's behavior
3. **Chat**: Start chatting with your selected AI model
4. **Save Conversations**: Save your chat history for later reference
5. **Manage Settings**: Configure API keys and default settings in the Settings tab

## API Keys

To use Claude or GPT models, you'll need to add your API keys in the Settings tab:

- For Claude models: Add your Anthropic API key
- For GPT models: Add your OpenAI API key

## Credits

Developed by the SkogAI team.