import requests
from bs4 import BeautifulSoup


# Create a country
json = {
    "id":3,
    "name":"China",
    "capital":"Beijing",
    "age": 5000,
    "affiliation_id":1
    }
# response = requests.post("http://127.0.0.1:8000/countries/", json=json)
# print(response.status_code)
# print(response.json())
# response = requests.get("http://127.0.0.1:8000/countries/3")
# print(response.json())
# response = requests.get("http://127.0.0.1:8000/affiliation/1")
# print(response.json())

# afil = {
#     "name": "NATO"
# }
# response = requests.post("http://127.0.0.1:8000/affiliation/", json=afil)
# print(response.status_code)
# print(response.json())

response = requests.get("http://127.0.0.1:8000/countries/1")
print(response.json())
response = requests.delete("http://127.0.0.1:8000/countries/1")
print(response.status_code)
print(response.json())
response = requests.get("http://127.0.0.1:8000/countries/1")
print(response.json())

