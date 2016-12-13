#! /usr/bin/python
import datetime


class Timing:

    def iso_ToUnixTime(self, year, month, day, hour, min, sec):
        t = datetime.datetime(year, month, day, hour, min, sec)
        t0 = datetime.datetime(1970, 1, 1, 0, 0, 0)
        return ((t-t0).total_seconds())

    def iso_ToGPSUnixTime(self, year, month, day, hour, min, sec):
        t = datetime.datetime(year, month, day, hour, min, sec)
        t0 = datetime.datetime(1980, 1, 6, 0, 0, 0)
        return float((t - t0).total_seconds()*1000)

    def weekToW_ToGPSUnixTime(self, week, tow):
        return float(86400000 * 7 * week + tow)