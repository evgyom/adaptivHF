from Server import MultiSocketServer
import time


serv = MultiSocketServer("localhost",20201,"asd",["asdffg"])
serv.start()

#serv.stop()