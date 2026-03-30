import time
import signal
from collections import defaultdict
import pyshark

INTERFACE = "wlan0"
FLOW_WINDOW = 5
RUN_DURATION = 30
stop_requested = False

def handle_exit(sig, frame):
    global stop_requested
    stop_requested = True

signal.signal(signal.SIGINT, handle_exit)

class FlowAggregator:
    def __init__(self):
        self.flows = defaultdict(lambda: {
            "packet_count": 0,
            "total_bytes": 0,
            "start": time.time(),
            "last": time.time()
        })
        self.window_start = time.time()

    def add(self, key, size):
        self.flows[key]["packet_count"] += 1
        self.flows[key]["total_bytes"] += size
        self.flows[key]["last"] = time.time()

    def flush(self):
        completed = []
        for k, v in self.flows.items():
            completed.append({
                "packet_count": v["packet_count"],
                "total_bytes": v["total_bytes"],
                "duration": round(v["last"] - v["start"], 3)
            })
        self.flows.clear()
        self.window_start = time.time()
        return completed

def start_flow_aggregation():
    print("[*] AEGISNET Flow Aggregation started")
    print("[*] Aggregating packets into flows...\n")

    capture = pyshark.LiveCapture(interface=INTERFACE)
    aggregator = FlowAggregator()
    start_time = time.time()
    total_flows = 0

    try:
        for pkt in capture.sniff_continuously():
            if stop_requested or time.time() - start_time > RUN_DURATION:
                break
            try:
                key = (
                    pkt.ip.src if hasattr(pkt, "ip") else "N/A",
                    pkt.ip.dst if hasattr(pkt, "ip") else "N/A",
                    pkt.highest_layer
                )
                aggregator.add(key, int(pkt.length))
            except Exception:
                continue

            if time.time() - aggregator.window_start >= FLOW_WINDOW:
                total_flows += len(aggregator.flush())
    finally:
        try:
            capture.close()
        except Exception:
            pass

    print("[*] Flow aggregation stopped")
    print(f"[*] Total flows generated: {total_flows}")

if __name__ == "__main__":
    start_flow_aggregation()
