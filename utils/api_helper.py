import requests

BASE_URL = "https://stellarburgers.nomoreparties.site/api/auth"

def create_user(email, password, name):
    response = requests.post(f"{BASE_URL}/register", json={
        "email": email,
        "password": password,
        "name": name
    })
    return response.json()

def delete_user(token):
    headers = {"Authorization": token}
    requests.delete(f"{BASE_URL}/user", headers=headers)
