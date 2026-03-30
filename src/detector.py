import json
import signal

BASELINE_PATH = "models/baseline.json"
ALERT_THRESHOLD = 70
stop_requested = False

def handle_exit(sig, frame):
    global stop_requested
    stop_requested = True

signal.signal(signal.SIGINT, handle_exit)

class AnomalyDetector:
    def __init__(self, baseline):
        self.b = baseline

    def z(self, v, m, s):
        return 0 if s == 0 else abs(v - m) / s

    def evaluate(self, f):
        z1 = self.z(f["packets_per_second"], self.b["packet_rate_mean"], self.b["packet_rate_std"])
        z2 = self.z(f["bytes_per_packet"], self.b["bytes_per_packet_mean"], self.b["bytes_per_packet_std"])
        mz = max(z1, z2)

        if mz < 1: c = 20
        elif mz < 2: c = 50
        else: c = min(95, 70 + (mz - 2) * 10)

        return round(c, 1)

def start_detection(features):
    with open(BASELINE_PATH) as f:
        baseline = json.load(f)

    det = AnomalyDetector(baseline)
    for f in features:
        if stop_requested:
            break
        conf = det.evaluate(f)
        if conf >= ALERT_THRESHOLD:
            yield conf
