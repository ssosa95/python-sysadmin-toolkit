import os
from email.message import EmailMessage
import smtplib

def load_config():
    sender = os.getenv("ALERT_SMTP_FROM")
    receiver = os.getenv("ALERT_SMTP_TO")
    
    if not sender or not receiver:
        return False, "Config error: ALERT_SMTP_FROM/ALERT_SMTP_TO is not configured. Please check and review."
        
    user = os.environ.get("ALERT_SMTP_USER", None)
    password = os.environ.get("ALERT_SMTP_PASSWORD", None)
    
    if user or password:
        if not (user and password):
            return False, "SMTP credentials are incomplete. Both user and password must be provided."
    
    host = os.environ.get("ALERT_SMTP_HOST", "127.0.0.1")

    try:
        port = int(os.environ.get("ALERT_SMTP_PORT", "1025"))
    except ValueError:
        return False, "Invalid SMTP port: Port should be an integer between 1 and 65535. Change ALERT_SMTP_PORT."
    
    if not 1 <= port <= 65535:
        return False, f"Invalid SMTP port: {port}. Port must be between 1 and 65535. Change ALERT_SMTP_PORT."

    configs = {
        "sender": sender,
        "receiver": receiver,
        "user": user,
        "password": password,
        "host": host,
        "port": port
    }

    return True, configs

def send_alert(configs, subject, body):

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = configs["sender"]
    msg["To"] = configs["receiver"]
    msg.set_content(body)

    try:
        with smtplib.SMTP(configs["host"], configs["port"], timeout=10) as server:
            if configs["user"] and configs["password"]:
                server.starttls()
                server.login(configs["user"], configs["password"])
            server.send_message(msg)
    except smtplib.SMTPAuthenticationError as e:
        return False, f"SMTP authentication error {e.smtp_code}: {e.smtp_error.decode()}"
    except smtplib.SMTPException as e:
        return False, f"SMTP error: {e}"
    except OSError as e:
        return False, f"OS error: {e}"

    
    
    return True, "E-mail sent successfully"