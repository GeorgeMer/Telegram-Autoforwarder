# Telegram Autoforwarder

The Telegram Autoforwarder is a Python script that allows you to forward messages from multiple chats (groups or channels) to one other based on specified keywords. It works with both groups and channels, requiring only the necessary permissions to access the messages.

## Features

-   Forward messages containing specific keywords from one chat to another.
-   Works with both groups and channels.
-   Simple setup and usage.

## How it Works

The script uses the Telethon library to interact with the Telegram API. You provide the script with your Telegram API ID, API hash, and phone number for authentication. Then, you can choose to list all chats you're a part of and select the ones you want to use for forwarding messages. Once configured, the script continuously checks for messages in the specified source chat and forwards them to the destination chat if they contain any of the specified keywords.

## Keywords

You can specify one or more keywords that, if found in a message, trigger the forwarding process. Keywords are case-insensitive and can be specified during setup.

## Setup and Usage

0. Go to [Telegram API Development tools](https://my.telegram.org/apps) and fill out the form. You will get the API id and API hash parameters required for user authorization.

1. Clone the repository:

    ```bash
    git clone https://github.com/GeorgeMer/Telegram-Autoforwarder.git
    cd Telegram-Autoforwarder
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the script:

    ```bash
    python TelegramForwarder.py
    ```

4. Configure the script:

    Create subdirectories in each of which you can create 3 files:

    - **credentials.txt** — stores API id, API hash, and phone number
    - **config.txt** — stores configuration properties, e.g. delay between checking for new messages
    - **forwarder.txt** — stores the source chat IDs, the destination chat ID, and the keywords

    The subdirectory as well as all the data can be specified by running the script.

    After one setup, you can rerun with the same subdirectory without having to input anything.

    If you want to setup another autoforward instance (with e.g. tmux), but don't want to re-input your credentials, you can create the subdirectory and the credentials.txt yourself, and then only specify the directory and the other 2 configuration files in the running script.

5. Before seting up forwarder, choose an option:
    - List Chats: View a list of all chats you're a part of and find the ones to use for message forwarding.
    - Forward Messages: Enter the source chat IDs, destination chat ID, and keywords to start forwarding messages.

## Notes

-   Remember to keep your API credentials secure and do not share them publicly.
-   Ensure that you have the necessary permissions to access messages in the chats you want to use.
-   Adjust the script's behavior and settings according to your requirements.

## License

This project is licensed under the MIT License.
