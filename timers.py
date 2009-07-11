#!/usr/bin/env python

import time

class Timers:
    class Timer:
        def __init__(self, timeout=None, method=None, args=None):
            self.is_expired = False
            self.timeout    = timeout
            self.method     = method
            if type(args) == tuple:
                self.arguments = args
            else:
                self.arguments = (args,)

        def set_timeleft(self, time_left): self.timeout = time.time()+time_left
        def extend(self, delay): self.timeout += delay
        def get_timeleft(self): return self.timeout - time.time()
        def remove(self): self.is_expired = True
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

    def set_timeleft(self, timer, time_left):
        self._timers[timer].set_timeleft(time_left)
        self._timers.sort()

    def extend_timer(self, timer, delay):
        self._timers[timer].extend(delay)
        self._timers.sort()

    def remove_all(self):
        self._timers = []

    def get_timer(self, method):
        for timer in self._timers:
            if timer.method == method: return timer
        return None

    def process_timeout(self):
        while self._timers:
            if time.time() >= self._timers[0].timeout:
                if not self._timers[0].is_expired:
                    self._timers[0].is_expired = True
                    self._timers[0].method(*self._timers[0].arguments)
                if self._timers:
                    if self._timers[0].is_expired: del self._timers[0]
            else:
                break
