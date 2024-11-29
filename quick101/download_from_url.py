from urllib.parse import urlencode

base_url = "https://example.com/api"
params = {
    "param1": "value1",
    "param2": "value2"
}
url = f"{base_url}?{urlencode(params)}"


import requests

url = "https://example.com/api?param1=value1&param2=value2"
response = requests.get(url)

with open("output.txt", "wb") as file:
    file.write(response.content)

from urllib.request import urlretrieve

url = "https://example.com/api?param1=value1&param2=value2"
urlretrieve(url, "output.txt")