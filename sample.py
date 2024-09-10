import requests

request = requests.post("https://swe-backend-bk7f.onrender.com/process-url")

print(request.json())
