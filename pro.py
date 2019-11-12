import requests
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

