#!/usr/bin/env python3
"""
Uses OpenAI API format, compatible with Ollama, OpenAI, LM Studio, and other providers.
Configuration is loaded from .env file.
"""

from pathlib import Path

from faster_whisper import WhisperModel
from openai import OpenAI
import time

# Edit system_prompt.txt to change how the LLM cleans transcriptions
PROMPT_FILE = Path(__file__).parent / "system_prompt.txt"
SYSTEM_PROMPT = PROMPT_FILE.read_text().strip()


class TranscriptionService:
    """Uses OpenAI-compatible API, works with any provider (Ollama, OpenAI, LM Studio, etc.)."""

    def __init__(
        self, whisper_model: str, llm_base_url: str, llm_api_key: str, llm_model: str
    ):
        print(f"🔄 Loading Whisper model '{whisper_model}'...")
        self.whisper = WhisperModel(
            whisper_model,
            device="auto",  # Auto-detect: Metal (Mac), CUDA (NVIDIA), or CPU
            compute_type="int8",
        )
        print(f"✅ Whisper model '{whisper_model}' loaded!")

        print(f"🔄 Connecting to LLM at {llm_base_url}...")
        self.llm_client = OpenAI(base_url=llm_base_url, api_key=llm_api_key)
        self.llm_model = llm_model

        try:
            self.llm_client.models.list()
            print("✅ Connected to LLM API!")
        except Exception as e:
            print(f"⚠️  Warning: Could not connect to LLM: {e}")
            print(f"   Make sure your LLM server is running at {llm_base_url}")

    def transcribe(self, audio_file):
        print("🔄 Transcribing...")

        segments, info = self.whisper.transcribe(
            audio_file, beam_size=5, language="en", condition_on_previous_text=False
        )

        text = " ".join([segment.text for segment in segments]).strip()
        print(f"📝 Raw: {text}")
        return text

    def get_default_system_prompt(self):
        return SYSTEM_PROMPT

    def clean_with_llm(self, text, system_prompt=None):
        if not text:
            return ""

        # Use custom prompt or fall back to default
        prompt_to_use = system_prompt if system_prompt else SYSTEM_PROMPT

        print("🤖 Cleaning with LLM...")

        try:
            response = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": prompt_to_use},
                    {"role": "user", "content": text},
                ],
                temperature=0.3,
                max_tokens=200,
            )

            cleaned = response.choices[0].message.content.strip()
            print(f"✨ Cleaned: {cleaned}")
            return cleaned

        except Exception as e:
            print(f"⚠️  LLM error: {e}")
            return text  # Fallback to raw text

    def transcribe_file(self, audio_file_path: str, use_llm: bool = True) -> dict:
        total_start = time.time()

        # Step 1: Whisper
        t0 = time.time()
        raw_text = self.transcribe(audio_file_path)
        transcription_time = time.time() - t0
        
        # Step 2: LLM
        t1 = time.time()
        if use_llm and raw_text:
            cleaned_text = self.clean_with_llm(raw_text)
            llm_time = time.time() - t1
        else:
            cleaned_text = raw_text
            llm_time = 0

        total_time = time.time() - total_start

        return {
            "raw_text": raw_text,
            "cleaned_text": cleaned_text,
            "transcription_time": transcription_time,
            "llm_time": llm_time,
            "total_time": total_time}
