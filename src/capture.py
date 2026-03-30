import pyshark
import time
import signal

INTERFACE = "wlan0"
stop_requested = False

def handle_exit(sig, frame):
    global stop_requested
    stop_requested = True

signal.signal(signal.SIGINT, handle_exit)

def packet_stream(interface):
    capture = pyshark.LiveCapture(interface=interface)
    try:
        for packet in capture.sniff_continuously():
            if stop_requested:
                break
            try:
                yield {
                    "src_ip": packet.ip.src if hasattr(packet, "ip") else "N/A",
                    "dst_ip": packet.ip.dst if hasattr(packet, "ip") else "N/A",
                    "protocol": packet.highest_layer,
                    "length": int(packet.length),
                    "timestamp": time.time()
                }
            except Exception:
                continue
    finally:
        try:
            capture.close()
        except Exception:
            pass

if __name__ == "__main__":
    print("[*] Packet capture module initialized")
    print("[*] Running silently. Press Ctrl + C to stop.\n")
    for _ in packet_stream(INTERFACE):
        if stop_requested:
            break
    print("[*] Packet capture stopped cleanly")
