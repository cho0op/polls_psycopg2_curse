import datetime
import pytz

eastern = pytz.timezone("Us/Eastern")
amsterdam = pytz.timezone("Europe/Amsterdam")

local_time = datetime.datetime.now(tz=pytz.utc)
#
# eastern_time = eastern.localize(local_time)


print(local_time)
# print(eastern_time)

