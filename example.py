from requests import get, post, put, delete

def make_request(method, url, data=None, **kwargs):
    response = method(url, data=data, **kwargs)
    if response.status_code == 200:
        return response.json()
    return f"Error: {response.status_code}, {response.text}"



print(make_request(get, "http://localhost:5000/convo/0"))

print(make_request(post, "http://localhost:5000/convo/0", {
        "name": "New Conversation",
        "user_ids": [0, 1, 2],
        "message_ids": [0, 1, 2]
    }))

print(make_request(put, "http://localhost:5000/convo/0", {
        "name": "Updated Conversation",
        "user_ids": [0, 1, 3],
        "message_ids": [0, 1]
    }))

print(make_request(delete, "http://localhost:5000/convo/0"))