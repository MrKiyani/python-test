# Monitors all running MT4/MT5 terminal processes and emits JSON metrics
import psutil
import json
from datetime import datetime

# Process names to watch (case-insensitive)
MT_NAMES = {
    'terminal.exe',
    'terminal64.exe',
    'metatrader.exe',
    'mt4.exe',
    'mt5.exe'
}

metrics = []
now = datetime.utcnow().isoformat() + 'Z'

# Iterate over all processes and capture MT4/5 instances
for proc in psutil.process_iter(['pid', 'name', 'create_time']):
    name = proc.info['name']
    if name and name.lower() in MT_NAMES:
        pid = proc.info['pid']
        up_secs = int(datetime.utcnow().timestamp() - proc.info['create_time'])
        metrics.append({
            "measurement": "mt4_status",
            "tags": {
                "instance": str(pid),
                "process": name
            },
            "fields": {
                "status": 1,
                "uptime_seconds": up_secs
            },
            "time": now
        })

# If no instances found, emit a single metric with status=0
if not metrics:
    metrics = [{
        "measurement": "mt4_status",
        "tags": {"instance": "none"},
        "fields": {"status": 0},
        "time": now
    }]

# Output the JSON metrics to stdout
print(json.dumps(metrics))
