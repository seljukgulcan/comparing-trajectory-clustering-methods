import time


class Stopwatch:

    def __init__(self):
        self.start_time = 0

    def start(self):
        self.start_time = time.time()

    def stop(self, message = "Stopwatch stopped"):
        elapsed = time.time() - self.start_time
        print( "%s : %.2f sn" % (message, elapsed))
