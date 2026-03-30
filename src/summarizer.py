class AlertSummarizer:
    def __init__(self):
        self.total = 0
        self.high = 0

    def record(self):
        self.total += 1
        self.high += 1

    def print_summary(self):
        print("\n===== AEGISNET SUMMARY (Last 5 Minutes) =====")
        print(f"• Total flows analyzed: {self.total}")
        print(f"• High-risk alerts: {self.high}")
        print("===========================================")
