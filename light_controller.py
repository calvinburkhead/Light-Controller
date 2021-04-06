import datetime, enum, RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

# Light controller operates in two modes. Day Mode and Night Mode.
# Day Mode:
#   In Day Mode the light controller will close relays 1 and 3 and will open relay 2.
# Night Mode:
#   In Night Mode the light controller will open relays 1 and 3 and will close relay 2.

class RelayPosition(enum.Enum):
    OPEN = False
    CLOSED = True

class Relay:
    def __init__(self, name, gpioPin):
        self.name = name
        self.gpioPin = gpioPin
        GPIO.setup(self.gpioPin, GPIO.OUT)
        self.position = GPIO.input(self.gpioPin)
        

    def setRelay(self, position):
        if position.value is not self.position:
            if position is RelayPosition.OPEN:
                GPIO.output(self.gpioPin, GPIO.LOW)
            if position is RelayPosition.CLOSED:
                GPIO.output(self.gpioPin, GPIO.HIGH)

# Define Relays
# R1 controlls the red and white LED strips
# R2 controlls the blue LED strips
# R3 controlls the Fluorescent tubes

r1 = Relay("Red + White LEDs", 26)
r2 = Relay("Blue LEDs", 20)
r3 = Relay("Fluorescent Tubes", 21)

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
schedules = [ LightControllerSchedule("Day Mode", 800, 1859, RelayPosition.CLOSED, RelayPosition.OPEN, RelayPosition.CLOSED),
              LightControllerSchedule("Night Mode", 1900, 759, RelayPosition.OPEN, RelayPosition.CLOSED, RelayPosition.OPEN)]

selectedSchedule = None
for schedule in schedules:
    print("Schedule Name:\t" + schedule.scheduleName)
    print(" Active:\t" + str(schedule.scheduleActive()))
    
    if schedule.scheduleActive():
        selectedSchedule = schedule

if selectedSchedule is not None:
    print("Selected schedule:\t" + selectedSchedule.scheduleName)
    print("Set relay 1:\t " + str(selectedSchedule.r1))
    r1.setRelay(selectedSchedule.r1)
    print("Set relay 2:\t " + str(selectedSchedule.r2))
    r2.setRelay(selectedSchedule.r2)
    print("Set relay 3:\t " + str(selectedSchedule.r3))
    r3.setRelay(selectedSchedule.r3)
else:
    print("No schedule is active at this time.")
    r1.setRelay(RelayPosition.OPEN)
    r2.setRelay(RelayPosition.OPEN)
    r3.setRelay(RelayPosition.OPEN)
