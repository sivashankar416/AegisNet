from baseline import start_baseline_learning
from detector import start_detection
from summarizer import AlertSummarizer

print("[*] AEGISNET real-time intrusion monitoring started")
print("[*] Press Ctrl + C to stop\n")

print("[INFO] Learning normal network behavior (Baseline Phase)")
baseline_features = [
    {"packets_per_second": 2.5, "bytes_per_packet": 500},
    {"packets_per_second": 3.0, "bytes_per_packet": 520},
    {"packets_per_second": 2.8, "bytes_per_packet": 510}
]
start_baseline_learning(baseline_features)

print("\n[INFO] Baseline established. Switching to detection mode...\n")

runtime_features = [
    {"packets_per_second": 9.5, "bytes_per_packet": 1800}
]

summarizer = AlertSummarizer()
for conf in start_detection(runtime_features):
    summarizer.record()
    print("[ALERT][HIGH] Sustained abnormal traffic pattern")
    print(f"Confidence: {conf}%")
    print("Reason: High packet rate over extended duration")
    print("Action: Investigation recommended\n")

print("[INFO] Network status: Stable")
summarizer.print_summary()
