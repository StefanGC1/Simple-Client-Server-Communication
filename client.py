import socket


def main():
    # Some constants
    host = '127.0.0.1'
    port = 12345
    client_id = None

    # Creating the socket and connecting to the server (address)
    client_socket = socket.socket()
    client_socket.connect((host, port))
    
    # Receive server port
    port_to_server = int(client_socket.recv(1024).decode())
    print(f"[CLIENT] Client connected to server on {host}:{port_to_server}.")

    # Receive the id
    client_id = int(client_socket.recv(1024).decode())
    print(f"[CLIENT_{client_id}] Client id given by server: {client_id}")

    while True:
        try:
            # Send data from input to the server
            data_to_send = input("[SYSTEM] Enter data to send to server (enter exit to quit): ")

            if data_to_send.lower() == 'exit':
                break

            client_socket.sendall(data_to_send.encode())

            received_data = client_socket.recv(1024)
            print(f"[CLIENT_{client_id}] Server received and sent back following data on port[{port_to_server}] from source(server) port[{port}]: {received_data.decode()}")
        except ConnectionAbortedError:
            # Handle server shutdown
            print("\n[CLIENT] Server closed down!")
            break


    client_socket.close()
    print(f"[CLIENT_{client_id}] Connection closed!")


if __name__ == '__main__':
    main()
