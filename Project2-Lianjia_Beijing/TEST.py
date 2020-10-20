import requests

url = "https://dps.kdlapi.com/api/getdps/?orderid=900257417255019&num=1&pt=1&sep=2"
resp = requests.get(url)
resp = resp.text.split('\n')
print(resp)