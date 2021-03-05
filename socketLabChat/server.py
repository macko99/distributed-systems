import common
import socket
from threading import Thread
from time import sleep

max_clients = 256
clients = {}


def accept_tcp_connection(server_socket):
    while True:
        client_socket, client_addr = server_socket.accept()
        if len(clients) < max_clients:
            client_thread = Thread(target=receive_tcp, args=(client_socket, client_addr))
            client_thread.start()
        else:
            client_socket.close()
            client_ip, client_port = client_addr
            print('### Connection from ' + str(client_ip) + ':' + str(client_port) + ' refused. ###')


def receive_tcp(client_socket, client_addr):
    client_ip, client_port = client_addr
    print('### Connection from ' + str(client_ip) + ':' + str(client_port) + ' accepted. ###')

    clients[client_addr] = client_socket

    while True:
        data = client_socket.recv(common.max_msg_length)
        if data == b'':
            del clients[client_addr]
            client_socket.close()
            print('### Connection from ' + str(client_ip) + ':' + str(client_port) + ' dropped by client. ###')
            return

        for is_my_socket in clients.values():
            if is_my_socket != client_socket:
                is_my_socket.sendall(data)

        print('(tcp): ' + str(data))


def receive_udp(udp_socket):
    while True:
        try:
            data, client_addr = udp_socket.recvfrom(common.max_msg_length)
        except OSError:
            return

        for is_my_addr in clients.keys():
            if is_my_addr != client_addr:
                udp_socket.sendto(data, is_my_addr)

        print('(udp): ' + str(data))


if __name__ == '__main__':
    print('### python chat server ###')

    server_socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    data_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    try:
        server_socket_tcp.bind(common.serverAddr)
        data_socket_udp.bind(common.serverAddr)
    except OSError:
        server_socket_tcp.close()
        print('### Error. Server bind command failed. ###')
        raise SystemExit

    server_socket_tcp.listen(10)

    Thread(target=accept_tcp_connection, args=(server_socket_tcp,), daemon=True).start()
    Thread(target=receive_udp, args=(data_socket_udp,), daemon=True).start()

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        for addr, sck in clients.items():
            sck.shutdown(socket.SHUT_WR)
            c_ip, c_port = addr
        print('### Disconnected all clients. Shutting down. ###')
        server_socket_tcp.close()
        raise SystemExit
