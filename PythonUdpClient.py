import socket

serverIP = "127.0.0.1"
serverPort = 9008
msg = "Ping Python Udp!"
msg2 = "żółta gęś"

if __name__ == '__main__':
    print('PYTHON UDP CLIENT')
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # EX1/2
    #
    #
    # client.sendto(bytes(msg2, 'utf8'), (serverIP, serverPort))
    # buff = client.recvfrom(1024)
    # print("python udp client received response: " + str(buff, 'cp1250'))
    #
    #
    #
    # EX3
    #
    #
    # client.sendto((300).to_bytes(4, byteorder='little'), (serverIP, serverPort))
    # buff, addr = client.recvfrom(1024)
    # number = int.from_bytes(buff, byteorder='little')
    # print("python udp client received response: " + str(number))
    #
    #
    #
    # EX4
    #
    #
    client.sendto((300).to_bytes(4, byteorder='little'), (serverIP, serverPort))
    buff, addr = client.recvfrom(1024)
    print("python udp client received response: " + str(buff))
    #
    #
    #
