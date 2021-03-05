import common
import socket
from threading import Thread
import select

inner_love ="""
  _    _ _____  _____    _      ______      ________   _    _           _____    _____          __  __ ______   _______ ____   __     ______  _    _ 
 | |  | |  __ \|  __ \  | |    / __ \ \    / /  ____| | |  | |   /\    / ____|  / ____|   /\   |  \/  |  ____| |__   __/ __ \  \ \   / / __ \| |  | |
 | |  | | |  | | |__) | | |   | |  | \ \  / /| |__    | |__| |  /  \  | (___   | |       /  \  | \  / | |__       | | | |  | |  \ \_/ / |  | | |  | |
 | |  | | |  | |  ___/  | |   | |  | |\ \/ / |  __|   |  __  | / /\ \  \___ \  | |      / /\ \ | |\/| |  __|      | | | |  | |   \   /| |  | | |  | |
 | |__| | |__| | |      | |___| |__| | \  /  | |____  | |  | |/ ____ \ ____) | | |____ / ____ \| |  | | |____     | | | |__| |    | | | |__| | |__| |
  \____/|_____/|_|      |______\____/   \/   |______| |_|  |_/_/    \_\_____/   \_____/_/    \_\_|  |_|______|    |_|  \____/     |_|  \____/ \____/ 
                                                                                                                                                     
   _______________                        |*\_/*|________
  |  ___________  |     .-.     .-.      ||_/-\_|______  |
  | |           | |    .****. .****.     | |           | |
  | |   0   0   | |    .*****.*****.     | |   0   0   | |
  | |     -     | |     .*********.      | |     -     | |
  | |   \___/   | |      .*******.       | |   \___/   | |
  | |___     ___| |       .*****.        | |___________| |
  |_____|\_/|_____|        .***.         |_______________|
    _|__|/ \|_|_.............*.............._|________|_
   / ********** \                          / ********** \\\ 
 /  ************  \                      /  ************  \\\ 
--------------------                    --------------------"""


def receive(tcp_sock, udp_sock):
    while True:
        ready_socks, _, _ = select.select([tcp_sock, udp_sock], [], [])

        if tcp_sock in ready_socks:
            try:
                rcv_data = tcp_sock.recv(common.max_msg_length)
            except Exception:
                print('### (tcp) receiving data failed. ###')
                raise SystemExit

            if rcv_data == b'':
                print('### server disconnected ###')
                raise SystemExit

            sender_id, rcv_msg = common.decode_msg(rcv_data)
            print('(tcp): ' + sender_id + ' -> ' + rcv_msg)

        if udp_sock in ready_socks:
            rcv_data, _ = udp_sock.recvfrom(common.max_msg_length)
            sender_id, rcv_msg = common.decode_msg(rcv_data)
            print('(udp): ' + sender_id + ' -> ' + rcv_msg)


if __name__ == '__main__':
    print('### python chat client ###')

    while True:
        try:
            uid = input('your id: ')
        except KeyboardInterrupt:
            raise SystemExit
        if uid:
            break

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    try:
        tcp_socket.connect(common.serverAddr)
        _, tcp_port = tcp_socket.getsockname()
        udp_socket.bind((common.serverIp, tcp_port))
    except ConnectionRefusedError:
        print('### connecting to server failed. ###')
        raise SystemExit

    thread = Thread(target=receive, args=(tcp_socket, udp_socket), daemon=True)
    thread.start()

    while True:
        try:
            msg = input()
        except KeyboardInterrupt:
            tcp_socket.close()
            udp_socket.close()
            raise SystemExit
        if not msg:
            continue

        if '/exit' in msg:
            tcp_socket.close()
            udp_socket.close()
            raise SystemExit
        elif '/udp ' in msg:
            data = common.encode_msg(uid, msg.replace('/udp ', ' '))
            udp_socket.sendto(data, common.serverAddr)
        elif '/udp_love' in msg:
            data = common.encode_msg(uid, inner_love)
            udp_socket.sendto(data, common.serverAddr)
        else:
            data = common.encode_msg(uid, msg)
            tcp_socket.sendall(data)
