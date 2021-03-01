# built in libraries
import time


class Timer:
    def __init__(self, time_corruption=0):
        """
        Makes a Timer Object
        :param time_corruption: float: value that will replace the corrupted lap value
        """
        self._time_corruption = time_corruption
        self._lap = time.perf_counter()

    def lap(self):
        """
        Gets time difference from last lap.
        :return: float
        """
        current_time = time.perf_counter()
        ret = current_time - self._lap
        if abs(ret) != ret:
            ret = self._time_corruption
        self._lap = current_time
        return ret

    def offset_sleep(self, sleep_time):
        """
        Will sleep the thread for a length of time based of the lap time.
        :param sleep_time: float
        :return: float
        """
        ran_time = time.perf_counter() - self._lap
        while sleep_time - (time.perf_counter() - self._lap) > 0:
            if sleep_time - (time.perf_counter() - self._lap) > 0.002:
                time.sleep(0.00001)
        total_time = time.perf_counter() - self._lap
        self.lap()
        return ran_time, total_time


class TickRateTracker:
    def __init__(self, frame=1):
        """
        Makes a TickRateTracker Object
        :param frame: int
        """
        self._frame = frame
        self._ticks = []

    def tick(self):
        """
        info: will add a tick
        :return:
        """
        tick = time.perf_counter()
        self._ticks.append(tick)
        while tick - self._ticks[0] > self._frame:
            self._ticks.pop(0)

    def tick_rate(self):
        """
        info: will get tick rate
        :return: int
        """
        return len(self._ticks)
