def extract_features(flows):
    features = []
    for f in flows:
        duration = max(f["duration"], 0.001)
        features.append({
            "packet_count": f["packet_count"],
            "total_bytes": f["total_bytes"],
            "flow_duration": duration,
            "packets_per_second": f["packet_count"] / duration,
            "bytes_per_packet": f["total_bytes"] / max(f["packet_count"], 1)
        })
    return features

if __name__ == "__main__":
    print("[*] Feature Engineering Module initialized\n")
    demo = [
        {"packet_count": 10, "total_bytes": 5000, "duration": 2.5},
        {"packet_count": 3, "total_bytes": 300, "duration": 1.2}
    ]
    for f in extract_features(demo):
        print(f)
