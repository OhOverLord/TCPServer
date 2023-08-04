import socket
from server import Server
from config import print_color


def main():
    server = Server()
    m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 4000)
    print_color(f'start server up on {server_address[0]} port {server_address[1]}', 'yellow')
    m_socket.bind(server_address)

    m_socket.listen(1)

    server.connection_to_server(m_socket)


if __name__ == "__main__":
    main()
