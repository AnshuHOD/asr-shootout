# 🎙️ ASR Shootout — Intern Assignment Roadmap

> **Goal:** Benchmark ASR systems for Indian conversational speech (Hindi/Hinglish/Kannada) and present findings comparing Deepgram (baseline) vs 2+ other models.

---

## 📁 Folder Structure

```
asr-shootout/
├── recordings/                  # Tumhari 20 audio files
│   ├── 01_koramangala_quiet.wav
│   ├── 02_indiranagar_noisy.wav
│   ├── 03_whitefield_phone.wav
│   └── ... (20 total)
├── data/                        # Optional open-source datasets
│   └── kathbath_samples/
├── transcripts/                 # Ground truth text files
│   └── ground_truth.json
├── pipeline/
│   ├── run_deepgram.py
│   ├── run_whisper.py
│   ├── run_indicwhisper.py
│   ├── compute_metrics.py
│   └── requirements.txt
├── results/
│   ├── raw_outputs.json         # All model transcriptions
│   └── metrics_summary.csv      # WER, CER, Entity Accuracy
└── report.md                    # Final 3-page report
```

---

## 🎙️ Phase 1: Audio Recording Checklist

### 20 Locality Names to Record

| # | Locality | Suggested Sentence |
|---|----------|-------------------|
| 1 | Koramangala | "Haan, main Koramangala mein rehta hoon" |
| 2 | Indiranagar | "Mera ghar Indiranagar ke paas hai" |
| 3 | Whitefield | "Main Whitefield se aata hoon daily" |
| 4 | Electronic City | "Meri company Electronic City mein hai" |
| 5 | Marathahalli | "Bhai, Marathahalli mein traffic bahut hai" |
| 6 | Jayanagar | "Main Jayanagar 4th block mein rehta hoon" |
| 7 | Rajajinagar | "Rajajinagar se bus milti hai kya?" |
| 8 | Hebbal | "Hebbal flyover ke paas hai mera ghar" |
| 9 | Yelahanka | "Yelahanka thoda door hai metro se" |
| 10 | Banashankari | "Banashankari temple ke paas rehti hoon" |
| 11 | HSR Layout | "HSR Layout mein flat liya hai maine" |
| 12 | BTM Layout | "BTM Layout 2nd stage mein hoon" |
| 13 | Majestic | "Majestic bus stand se pakad lena bus" |
| 14 | Silk Board | "Silk Board junction pe jam lagta hai" |
| 15 | Bellandur | "Bellandur lake ke paas hai office" |
| 16 | Sarjapur | "Sarjapur road pe naya project aa raha" |
| 17 | Bommanahalli | "Bommanahalli se Koramangala kitna time?" |
| 18 | KR Puram | "KR Puram railway station ke paas hoon" |
| 19 | Peenya | "Peenya Industrial Area mein kaam karta hoon" |
| 20 | Yeshwanthpur | "Yeshwanthpur se train pakadni hai mujhe" |

> **Tip:** Remaining localities (Byatarayanapura, Kadugondanahalli, etc.) are bonus — record karo agar time ho.

### Recording Conditions — Vary Karo! (Critical)

| Recording # | Condition | How to Achieve |
|------------|-----------|---------------|
| 1–5 | Quiet room | Bedroom, closed windows |
| 6–10 | Street/traffic noise | Balcony ya road ke paas |
| 11–14 | Rushed/fast speech | Bolte time jaldi karo |
| 15–17 | Whispered | Slowly whisper karo |
| 18–20 | Phone simulation | Call karke record karo, ya speakerphone |

### Recording Guidelines
- **Format:** WAV ya MP3, minimum 16kHz sample rate
- **Device:** Apna phone ka mic (studio setup mat karo)
- **Naming:** `01_koramangala_quiet.wav` (number_locality_condition)
- **Duration:** 3–8 seconds per clip
- **Language:** Mix karo — kuch Hindi, kuch Hinglish, kuch Kannada

