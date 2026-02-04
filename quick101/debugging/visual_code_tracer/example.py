"""
Example: Visual Tracer
======================
Just ONE line needed!
"""
from visual_tracer import trace; trace()

import time

def fetch_data(user_id):
    time.sleep(0.02)
    return {"id": user_id, "name": f"User_{user_id}"}

def process(data):
    return data["name"].upper()

def main():
    data = fetch_data(123)
    result = process(data)
    print(f"Result: {result}")
    return result

main()
