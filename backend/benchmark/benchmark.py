import time
import requests
import statistics
import csv
from pathlib import Path
import wave

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════════════════════
BACKEND_URL = "http://localhost:8000/api/full"

AUDIO_DIR = Path("benchmark/audio")
# SETUP INFO
LLM_MODEL="gemma3:4b"
WHISPER_MODEL="base.en"

SETUP = {
        "whisper": WHISPER_MODEL,
        "llm": LLM_MODEL,
        "setup_name": f"whisper:{WHISPER_MODEL} + llm:{LLM_MODEL}",
    }

AUDIO_FILES = [
    "sample_a.wav",
    "sample_b.wav",
    "sample_c.wav",
]

N_RUNS = 4
WARMUP_RUNS = 1

OUTPUT_CSV = f"benchmark/results_{LLM_MODEL}_{WHISPER_MODEL}.csv"

# ═══════════════════════════════════════════════════════════════════════════════
# SINGLE RUN
# ═══════════════════════════════════════════════════════════════════════════════

def run_single(audio_path):
    with open(audio_path, "rb") as f:
        files = {
            "audio": (audio_path.name, f, "audio/wav")
        }

        start = time.time()
        res = requests.post(BACKEND_URL, files=files)
        end = time.time()

    if res.status_code != 200:
        raise RuntimeError(f"Request failed: {res.text}")

    data = res.json()

    if not data.get("success", False):
        raise RuntimeError(f"Backend error: {data.get('error')}")

    return {
        "transcription_time": data["transcription_time"],
        "llm_time": data["llm_time"],
        "total_time": data["total_time"],
        "wall_time": end - start,
    }

# ═══════════════════════════════════════════════════════════════════════════════
# GET AUDIO DURATION
# ═══════════════════════════════════════════════════════════════════════════════

def get_audio_duration(path):
    with wave.open(str(path), 'rb') as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return frames / float(rate)
# ═══════════════════════════════════════════════════════════════════════════════
# BENCHMARK LOOP
# ═══════════════════════════════════════════════════════════════════════════════

def benchmark():
    results = []

    print(f"\n⚙️ Setup: {SETUP['setup_name']}")
    print(f"🎧 Audio duration: {get_audio_duration(AUDIO_DIR / AUDIO_FILES[0])} seconds")

    for audio_file in AUDIO_FILES:
        audio_path = AUDIO_DIR / audio_file

        print(f"\n🎧 Benchmarking: {audio_file}")

        runs = []

        for i in range(N_RUNS):
            print(f"  Run {i + 1}/{N_RUNS}...")

            try:
                metrics = run_single(audio_path)
                runs.append(metrics)

                print(
                    f"    STT: {metrics['transcription_time']:.2f}s | "
                    f"LLM: {metrics['llm_time']:.2f}s | "
                    f"Total: {metrics['total_time']:.2f}s"
                )

            except Exception as e:
                print(f"    ❌ Error: {e}")

        # Remove warmup runs
        valid_runs = runs[WARMUP_RUNS:]

        if not valid_runs:
            print("    ⚠️ No valid runs")
            continue

        # Aggregation helper
        def agg(key):
            values = [r[key] for r in valid_runs]
            return (
                statistics.mean(values),
                statistics.stdev(values) if len(values) > 1 else 0.0
            )

        t_mean, t_std = agg("transcription_time")
        l_mean, l_std = agg("llm_time")
        tot_mean, tot_std = agg("total_time")
        w_mean, w_std = agg("wall_time")

        summary = {
            **SETUP,
            "audio_file": audio_file,
            "n_runs": len(valid_runs),

            "transcription_time_mean": t_mean,
            "transcription_time_std": t_std,

            "llm_time_mean": l_mean,
            "llm_time_std": l_std,

            "total_time_mean": tot_mean,
            "total_time_std": tot_std,

            "wall_time_mean": w_mean,
            "wall_time_std": w_std,
        }

        results.append(summary)

        print("\n  ✅ Summary:")
        print(f"    STT:   {t_mean:.2f}s ± {t_std:.2f}")
        print(f"    LLM:   {l_mean:.2f}s ± {l_std:.2f}")
        print(f"    Total: {tot_mean:.2f}s ± {tot_std:.2f}")

    return results

# ═══════════════════════════════════════════════════════════════════════════════
# SAVE RESULTS
# ═══════════════════════════════════════════════════════════════════════════════

def save_csv(results):
    OUTPUT_CSV_PATH = Path(OUTPUT_CSV)
    OUTPUT_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

    keys = results[0].keys()

    with open(OUTPUT_CSV_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)

    print(f"\n📁 Results saved to: {OUTPUT_CSV_PATH}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    results = benchmark()

    if results:
        save_csv(results)
    else:
        print("❌ No results to save")