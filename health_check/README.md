# Server Health Check

Connects to a list of Linux servers over SSH, checks disk usage on a given
path, and reports each host as OK, WARNING (usage at or above the threshold)
or UNKNOWN (the check itself failed). Results are printed, appended to a log
file, and emailed if any host needs attention.

## Installation

```
pip install -r requirements.txt
```

Ran on Python 3.14.6

## Prerequisites

- Key-based SSH access to every server (password login is not supported).
- Each server must already be in your `known_hosts` file. Connect to it once
  manually with `ssh` first, otherwise the check fails for that host.
- Target servers must support `df -P` (Linux/Unix).

## Configuration

Set these environment variables (PowerShell: `$env:MY_VARIABLE = "my value"` which is valid for that terminal session; Linux: `export MY_VARIABLE="my value"` which is valid for that terminal session) before running:

|           Variable          | Required |                                 Purpose                            |
|-----------------------------|----------|--------------------------------------------------------------------|
|      `HEALTH_SSH_USER`      |    Yes   |                  Username used to log in to the servers            |
|     `HEALTH_SSH_KEY_PATH`   |    Yes   |                    Path to the private key file                    |
|      `ALERT_SMTP_FROM`      |    Yes   |                  Sender address of the alert email                 |
|       `ALERT_SMTP_TO`       |    Yes   |                         Recipient address                          |
|      `ALERT_SMTP_USER`      |    No    |              SMTP login (must be set together with the password)   |
|    `ALERT_SMTP_PASSWORD`    |    No    | SMTP password or app password (must be set together with the user) |
|      `ALERT_SMTP_HOST`      |    No    |                    SMTP server (default `127.0.0.1`)               |
|      `ALERT_SMTP_PORT`      |    No    |                    SMTP port, 1-65535 (default `1025`)             |

**With no credentials set, the script sends over a plain connection with no login. The defaults (`127.0.0.1:1025`) point at a local test mail server, so a fresh clone won’t send real email until the host and port are configured.

**When credentials are set, the script upgrades the connection with `starttls()`. This suits ports like 587 (Gmail’s `smtp.gmail.com:587` works this way with an app password). This would not work for a port that expects encryption from the first byte.

## Usage

```
python health_check.py <servers_file> <threshold> [path]
```

- `servers_file`: text file with one hostname or IP per line (blank lines ignored)
- `threshold`: integer from 1 to 100; usage at or above it triggers a warning
- `path`: optional, the filesystem path to check (default `/`)

Each run prints the report, appends it with a timestamp to
`health_check_report.log`, and sends an alert email if any host is in
WARNING or UNKNOWN state.

## Exit codes

| Code |                       Meaning                      |
|------|----------------------------------------------------|
|  0   |           All hosts OK, no email sent              |
|  1   |        Problems found, alert email sent            |
|  2   |     Bad setup (arguments, config, or servers file) |
|  3   | Problems found, but the alert email failed to send |