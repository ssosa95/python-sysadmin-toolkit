# Python Sysadmin Toolkit

A collection of Python scripts for everyday system administration tasks,
built while learning Python for sysadmin and DevOps work. Each tool lives in
its own folder with its own README, dependencies and usage instructions.

## Tools

| Tool | What it does |
|---|---|
| [health_check](health_check/) | Checks disk usage on a list of servers over SSH, writes a report and emails an alert when a threshold is exceeded |
| alert_email | If an issue is caught, then an email is sent |
| filesystem_navigation | os, pathlib, and datetime usage |
| log_alert | Sending log of just errors |
| log_analyser | precursor program for log_alert |
| scheduler_log | contains log_line function that prints the date time along with the message being passed |
| scheduler_subprocess | subprocess version of the above program |
| scheduler | automatic log alert |
| smtp_alert | contains load_config and send_alert |
| socket_toolkit | socket library examples with a check port function |
| subprocesses | subprocess examples and usage |

## Getting started

```
git clone https://github.com/ssosa95/python-sysadmin-toolkit.git
cd python-sysadmin-toolkit/<tool folder>
pip install -r requirements.txt
```

Then follow the README inside that tool's folder. Scripts that send email or
use SSH read their settings from environment variables, and nothing sensitive
is stored in the repo.

## Notes

- Developed and tested on Windows with Python 3.14.6.
- Target servers for the SSH-based tools are expected to be Linux/Unix.

## Status

This is a learning project and a work in progress. Tools are added as I build
them, and older ones may be refactored as I learn better structure.