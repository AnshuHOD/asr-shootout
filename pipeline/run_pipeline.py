import os
import subprocess
import sys

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def run_script(script_name):
    """Runs a python script in the pipeline subdirectory."""
    pipeline_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(pipeline_dir, script_name)
    
    print("\n" + "=" * 80)
    print(f"[RUNNING] {script_name}")
    print("=" * 80)
    
    try:
        # Run with the same python interpreter
        result = subprocess.run([sys.executable, script_path], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] running {script_name}: {e}")
        return False

def main():
    print("=" * 80)
    print("ASR SHOOTOUT PIPELINE COORDINATOR")
    print("=" * 80)
    print("This script will run the entire ASR benchmarking process:")
    print("1. Generate synthetic recordings (if files are not present in recordings/)")
    print("2. Run Deepgram Nova-2 baseline (runs in Mock Mode if API key is missing)")
    print("3. Run OpenAI Whisper local model")
    print("4. Run Indic ASR local model")
    print("5. Compute metrics (WER, CER, Entity Accuracy, Latency, Cost) & generate charts")
    print("=" * 80)
    
    # 1. Generate recordings
    if not run_script("generate_synthetic_recordings.py"):
        print("[ERROR] Pipeline aborted: Recording generation failed.")
        return
        
    # 2. Run Deepgram
    if not run_script("run_deepgram.py"):
        print("[ERROR] Pipeline aborted: Deepgram run failed.")
        return
        
    # 3. Run Whisper
    if not run_script("run_whisper.py"):
        print("[ERROR] Pipeline aborted: Whisper run failed.")
        return
        
    # 4. Run Indic ASR
    if not run_script("run_indicwhisper.py"):
        print("[ERROR] Pipeline aborted: Indic ASR run failed.")
        return
        
    # 5. Compute metrics
    if not run_script("compute_metrics.py"):
        print("[ERROR] Pipeline aborted: Metric computation failed.")
        return
        
    print("\n" + "=" * 80)
    print("[SUCCESS] PIPELINE COMPLETED SUCCESSFULLY!")
    print("Check the 'results/' folder for: ")
    print("  - raw_outputs.json (Individual predictions)")
    print("  - metrics_summary.csv (Aggregated WER/CER/Entity Accuracy/Latency)")
    print("  - accuracy_comparison.png & wer_by_condition.png (Visualization charts)")
    print("=" * 80)

if __name__ == "__main__":
    main()
