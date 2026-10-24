import paramiko

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

def check_all(servers_file, user, key_path, disk_path="/"):
    results = []
    with open(servers_file, "r") as file:
        for line in file:
            host = line.strip()
            if not host:
                continue
            ok, result = check_disk(host, user, key_path, disk_path)
            results.append((host, ok, result))
    return results