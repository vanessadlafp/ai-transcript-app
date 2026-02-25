import streamlit as st
import requests

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="AI Transcript Pipeline",
    page_icon="🎙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BACKEND_URL = "http://localhost:8000"

# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOM CSS - MATCHING THE REDESIGN
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');
    
    :root {
        --bg: #f0f4ff;
        --surface: #ffffff;
        --surface2: #f5f7fd;
        --text: #0c0e1e;
        --text-2: #4e5470;
        --text-3: #9fa6c0;
        --blue: #1e4dff;
        --blue-soft: rgba(30,77,255,0.07);
        --blue-border: rgba(30,77,255,0.18);
        --border: rgba(20,30,90,0.08);
        --border-md: rgba(20,30,90,0.12);
        --sans: 'Plus Jakarta Sans', system-ui, sans-serif;
        --serif: 'Syne', sans-serif;
        --mono: 'DM Mono', monospace;
    }
    
    .stApp {
        background: var(--bg);
    }
    
    .main .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 680px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Typography */
    h1, h2, h3 {
        font-family: var(--serif);
        color: var(--text);
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    
    h1 {
        font-size: 42px;
        line-height: 1.07;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.13em;
        color: var(--text-3);
        font-family: var(--mono);
        font-weight: 500;
        margin-top: 2rem;
        margin-bottom: 0.75rem;
    }
    
    h3 {
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    p, div, span {
        font-family: var(--sans);
        color: var(--text);
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--blue);
        color: white;
        border: none;
        border-radius: 9px;
        padding: 0.7rem 2rem;
        font-family: var(--serif);
        font-weight: 700;
        font-size: 15px;
        transition: all 0.2s;
        box-shadow: 0 4px 18px rgba(30,77,255,0.14);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 28px rgba(30,77,255,0.18);
        background: #1a3fd4;
    }
    
    /* Audio recorder */
    .stAudioInput {
        background: var(--surface2);
        border: 1.5px dashed var(--border-md);
        border-radius: 10px;
        padding: 2rem 1.5rem;
        text-align: center;
    }
    
    .stAudioInput:hover {
        border-color: var(--blue);
        background: var(--blue-soft);
    }
    
    /* Audio player */
    audio {
        width: 100%;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: var(--serif);
        font-weight: 700;
        font-size: 28px;
        color: var(--text);
    }
    
    [data-testid="stMetricLabel"] {
        font-family: var(--mono);
        font-size: 11px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--text-3);
    }
    
    [data-testid="stMetricDelta"] {
        font-family: var(--mono);
        font-size: 12px;
    }
    
    /* Content boxes */
    .stMarkdown {
        font-family: var(--sans);
    }
    
    /* Text content styling */
    .transcript-box {
        background: var(--surface);
        border: 1px solid var(--border-md);
        border-radius: 10px;
        padding: 1.25rem 1.5rem;
        margin: 1rem 0;
        font-size: 15px;
        line-height: 1.8;
        color: var(--text-2);
    }
    
    .cleaned-box {
        background: var(--surface);
        border: 1px solid var(--border-md);
        border-radius: 10px;
        padding: 1.25rem 1.5rem;
        margin: 1rem 0;
        font-size: 16px;
        line-height: 1.85;
        color: var(--text);
        font-weight: 400;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: var(--blue) transparent transparent transparent;
    }
    
    /* Error messages */
    .stAlert {
        background: rgba(239,68,68,0.08);
        border: 1px solid rgba(239,68,68,0.2);
        border-radius: 10px;
        font-family: var(--sans);
        color: #dc2626;
    }
    
    /* Section divider */
    hr {
        border: none;
        border-top: 1px solid var(--border-md);
        margin: 2rem 0;
    }
    
    /* Eyebrow labels */
    .eyebrow {
        font-family: var(--mono);
        font-size: 10px;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        color: var(--text-3);
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .eyebrow::after {
        content: '';
        flex: 1;
        height: 1px;
        background: var(--border-md);
    }
    
    /* Tag badge */
    .tag {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        font-family: var(--mono);
        font-size: 11px;
        letter-spacing: 0.09em;
        color: var(--blue);
        background: var(--blue-soft);
        border: 1px solid var(--blue-border);
        padding: 4px 12px;
        border-radius: 99px;
        margin-bottom: 1rem;
    }
    
    .tag-dot {
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: var(--blue);
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════════════════════════════

# Hero section
st.markdown("""
<div style='margin-bottom: 2.5rem;'>
    <div class='tag'>
        <div class='tag-dot'></div>
       STT + LLM Cleaning
    </div>
    <h1>AI Transcript<br><span style='color: #1e4dff;'>Pipeline</span></h1>
    <p style='font-size: 15px; color: #4e5470; line-height: 1.7; margin-top: 0.75rem;'>
       Full transcription pipeline with real-time latency metrics.
    </p>
</div>
""", unsafe_allow_html=True)

# Input section
st.markdown("<div class='eyebrow'>Input Audio</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🎙 Record**")
    recorded_audio = st.audio_input("Record your voice", label_visibility="collapsed")

with col2:
    st.markdown("**📁 Upload**")
    uploaded_audio = st.file_uploader(
        "Upload audio",
        type=["wav", "mp3", "m4a", "ogg"],
        label_visibility="collapsed"
    )
# ═══════════════════════════════════════════════════════════════════════════════
# INPUT PRIORITY LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
audio_bytes = None
filename = "audio.wav"

if recorded_audio and uploaded_audio:
    st.warning("⚠️ Using recorded audio (upload ignored)")
    audio_bytes = recorded_audio.read()
    filename = "recording.wav"

elif recorded_audio:
    audio_bytes = recorded_audio.read()
    filename = "recording.wav"

elif uploaded_audio:
    audio_bytes = uploaded_audio.read()
    filename = uploaded_audio.name


if audio_bytes is not None:
    st.audio(audio_bytes)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Process Audio →"):
        with st.spinner("Processing..."):
            files = {
                "audio": (filename, audio_bytes)
            }
            try:
                res = requests.post(
                    f"{BACKEND_URL}/api/full",
                    files=files
                )
                
                if res.status_code != 200:
                    st.error("❌ Request failed. Is the backend running?")
                    st.stop()
                
                data = res.json()
                
                if not data["success"]:
                    st.error(f"❌ {data['error']}")
                    st.stop()
                
                # Success! Show results
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Raw transcript
                st.markdown("<div class='eyebrow'>Raw Transcript</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='transcript-box'>{data['raw_text']}</div>", unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Cleaned transcript
                st.markdown("<div class='eyebrow'>Cleaned Transcript</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='cleaned-box'>{data['cleaned_text']}</div>", unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Latency metrics
                st.markdown("<div class='eyebrow'>Performance Metrics</div>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        label="Whisper",
                        value=f"{data['transcription_time']:.2f}s"
                    )
                
                with col2:
                    st.metric(
                        label="LLM Cleaning",
                        value=f"{data['llm_time']:.2f}s"
                    )
                
                with col3:
                    st.metric(
                        label="Total Time",
                        value=f"{data['total_time']:.2f}s"
                    )
                
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure it's running at http://localhost:8000")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
else:
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0; color: #9fa6c0; font-size: 14px;'>
        👆 Click the button above to start recording
    </div>
    """, unsafe_allow_html=True)