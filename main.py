import socket
from threading import Thread

# The listening side of the proxy that will intercept traffic
class ProxyEntry(Thread):
    def __init__(self, host, port):
        super(ProxyEntry, self).__init__()
        self.proxyExit = None
        self.port = int(port)
        self.host = host
        # creating an IPv4 TCP Socket to listen
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # prevents socket in TIME_WAIT state
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        # starts listening
        sock.listen(1)
        print(f"listening on {self.host}:{self.port}...")
        # accept returns new socket object to send/recv to client connecting
        self.conn, addr = sock.accept()
        print(f"{addr} : has connected!")

    # runs as thread
    def run(self):
        try:
            while True:
                data = self.conn.recv(1024)
                if data:
                    print(data)
                    # send to server
                    self.proxyExit.sendall(data)
        except Exception as e:
            print(e)

# The exit side that pushes and pulls traffic from server
class ProxyExit(Thread):
    def __init__(self, host, port):
        super(ProxyExit, self).__init__()
        self.proxyEntry = None
        self.port = int(port)
        self.host = host
        # creating an IPv4 TCP Socket to listen
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        print(f'Connected to server {host}:{port}!')
    # runs as thread
    def run(self):
        try:
            while True:
                data = self.sock.recv(1024)
                if data:
                    print(data)
                    # sends data back to client
                    self.proxyEntry.sendall(data)
        except Exception as e:
            print(e)


client_proxy = ProxyEntry("127.0.0.1",5000)
server_proxy = ProxyExit("127.0.0.1", 5555)

client_proxy.proxyExit = server_proxy.sock
server_proxy.proxyEntry = client_proxy.conn

client_proxy.start()
server_proxy.start()