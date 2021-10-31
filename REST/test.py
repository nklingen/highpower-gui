from datetime import datetime

while True:
    lasthour = datetime.now() #Update the hourly timer
    hour = lasthour.strftime("%H")
