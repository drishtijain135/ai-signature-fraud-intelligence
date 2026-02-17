import json
from datetime import datetime

def log_result(data):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        **data
    }

    with open("fraud_logs.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
