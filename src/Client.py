import struct
import sys
import socket
import selectors
import time
import types
import json
from queue import Queue
from threading import Thread

#Message: {command:, name:, payload:}


messages = [json.dumps({"command": "SetName", "name": "Player", "payload": None}).encode("utf-8"),
            json.dumps({"command": "printer", "name": "Player", "payload": "Check"}).encode("utf-8")]


class SocketClient:
    def __init__(self, ip, port, callback):
        self.host = ip
        self.port = port
        self.running = True
        self.t = None
        self.sendQueue = Queue()
        self.callback = callback

    def sendData(self, data):
        self.sendQueue.put(data)


    def start(self):
        self.running = True
        self.t = Thread(target=self._run)
        self.t.start()

    def stop(self):
        self.running = False
        if self.t is not None:
            self.t.join()

    def start_connections(self, host, port, num_conns):
        server_addr = (host, port)
        print(f"Starting connection to {server_addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(sock, events)

    def service_connection(self, key, mask):
        sock = key.fileobj
        if mask & selectors.EVENT_READ:
            size = struct.unpack("i", sock.recv(struct.calcsize("i")))[0]
            recv_data = ""
            while len(recv_data) < size:
                msg = sock.recv(size - len(recv_data))
                if not msg:
                    break
                recv_data += msg.decode('utf-8')
            if recv_data != "":
                jsondata = None
                try:
                    jsondata = json.loads(recv_data)
                except:
                    pass
                if jsondata is not None:
                    if "pos" in jsondata.keys() and "tick" in jsondata.keys() and "active" in jsondata.keys() and "size" in jsondata.keys() and "vision" in jsondata.keys():
                        self.callback(jsondata, self.sendData)
                #print(f"Received {recv_data}")
            if not recv_data:
                print(f"Closing connection ")
                self.sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            while not self.sendQueue.empty():
                msg = self.sendQueue.get().encode("utf-8")
                datasend = struct.pack("i", len(msg)) + msg
                sent = sock.send(datasend)

    def _run(self):
        self.sel = selectors.DefaultSelector()
        self.start_connections(self.host, self.port, 1)

        try:
            while self.running:
                events = self.sel.select(timeout=1)
                if events:
                    for key, mask in events:
                        self.service_connection(key, mask)
                # Check for a socket being monitored to continue.
                if not self.sel.get_map():
                    print("Closing")
                    break
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            self.sel.close()

