import time

class Timer:
    def __init__(self, uiRoot, onTick):
        self.uiRoot = uiRoot
        self.onTick = onTick  
        self.isRunning = False
        self.lastUpdateTime = None
        self.elapsedSeconds = 0
        self._afterId = None

    def Start(self):
        if self.isRunning:
            return
        self.isRunning = True
        self.lastUpdateTime = time.time()
        self._RunLoop()

    def Pause(self):
        if not self.isRunning:
            return
        self.isRunning = False
        self._CancelLoop()
        self._UpdateElapsed()

    def Reset(self):
        self._CancelLoop()
        self.elapsedSeconds = 0
        self.isRunning = False
        self.lastUpdateTime = None
        self.onTick(self.elapsedSeconds)

    def _RunLoop(self):
        if not self.isRunning:
            return
        self._UpdateElapsed()
        self.onTick(self.elapsedSeconds)
        self._afterId = self.uiRoot.after(1000, self._RunLoop)

    def _UpdateElapsed(self):
        now = time.time()
        if self.lastUpdateTime:
            self.elapsedSeconds += int(now - self.lastUpdateTime)
        self.lastUpdateTime = now

    def _CancelLoop(self):
        if self._afterId is not None:
            self.uiRoot.after_cancel(self._afterId)
            self._afterId = None
