import json
import uuid
from datetime import datetime

LOG_FILE = "fraud_logs.json"

def log_result(data):
    log_entry = {
        "log_id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        **data
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
