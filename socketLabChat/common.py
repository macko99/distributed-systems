import json

serverIp = '127.0.0.1'
serverPort = 5511
serverAddr = (serverIp, serverPort)

max_msg_length = 2048


def encode_msg(user, data):
    data = json.dumps({
        'user': user,
        'data': data,
    }).encode()
    return data


def decode_msg(data):
    msg = json.loads(data.decode())
    return msg['user'], msg['data']