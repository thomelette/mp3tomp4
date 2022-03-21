# TimeHelper.py
#
# helper class for time (num seconds) handling

import datetime

class TimeHelper:

    curr_s = 0
    StartTime = datetime.datetime.now().strftime("%y%m%d-%H%M%S")

    def __init__(self):
        self.curr_s = 0
        #self.start_time = datetime.datetime.now().strftime("%y%m%d-%H%M%S")

    #def StartTime(self):
    #    return str(self.start_time)


    def GetTimeMinutes(self):
        return (self.curr_s / 60.0)

    def ResetTimer(self):
        self.curr_s = 0
    
    def IncrementTimer(self, num_s):
        self.curr_s += num_s

    def ToString(self):
        hours, rem = divmod(self.curr_s, 3600)
        minutes, seconds = divmod(rem, 60)

        return "{:02}:{:02}:{:02}".format(
                int(hours),
                int(minutes),
                int(seconds)
        )

    def __str__(self):
        return self.ToString()