from datetime import datetime

def log_line(message):
    with open("scheduler.log", 'a') as file:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{now}: {message}\n")