---

## 🤖 Phase 2: Model Selection

### Baseline (Mandatory)
| Model | Type | Why |
|-------|------|-----|
| **Deepgram Nova-2** | API | Assignment ka baseline; fast, multilingual support |

### Additional Models (Pick 2–3)

| Model | Type | Why Choose It |
|-------|------|--------------|
| **OpenAI Whisper (large-v3)** | Open-source, local | Best open-source multilingual; strong Hindi support |
| **AI4Bharat IndicWhisper** | Open-source, Indic-specific | Trained on Indian languages; strong for Hindi/Kannada |
| **Google Speech-to-Text v2** | API | Industry standard; good comparison point |
| **Azure Speech (hi-IN)** | API | Hindi-specific model; enterprise baseline |

**Recommended combo:** Deepgram + Whisper large-v3 + IndicWhisper
- Deepgram: API-based baseline
- Whisper: Best open-source reference
- IndicWhisper: India-specific challenger

---

## 📊 Phase 3: Metrics to Measure

### Primary Metrics

```python
# 1. Word Error Rate (WER) — standard metric
WER = (Substitutions + Deletions + Insertions) / Total Words

# 2. Character Error Rate (CER) — better for Indian scripts
CER = (Char-level S + D + I) / Total Characters

# 3. Entity Accuracy (MOST IMPORTANT for this task)
Entity_Accuracy = Correctly_Recognized_Locality_Names / Total_Locality_Names
```

### Secondary Metrics (Production-relevant)

```
- Latency: Time from audio upload to first transcript byte
- RTF (Real Time Factor): Processing time / Audio duration (< 1.0 = faster than real-time)
- Cost per minute (API-based models)
- Noise robustness: WER delta between quiet vs noisy recordings
```

### Why Entity Accuracy Matters Most
> Standard WER punishes "Koramangala" → "Koram Angala" the same as any other word error. But in a hiring platform, getting the locality NAME right is literally the job. Track this separately.

---

## 🐍 Phase 4: Python Pipeline

### requirements.txt
```
deepgram-sdk>=3.0.0
openai-whisper
jiwer          # WER/CER computation
pandas
matplotlib
tqdm
python-dotenv
requests
```

### ground_truth.json format
```json
{
  "01_koramangala_quiet": {
    "locality": "Koramangala",
    "full_text": "Haan main Koramangala mein rehta hoon",
    "condition": "quiet",
    "language": "hinglish"
  },
  "02_indiranagar_noisy": {
    "locality": "Indiranagar",
    "full_text": "Mera ghar Indiranagar ke paas hai",
    "condition": "noisy",
    "language": "hindi"
  }
}
```

### run_deepgram.py (skeleton)
```python
import os
from deepgram import DeepgramClient, PrerecordedOptions
from dotenv import load_dotenv

load_dotenv()
dg = DeepgramClient(os.getenv("DEEPGRAM_API_KEY"))

def transcribe_deepgram(audio_path):
    with open(audio_path, "rb") as f:
        buffer_data = f.read()
    options = PrerecordedOptions(
        model="nova-2",
        language="hi",          # Hindi; try "multi" for Hinglish
        punctuate=True,
    )
    response = dg.listen.prerecorded.v("1").transcribe_file(
        {"buffer": buffer_data}, options
    )
    return response.results.channels[0].alternatives[0].transcript
```

### run_whisper.py (skeleton)
```python
import whisper

model = whisper.load_model("large-v3")

def transcribe_whisper(audio_path):
    result = model.transcribe(
        audio_path,
        language="hi",          # Force Hindi; remove for auto-detect
        task="transcribe"
    )
    return result["text"]
```

