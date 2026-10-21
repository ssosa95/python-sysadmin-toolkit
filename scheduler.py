import sys
from log_analyser import parse_log
from smtp_alert import load_config, send_alert
from scheduler_log import log_line
import time
import schedule

def save_reported(report_filepath, new_errors):
    with open(report_filepath, 'a') as file:
        for error in new_errors:
            file.write(f"{error}\n")


def find_new(errors, reported):
    new_errors = []
    for error in errors:
        if error not in reported:
            new_errors.append(error)
    return new_errors


def load_reported(report_filepath):
    try:
        with open(report_filepath, 'r') as file:
            reported = set()
            for line in file:
                line = line.strip()
                reported.add(line)
    except FileNotFoundError:
        reported = set()
    return reported


def check_logs(log_filepath, configs, report_filepath):
    try:
        try:
            total_entries, infos, warnings, errors = parse_log(log_filepath)
        except FileNotFoundError:
            log_line(f"{log_filepath} was not found. Please enter a correct filepath.")
            return
        
        reported = load_reported(report_filepath)
        new_errors = find_new(errors, reported)
        

        subject = "Log Alert: Errors found"

        if len(new_errors) > 0:
            body = f"Found {len(new_errors)} error(s) in {log_filepath}:\n\n" + "\n".join(new_errors)
            success, message = send_alert(configs, subject, body)
            
            if not success:
                log_line(f"Error. Email not sent: {message}")
            else:
                log_line(f"Alert transmission status: {message}")
                save_reported(report_filepath, new_errors)
        
        elif len(errors) == 0:
            log_line(f"No errors in file {log_filepath}. No email was sent.")

        else: 
            log_line(f"No new errors, all errors reported already. No email was sent.")
    except Exception as e:
        log_line(f"An unexpected error occurred. {type(e).__name__}: {e}")



if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scheduler.py <logfile> <report file>")
        sys.exit(1)
    
    log_filepath = sys.argv[1]   
    report_filepath = sys.argv[2]

    ok, result = load_config()
    if not ok:
        print(result)
        sys.exit(1)
    
    configs = result

    schedule.every(30).seconds.do(check_logs, log_filepath, configs, report_filepath)

    while True:
        schedule.run_pending()
        time.sleep(1)