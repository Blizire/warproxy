import socket

# fake server to test proxy
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', 5555))
    sock.listen(1)
    print("waiting for connection...")
    conn, addr = sock.accept()
    with conn as c:
        print(f'{addr} has connected')
        while True:
            data = conn.recv(1024)
            if data:
                print(f'recvd : {data}')
                conn.sendall('byte this!!!'.encode('utf-8'))
