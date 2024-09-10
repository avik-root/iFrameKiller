import requests
from termcolor import colored
import socket
import pyfiglet
import os
import http.server
import socketserver
def create_banner():
    banner = pyfiglet.figlet_format("iFrameKiller", font="big")
    print(banner)
    banner = pyfiglet.figlet_format("by avik-root Version 1.5", font="digital")
    print(banner)
    banner = pyfiglet.figlet_format("BETA", font="digital")
    print(banner)
    print("Github: https://github.com/avik-root\n")  
def get_public_ip():
    try:
        response = requests.get('https://api64.ipify.org?format=json')
        return response.json()['ip']
    except Exception as e:
        print(colored(f"Error fetching public IP: {e}", 'red'))
        return "Unknown"
def get_website_ip(url):
    try:
        domain = url.replace("http://", "").replace("https://", "").split('/')[0]
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except Exception as e:
        print(colored(f"Error fetching website IP: {e}", 'red'))
        return "Unknown"
def check_iframe(url):
    try:
        response = requests.get(url)
        if 'X-Frame-Options' in response.headers:
            option = response.headers['X-Frame-Options'].lower()
            if option == 'deny' or option == 'sameorigin':
                print(colored('Iframe is not possible', 'red'))
                return False
        print(colored('Iframe is possible', 'green'))
        return True
    except Exception as e:
        print(colored(f'Error: {e}', 'red'))
        return False
def create_html_with_iframe(url):
    html_content = f'''<!DOCTYPE html>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <title>FrameKiller</title>
    <style>
        div {{
            position: absolute;
            top: 452px;
            left: 340px;
            z-index: 1;
        }}
    </style>
</head>
<body>
    <iframe src="{url}" height="1000px" width="800px" ></iframe>
</body>
</html>'''
    with open("iframe_test.html", "w") as file:
        file.write(html_content)

    PORT = 8000
    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving at port {PORT}, visit http://localhost:{PORT}/iframe_test.html")
        httpd.serve_forever()
def log_to_file(url, public_ip, website_ip, iframe_status):
    with open("websitehistory.txt", "a") as file:
        file.write(f"Website URL: {url}\n")
        file.write(f"Public IP: {public_ip}\n")
        file.write(f"Entered Website Hosting IP: {website_ip}\n")
        file.write(f"Iframe Allowed: {iframe_status}\n")
        file.write(f"{'-'*40}\n")
def main():
    create_banner()
    while True:
        public_ip = get_public_ip()
        print(colored(f"Public IP of your computer: {public_ip}", 'cyan'))
        url = input("Enter the website URL: ")
        website_ip = get_website_ip(url)
        print(colored(f"Website's hosting IP address: {website_ip}", 'yellow'))
        iframe_allowed = check_iframe(url)
        iframe_status = "Allowed" if iframe_allowed else "Not Allowed"
        log_to_file(url, public_ip, website_ip, iframe_status)
        if iframe_allowed:
            create_html_with_iframe(url)
        else:
            print(colored("Iframe embedding is not possible for this website.", 'red'))
        choice = input("\nDo you want to continue scanning another website? (y/n): ").lower()
        if choice != 'y':
            print("Exiting the program. hahahaha!")
            break
if __name__ == "__main__":
    main()
