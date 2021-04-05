import datetime, enum

# Light controller operates in two modes. Day Mode and Night Mode.
# Day Mode:
#   In Day Mode the light controller will close relays 1 and 3 and will open relay 2.
# Night Mode:
#   In Night Mode the light controller will open relays 1 and 3 and will close relay 2.

class Relay(enum.Enum):
    OPEN = False
    CLOSED = True

# Define Schedule
class LightControllerSchedule:
    def __init__(self,scheduleName, startTime, endTime, r1, r2, r3):
        self.scheduleName = scheduleName
        self.startTime = startTime
        self.endTime = endTime
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.currentTime = None
    
    def scheduleActive(self):
        currentTime = self.getCurrentTime()
        # Intraday schedule
        if self.startTime < self.endTime:
            if currentTime >= self.startTime and currentTime < self.endTime:
                return True
            else:
                return False
        # Interday (Overnight) schedule
        else:
            if currentTime >= self.startTime or currentTime < self.endTime:
                return True
            else:
                return False

    def getCurrentTime(self):
        if self.currentTime is None:
            self.setCurrentTime()
        return self.currentTime
            
    def setCurrentTime(self):
        currentTime = datetime.datetime.now()
        self.currentTime = int(str(currentTime.hour) + str(currentTime.minute))

# Caution, there is no protection against overlapping schedules.
# Schedules are processed in order so in the event of an overlap condition the last matching schedule will be applied.
schedules = [ LightControllerSchedule("Day Mode", 800, 1859, Relay.CLOSED, Relay.OPEN, Relay.CLOSED),
              LightControllerSchedule("Night Mode", 1900, 759, Relay.OPEN, Relay.CLOSED, Relay.OPEN)]

selectedSchedule = None
for schedule in schedules:
    print("Schedule Name:\t" + schedule.scheduleName)
    print(" Active:\t" + str(schedule.scheduleActive()))
    
    if schedule.scheduleActive():
        selectedSchedule = schedule

if selectedSchedule is not None:
    print("Selected schedule:\t" + selectedSchedule.scheduleName)
    print("Set relay 1:\t " + str(selectedSchedule.r1))
    print("Set relay 2:\t " + str(selectedSchedule.r2))
    print("Set relay 3:\t " + str(selectedSchedule.r3))
else:
    print("No schedule is active at this time.")
