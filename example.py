from requests import get, post, put, delete
from iformat import iprint

def make_request(method, url, json=None, **kwargs):
    response = method(url, json=json, **kwargs)
    if response.status_code//100 == 2:
        iprint(response.json())
    else:
        iprint(f"Error: {response.status_code}, {response.text}")

if input("Create messages?"):

    make_request(post, "http://localhost:5000/messages", json={
        "convo_id": 0,
        "user_id": 0,
        "content": "Hello, World!"
    })

    make_request(post, "http://localhost:5000/messages", json={
        "convo_id": 0,
        "user_id": 1,
        "content": "Hello, World!"
    })

    make_request(post, "http://localhost:5000/messages", json={
        "convo_id": 1,
        "user_id": 1,
        "content": "Hello, World!"
    })

make_request(get, "http://localhost:5000/message/")