import requests

pair_id = 1
time_frame = 3600
url = f"https://www.investing.com/technical/Service/GetStudiesContent?action=get_studies&pair_ID={pair_id}&time_frame={time_frame}"

response = requests.get(url)
if response.history:
    print("Request was redirected")
    for resp in response.history:
        print(f"Redirected from {resp.url} to {resp.headers['Location']}")
else:
    print("Request was not redirected")

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Failed to fetch data: {response.status_code}")
