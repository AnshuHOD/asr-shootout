import os
import json
import time

def record_audio_clip(filename, duration=5, sample_rate=16000):
    """Records audio from the microphone and saves it as a WAV file."""
    try:
        import sounddevice as sd
        import soundfile as sf
    except ImportError:
        print("\n[ERROR] Missing required libraries for recording.")
        print("Please run: pip install sounddevice soundfile")
        return False

    print(f"🎤 Recording in 3... (get ready to speak)")
    time.sleep(1)
    print(f"🎤 Recording in 2...")
    time.sleep(1)
    print(f"🎤 Recording in 1...")
    time.sleep(1)
    
    print("\n🔴 RECORDING... Speak now!")
    # Record mono channel audio
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    
    # Simple countdown in terminal
    for i in range(duration, 0, -1):
        print(f"[{i}s remaining...]", end="\r")
        time.sleep(1)
    
    sd.wait()  # Wait until the recording is finished
    print("\n🛑 Recording complete.")
    
    # Ensure directories exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Save the file
    sf.write(filename, recording, sample_rate)
    print(f"💾 Saved file to: {filename}\n")
    return True

def main():
    # Paths relative to the repository root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gt_path = os.path.join(base_dir, "transcripts", "ground_truth.json")
    recordings_dir = os.path.join(base_dir, "recordings")
    
    if not os.path.exists(gt_path):
        print(f"Error: {gt_path} not found. Please create it first.")
        return
        
    with open(gt_path, "r") as f:
        ground_truth = json.load(f)
        
    print("=" * 60)
    print("🎤 ASR Shootout — Interactive Audio Recorder")
    print("=" * 60)
    print("This script will guide you through recording the 20 audio files.")
    print("For each sample, speak naturally as if you are on a phone call.")
    print("=" * 60)
    
    items = list(ground_truth.items())
    
    for idx, (file_id, info) in enumerate(items, 1):
        filename = os.path.join(recordings_dir, f"{file_id}.wav")
        
        # Check if file already exists
        exists = os.path.exists(filename)
        status = "[Already Recorded]" if exists else "[Pending]"
        
        print(f"\n[{idx}/20] {status} File: {file_id}.wav")
        print(f"📍 Locality:  {info['locality']}")
        print(f"🔊 Condition: {info['condition'].upper()}")
        print(f"📝 Sentence:  \"{info['full_text']}\"")
        
        if exists:
            choice = input("This file already exists. Do you want to re-record? (y/N): ").strip().lower()
            if choice != 'y':
                continue
                
        input("Press [Enter] to START recording...")
        success = record_audio_clip(filename, duration=5)
        if not success:
            break
            
    print("\n🎉 Recording process finished! Check the 'recordings/' folder.")

if __name__ == "__main__":
    main()
