import socket
import threading

# A sort of flag to indicate when the server is in the process of closing
shutdown_event = threading.Event()


def handle_client(conn, addr, client_id, server_port):
    print(f"[SERVER_THREAD] Connected to CLIENT_{client_id} on {addr}")
    conn.settimeout(1.0)

    if not shutdown_event.is_set():
        conn.sendall(str(addr[1]).encode())

    if not shutdown_event.is_set():
        conn.sendall(str(client_id).encode())

    while not shutdown_event.is_set():
        try:
            # Sets a 1-second limit on how long the server can wait for receiving data
            data = conn.recv(1024)
            if not data:
                break
            # Checks the flag to see if server is shutting down
            if shutdown_event.is_set():
                print(f"[SERVER_THREAD] Shutdown in progress. Closing connection with CLIENT_{client_id}")
                break
            # Receive data and send it back to the client
            print(f"[SERVER_THREAD] Received data from CLIENT_{client_id} on port[{server_port}] from port[{addr[1]}]: {data.decode()}")
            conn.sendall(data)
        except socket.timeout:
            continue
        except ConnectionResetError:
            break

    print(f"[SERVER_THREAD] CLIENT_{client_id} disconnected")
    conn.close()


def main():
    # Some constants
    client_counter = 0
    host = '127.0.0.1'
    port = 12345

    # Creating the socket and linking an address to it
    server_socket = socket.socket()
    server_socket.bind((host, port))

    try:
        # Sets the server into a state to listen for connections
        server_socket.listen()
        print(f"[SERVER] listening on {host}:{port}.")

        # Sets a 1-second limit on how long the server can wait for a connection
        server_socket.settimeout(1.0)

        while not shutdown_event.is_set():
            try:
                # Wait for a connection
                conn, addr = server_socket.accept()
            except socket.timeout:
                continue

            # When a connection is established, increase client_counter and create a thread that handles
            # the current client
            client_counter += 1
            client_thread = threading.Thread(target=handle_client, args=(conn, addr, client_counter, port))
            client_thread.start()
            print(f"\n[SERVER] Active connections: {threading.active_count() - 1}")
    except KeyboardInterrupt:
        # Handle a shutdown event
        print("\n[SERVER] Shutdown signal received. Shutting down...")
        shutdown_event.set()

    server_socket.close()

    # Wait for client threads to finish
    for thread in threading.enumerate():
        if thread is not threading.main_thread():
            thread.join()


if __name__ == '__main__':
    main()
