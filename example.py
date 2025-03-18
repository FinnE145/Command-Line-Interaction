from requests import sessions
from iformat import iprint
from sys import argv

s = sessions.Session()

def make_request(method, url, json=None, **kwargs):
    response = s.__getattribute__(method)(url, json=json, **kwargs)
    if response.status_code//100 == 2:
        iprint(response.json())
    else:
        iprint(f"Error: {response.status_code}, {response.json().get('error') or response.text}")

if len(argv) < 2 and input("Create messages?"):
    make_request("post", "http://localhost:5000/messages", json={
        "convo_id": 0,
        "user_id": 0,
        "content": "Hello, World!"
    })

    make_request("post", "http://localhost:5000/messages", json={
        "convo_id": 0,
        "user_id": 1,
        "content": "Hello, World!"
    })

    make_request("post", "http://localhost:5000/messages", json={
        "convo_id": 1,
        "user_id": 1,
        "content": "Hello, World!"
    })

""" make_request("post", "http://localhost:5000/messages", json={
    "convo_id": 0,
    "user_id": 0,
    "content": "Hello, World!"
})

make_request("post", "http://localhost:5000/messages", json={
    "convo_ids": [0, 0],
    "user_ids": [0, 1],
    "contents": ["Hello, World!", "Hello, World!"]
}) """

make_request("post", "http://localhost:5000/users", json={
    "name": "billybob"
})

make_request("get", "http://localhost:5000/users")

make_request("post", "http://localhost:5000/messages", json={
    "convo_id": 0,
    "user_id": 0,
    "content": "I just created a user!"
})

make_request("get", "http://localhost:5000/messages?user_ids=0")

make_request("put", "http://localhost:5000/user/0", json={
    "name": "newname"
})

make_request("get", "http://localhost:5000/user/0")

make_request("delete", "http://localhost:5000/user/0")

make_request("get", "http://localhost:5000/user/0")

make_request("get", "http://localhost:5000/users")