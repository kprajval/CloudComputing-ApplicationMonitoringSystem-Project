import requests
import random
import time

base_url = "http://localhost:5000"
endpoints = ["/login", "/products", "/product/1", "/order", "/health", "/error"]

while True:
    endpoint = random.choice(endpoints)
    url = base_url + endpoint
    try:
        method = "post" if endpoint in ["/login", "/order"] else "get"
        response = getattr(requests, method)(url)
        print(f"{method.upper()} {url} => {response.status_code}")
    except Exception as e:
        print(f"Failed to reach {url}: {e}")
    time.sleep(2)
