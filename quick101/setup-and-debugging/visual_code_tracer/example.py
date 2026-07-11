"""
Example: Visual Tracer
======================
Just ONE line needed!
"""

# Basic usage - trace everything
from visual_tracer import trace; trace()

# OR: Only trace functions matching patterns
# from visual_tracer import trace; trace(include=['process', 'fetch'])

# OR: Skip certain functions
# from visual_tracer import trace; trace(exclude=['helper', 'log'])

import time

def helper_log(msg):
    print(f"  [log] {msg}")

def fetch_data(user_id):
    helper_log("fetching")
    time.sleep(0.02)
    return {"id": user_id, "name": f"User_{user_id}"}

def process(data):
    helper_log("processing")
    return data["name"].upper()

def main():
    data = fetch_data(123)
    result = process(data)
    print(f"Result: {result}")
    return result

main()

# In the browser UI:
# - Use the search box to filter by function name
# - Uncheck functions in sidebar to hide them (and their children)
