import paramiko
import os
import sys
from smtp_alert import load_config, send_alert
from datetime import datetime

EXIT_OK = 0
EXIT_PROBLEMS = 1
EXIT_BAD_SETUP = 2
EXIT_EMAIL_FAILED = 3
report_filepath = "no_such_folder/health_check_report.log"

def write_report(report_filepath, report):
    try:
        with open(report_filepath, 'a') as file:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{now}:\n{report}\n\n")
        return True, f"Report written to {report_filepath}"
    except FileNotFoundError:
        return False, f"Report file {report_filepath} was not found. Please enter a correct filepath."
    except PermissionError:
        return False, f"Permission denied when writing to report file ({report_filepath}). Please check permissions."
    except OSError as e:
        return False, f"Error writing to report file ({report_filepath}): {e}"

def load_ssh_config():
    user = os.environ.get("HEALTH_SSH_USER", None)
    key_path = os.environ.get("HEALTH_SSH_KEY_PATH", None)
    
    if not user:
        return False, "Config error: HEALTH_SSH_USER is not configured. Please check and review."
    
    if not key_path:
        return False, "Config error: HEALTH_SSH_KEY_PATH is not configured. Please check and review."

    if not os.path.isfile(key_path):
        return False, f"Config error: SSH key file not found at {key_path}. Please check and review."
    
    return True, {"user": user, "key_path": key_path}

def is_over(usage, threshold):
    return usage >= threshold

def parse_usage(output):
    lines = output.splitlines()
    if len(lines) < 2:
        return False, "Invalid output format"
    columns = lines[1].split()
    if len(columns) < 5:
        return False, "Invalid usage format"
    usage = columns[4]
    try:
        usage = int(usage.rstrip("%"))
    except ValueError:
        return False, "Invalid usage value"
    return True, usage

def check_disk(host, user, key_path, path="/"):
    try:
        with paramiko.SSHClient() as client:
            client.load_system_host_keys()
            client.connect(host, port=22, username=user, key_filename=key_path, timeout=10)
            stdin, stdout, stderr = client.exec_command(f"df -P {path}", timeout=10)
            output = stdout.read().decode()
            exit_status = stdout.channel.recv_exit_status()
            if exit_status != 0:
                output = stderr.read().decode().strip()
                return False, f"Host: {host} | Error: {output} | Exit code: {exit_status}"
            
            ok, result = parse_usage(output)        
            
            if not ok:
                return False, f"Host: {host} | Error: {result}"
            
            return True, result

    except paramiko.AuthenticationException as e:
        return False, f"Authentication error, {host} failed: {e}"
    except paramiko.SSHException as e:
        return False, f"SSH error, {host} failed: {e}"
    except OSError as e:
        return False, f"Error, {host} failed: {e}"

def check_all(servers_file, user, key_path, disk_path):
    results = []
    with open(servers_file, "r") as file:
        for line in file:
            host = line.strip()
            if not host:
                continue
            ok, result = check_disk(host, user, key_path, disk_path)
            results.append((host, ok, result))
    return results

def build_report(results, threshold):
    report_lines = []
    for host, ok, result in results:
        if not ok:
            report_lines.append(f"UNKNOWN | Host: {host} | Error: {result}")
        else:
            usage = result
            if is_over(usage, threshold):
                report_lines.append(f"WARNING | Host: {host} | Disk usage: {usage}% (above threshold)")
            else:
                report_lines.append(f"OK | Host: {host} | Disk usage: {usage}%")
    return "\n".join(report_lines)

def find_problems(results, threshold):
    problem_list = []
    for host, ok, result in results:
        if not ok or is_over(result, threshold):
            problem_list.append((host, ok, result))
            

    return problem_list

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python health_check.py <servers_file> <threshold> <optional: path>")
        sys.exit(EXIT_BAD_SETUP)
    
    servers_file = sys.argv[1]
    try:
        threshold = int(sys.argv[2])
    except ValueError:
        print("Threshold must be an integer.")
        sys.exit(EXIT_BAD_SETUP)

    if threshold <= 0 or threshold > 100:
        print("Threshold must be an integer between 1 and 100.")
        sys.exit(EXIT_BAD_SETUP)

    if len(sys.argv) < 4:
        disk_path = "/"
    else:
        disk_path = sys.argv[3]

    ok, result = load_ssh_config()
    if not ok:
        print(result)
        sys.exit(EXIT_BAD_SETUP)

    ssh_config = result
    user = ssh_config["user"]
    key_path = ssh_config["key_path"]

    ok, result = load_config()
    if not ok:
        print(result)
        sys.exit(EXIT_BAD_SETUP)
    try:
        results = check_all(servers_file, user, key_path, disk_path)
    except FileNotFoundError:
        print(f"Servers file {servers_file} was not found. Please enter a correct filepath.")
        sys.exit(EXIT_BAD_SETUP)
    if not results:
        print(f"No servers found in {servers_file}. Please check the file.")
        sys.exit(EXIT_BAD_SETUP)
    report = build_report(results, threshold)
    print(report)
    report_ok, report_message = write_report(report_filepath, report)
    if not report_ok:
        print(report_message)

    problems = find_problems(results, threshold)
    
    if problems:
        configs = result
        subject = f"{len(problems)} problem(s) found, please check."
        body = f"Disk usage issues detected:\n\n{report}"
        success, message = send_alert(configs, subject, body)
        
        if not success:
            print(f"Error sending alert email: {message}")
            sys.exit(EXIT_EMAIL_FAILED)
        else:
            print(f"{report_message} Alert email sent successfully: {message}")
            sys.exit(EXIT_PROBLEMS)
    else:
        print(f"{report_message} No problems detected. No email sent.")
        sys.exit(EXIT_OK)