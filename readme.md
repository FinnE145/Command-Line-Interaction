# *CLI*nteraction

*CLI*nteraction is a simple Flask-based API and command-line client for managing conversations, messages, and users.

## Features

- Create, update, delete, and retrieve conversations
- Add and remove users from conversations
- Create, update, delete, and retrieve messages within conversations
- Manage user information

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    ```
2. Navigate to the project directory:
    ```sh
    cd CLInteraction
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:
    ```sh
    python app.py
    ```
2. The API will be available at `http://localhost:5000`.

## Endpoints

- `/convo` - Manage conversations
- `/convo/<int:convo_id>` - Manage a specific conversation
- `/convo/<int:convo_id>/user/<int:user_id>` - Manage users in a specific conversation
- `/convo/<int:convo_id>/message/<int:message_id>` - Manage messages in a specific conversation
- `/user/<int:user_id>` - Manage users

> For more information, see the api docs

## Example

```python
from requests import get, post, put, delete

def make_request(method, url, data=None, **kwargs):
    response = method(url, data=data, **kwargs)
    if response.status_code == 200:
        return response.json()
    return f"Error: {response.status_code}, {response.text}"

print(make_request(get, "http://localhost:5000/convo/0"))
print(make_request(post, "http://localhost:5000/convo/0", {"name": "New Conversation", "user_ids": [0, 1, 2]}))
print(make_request(put, "http://localhost:5000/convo/0", {"name": "Updated Conversation", "user_ids": [0, 1, 3]}))
print(make_request(delete, "http://localhost:5000/convo/0"))
```

## License

This project is licensed under the MIT License.