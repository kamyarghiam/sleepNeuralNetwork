
import csv
import datetime
class sleepData(object):
	def __init__(self, path):
		# becomes 2D list with sleep entries as elements
		self.info = []
		#each entry is made up of: start, end, sleep quality,
		#time in bed, wake up, sleep notes, heart rate, and activity

		with open(path, "rt") as file:
			reader = csv.reader(file)
			for row in reader:
				self.info.append(row)
		#gets rid of first row, which is titles
		self.info = self.info[1:]

#Auxilliary functions used before running 
def findLatestSleepTime():
	data = sleepData(("sleep.csv")).info
	mini = datetime.datetime.strptime(str(data[0][0]), '%Y-%m-%d %H:%M:%S')
	for row in data:
		#day slept and day woke up 
		date1 = datetime.datetime.strptime(str(row[0]), '%Y-%m-%d %H:%M:%S')
		date2 = datetime.datetime.strptime(str(row[1]), '%Y-%m-%d %H:%M:%S')
		timeSlept = row[3]
		#latest sleep time will be on the same day and lnoger than a nap
		if date1.date() == date2.date() and date1.time() > mini.time() and timeSlept > '3:00':
			mini = date1
	print(mini)
#latest sleep time: 2017-10-01 02:07:47

def findEarliestSleepTime():
	data = sleepData(("sleep.csv")).info
	#to find minimum, but not after midnight
	lateTime = datetime.datetime.strptime('03:00:00', '%H:%M:%S')
	mini = datetime.datetime.strptime(str(data[1][0]), '%Y-%m-%d %H:%M:%S')
	for row in data:
		date1 = datetime.datetime.strptime(str(row[0]), '%Y-%m-%d %H:%M:%S')
		timeSlept = row[3]
		if (date1.time() < mini.time()) and date1.time() > lateTime.time() and timeSlept > '3:00':
			mini = date1
	print(mini)
#earliest sleep time: 2016-09-25 20:15:24

def findLongestSleep():
	data = sleepData(("sleep.csv")).info
	maxTime = datetime.datetime.strptime(str(data[0][3]), '%H:%M')
	for row in data:
		time1 = datetime.datetime.strptime(str(row[3]), '%H:%M')
		if (time1.time() > maxTime.time()):
			maxTime = time1
	print(maxTime.time())
#longest sleep: 2017-20-26 11:23 hours

#non-nap shortest sleep
def findShortestSleep():
	data = sleepData(("sleep.csv")).info
	minTime = datetime.datetime.strptime(str(data[0][3]), '%H:%M')
	napTime = datetime.datetime.strptime('03:00', '%H:%M')
	for row in data:
		time1 = datetime.datetime.strptime(str(row[3]), '%H:%M')
		if (time1.time() < minTime.time()) and time1.time() > napTime.time():
			minTime = time1
	print(minTime.time())
#shortest non-nap sleep: 2016-05-30 4:39 hours

def findLatestWakeUpTime():
	data = sleepData(("sleep.csv")).info
	mini = datetime.datetime.strptime(str(data[0][1]), '%Y-%m-%d %H:%M:%S')
	for row in data:
		#day slept and day woke up 
		date1 = datetime.datetime.strptime(str(row[0]), '%Y-%m-%d %H:%M:%S')
		date2 = datetime.datetime.strptime(str(row[1]), '%Y-%m-%d %H:%M:%S')
		timeSlept = row[3]
		#latest sleep time will be on the same day and lnoger than a nap
		if date2.time() > mini.time() and timeSlept > '3:00':
			mini = date2
	print(mini)
#latest wake up time: 2017-09-26 09:39:17

def findEarliestWakeUpTime():
	data = sleepData(("sleep.csv")).info
	#to find minimum, but not after midnight
	lateTime = datetime.datetime.strptime('03:00:00', '%H:%M:%S')
	mini = datetime.datetime.strptime(str(data[0][1]), '%Y-%m-%d %H:%M:%S')
	for row in data:
		date1 = datetime.datetime.strptime(str(row[1]), '%Y-%m-%d %H:%M:%S')
		timeSlept = row[3]
		if (date1.time() < mini.time()) and date1.time() > lateTime.time() and timeSlept > '3:00':
			mini = date1
	print(mini)
#earliest wake up time: 2016-05-31 03:33:39

#findEarliestSleepTime()
#findLatestSleepTime()
#findLongestSleep()
#findShortestSleep()
#findLatestWakeUpTime()
#findEarliestWakeUpTime()