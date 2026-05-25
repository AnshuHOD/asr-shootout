# 🎙️ ASR Benchmarking for Indian Conversational Speech

This repository contains the benchmarking pipeline and evaluation codebase for Automatic Speech Recognition (ASR) systems, tailored for Indian conversational speech (Hindi, Hinglish, and Kannada) under varying real-world acoustic conditions.

This evaluation is designed to determine the optimal Speech-to-Text configuration for candidate onboarding voice notes and telephony channels on a blue-collar hiring platform.

---

## 📁 Repository Structure

```text
Vahan/
├── recordings/                  # 20 raw audio recordings under 5 acoustic conditions (.mp3)
├── transcripts/
│   └── ground_truth.json        # Reference transcription annotations, targets, & metadata
├── pipeline/
│   ├── run_pipeline.py          # Master execution script (runs full evaluation)
│   ├── run_deepgram.py          # Deepgram Nova-2 API integration script
│   ├── run_whisper.py           # OpenAI Whisper local CPU inference execution script
│   ├── run_indicwhisper.py      # Indic ASR model integration script
│   ├── generate_synthetic_recordings.py  # Utility to auto-generate TTS baseline recordings
│   ├── record_audio.py          # Interactive script to record audio via local microphone
│   ├── compute_metrics.py       # Metrics engine (WER, CER, Entity Accuracy, latency plots)
│   └── requirements.txt         # Project python dependencies
├── results/
│   ├── predictions_deepgram.json     # Baseline output transcripts
│   ├── predictions_whisper.json      # OpenAI Whisper base output transcripts
│   ├── predictions_indicwhisper.json # IndicWhisper output transcripts
│   ├── metrics_summary.csv           # Tabulated benchmark metrics
│   ├── accuracy_comparison.png       # Model comparison visualization plot
│   └── wer_by_condition.png          # Condition-wise WER performance chart
├── report.md                    # Detailed 3-page benchmarking report
└── README.md                    # Project documentation (this file)
```

---

## 🚀 Setup & Execution

### 1. Installation
Clone the repository and install the Python dependencies:

```bash
# Clone the repository
git clone <your-repository-url>
cd Vahan

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install required packages
pip install -r pipeline/requirements.txt
```

### 2. Configure Environment (Optional for Deepgram)
If you have a Deepgram API key, add it to a `.env` file in the root directory:
```bash
DEEPGRAM_API_KEY=your_actual_api_key_here
```
*Note: If no key is provided, the pipeline automatically falls back to Mock Simulation mode for validation purposes.*

### 3. Run the Evaluation Pipeline
Execute the master script to run transcription on all models and generate accuracy reports and charts:
```bash
python pipeline/run_pipeline.py
```

---

## 📊 Summary of Benchmark Results

The evaluation dataset consists of **20 audio files** testing 20 distinct Bangalore locality names (e.g., Koramangala, Whitefield, Majestic) spoken naturally across 5 varied acoustic environments (Quiet, Noisy, Rushed, Whispered, Phone simulated).

| ASR Model | WER ↓ | CER ↓ | Entity Accuracy (Locality Match) ↑ | Avg Latency (s) | RTF ↓ | Cost/Min |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Deepgram Nova-2** | **6.30%** | **5.52%** | **95.0%** | **0.29s** | **0.09** | $0.0044 |
| **OpenAI Whisper (base)** | 8.66% | 6.08% | **95.0%** | 1.46s | 0.48 | **Free** |
| **IndicWhisper** | 8.66% | 9.25% | **95.0%** | 2.40s | 0.78 | **Free** |

### Key Takeaway
* **Real-Time Channels (Telephony/IVR):** Use **Deepgram Nova-2** for low latency (~0.30s) and rapid response factor.
* **Asynchronous Channels (WhatsApp Voice Notes):** Use self-hosted **OpenAI Whisper (base)**. Since latency is non-critical for async chats, self-hosting on a GPU node eliminates paid API costs entirely while delivering the **exact same 95.0% Entity Accuracy** as Deepgram Nova-2.

For a detailed analysis of failure modes (noise, code-switching, pronunciation) and scaling costs, refer to the [report.md](file:///c:/Users/Lenovo/Desktop/Vahan/report.md) document.
