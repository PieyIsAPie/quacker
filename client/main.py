from lib import ChatClient

def main():
    host = "localhost"  # Change this to your server's hostname or IP address
    port = 55555        # Change this to your server's port

    client = ChatClient(host, port)

    try:
        username = input("Enter your username: ")
        color = input("Enter your color: ")
        password = input("Enter the server password (if required): ")

        if client.connect(username, color, password):
            print("Connected to the server!")

            while True:
                message = input("Enter your message (or 'exit' to quit): ")
                if message.lower() == 'exit':
                    client.disconnect()
                    break

                client.send_message(message)
    finally:
        print("Exiting...")

if __name__ == "__main__":
    main()