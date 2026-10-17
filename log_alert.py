import sys
from log_analyser import parse_log
from smtp_alert import send_alert, load_config

if __name__ == "__main__":
    ok, result = load_config()
    if not ok:
        print(result)
        sys.exit(1)

    configs = result
    
    log_filepath = 'test_bad.log'
    try:
        total_entries, infos, warnings, errors = parse_log(log_filepath)
    except FileNotFoundError:
        print(f"{log_filepath} was not found. Please enter a correct filepath.")
        sys.exit(1)

    subject = "Log Alert: Errors found"

    if len(errors) > 0:
        body = f"Found {len(errors)} error(s) in {log_filepath}:\n\n" + "\n".join(errors)
        success, message = send_alert(configs, subject, body)
        print(f"Alert transmission status: {message}")
        if not success:
            sys.exit(1)
    else: 
        print(f"No errors in file {log_filepath}. No email was sent.")
        sys.exit(0)  