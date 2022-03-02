import struct
import sys
import socket
import selectors
import time
import types
import json

#Message: {command:, name:, payload:}




sel = selectors.DefaultSelector()
messages = [json.dumps({"command":"SetName", "name":"asd","payload":None}).encode("utf-8"),
            json.dumps({"command":"asdf", "name":"asd"}).encode("utf-8") ]


def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print(f"Starting connection {connid} to {server_addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
            connid=connid,
            msg_total=sum(len(m) for m in messages),
            recv_total=0,
            messages=messages.copy(),
            outb=b"",
        )
        sel.register(sock, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        size = struct.unpack("i", sock.recv(struct.calcsize("i")))[0]
        recv_data = ""
        while len(recv_data) < size:
            msg = sock.recv(size - len(recv_data))
            if not msg:
                break
            recv_data += msg.decode('utf-8')
        if recv_data != "":
            print(f"Received {recv_data} from connection {data.connid}")
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print(f"Closing connection {data.connid}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            msg = data.messages.pop(0)
            data.outb = struct.pack("i", len(msg)) + msg
        if data.outb:
            print(f"Sending {data.outb!r} to connection {data.connid}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


start_connections("localhost", 20201, 1)

try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key, mask in events:
                service_connection(key, mask)
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()

