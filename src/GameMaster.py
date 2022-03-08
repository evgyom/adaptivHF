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
        self.serv.start()
        self.engine = AdaptIOEngine(sender=self.serv.sendData, getter=self.serv.getLatestForName)
        self.tickLength = DEFAULT_TICK_LENGTH_S
        self.timer = RepeatTimer(self.tickLength,self.processTick)
        self.running = False
        self.gameState = STATE.RUNNING
        self.pollGameCommands = True
        self.exitTimer = None
        self.gameStartTimer = None
        self.autoStartTimer = None
        self.canStart = False

    def _startGame(self):
        self.gameState = STATE.RUNNING

    def processTick(self):
        if self.gameState == STATE.PRERUN:
            if self.autoStartTimer is None:
                self.autoStartTimer = Timer(30, self._startGame)
            if not self.serv.checkMissingPlayers():
                self.gameState = STATE.RUNNING

        elif self.gameState == STATE.RUNNING:
            self.autoStartTimer = None
            if not self.engine.tick():
                self.gameState = STATE.WAIT_COMMAND
            else:
                print(self.engine.ticknum)

        elif self.gameState == STATE.WAIT_COMMAND:
            if self.exitTimer is None:
                self.exitTimer = Timer(30, self.close)
                self.exitTimer.start()
            pass

        elif self.gameState == STATE.WAIT_START:
            if self.canStart:
                self.serv.sendData("Starting","all")
                self.gameState = STATE.RUNNING
                self.canStart = False

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
        self.timer.join()
        self.pollGameCommands = False
        self.serv.stop()
        if self.exitTimer is not None:
            self.exitTimer.cancel()
        print("Close finished")

    def run(self):
        self.timer.start()
        self.running = True
        try:
            while self.pollGameCommands:
                action = self.serv.getGameMasterFIFO()
                if action is None:
                    continue
                if not("type" in action.keys() and "data" in action.keys()):
                    continue
                if action["type"] == "interrupt":
                    self.close()
                if action["type"] == "start":
                    self.canStart = True
                if action["type"] == "reset":
                    self.canStart = False
                    self.engine.reset_state(action["data"]["mapPath"],action["data"]["updateMapPath"])
        except KeyboardInterrupt:
            print("Interrupted, stopping")
            self.close()


if __name__ == "__main__":
    gm = GameMaster()
    gm.run()