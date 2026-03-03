import requests
import warnings
import time
import random
from urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter("ignore", InsecureRequestWarning)

BASE = "https://ast42.demo.f5:8443"

s = requests.Session()
s.verify = False  # or point to a CA bundle in lab

# 1) Hit protected page to establish APM flow
r1 = s.get(f"{BASE}/protected/page", allow_redirects=True)

# 2) POST credentials to the APM logon form
payload = {
    "username": "user",
    "password": "user",
}
r2 = s.post(f"{BASE}/my.policy", data=payload, allow_redirects=True)

print(s.cookies.get_dict())

# 4) Slow loop: ~5–15 requests per minute
i = 0
while True:
    r = s.get(f"{BASE}/protected/page",
              headers={"User-Agent": "apm-loadgen-python"})
    print(i, r.status_code)
    i += 1
    # sleep 4–12 seconds between requests
    time.sleep(random.randint(4, 12))