### compute_metrics.py (skeleton)
```python
from jiwer import wer, cer
import json, pandas as pd

def compute_entity_accuracy(predictions, ground_truth):
    """Check if locality name appears in predicted transcript."""
    correct = 0
    for file_id, pred in predictions.items():
        locality = ground_truth[file_id]["locality"].lower()
        if locality in pred.lower():
            correct += 1
    return correct / len(predictions)

def run_evaluation(predictions_dict, ground_truth_dict):
    results = {}
    for model_name, preds in predictions_dict.items():
        refs = [ground_truth_dict[k]["full_text"] for k in preds]
        hyps = list(preds.values())
        results[model_name] = {
            "WER": round(wer(refs, hyps), 3),
            "CER": round(cer(refs, hyps), 3),
            "Entity_Accuracy": round(compute_entity_accuracy(preds, ground_truth_dict), 3)
        }
    return pd.DataFrame(results).T
```

---

## 📝 Phase 5: Report Structure (3 pages max)

### Page 1: Approach + Model Selection
```
- Why these 3 models? (1 paragraph each)
- Recording methodology (conditions, language mix)
- Metrics rationale (why entity accuracy > WER here)
```

### Page 2: Results + Failure Analysis
```
Table 1: Overall Results
| Model        | WER ↓  | CER ↓  | Entity Acc ↑ | Latency | Cost/min |
|--------------|--------|--------|--------------|---------|----------|
| Deepgram     | 0.XX   | 0.XX   | 0.XX         | XXms    | $0.0XX   |
| Whisper      | 0.XX   | 0.XX   | 0.XX         | XXs     | Free     |
| IndicWhisper | 0.XX   | 0.XX   | 0.XX         | XXs     | Free     |

Table 2: Results by Condition
| Condition | Deepgram WER | Whisper WER | IndicWhisper WER |
|-----------|-------------|-------------|-----------------|
| Quiet     | ...         | ...         | ...             |
| Noisy     | ...         | ...         | ...             |
| Whispered | ...         | ...         | ...             |
| Phone     | ...         | ...         | ...             |

Failure Analysis:
- Hard locality names (Byatarayanapura, Kadugondanahalli)
- Noisy condition failures
- Code-switching errors (Hindi + English mix)
- Show 3–5 konkrete examples with actual wrong transcriptions
```

### Page 3: Recommendation
```
Production Recommendation:
- Use Case A (real-time phone calls): → [Model X] because latency < Ys
- Use Case B (WhatsApp voice notes, batch): → [Model Y] because accuracy higher
- Cost at scale: 10,000 calls/day = $X/month (Deepgram) vs $0 (self-hosted Whisper)

One Surprising Finding:
[Something that actually surprised you in your results]

Limitations:
- Only 20 samples (small dataset)
- Single speaker (you)
- No actual phone channel degradation
```

---

## ⚡ Quick Start Checklist

```
Day 1: Record all 20 audio files ✅
Day 2: Set up pipeline, run Deepgram baseline ✅
Day 3: Run Whisper + IndicWhisper, compute metrics ✅
Day 4: Failure analysis + charts + report writing ✅
Day 5: Polish, review, walkthrough prep ✅
```

---

## 🔑 API Keys Needed

```bash
# .env file
DEEPGRAM_API_KEY=your_key_here        # deepgram.com — free tier sufficient
GOOGLE_API_KEY=your_key_here          # optional
AZURE_SPEECH_KEY=your_key_here        # optional
```

---

## 📌 Common Pitfalls to Avoid

1. **Sabhi recordings ek jaisi mat karo** — vary conditions genuinely
2. **Sirf WER mat report karo** — entity accuracy is the key metric here
3. **Failure analysis skip mat karo** — yahi cheez strong submissions ko differentiate karti hai
4. **Copy-paste HuggingFace tutorial mat karo** — samajh ke likhna
5. **"Compute nahi tha" excuse mat do** — Colab free tier Whisper large-v3 chala sakta hai

---

*Good luck! Thoughtful partial > sloppy complete. 🚀*
