import streamlit as st
import ollama

# Configure the page - set sidebar to collapsed initially for a cleaner look
st.set_page_config(
    page_title="SecureNotes AI", 
    page_icon="🌿", 
    layout="centered",
    initial_sidebar_state="collapsed" # Users can open it using the top-left arrow
)

# --- Custom CSS for 1.6x Font Size & Modern UI ---
st.markdown("""
<style>
    /* Increase global font size */
    html, body, [class*="css"] {
        font-size: 18px !important; 
    }
    
    /* Make headers pop and significantly larger */
    h1 {
        font-size: 3.5rem !important;
        color: #2d382d !important;
        font-weight: 800 !important;
        padding-bottom: 0.5rem;
    }
    h3 {
        font-size: 1.8rem !important;
        color: #4a5c4a !important;
        font-weight: 600 !important;
    }
    
    /* Style the text area to look softer, larger, and more inviting */
    .stTextArea textarea {
        font-size: 1.3rem !important;
        border-radius: 12px !important;
        border: 2px solid #cbd5cb !important;
        padding: 15px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        line-height: 1.6 !important;
    }
    .stTextArea textarea:focus {
        border-color: #5b7c5b !important;
        box-shadow: 0 4px 12px rgba(91,124,91,0.2) !important;
    }
    
    /* Beautify the primary button */
    .stButton button {
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        width: 100%;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
    }
    
    /* Make markdown paragraphs bigger */
    .stMarkdown p {
        font-size: 1.3rem !important;
        line-height: 1.6 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- UI Header ---
st.title("🌿 SecureNotes AI")
st.markdown("**100% Offline, Private Note Structuring for Professionals.**")
st.markdown("*(Click the arrow in the top left to open settings)*")
st.markdown("---")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Settings")
    st.write("Because this uses local AI, your client data never touches the internet.")
    
    model_choice = st.selectbox("Open-Weight Model", ["llama3.2", "phi3", "mistral"])
    
    output_format = st.radio(
        "What do you need?",
        ["Structured Client File", "Follow-up Email", "Both (File & Email)"]
    )

# --- Main Interface ---
st.write("### Paste your messy session notes below:")
raw_notes = st.text_area("Raw Notes", height=250, label_visibility="collapsed", placeholder="e.g., Met with client today. wants to increase budget by 20%. struggling with time management. need to send them the Q3 report by friday...")

if st.button("Process Securely (Local)", type="primary"):
    if not raw_notes.strip():
        st.warning("Please enter some notes first.")
    else:
        with st.spinner(f"Processing locally using {model_choice}..."):
            system_prompt = f"""
            You are an expert assistant. Your job is to take messy, stream-of-consciousness notes and organize them professionally. 
            The user has requested this output format: {output_format}.
            
            If 'Structured Client File': Extract Key Takeaways, Action Items, and Next Steps.
            If 'Follow-up Email': Draft a polite, professional email summarizing the notes and next steps.
            If 'Both': Do both, clearly separated.
            
            Keep the tone professional and concise. Do not add information that is not in the notes.
            """
            
            try:
                response = ollama.chat(model=model_choice, messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': raw_notes}
                ])
                st.success("✨ Done!")
                st.markdown("### Result:")
                
                # Wrap output in a clean, modern card
                st.markdown(f"""
                <div style="background-color: #ffffff; padding: 25px; border-radius: 12px; border-left: 6px solid #5b7c5b; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                    <p style="font-size: 1.25rem; white-space: pre-wrap; color: #2d382d; margin: 0;">{response['message']['content']}</p>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error("⚠️ Could not connect to the local model.")
                st.write(f"Error details: {e}")