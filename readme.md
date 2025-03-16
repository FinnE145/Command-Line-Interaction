# *CLI*nteraction

*CLI*nteraction is a simple Flask-based API and command-line client for managing conversations, messages, and users.

## Features

- Create, update, delete, and retrieve conversations
- Add and remove users from conversations
- Create, update, delete, and retrieve messages within conversations
- Manage user information

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/FinnE145/Command-Line-Interaction
    ```
2. Navigate to the project directory:
    ```
    cd <project-directory>
    ```
3. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:
    ```
    python app.py
    ```
2. The API will be available at `http://localhost:5000`.
    a) [Optional] Use various means of port forwarding to make your API instance available on your local network or the internet. Look into vscode port forwarding for the simplest solution.
3. Run the CLI client:
    ```
    python client.py
    ```
4. Follow the prompts to interact with the API.

# API Information

## Endpoints

- `/convo` - Manage conversations
- `/convo/<int:convo_id>` - Manage a specific conversation
- `/convo/<int:convo_id>/user/<int:user_id>` - Manage users in a specific conversation
- `/convo/<int:convo_id>/message/<int:message_id>` - Manage messages in a specific conversation
- `/user/<int:user_id>` - Manage users

> For more information, see the [API docs](#api_docs.md)

> For a direct usage example, see [example.py](#example.py)

# License

This project is licensed under the MIT License.