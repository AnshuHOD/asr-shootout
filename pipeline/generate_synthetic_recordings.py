import os
import json
import sys
from gtts import gTTS

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gt_path = os.path.join(base_dir, "transcripts", "ground_truth.json")
    recordings_dir = os.path.join(base_dir, "recordings")
    
    if not os.path.exists(gt_path):
        print(f"[ERROR] {gt_path} not found.")
        return
        
    with open(gt_path, "r") as f:
        ground_truth = json.load(f)
        
    os.makedirs(recordings_dir, exist_ok=True)
    
    print("=" * 60)
    print("[INFO] Generating Synthetic Audio Recordings via gTTS")
    print("=" * 60)
    
    for file_id, info in ground_truth.items():
        # Check if the file (either .mp3 or .wav) already exists
        mp3_path = os.path.join(recordings_dir, f"{file_id}.mp3")
        wav_path = os.path.join(recordings_dir, f"{file_id}.wav")
        
        if os.path.exists(mp3_path) or os.path.exists(wav_path):
            print(f"[SKIP] Skipping {file_id} (already exists)")
            continue
            
        print(f"[TTS] Generating audio for: \"{info['full_text']}\" -> {file_id}.mp3")
        
        # Decide language code for gTTS
        lang = 'hi'
        if info['language'].lower() == 'kannada':
            lang = 'kn'
            
        try:
            tts = gTTS(text=info['full_text'], lang=lang, slow=False)
            tts.save(mp3_path)
        except Exception as e:
            print(f"[ERROR] Error generating {file_id}: {e}")
            
    print("\n[SUCCESS] Synthetic audio files generated in 'recordings/' folder!")

if __name__ == "__main__":
    main()
