import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from jiwer import wer, cer
import sys

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def get_audio_duration(audio_path):
    """Calculates the duration of the audio file in seconds."""
    try:
        import soundfile as sf
        info = sf.info(audio_path)
        return info.duration
    except Exception:
        return 5.0

def normalize_text(text):
    """Cleans up text for better matching (lowercase, removes punctuation)."""
    import string
    if not text:
        return ""
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return " ".join(text.split())

def check_locality_match(predicted_text, target_locality):
    """
    Robust check if the locality name is present in the predicted text.
    Handles common spelling variations, spaces, and abbreviations.
    """
    pred_clean = normalize_text(predicted_text)
    loc_clean = normalize_text(target_locality)
    
    if loc_clean in pred_clean:
        return True
        
    variations = {
        "koramangala": ["koramangla", "koramangala", "koramangalam", "kora mangala"],
        "indiranagar": ["indiranagar", "indira nagar", "indiranagura"],
        "whitefield": ["whitefield", "white field", "waitfield", "whitfield"],
        "electronic city": ["electronic city", "electroniccity", "e city", "ecity"],
        "marathahalli": ["marathahalli", "marathahali", "marathalli", "marathli"],
        "jayanagar": ["jayanagar", "jaya nagar"],
        "rajajinagar": ["rajajinagar", "rajaji nagar"],
        "hebbal": ["hebbal", "hebal"],
        "yelahanka": ["yelahanka", "yelahanka"],
        "banashankari": ["banashankari", "banashankari temple", "banshankari"],
        "hsr layout": ["hsr layout", "hsr", "hsrlayout"],
        "btm layout": ["btm layout", "btm", "btmlayout"],
        "majestic": ["majestic", "majestic bus", "majestic stand"],
        "silk board": ["silk board", "silkboard", "silk board junction"],
        "bellandur": ["bellandur", "bellandur lake", "belandur"],
        "sarjapur": ["sarjapur", "sarjapur road"],
        "bommanahalli": ["bommanahalli", "bomanahalli", "bommanahali"],
        "kr puram": ["kr puram", "k r puram", "krpuram", "krishnarajapuram"],
        "peenya": ["peenya", "peenya industrial"],
        "yeshwanthpur": ["yeshwanthpur", "yeswanthpur", "yeshwanthpura"]
    }
    
    if loc_clean in variations:
        for var in variations[loc_clean]:
            if var in pred_clean:
                return True
                
    loc_tokens = loc_clean.split()
    if len(loc_tokens) > 1:
        all_tokens_present = True
        for tok in loc_tokens:
            if tok not in pred_clean:
                all_tokens_present = False
                break
        if all_tokens_present:
            return True
            
    return False

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gt_path = os.path.join(base_dir, "transcripts", "ground_truth.json")
    recordings_dir = os.path.join(base_dir, "recordings")
    results_dir = os.path.join(base_dir, "results")
    
    if not os.path.exists(gt_path):
        print(f"[ERROR] {gt_path} not found.")
        return
        
    with open(gt_path, "r") as f:
        ground_truth = json.load(f)
        
    models = ["deepgram", "whisper", "indicwhisper"]
    model_predictions = {}
    
    for m in models:
        pred_file = os.path.join(results_dir, f"predictions_{m}.json")
        if os.path.exists(pred_file):
            with open(pred_file, "r") as f:
                model_predictions[m] = json.load(f)
        else:
            print(f"[WARN] Predictions file for model '{m}' not found at: {pred_file}")
            
    if not model_predictions:
        print("[ERROR] No prediction files found. Run the runner scripts first.")
        return
        
    overall_results = []
    condition_results = []
    
    for model_name, preds in model_predictions.items():
        refs = []
        hyps = []
        latencies = []
        costs = []
        rtfs = []
        entity_correct = 0
        total_entities = 0
        
        cond_data = {}
        
        for file_id, pred in preds.items():
            if file_id not in ground_truth:
                continue
                
            gt_info = ground_truth[file_id]
            ref_text = gt_info["full_text"]
            hyp_text = pred["transcript"]
            
            refs.append(ref_text)
            hyps.append(hyp_text)
            
            lat = pred["latency"]
            latencies.append(lat)
            costs.append(pred.get("cost", 0.0))
            
            audio_path = os.path.join(recordings_dir, f"{file_id}.wav")
            if not os.path.exists(audio_path):
                audio_path = os.path.join(recordings_dir, f"{file_id}.mp3")
            dur = get_audio_duration(audio_path)
            rtf = lat / dur if dur > 0 else 0.0
            rtfs.append(rtf)
            
            is_match = check_locality_match(hyp_text, gt_info["locality"])
            if is_match:
                entity_correct += 1
            total_entities += 1
            
            cond = gt_info["condition"]
            if cond not in cond_data:
                cond_data[cond] = {"refs": [], "hyps": []}
            cond_data[cond]["refs"].append(ref_text)
            cond_data[cond]["hyps"].append(hyp_text)
            
        overall_wer = wer(refs, hyps) if refs else 0.0
        overall_cer = cer(refs, hyps) if refs else 0.0
        entity_acc = entity_correct / total_entities if total_entities > 0 else 0.0
        avg_latency = np.mean(latencies) if latencies else 0.0
        total_cost = sum(costs)
        avg_rtf = np.mean(rtfs) if rtfs else 0.0
        
        overall_results.append({
            "Model": model_name.capitalize(),
            "WER": overall_wer,
            "CER": overall_cer,
            "Entity Accuracy": entity_acc,
            "Avg Latency (s)": avg_latency,
            "RTF": avg_rtf,
            "Total Cost ($)": total_cost
        })
        
        for cond, c_info in cond_data.items():
            cond_wer = wer(c_info["refs"], c_info["hyps"])
            condition_results.append({
                "Model": model_name.capitalize(),
                "Condition": cond.capitalize(),
                "WER": cond_wer
            })
            
    df_overall = pd.DataFrame(overall_results)
    overall_csv = os.path.join(results_dir, "metrics_summary.csv")
    df_overall.to_csv(overall_csv, index=False)
    
    print("\n📊 OVERALL RESULTS")
    print("=" * 90)
    print(df_overall.to_string(index=False))
    print("=" * 90)
    
    df_cond = pd.DataFrame(condition_results)
    df_cond_pivot = df_cond.pivot(index="Condition", columns="Model", values="WER")
    print("\n📈 WER BY ACOUSTIC CONDITION")
    print("=" * 60)
    print(df_cond_pivot)
    print("=" * 60)
    
    generate_charts(df_overall, df_cond_pivot, results_dir)

