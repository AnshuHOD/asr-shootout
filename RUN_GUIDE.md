# 🚀 Run & Test Guide (Hinglish / English)

Future me agar aapko is project ko dobara run karna ho, ya nayi recordings ke sath test karna ho, toh aap is guide ko follow kar sakte hain.

---

## 🛠️ Step 1: Environment Setup (Pehli baar chalane ke liye)

Sabse pehle check karein ki aapke computer me Python installed hai. Phir PowerShell open karke project folder me jayein:
```powershell
cd c:\Users\Lenovo\Desktop\Vahan
```

### 1. Virtual Environment Create karein:
Isse aapke computer ke dusre projects me koi interference nahi hoga:
```powershell
python -m venv venv
```

### 2. Virtual Environment ko Activate karein:
```powershell
.\venv\Scripts\activate
```
*Note: Jab environment activate ho jayega, toh terminal ke shuru me `(venv)` likha hua dikhega.*

### 3. Dependencies Install karein:
```powershell
pip install -r pipeline/requirements.txt
```

---

## 🎙️ Step 2: Audio Files Setup (Test data taiyar karna)

Aapke paas do tarike hain test audio create karne ke:

### Option A: Apni voice record karna (Interactive Mode)
Agar aap khud bolkar nayi audio notes record karna chahte hain:
```powershell
python pipeline/record_audio.py
```
* **Kaise kaam karta hai?** Terminal par screen par ek sentence aayega (jaise *"Haan main Koramangala mein rehta hoon"*). Aapko sound device mic se bolna hai, aur wo automatic sound file save kar dega.

### Option B: Automatic Audios generate karna (gTTS Mode)
Agar aap bina bole automatic voice test files download karna chahte hain:
```powershell
python pipeline/generate_synthetic_recordings.py
```
* **Kaise kaam karta hai?** Yeh script Google Text-To-Speech (gTTS) API use karke saari 20 localities ki dynamic voices automatically `recordings/` folder me save kar degi.

---

## 📊 Step 3: Pipeline Run Karna (Analysis & Transcription)

Jab aapki recordings ready ho jayein, tab poori pipeline ko analyze aur benchmark karne ke liye run karein:

```powershell
python pipeline/run_pipeline.py
```

### Script kya karegi?
1. `results/` directory me check karegi.
2. Sabhi 20 audio files ko line-by-line **Deepgram Nova-2**, **OpenAI Whisper**, aur **IndicWhisper** models ke paas bhej kar unka Text output generate karegi.
3. Transcription output complete hote hi `compute_metrics.py` automatic execute hoga aur accuracy tables/plots update kar dega.

---

## 🔍 Step 4: Results Kahan Dekhein?

Run complete hone ke baad, `results/` folder me ye files check karein:

1. **`metrics_summary.csv`**: Ek complete spreadsheet table jisme teeno models ke overall metrics (WER, CER, Entity Accuracy, Avg Latency, Cost, RTF) honge.
2. **`accuracy_comparison.png`**: Ek graph chart jo models ki accuracy aur Word Error Rate compare karega.
3. **`wer_by_condition.png`**: Ek visual chart jo batayega ki kis noise/condition (Quiet, Noisy, Rushed, Whispered, Phone) me kis model ne kaisa perform kiya.
4. **`predictions_*.json`**: Models ke individual text outputs aur actual latency records.

---

## ⚠️ Common Troubleshooting (Problems ke solutions)

* **Deepgram Mock Mode Error:** Agar aapko Deepgram ka actual API call karna hai, toh root me `.env` file banakar `DEEPGRAM_API_KEY=your_key_here` set karein. Agar key nahi hogi, toh program test validation ke liye mock values use karega aur error nahi dega.
* **FFmpeg Error on Windows (Whisper):** OpenAI Whisper run hote waqt agar Windows system me `ffmpeg` library path par nahi milti, toh script fallback function use karti hai jisse aapka pipeline bina crash hue result compute kar lega.
