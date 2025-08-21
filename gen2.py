#
# Things to examine:
#
# url_list <-- Set this with your own values. Ask for permission first.
# max_workers <-- tune to your cpus, 50-100 works well with 8vCPUs
# methods <-- if your server supports you can enable POST and/or DELETE here
#

import requests
import random
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from concurrent.futures import ThreadPoolExecutor

user_agents = [
    # Chrome on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    # Chrome on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    # Edge on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78",
    # Firefox on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    # Firefox on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0",
    # Safari on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    # Chrome on Android
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    # Firefox on Android
    "Mozilla/5.0 (Android 12; Mobile; rv:124.0) Gecko/124.0 Firefox/124.0",
    # Mobile Safari (iPhone)
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    # Chrome on iOS
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/124.0.0.0 Mobile/15E148 Safari/604.1",
    # Samsung Internet Browser
    "Mozilla/5.0 (Linux; Android 10; SAMSUNG SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/21.0 Chrome/92.0.4515.131 Mobile Safari/537.36",
    # UC Browser on Android
    "Mozilla/5.0 (Linux; U; Android 10; en-US; SM-N976N Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 UCBrowser/13.3.5.1305 Mobile Safari/537.36",
    # Opera Desktop
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 OPR/98.0.4759.15",
    # Brave Browser
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Brave/124.0.0.0"
]

accepts = [
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "application/json",
    "application/xml",
    "*/*"
]

content_types = [
    "application/json",
    "application/x-www-form-urlencoded",
    "text/plain"
]

# Add back in POST and DELETE later, configure on server first
methods = ["GET", "HEAD"]

url_list = [
    "https://ast.demo.f5",
    "https://ast.demo.f5",
    "https://ast50.demo.f5",
    "http://ast55.demo.f5",
    "https://ast42.demo.f5",
    "http://ast50.demo.f5"
]

def send_request(i):
    url = random.choice(url_list)
    headers = {
        "X-Forwarded-For": ".".join(str(random.randint(1, 254)) for _ in range(4)),
        "User-Agent": random.choice(user_agents),
        "Accept": random.choice(accepts),
        "Content-Type": random.choice(content_types)
    }
    method = random.choice(methods)
    data = None
    if method in ["POST", "PUT"]:
        if headers["Content-Type"] == "application/json":
            data = '{"key": "value", "num": %d}' % i
        elif headers["Content-Type"] == "application/x-www-form-urlencoded":
            data = "key=value&num=%d" % i
        else:
            data = "key: value, num: %d" % i
    try:
        response = requests.request(method, url, headers=headers, data=data, timeout=5, verify=False)
        print(f"Request {i+1}: {method} {url} -- Status: {response.status_code}")
    except Exception as e:
        print(f"Request {i+1} failed: {e}")

# Number of requests and concurrent threads (adjust as needed)
total_requests = 10000
max_workers = 75  # 50-100-ish, tune based on vCPU

while True: # run indefinitely
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(send_request, range(total_requests))
    time.sleep(3)
