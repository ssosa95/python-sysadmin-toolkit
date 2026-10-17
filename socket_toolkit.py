import socket

def check_port(host, port):
    try:
        with socket.create_connection((host, port), timeout=3):
            return "success", None
    except TimeoutError:
        return "timeout", None
    except ConnectionRefusedError:
        return "refused", None
    except socket.gaierror:
        return "dns_failure", None
    except OSError as e:
        return "error", e

def run_scan():
    counts = {
    "success": 0,
    "timeout": 0,
    "dns_failure": 0,
    "refused": 0,
    "error": 0,
        }

    for port in ports:
        result, e = check_port(host, port)
        counts[result] += 1
        print(messages[result].format(host=host, port=port, e=e))

    for status in counts:
        print(f"{status}: {counts[status]}")
    
    return counts


host = "127.0.0.1"
ports = [22, 80, 443, 1025, 3389]


messages = {
    "success": "Success: Tried connecting to {host} -> {port} is open.",
    "timeout": "Timed out: Tried connecting to {host} -> Port {port} is not reachable.",
    "dns_failure": "DNS Failure: Tried connecting to {host} -> Port {port} is not reachable.",
    "refused": "Host refused connection: Tried connecting to {host} -> Access to port {port} was denied.",
    "error": "Generic error: Tried connecting to {host} -> Port {port} is not reachable: {e}",
}



if __name__ == "__main__":
    first = run_scan()
    second = run_scan()
    print(sum(second.values()), len(ports))