def generate_charts(df_overall, df_cond_pivot, results_dir):
    """Creates performance comparison charts and saves them as images."""
    try:
        plt.figure(figsize=(10, 5))
        x = np.arange(len(df_overall["Model"]))
        width = 0.35
        
        plt.bar(x - width/2, df_overall["WER"], width, label='WER (Lower is Better)', color='#ff6b6b')
        plt.bar(x + width/2, df_overall["Entity Accuracy"], width, label='Entity Accuracy (Higher is Better)', color='#4ecdc4')
        
        plt.xlabel('ASR Model')
        plt.ylabel('Score (0.0 to 1.0)')
        plt.title('ASR Accuracy vs Word Error Rate (WER) Comparison')
        plt.xticks(x, df_overall["Model"])
        plt.ylim(0, 1.1)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(results_dir, "accuracy_comparison.png"))
        plt.close()
        
        df_cond_pivot.plot(kind='bar', figsize=(10, 5), color=['#4285F4', '#EA4335', '#FBBC05'])
        plt.xlabel('Acoustic Condition')
        plt.ylabel('WER')
        plt.title('Word Error Rate (WER) by Acoustic Condition')
        plt.xticks(rotation=45)
        plt.ylim(0, max(df_cond_pivot.max()) * 1.2 if not df_cond_pivot.empty else 1.0)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(results_dir, "wer_by_condition.png"))
        plt.close()
        
        print(f"\n[INFO] Saved comparison charts to results folder!")
    except Exception as e:
        print(f"[WARN] Failed to generate charts: {e}")

if __name__ == "__main__":
    main()
