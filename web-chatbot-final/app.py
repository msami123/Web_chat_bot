# app.py
import os
import json
import streamlit as st
from typing import List, Dict, Any
from openai import OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# -----------------------------
# Configuration
# -----------------------------
st.set_page_config(
    page_title="Web Chat Bot",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

MODEL_NAME = "gpt-4o"
TOP_K = 5
MAX_CONTEXT_CHARS = 8000

QUICK_ACTIONS = [
    {"ar": "خدماتنا", "en": "Our Services", "icon": "🛠️"},
    {"ar": "تطبيق ريالك", "en": "Riyalak App", "icon": "💰"},
    {"ar": "المصرفية المفتوحة", "en": "Open Banking", "icon": "🏦"},
    {"ar": "اتصل بنا", "en": "Contact Us", "icon": "📞"}
]

# -----------------------------
# Load JSON Files
# -----------------------------
@st.cache_data
def load_json_file(filename: str) -> Dict[str, Any]:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    if not os.path.exists(filepath):
        st.error(f"❌ File not found: {filename}")
        st.stop()
    
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

SYSTEM_JSON = load_json_file("system_prompt_webbot.json")
KNOWLEDGE = load_json_file("knowledge_webbot.json")

SYSTEM_PROMPT = SYSTEM_JSON.get("system_prompt", {})
SYSTEM_TEXT = (
    f"{SYSTEM_PROMPT.get('goal','')}\n\n"
    f"Restrictions:\n- " + "\n- ".join(SYSTEM_PROMPT.get("restrictions", [])) + "\n\n"
    f"Style:\n- " + "\n- ".join(SYSTEM_PROMPT.get("style", [])) + "\n\n"
    f"Fallback AR: {SYSTEM_PROMPT.get('fallbacks',{}).get('ar','')}\n"
    f"Fallback EN: {SYSTEM_PROMPT.get('fallbacks',{}).get('en','')}\n\n"
    "Important: Always respond in the same language as the user's question."
).strip()

CHUNKS: List[Dict[str, Any]] = KNOWLEDGE.get("chunks", [])
if not CHUNKS:
    st.error("❌ Knowledge base is empty.")
    st.stop()

# -----------------------------
# RAG System
# -----------------------------
@st.cache_resource
def build_search_index(chunks: List[Dict[str, Any]]):
    texts = [c.get("text", "") for c in chunks]
    vectorizer = TfidfVectorizer(analyzer="word", ngram_range=(1, 2), min_df=1, max_df=0.95)
    tfidf_matrix = vectorizer.fit_transform(texts)
    return vectorizer, tfidf_matrix

VECTORIZER, TFIDF_MATRIX = build_search_index(CHUNKS)

def detect_language(text: str) -> str:
    arabic_chars = sum(1 for ch in text if "\u0600" <= ch <= "\u06FF")
    return "ar" if arabic_chars > len(text) * 0.2 else "en"

def retrieve_relevant_chunks(query: str, k: int = TOP_K, user_lang: str = "auto") -> List[Dict[str, Any]]:
    query_vec = VECTORIZER.transform([query])
    similarities = linear_kernel(query_vec, TFIDF_MATRIX).flatten()
    
    is_arabic = user_lang.lower().startswith("ar")
    is_english = user_lang.lower().startswith("en")
    
    scored_chunks = []
    for idx, score in enumerate(similarities):
        chunk = CHUNKS[idx]
        chunk_lang = str(chunk.get("lang", "")).lower()
        same_language = (is_arabic and chunk_lang.startswith("ar")) or (is_english and chunk_lang.startswith("en"))
        language_bonus = 0.08 if same_language else 0.0
        final_score = score + language_bonus
        scored_chunks.append((final_score, idx))
    
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return [CHUNKS[idx] for _, idx in scored_chunks[:k]]

def build_context_string(chunks: List[Dict[str, Any]]) -> str:
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        header = f"[{i}] (source={chunk.get('source','')}, page={chunk.get('page','')}, section={chunk.get('section','')})"
        text = chunk.get("text", "")
        context_parts.append(f"{header}\n{text}")
    full_context = "\n\n".join(context_parts)
    return full_context[:MAX_CONTEXT_CHARS]

# -----------------------------
# OpenAI Client
# -----------------------------
@st.cache_resource
def get_openai_client():
    """Initialize OpenAI client with API key"""
    api_key = None
    
    # Try Streamlit secrets (for cloud deployment)
    try:
        if "OPENAI_API_KEY" in st.secrets:
            api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass
    
    # Try environment variable
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
    
    # Try .env file (for local development)
    if not api_key:
        try:
            env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
            if os.path.exists(env_path):
                with open(env_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('OPENAI_API_KEY'):
                            api_key = line.split('=', 1)[1].strip()
                            api_key = api_key.strip('"').strip("'")
                            break
        except Exception:
            pass
    
    if not api_key or api_key == "your-api-key-here":
        st.error("❌ OPENAI API KEY NOT CONFIGURED")
        st.markdown("""
        ### Add your API key:
        
        **On Streamlit Cloud:**
        - Click "Manage app" → Settings → Secrets
        - Add: `OPENAI_API_KEY = "sk-proj-your-key"`
        
        **Locally:**
        - Edit `.env` file
        - Add your key
        
        Get key: https://platform.openai.com/api-keys
        """)
        st.stop()
    
    try:
        # Initialize with explicit timeout to avoid httpx issues
        client = OpenAI(
            api_key=api_key,
            timeout=30.0,
            max_retries=2
        )
        return client
    except Exception as e:
        st.error(f"❌ Error initializing OpenAI: {str(e)}")
        st.info("Try updating openai package: pip install --upgrade openai")
        st.stop()

def generate_response(system_prompt: str, user_query: str, context: str, user_lang: str = "auto") -> str:
    client = get_openai_client()
    
    user_message = (
        f"User Question: {user_query}\n"
        f"Question Language: {user_lang}\n\n"
        f"Available Knowledge:\n{context}\n\n"
        "Instructions: Answer ONLY based on the chunks above."
    )
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"

# -----------------------------
# CSS Styling
# -----------------------------
def inject_custom_css():
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# -----------------------------
# Main App
# -----------------------------
def main():
    inject_custom_css()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending_query" not in st.session_state:
        st.session_state.pending_query = None
    
    st.title("💬 Web Chat Bot")
    
    # Always show quick action buttons at the top
    st.markdown("### Quick Start")
    cols = st.columns(2)
    for idx, action in enumerate(QUICK_ACTIONS):
        col = cols[idx % 2]
        with col:
            button_text = f"{action['icon']} {action['ar']}\n{action['en']}"
            if st.button(button_text, key=f"quick_{idx}", use_container_width=True):
                st.session_state["pending_query"] = action["ar"]
                st.rerun()
    
    st.markdown("---")
    
    # Chat input BEFORE messages (so it stays visible)
    user_input = st.chat_input("Type your message...")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle pending query from quick action button
    if st.session_state.pending_query:
        user_input = st.session_state.pending_query
        st.session_state.pending_query = None
    
    if user_input:
        user_lang = detect_language(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                relevant_chunks = retrieve_relevant_chunks(user_input, k=TOP_K, user_lang=user_lang)
                context = build_context_string(relevant_chunks)
                response = generate_response(SYSTEM_TEXT, user_input, context, user_lang=user_lang)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

if __name__ == "__main__":
    main()
