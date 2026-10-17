import os
from pathlib import Path
from datetime import datetime

os.path.exists(r"C:\Users\user\projects\python-basics") # remember the r before the string to avoid escape sequences
os.path.isfile(r"C:\Users\user\projects\python-basics")
os.path.isdir(r"C:\Users\user\projects\python-basics")
os.listdir(r"C:\Users\user\projects\python-basics")
os.makedirs(r"C:\Users\user\projects\python-basics", exist_ok=True) # remember the flag exist_ok=True to avoid errors if the directory already exists

base = Path("C:/") / "Users" / "user" / "projects"
file_path = base / "python-basics"

p = Path("C:/") / "Users" / "user" / "projects" / "python-basics"
p.exists()
p.is_file()
p.is_dir()
p.mkdir(exist_ok=True) # remember the flag exist_ok=True to avoid errors if the directory already exists

info = p.stat()
print(info.st_size)   # size in bytes
print(info.st_mtime)  # last modified time -> a raw timestamp (seconds since epoch), not human-readable yet
readable_time = datetime.fromtimestamp(info.st_mtime)
print(readable_time)  # last modified time -> human-readable