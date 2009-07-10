#!/usr/bin/env python

import time

class Timers:
    class Timer:
        def __init__(self, timeout=None, method=None, args=None):
            self.timeout   = timeout
            self.method    = method
            if type(args) == tuple:
                self.arguments = args
            else:
                self.arguments = (args,)
        def extend(self, delay): self.timeout += delay
        def get_timeleft(self): return self.timeout - time.time()
        def remove(self): self.method = None
        def __cmp__(self, other): return self.timeout - other.timeout
        def __repr__(self): return '<Timer "%d">' % self.timeout
        time_left = property(get_timeleft)

    def __init__(self):
        self._timers = []

    def add_timer(self, delay, method, args=()):
        timer = self.Timer(time.time() + delay, method, args)
        self._timers.append(timer)
        self._timers.sort()
        return timer

    def remove_timer(self, timer):
        self._timers.remove(timer)

    def extend_timer(self, timer, delay):
        self._timers[timer].extend(delay)

    def process_timeout(self):
        while self._timers:
            if time.time() >= self._timers[0].timeout:
                if self._timers[0].method != None:
                    self._timers[0].method(*self._timers[0].arguments)
                del self._timers[0]
            else:
                break