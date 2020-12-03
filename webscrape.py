import requests

url = "http://www.bureauwbtv.nl/tolkvertaler-search/api/search/s"

content = {
    "searchType": "wbtv_search",
    "wbtvNumber": 1
}

headers = {
}

for i in range(1, 10):
    try:
        response = requests.post(url, headers=headers, json=content)
    except Exception as ex:
        print(f"Exception on POST for #{i}: {ex}")

    test

print(response.text[:50])
