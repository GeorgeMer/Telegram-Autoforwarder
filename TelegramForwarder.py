import time
import asyncio
from telethon.sync import TelegramClient
from telethon.tl.types import Message
from concurrent.futures import ProcessPoolExecutor


class TelegramForwarder:
    def __init__(self, api_id, api_hash, phone_number, try_delay):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.try_delay = try_delay
        self.client = TelegramClient(
            'session_' + phone_number, api_id, api_hash)

    async def list_chats(self):
        await self.client.connect()

        # Ensure you're authorized
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            await self.client.sign_in(self.phone_number, input('Enter the code: '))

        # Get a list of all the dialogs (chats)
        dialogs = await self.client.get_dialogs()
        # Print information about each chat
        for dialog in dialogs:
            print(f"Chat ID: {dialog.id}, Title: {dialog.title}")

        print("List of groups printed successfully!")

    async def forward_messages_to_channel(self, source_chat_id, destination_channel_id, keywords):
        await self.client.connect()

        # Ensure you're authorized
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            await self.client.sign_in(self.phone_number, input('Enter the code: '))

        last_message_id = (await self.client.get_messages(source_chat_id, limit=1))[0].id

        while True:
            print("Checking for messages and forwarding them...")
            # Get new messages since the last checked message
            messages = await self.client.get_messages(source_chat_id, min_id=(last_message_id + 1), limit=None)

            if (messages is None):
                print("No new messages found")
                await asyncio.sleep(self.try_delay)
                continue

            if (isinstance(messages, Message)):
                await self.forward_message(message, destination_channel_id)
                continue

            for message in reversed(messages):
                # Check if the message text includes any of the keywords
                if keywords and message.text and any(keyword in message.text.lower() for keyword in keywords):
                    print(f"Message contains a keyword: {message.text}")

                    await self.forward_message(message, destination_channel_id)
                else:
                    await self.forward_message(message, destination_channel_id)

                # Update the last message ID
                last_message_id = max(last_message_id, message.id)

            # Add a delay before checking for new messages again
            await asyncio.sleep(self.try_delay)

    async def forward_message(seld, message, destination_channel_id):
        await message.forward_to(destination_channel_id)
        print("Message forwarded, {}".format(message.text))

# Function to read credentials from file


def read_credentials():
    try:
        with open("credentials.txt", "r") as file:
            lines = file.readlines()
            api_id = lines[0].strip()
            api_hash = lines[1].strip()
            phone_number = lines[2].strip()
            return api_id, api_hash, phone_number
    except FileNotFoundError:
        print("Credentials file not found.")
        return None, None, None

# Function to write credentials to file


def write_credentials(api_id, api_hash, phone_number):
    with open("credentials.txt", "w") as file:
        file.write(api_id + "\n")
        file.write(api_hash + "\n")
        file.write(phone_number + "\n")


def read_config():
    try:
        with open("config.txt", "r") as file:
            lines = file.readlines()
            try_delay = int(lines[0].strip())
            return try_delay
    except FileNotFoundError:
        print("Config file not found.")
        return None


def write_config(try_delay):
    with open("config.txt", "w") as file:
        file.write(str(try_delay) + "\n")


async def main():
    # Attempt to read credentials from file
    api_id, api_hash, phone_number = read_credentials()

    # If credentials not found in file, prompt the user to input them
    if api_id is None or api_hash is None or phone_number is None:
        api_id = input("Enter your API ID: ")
        api_hash = input("Enter your API Hash: ")
        phone_number = input("Enter your phone number: ")
        # Write credentials to file for future use
        write_credentials(api_id, api_hash, phone_number)

    try_delay = read_config()
    if try_delay is None:
        try_delay = int(
            input("Enter the delay time in seconds to check for new messages: "))
        write_config(try_delay)

    forwarder = TelegramForwarder(api_id, api_hash, phone_number, try_delay)

    print("Choose an option: \n")
    print("1. List Chats \n")
    print("2. Forward Messages. \nReads forwarder.txt for source and destination chat IDs, first line is comma separated source chat IDs, second line is destination chat ID, \nthird line is comma separated keywords or does not exist for no filtering)\n")

    choice = input("Enter your choice: ")

    if choice == "1":
        await forwarder.list_chats()
    elif choice == "2":
        try:
            with open("forwarder.txt", "r") as file:
                lines = file.readlines()
                if (len(lines) != 3 and len(lines) != 2):
                    print(
                        "Invalid forwarder.txt file format. Please follow the format.")
                    return

                source_chat_ids = list(
                    map(lambda s: int(s), lines[0].strip().split(",")))
                destination_channel_id = lines[1].strip()
                keywords = []
                if len(lines) == 3:
                    keywords = lines[2].strip().lower().split(",")

                await run_loop(forwarder, source_chat_ids,
                               destination_channel_id, keywords)

        except FileNotFoundError:
            print("Forwarder file not found.")
    else:
        print("Invalid choice")


async def run_loop(forwarder, source_chat_ids, destination_channel_id, keywords):
    await asyncio.gather(*(forwarder.forward_messages_to_channel(
        int(source_chat_ids[index]), int(destination_channel_id), keywords) for index in range(len(source_chat_ids))))


# Start the event loop and run the main function
if __name__ == "__main__":
    asyncio.run(main())
