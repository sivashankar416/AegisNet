import json
import numpy as np
import os

BASELINE_PATH = "models/baseline.json"

def start_baseline_learning(feature_stream):
    packet_rates = [f["packets_per_second"] for f in feature_stream]
    bytes_pkts = [f["bytes_per_packet"] for f in feature_stream]

    baseline = {
        "packet_rate_mean": float(np.mean(packet_rates)),
        "packet_rate_std": float(np.std(packet_rates)),
        "bytes_per_packet_mean": float(np.mean(bytes_pkts)),
        "bytes_per_packet_std": float(np.std(bytes_pkts)),
        "samples": len(packet_rates)
    }

    os.makedirs("models", exist_ok=True)
    with open(BASELINE_PATH, "w") as f:
        json.dump(baseline, f, indent=4)

    print("[INFO] Baseline learning completed")
    print(f"[INFO] Baseline saved to {BASELINE_PATH}")

if __name__ == "__main__":
    print("[INFO] Learning normal network behavior (Baseline Phase)")
    demo = [
        {"packets_per_second": 2.5, "bytes_per_packet": 500},
        {"packets_per_second": 3.0, "bytes_per_packet": 520},
        {"packets_per_second": 2.8, "bytes_per_packet": 510}
    ]
    start_baseline_learning(demo)
