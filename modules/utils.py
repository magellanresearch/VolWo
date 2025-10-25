from datetime import datetime

def get_status_date(data):
    latest = max(df.index[-1] for df in data.values())
    return latest.strftime("%Y-%m-%d")

def estimate_time_remaining(start_time, current_index, total):
    elapsed = datetime.now() - start_time
    avg_time = elapsed.total_seconds() / (current_index + 1)
    remaining = avg_time * (total - current_index - 1)
    return f"{remaining:.2f} seconds remaining"
