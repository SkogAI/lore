import streamlit as st
import time

# This is a demo script to showcase the UI appearance
# It doesn't actually connect to any models

# Page Configuration
st.set_page_config(
    page_title="SkogAI Chat Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
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

# Sidebar
st.sidebar.title("SkogAI Chat")
st.sidebar.image("https://placehold.co/200x100?text=SkogAI", width=200)

tab = st.sidebar.radio("Menu", ["Chat", "Settings", "History"])

if tab == "Chat":
    # MODEL SELECTION
    models_col1, models_col2 = st.sidebar.columns(2)
    
    with models_col1:
        model_type = st.radio("Model Type", ["Local (Ollama)", "API"])
    
    with models_col2:
        if model_type == "Local (Ollama)":
            selected_model = st.selectbox("Select Model", ["llama3", "mistral", "gemma"])
        else:
            selected_model = st.selectbox("Select Model", ["claude-3.7-reasoning", "claude-3.5-sonnet", "gpt-4o", "gpt-4-turbo"])
    
    # TEMPERATURE
    st.sidebar.slider("Temperature", min_value=0.0, max_value=1.5, value=0.7, step=0.1)
    
    # SYSTEM PROMPT
    st.sidebar.text_area("System Prompt", height=100, value="You are a helpful, harmless, and honest AI assistant.")
    
    # PRESET SYSTEM PROMPTS
    st.sidebar.markdown("### Quick System Prompts")
    system_preset_cols = st.sidebar.columns(3)
    
    with system_preset_cols[0]:
        st.button("General Assistant")
    
    with system_preset_cols[1]:
        st.button("Creative")
    
    with system_preset_cols[2]:
        st.button("Technical")
    
    # SAVE/CLEAR BUTTONS
    st.sidebar.markdown("### Chat Actions")
    save_clear_cols = st.sidebar.columns(2)
    
    with save_clear_cols[0]:
        st.button("Save Chat")
    
    with save_clear_cols[1]:
        st.button("Clear Chat")
    
    # Main chat interface
    st.header("Chat Interface")
    
    # Sample chat messages
    st.markdown("""
    <div class="message-container">
        <div class="user-bubble">
            Hello! Can you help me understand how to use Transformer models in PyTorch?
            <div class="timestamp">2025-04-01 09:30:15</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="message-container">
        <div class="ai-bubble">
            Of course! I'd be happy to help you understand Transformer models in PyTorch.<br><br>Transformer models are a type of neural network architecture that was introduced in the paper "Attention Is All You Need" by Vaswani et al. in 2017. They've become the backbone of modern NLP systems.<br><br>Here's how to use them in PyTorch:<br><br>1. First, you'll need to install the necessary libraries:
            ```python
            pip install torch transformers
            ```<br><br>2. Import the libraries:
            ```python
            import torch
            from transformers import BertModel, BertTokenizer
            ```<br><br>3. Load a pre-trained model:
            ```python
            tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
            model = BertModel.from_pretrained('bert-base-uncased')
            ```<br><br>4. Tokenize your input:
            ```python
            inputs = tokenizer("Hello, I'm a language model", return_tensors="pt")
            ```<br><br>5. Get model outputs:
            ```python
            outputs = model(**inputs)
            ```<br><br>Would you like me to go into more detail about any specific aspect of Transformer models?
            <div class="timestamp">2025-04-01 09:30:25</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="message-container">
        <div class="user-bubble">
            Yes, could you explain the attention mechanism in more detail?
            <div class="timestamp">2025-04-01 09:31:05</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="message-container">
        <div class="ai-bubble">
            Absolutely! The attention mechanism is the core innovation of Transformer models. In simple terms, it allows the model to "focus" on different parts of the input sequence when producing each part of the output.<br><br>Here's a detailed breakdown of the attention mechanism:<br><br>## Self-Attention<br><br>The self-attention mechanism follows these steps:<br><br>1. **Create Query, Key, and Value vectors:** For each word in your input sequence, the model creates three vectors - Query (Q), Key (K), and Value (V) vectors. These are created by multiplying the embedding of each word by three different weight matrices that the model learns during training.<br><br>2. **Calculate attention scores:** For each word, calculate how much attention to pay to each word in the sequence (including itself). This is done by taking the dot product of the Query vector of the current word with the Key vectors of all words.<br><br>3. **Scale the scores:** Divide the scores by the square root of the dimension of the Key vectors. This helps stabilize gradients during training.<br><br>4. **Apply softmax:** Convert the scores to probabilities by applying a softmax function. This ensures all scores are positive and sum to 1.<br><br>5. **Weight the Value vectors:** Multiply each Value vector by its corresponding attention probability.<br><br>6. **Sum up the weighted Value vectors:** This gives you the output of the attention layer for the current word.<br><br>Here's a simplified implementation in PyTorch:
            ```python
            import torch
            import torch.nn.functional as F

            def self_attention(query, key, value):
                # query, key, value shape: [batch_size, seq_len, d_model]
                d_k = key.size(-1)
                
                # Calculate attention scores
                scores = torch.matmul(query, key.transpose(-2, -1))
                
                # Scale
                scores = scores / (d_k ** 0.5)
                
                # Apply softmax
                attention_weights = F.softmax(scores, dim=-1)
                
                # Weight values
                output = torch.matmul(attention_weights, value)
                
                return output, attention_weights
            ```<br><br>The Transformer architecture actually uses multi-head attention, which means this process is repeated multiple times in parallel with different weight matrices, and the results are concatenated and linearly transformed.<br><br>Would you like me to explain any other aspects of the attention mechanism or Transformers?
            <div class="timestamp">2025-04-01 09:31:35</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Message input
    st.text_input("Message", placeholder="Type your message here...", label_visibility="collapsed")

elif tab == "Settings":
    st.header("Settings")
    
    # General settings
    st.subheader("General Settings")
    st.selectbox("Default Model", ["llama3", "claude-3.5-sonnet", "gpt-4o"])
    st.slider("Default Temperature", min_value=0.0, max_value=1.5, value=0.7, step=0.1)
    st.text_area("Default System Prompt", value="You are a helpful AI assistant.")
    
    # API Keys
    st.subheader("API Keys")
    st.text_input("OpenAI API Key", type="password")
    st.text_input("Anthropic API Key", type="password")
    
    st.button("Save Settings")

elif tab == "History":
    st.header("Chat History")
    
    st.selectbox("Select a saved chat to load", [
        "llama3_2025-04-01_08-15-30.json",
        "claude-3.5-sonnet_2025-03-30_14-22-05.json",
        "gpt-4o_2025-03-28_19-45-12.json"
    ])
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("Load Selected Chat")
    with col2:
        st.button("Refresh List")
    
    with st.expander("Preview Selected Chat", expanded=False):
        st.markdown("**User** (2025-03-30 14:22:05):")
        st.markdown("> Can you help me understand quantum computing?")
        st.markdown("---")
        st.markdown("**AI** (2025-03-30 14:22:15):")
        st.markdown("> Quantum computing is a type of computation that harnesses quantum mechanical phenomena like superposition and entanglement to perform operations on data...")
        st.markdown("---")
        st.markdown("**User** (2025-03-30 14:23:05):")
        st.markdown("> What are qubits?")
        st.markdown("---")
        st.markdown("**AI** (2025-03-30 14:23:15):")
        st.markdown("> Qubits (quantum bits) are the fundamental units of quantum information in quantum computing...")