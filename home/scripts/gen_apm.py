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
    # add up to 7 if you like:
    # ("user5", "user5"),
    # ("user6", "user6"),
    # ("user7", "user7"),
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
    r = s.post(f"{BASE}/my.policy", data=payload, allow_redirects=True)

    print(f"[login] {username} status={r.status_code} cookies={s.cookies.get_dict()}")
    return s

# map username -> session
sessions = {u: login(u, p) for (u, p) in USERS}

i = 0
while True:
    user, pwd = random.choice(USERS)
    s = sessions[user]

    # send one request from that “user”
    r = s.get(
        f"{BASE}/protected/page",
        headers={"User-Agent": "apm-loadgen-python"},
        allow_redirects=True,
    )

    # if we got bumped back to my.policy, the APM session probably expired -> re-login
    if "/my.policy" in r.url:
        print(f"[relogin] session expired for {user}, re-authenticating")
        sessions[user] = login(user, pwd)
    else:
        print(i, r.status_code, "user=", user, "MRHSession=", s.cookies.get("MRHSession"))
        i += 1

    # overall rate ~5–15 reqs/min across all sessions
    time.sleep(random.randint(4, 12))
