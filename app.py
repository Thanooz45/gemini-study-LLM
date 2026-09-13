import os
import streamlit as st
from google import genai
from google.genai import types

# ----------------------------------------------------
# Page Configuration & UI Theming
# ----------------------------------------------------
st.set_page_config(
    page_title="AI Study Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #4F46E5, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #6B7280;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .persona-card {
        padding: 1rem;
        border-radius: 10px;
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# API Key Management
# ----------------------------------------------------
api_key = os.getenv("GEMINI_API_KEY")

with st.sidebar:
    st.header("⚙️ Settings")
    
    # Allow manual override if secret is not set
    if not api_key:
        api_key = st.text_input(
            "Gemini API Key", 
            type="password", 
            placeholder="Paste AIzaSy... key",
            help="Get your key at https://aistudio.google.com"
        )
    else:
        st.success("API Key detected from environment/secrets", icon="🔑")

    st.markdown("---")
    st.subheader("🎭 Persona Profiles")
    persona = st.radio(
        "Select your assistant's style:",
        ["Friendly Guide", "Academic Professor", "Socratic Tutor"],
        index=0
    )
    
    persona_descriptions = {
        "Friendly Guide": "Encouraging, enthusiastic, and simplifies complex ideas using relatable everyday analogies.",
        "Academic Professor": "Rigorous, structured, precise academic vocabulary, and detailed breakdowns.",
        "Socratic Tutor": "Guides you toward the answer by asking thoughtful questions and promoting active recall."
    }
    st.caption(persona_descriptions[persona])

# System Prompts Mapping
personalities = {
    "Friendly Guide": (
        "You are a friendly, enthusiastic, and highly encouraging Study Assistant. "
        "Break down complex concepts into intuitive, simple explanations with real-world analogies. "
        "End with a short check-for-understanding question."
    ),
    "Academic Professor": (
        "You are a university Professor. Provide thorough, precise, and well-structured academic explanations. "
        "Use formal discipline-specific terminology, cite standard theoretical foundations, and offer structured key takeaways."
    ),
    "Socratic Tutor": (
        "You are a Socratic tutor. Do not provide direct answers immediately. Instead, explain foundational concepts "
        "and ask guided, probing questions to lead the user to synthesize their own solution."
    )
}

# ----------------------------------------------------
# Main Interface
# ----------------------------------------------------
st.markdown('<div class="main-title">🎓 AI Study Companion</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask any question to get clear explanations tailored to your preferred learning mode.</div>', unsafe_allow_html=True)

# Input Layout
question = st.text_area(
    "What would you like to learn today?",
    placeholder="e.g., Explain the difference between process and thread in operating systems...",
    height=120
)

col1, col2 = st.columns([1, 4])
with col1:
    submit_btn = st.button("🚀 Explain", type="primary", use_container_width=True)
with col2:
    if st.button("🧹 Clear", use_container_width=False):
        st.rerun()

# ----------------------------------------------------
# Response Generation (Streaming with gemini-3.6-flash)
# ----------------------------------------------------
if submit_btn:
    if not api_key:
        st.error("Please provide a Gemini API Key in the sidebar or via Streamlit Secrets.")
    elif not question.strip():
        st.warning("Please enter a question first.")
    else:
        try:
            client = genai.Client(api_key=api_key.strip())
            
            st.markdown("---")
            st.subheader(f"Explanation ({persona})")
            
            response_container = st.empty()
            full_response = ""

            # Stream the response using gemini-3.6-flash
            with st.spinner("Analyzing and preparing response..."):
                response_stream = client.models.generate_content_stream(
                    model="gemini-3.6-flash",
                    config=types.GenerateContentConfig(
                        system_instruction=personalities[persona],
                        max_output_tokens=2500
                    ),
                    contents=question
                )

                for chunk in response_stream:
                    if chunk.text:
                        full_response += chunk.text
                        response_container.markdown(full_response + "▌")

                # Final display without the streaming cursor
                response_container.markdown(full_response)

        except Exception as e:
            st.error(f"Generation error: {e}")
