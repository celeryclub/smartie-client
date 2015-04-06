import threading, time, datetime

class Clock(threading.Thread):
  def __init__(self, timeformat):
    super(Clock, self).__init__()
    self._stop = threading.Event()
    self.timeformat = timeformat

  def run(self):
    while True:
      if self.stopped():
        break

      print datetime.datetime.now().strftime(self.timeformat).decode('string_escape')
      time.sleep(1)

  def stop(self):
    self._stop.set()

  def stopped(self):
    return self._stop.isSet()
