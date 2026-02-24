import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.title("🎤 AI Transcript App (with Latency)")

audio_file = st.audio_input("Record your voice")

if audio_file is not None:
    st.audio(audio_file)

    if st.button("Run Full Pipeline"):
        with st.spinner("Processing..."):
            files = {
                "audio": ("audio.wav", audio_file.read(), "audio/wav")
            }

            res = requests.post(
                f"{BACKEND_URL}/api/full",
                files=files
            )

        if res.status_code != 200:
            st.error("Request failed")
            st.stop()

        data = res.json()

        if not data["success"]:
            st.error(data["error"])
            st.stop()

        # Outputs
        st.subheader("📄 Raw Transcript")
        st.write(data["raw_text"])

        st.subheader("✨ Cleaned Transcript")
        st.write(data["cleaned_text"])

        # Metrics
        latency = data["total_time"]

        st.subheader("⏱️ Latency Breakdown")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Whisper",
            f"{data['transcription_time']:.2f}s"
        )

        col2.metric(
            "LLM",
            f"{data['llm_time']:.2f}s"
        )

        col3.metric(
            "Total",
            f"{data['total_time']:.2f}s"
        )