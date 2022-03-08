from Config import *
from Engine import AdaptIOEngine
from Server import MultiSocketServer
import sched, time
from threading import Timer

class STATE:
    PRERUN = 0
    RUNNING = 1
    WAIT_COMMAND = 2
    WAIT_START = 3


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval) and not self.finished.is_set():
            self.function(*self.args, **self.kwargs)

class GameMaster:
    def __init__(self):
        self.serv = MultiSocketServer(IP,PORT,GAMEMASTER_NAME,list(STRATEGY_DICT.keys()))
        self.engine = AdaptIOEngine(sender=self.serv.sendData, getter=self.serv.getLatestForName)
        self.tickLength = DEFAULT_TICK_LENGTH_S
        self.timer = RepeatTimer(self.tickLength,self.processTick)
        self.running = False
        self.gameState = STATE.RUNNING

    def processTick(self):
        if self.gameState == STATE.PRERUN:
            pass
        elif self.gameState == STATE.RUNNING:
            if not self.engine.tick():
                self.gameState = STATE.WAIT_COMMAND
            else:
                print(self.engine.ticknum)
        elif self.gameState == STATE.WAIT_COMMAND:
            pass
        elif self.gameState == STATE.WAIT_START:
            pass
        else:
            pass

    def changeTickLength(self, newInterval):
        if self.running:
            self.timer.cancel()
            self.tickLength = newInterval
            self.timer = RepeatTimer(self.tickLength,self.processTick)
            self.timer.start()
        else:
            self.tickLength = newInterval
            self.timer = RepeatTimer(self.tickLength, self.processTick)

    def close(self):
        self.timer.cancel()
        self.serv.stop()
        self.timer.join()

    def run(self):
        self.timer.start()
        self.running = True
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("Interrupted, stopping")
            self.close()




if __name__ == "__main__":
    gm = GameMaster()
    gm.run()