# AI Transcript App

A **follow-along and improvement project** based on the [AI-Engineer-Skool/local-ai-transcript-app](https://github.com/AI-Engineer-Skool/local-ai-transcript-app) tutorial. The goal is to learn about **speech-to-text (STT)** and **text-to-speech (TTS)** models, experiment with different backends, and evolve the app for lower latency and better performance.

- **Upstream repo & tutorial:** [github.com/AI-Engineer-Skool/local-ai-transcript-app](https://github.com/AI-Engineer-Skool/local-ai-transcript-app)
- **📺 Video walkthrough:** [YouTube – project structure and API details](https://youtu.be/WUo5tKg2lnE)

This fork starts from the vanilla stack: **Whisper** for STT and an LLM for transcript cleaning, with a browser-based recording UI and FastAPI backend. The roadmap includes **expanding model selection** (e.g. alternative STT/TTS engines) to **reduce latency** and **improve performance** while keeping the app usable locally.

---

## Learning focus: STT & TTS

- **Initial setup:** STT via **Whisper** (English, runs locally).
- **Planned improvements:** Broaden model choices for both STT and (optionally) TTS to compare latency, accuracy, and resource use; tune for faster transcription and better quality.

---
**Features:**

- 🎤 Browser-based voice recording
- 🔊 English Whisper speech-to-text (runs locally)
- 🤖 LLM cleaning (removes filler words, fixes errors)
- 🔌 **OpenAI API-compatible** (works with Ollama, LM Studio, OpenAI, or any OpenAI-compatible API)
- 📋 One-click copy to clipboard

---

## Quick Start 

### 🚀 Dev Container 

1. **Prerequisites:** [Docker Desktop](https://www.docker.com/products/docker-desktop/), [VS Code](https://code.visualstudio.com/), [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
2. **Open in container:** In VS Code, **"Reopen in Container"** (or `Cmd/Ctrl+Shift+P` → **"Dev Containers: Reopen in Container"**).
3. **Wait ~5–10 minutes** for build and Ollama model download. The devcontainer creates `backend/.env` and starts Ollama automatically.

Then go to [How to run the app](#how-to-run-the-app).

---

## How to run the app

After your environment is ready (Dev Container), use **two terminals** and follow these steps.

**Step 1 — Start the backend**

In the first terminal, from the project root:

```bash
cd backend
uv sync && uv run uvicorn app:app --reload --host 0.0.0.0 --port 8000 --timeout-keep-alive 600
```

Wait until you see `✅ Ready!` (Whisper and LLM are loaded).  
`uv sync` keeps dependencies up to date; `--timeout-keep-alive 600` allows long audio processing.

**Step 2 — Start the frontend**

In a second terminal, from the project root:

```bash
cd frontend
npm install && npm run dev
```

Wait until the dev server is running (e.g. "Local: http://localhost:3000").

**Step 3 — Open the app**

In your browser, go to **http://localhost:3000**.

You can now record, upload audio, or paste text; use the settings to toggle LLM cleaning and copy the transcript.

---

## Configuration

### OpenAI API Compatibility

**This app is compatible with any OpenAI API-format LLM provider:**

- **Ollama** (default - works out of the box in devcontainer)
- **LM Studio** (local alternative)
- **OpenAI API** (cloud-based)
- Any other OpenAI-compatible API

The devcontainer automatically creates `backend/.env` with working Ollama defaults. **No configuration needed to get started.**

To use a different provider, edit `backend/.env`:

- `LLM_BASE_URL` - API endpoint
- `LLM_API_KEY` - API key
- `LLM_MODEL` - Model name

---

## Troubleshooting

**Container won't start or is very slow:**

⚠️ **This app runs an LLM on CPU and requires adequate Docker resources.**

Configure Docker Desktop resources:

1. Open **Docker Desktop** → **Settings** → **Resources**
2. Set **CPUs** to maximum available (8+ cores recommended)
3. Set **Memory** to at least 16GB
4. Click **Apply & Restart**

**Expected specs:** Modern laptop/desktop with 8+ CPU cores and 16GB RAM. More CPU = faster LLM responses.

**Microphone not working:**

- Use Chrome or Firefox (Safari may have issues)
- Check browser permissions: Settings → Privacy → Microphone

**Backend fails to start:**

- Check Whisper model downloads: `~/.cache/huggingface/`
- Ensure enough disk space (models are ~150MB)

**LLM errors:**

- Make sure Ollama service is running (it auto-starts with devcontainer)
- Check model is downloaded: Model downloads automatically during devcontainer setup
- Transcription still works without LLM (raw Whisper only)

**LLM is slow:**

- See "Container won't start or is very slow" section above for Docker resource configuration
- **Fallback option:** Switch to another model (edit `LLM_MODEL` in `backend/.env`)
  - ⚠️ **Trade-off:** 3b is faster but **significantly worse at cleaning transcripts**
- **Best alternative:** Use a cloud API like OpenAI for instant responses with excellent quality (edit `.env`)

**Cannot access localhost:3000 or localhost:8000 from host machine:**

- **Docker Desktop:** Go to **Settings** → **Resources** → **Network**
- Enable **"Use host networking"** (may require Docker Desktop restart)
- Restart the frontend and backend servers

**Port already in use:**

- Backend: Change port with `--port 8001`
- Frontend: Edit `vite.config.js`, change `port: 3000`
