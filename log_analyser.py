import sys
from datetime import datetime

def parse_log(filepath):    
    total_entries = []
    infos = []
    warnings = []
    errors = []

    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            parts = line.split(" ", 3)
            if len(parts) < 4:
                continue
            date = parts[0]
            time = parts[1]
            status = parts[2]
            message = parts[3]
            
            if status == "INFO":
                    infos.append(f"{date} - {time} - {message}")
                    total_entries.append(1)
                
            elif status == "WARNING":
                    warnings.append(f"{date} - {time} - {message}")
                    total_entries.append(1)
                
            elif status == "ERROR":
                    errors.append(f"{date} - {time} - {message}")
                    total_entries.append(1)
    return total_entries, infos, warnings, errors
    
def write_report(filepath, total_entries, infos, warnings, errors):
        with open(filepath, 'w') as file:
            file.write("LOG ANALYSIS SUMMARY\n")
            file.write("====================\n")
            file.write(f"Total entries: {len(total_entries)}\n")
            file.write(f"Number of INFO: {len(infos)}\n")
            file.write(f"Number of WARNING: {len(warnings)}\n")
            file.write(f"Number of ERROR: {len(errors)}\n")

            if len(errors) > 0:
                file.write("Error entries requiring attention:\n")
                for i in range(len(errors)):
                    file.write(f"- {errors[(i)]}\n")
        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
        
        with open('system.log', 'a') as file:
            file.write(f"{formatted_date} INFO Log analyzed successfully\n")

def get_severity_count(log_list):
     return len(log_list)


if __name__ == "__main__":
    log_filepath = 'system.log'
    report_filepath = 'log_report.txt'
    try:
        total_entries, infos, warnings, errors = parse_log(log_filepath)
    except FileNotFoundError:
        print(f"{log_filepath} was not found. Please enter a correct filepath.")
        sys.exit(1)
    write_report(report_filepath, total_entries, infos, warnings, errors)

    print("LOG ANALYSIS SUMMARY")
    print("====================")
    print(f"Total entries: {get_severity_count(total_entries)}")
    print(f"Number of INFO: {get_severity_count(infos)}")
    print(f"Number of WARNING: {get_severity_count(warnings)}")
    print(f"Number of ERROR: {get_severity_count(errors)}")
    if len(errors) > 0:
        print("Error entries requiring attention:")
        for i in range(len(errors)):
                print(f"- {errors[(i)]}")