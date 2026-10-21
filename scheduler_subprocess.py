import subprocess
import sys
from scheduler_log import log_line

def run_log_alert(log_filepath):
    result = subprocess.run([sys.executable, "log_alert.py", log_filepath], capture_output=True, text=True)
    message = f"log_alert.py on {log_filepath}: exit code {result.returncode}: {result.stdout.strip()}"
    if result.stderr:
        message += f"| stderr found: {result.stderr.splitlines()[-1]}"
    log_line(message)