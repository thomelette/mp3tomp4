# Timer.py
#
# helper class for time (number of seconds) handling

class Timer:

    curr_s = 0 # num seconds elapsed

    # constructor
    #
    def __init__(self):
        self.curr_s = 0

    # reset timer
    #
    def Reset(self):
        self.curr_s = 0

    # increment timer
    # 
    # num_s [input] - number of seconds to add
    def Increment(self, num_s):
        self.curr_s += num_s

    # get current timer status in minutes
    #
    # [return] number of minutes elapsed
    def GetMinutes(self):
        return (self.curr_s / 60.0)

    # override to string method
    #
    # [return] string representation of timer status
    def __str__(self):
        hours, rem = divmod(self.curr_s, 3600)
        minutes, seconds = divmod(rem, 60)

        return "{:02}:{:02}:{:02}".format(
                int(hours),
                int(minutes),
                int(seconds)
        )