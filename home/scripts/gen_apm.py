import requests
import warnings
import time
import random
from urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter("ignore", InsecureRequestWarning)

BASE = "https://ast42.demo.f5:8443"

USERS = [
    ("user1", "user1"),
    ("user2", "user2"),
    ("user3", "user3"),
    ("user4", "user4"),
    ("user5", "user5"),
    ("user6", "user6"),
    ("user7", "user7"),
    ("user8", "user8"),
]

def login(username, password):
    s = requests.Session()
    s.verify = False  # lab only

    # 1) Hit protected page to start APM flow
    s.get(f"{BASE}/protected/page", allow_redirects=True)

    # 2) Logon
    payload = {
        "username": username,
        "password": password,
    }
    s.post(f"{BASE}/my.policy", data=payload, allow_redirects=True)

    print(username, "cookies:", s.cookies.get_dict())
    return s

# create N sessions (1 per user)
sessions = [login(u, p) for (u, p) in USERS]

i = 0
while True:
    # pick a random logged-in session
    s = random.choice(sessions)

    # send one request from that “user”
    r = s.get(f"{BASE}/protected/page",
              headers={"User-Agent": "apm-loadgen-python"})
    print(i, r.status_code, "from", s.cookies.get("MRHSession"))
    i += 1

    # sleep so overall rate stays ~5–15 per minute
    time.sleep(random.randint(4, 12))
