import subprocess

#result = subprocess.run(["df", "-h", "/mnt/c"], capture_output=True, text=True, check=True)
#print(result.stdout)

result = subprocess.run(["df", "-h", "/mnt/d"], capture_output=True, text=True)
print(result.stdout)

if result.returncode == 0:
    print("Success")
else:
    print(f"Command failed with code {result.returncode}")
    print(result.stderr)


# check=True will always raise a non-zero exit code exception if the command fails
# checking manually allows you to handle the error more gracefully and provide custom error messages or recovery steps.
# if a grep is supposed to find a non-zero exit code, you can handle it manually instead of using check=True.