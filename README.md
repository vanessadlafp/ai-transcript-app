# AI Transcript App

A **follow-along and improvement project** based on the [AI-Engineer-Skool/local-ai-transcript-app](https://github.com/AI-Engineer-Skool/local-ai-transcript-app) tutorial. The goal is to learn about **speech-to-text (STT)** and **text-to-speech (TTS)** models, experiment with different backends, and evolve the app for lower latency and better performance.

- **Upstream repo & tutorial:** [github.com/AI-Engineer-Skool/local-ai-transcript-app](https://github.com/AI-Engineer-Skool/local-ai-transcript-app)
- **📺 Video walkthrough:** [YouTube – project structure and API details](https://youtu.be/WUo5tKg2lnE)

This fork starts from the vanilla stack: **Whisper** for STT and an LLM for transcript cleaning, with a **Streamlit** frontend and FastAPI backend. A **latency tracker** shows Whisper, LLM, and total pipeline times. The roadmap includes **expanding model selection** (e.g. alternative STT/TTS engines) to **reduce latency** and **improve performance** while keeping the app usable locally.

### Quick demo

Record or upload audio, then run the full pipeline to get the cleaned transcript and latency metrics.

![AI Transcript Pipeline demo](assets/local-ai-transcript-demo.gif)

---

## Learning focus: STT & TTS

- **Initial setup:** STT via **Whisper** (English, runs locally).
- **Planned improvements:** Broaden model choices for both STT and (optionally) TTS to compare latency, accuracy, and resource use; tune for faster transcription and better quality.

---
**Features:**

- 🎤 **Record or upload** — Browser-based voice recording or drag-and-drop upload (WAV, MP3, M4A, OGG; limit 200MB per file)
- 🔊 English Whisper speech-to-text (runs locally)
- 🤖 LLM cleaning (removes filler words, fixes errors)
- ⏱️ **Latency tracker** — Whisper time, LLM time, and total pipeline time
- 🔌 **OpenAI API-compatible** (works with Ollama, LM Studio, OpenAI, or any OpenAI-compatible API)

**Recent frontend updates:**

- Header updated to **STT + LLM Cleaning** with subtitle: *Full transcription pipeline with real-time latency metrics.*
- **Input Audio** section with two options side by side: **Record** (microphone) and **Upload** (file picker or drag-and-drop).
- If both recorded and uploaded audio are present, the app uses the recording and shows a short notice; otherwise it uses whichever source is available.
- Single **Process Audio →** action for either input; results show cleaned transcript and overall latency.

---

## Quick Start 

### 🚀 Dev Container 

1. **Prerequisites:** [Docker Desktop](https://www.docker.com/products/docker-desktop/), [VS Code](https://code.visualstudio.com/), [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
2. **Open in container:** In VS Code, **"Reopen in Container"** (or `Cmd/Ctrl+Shift+P` → **"Dev Containers: Reopen in Container"**).
3. **Wait ~5–10 minutes** for build and Ollama model download. The devcontainer creates `backend/.env` and starts Ollama automatically.

Then go to [How to run the app](#how-to-run-the-app).

---

## How to run the app (dev)

The app runs inside the dev container. Use **Docker Compose** to start the environment, then run backend and frontend in **two terminals** (both inside the container).

**Step 1 — Start the environment**

From the project root (e.g. repo root on your machine):

```bash
docker compose up -d
```

**Step 2 — Enter the container**

```bash
docker compose exec app bash
```

**Step 3 — Start the backend** (first terminal, inside container)

```bash
cd workspaces/ai-transcript-app/backend
uv sync
uv run uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Wait until you see `✅ Ready!` (Whisper and LLM are loaded).

- **API docs:** http://localhost:8000/docs  
- **Health check:** http://localhost:8000/api/status  

**Step 4 — Start the frontend** (new terminal, inside container)

Open a **new terminal**, then:

```bash
docker compose exec app bash
cd workspaces/ai-transcript-app/frontend
export HOME=/tmp
uv run streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

- **Frontend app:** http://localhost:8501  

**Step 5 — Use the app**

Open **http://localhost:8501** in your browser. Use **Record** or **Upload** to provide audio, click **Process Audio →**, and see the raw transcript, cleaned transcript, and **latency breakdown** (Whisper, LLM, total time). No extra env vars needed inside the container.

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

**Cannot access localhost:8501 or localhost:8000 from host machine:**

- **Docker Desktop:** Go to **Settings** → **Resources** → **Network**
- Enable **"Use host networking"** (may require Docker Desktop restart)
- Restart the frontend and backend servers

**Port already in use:**

- Backend: Change port with `--port 8001` (and set `BACKEND_URL` in the Streamlit app if needed)
- Frontend: Use a different port, e.g. `uv run streamlit run streamlit_app.py --server.port 8502 --server.address 0.0.0.0`
