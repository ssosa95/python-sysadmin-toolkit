from socket_toolkit import run_scan
import sys
from smtp_alert import load_config
from smtp_alert import send_alert

if __name__ == "__main__":
    ok, result = load_config()
    if not ok:
        print(result)
        sys.exit(1)

    configs = result

    subject = "Port Scan Alert"

    counts = run_scan()

    body = (
        f"The port scan has completed.\n\n"
        f"Results Summary:\n"
        f"- Success (Open): {counts['success']}\n"
        f"- Refused: {counts['refused']}\n"
        f"- Timeout: {counts['timeout']}\n"
        f"- DNS Failure: {counts['dns_failure']}\n"
        f"- Errors: {counts['error']}\n"
    )


    if counts["timeout"] > 0 or counts["dns_failure"] > 0 or counts["error"] > 0:
        success, message = send_alert(configs, subject, body)
        print(f"Alert transmission status: {message}")
        if not success:
            sys.exit(1)
    else: 
        print("Scan clean. No email sent.")
        sys.exit(0)