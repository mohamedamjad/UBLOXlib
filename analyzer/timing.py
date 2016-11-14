#! /usr/bin/python
import datetime


class Timing:

    def ToUnixTime(self, year, month, day, hour, min, sec):
        t = datetime.datetime(year, month, day, hour, min, sec)
        t0 = datetime.datetime(1970, 1, 1, 0, 0, 0)
        return ((t-t0).total_seconds())

    def ToGPSUnixTime(self, year, month, day, hour, min, sec, leap_seconds):
        t = datetime.datetime(year, month, day, hour, min, sec)
        t0 = datetime.datetime(1980, 1, 6, 0, 0, 0)
        print ((t - t0).total_seconds()+leap_seconds)
