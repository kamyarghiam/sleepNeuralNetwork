#Author: Kamyar Ghiam
"""
this program was created to analyze my sleep schedule 
and predict the optimal sleep time
"""

import numpy as np
import random 
import csv
import datetime 
import math 

class sleepData(object):
	#obtained from auxiliary functions
	latestSleepTime = datetime.datetime.strptime('02:07:47', '%H:%M:%S')
	earliestSleepTime = datetime.datetime.strptime('20:15:24', '%H:%M:%S')
	longestSleep = 11*60*60 + 23*60
	shortestSleep = 4*60*60 + 39*60
	sleepRange = longestSleep - shortestSleep
	earliestWakeUpTime = datetime.datetime.strptime('03:33:39', '%H:%M:%S')
	latestWakeUpTime = datetime.datetime.strptime('09:39:17', '%H:%M:%S')
	wakeUpTimeRange = (latestWakeUpTime - earliestWakeUpTime).seconds


	#subtract by three to get them on the same day
	earlyAdjTime = (earliestSleepTime - datetime.timedelta(hours = 3)).time()
	lateAdjTime = (latestSleepTime - datetime.timedelta(hours = 3)).time()
	timeRange = (latestSleepTime - earliestSleepTime).seconds

	firstDay = datetime.datetime.strptime('2015-09-17 00:25:30', '%Y-%m-%d %H:%M:%S')

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
	
	#sets how late you slept (using weight from 0 to 1)
	@staticmethod
	def bedtimeRatio(time):
		#3 hours is greater than latest sleep time
		time = datetime.datetime.strptime(str(time), '%H:%M:%S')
		timeAdj = (time - datetime.timedelta(hours = 3))
		earlyDateTime = datetime.datetime.strptime(str(sleepData.earlyAdjTime), '%H:%M:%S')

		ratio = (((timeAdj - earlyDateTime)).seconds)/sleepData.timeRange
		
		return ratio

	@staticmethod
	def qualityRatio(quality):
		quality = int(quality[:2])
		return quality/100

	#nap is defined as less than three hours of sleep
	@staticmethod
	def isNap(time):
		return datetime.datetime.strptime(time, '%H:%M') < datetime.datetime.strptime('3:00:00', '%H:%M:%S')

	@staticmethod
	def timeInBedRatio(time):
		assert(not sleepData.isNap(time))
		hours = time[:2]
		minutes = time[-2:]

		if hours[-1] == ':':
			hours = hours[:-1]

		totalSeconds = int(hours)*60*60 + int(minutes)*60

		return (totalSeconds - sleepData.shortestSleep)/(sleepData.sleepRange)

	#cyclicfunction that finds a value between and 0 and 1 to represent the day of the week
	@staticmethod
	def dayOfWeekRatio(time):
		time = datetime.datetime.strptime(str(time), '%Y-%m-%d %H:%M:%S')
		difference = time - sleepData.firstDay
		totalSeconds = (difference.days)*24*60*60 + difference.seconds
		oneWeek = 7*24*60*60

		ratio = (math.cos(((2*math.pi)/oneWeek)*totalSeconds)+1)/2

		return ratio
	

	@staticmethod
	def wakeUpTimeRatio(time):
		#3 hours is greater than latest sleep time
		time = datetime.datetime.strptime(str(time), '%H:%M:%S')
		timeAdj = (time - datetime.timedelta(hours = 0))
		ratio = (((timeAdj - sleepData.earliestWakeUpTime)).seconds)/sleepData.wakeUpTimeRange
		
		return ratio


class sleepNeuralNet(object): 
	#class attributes of weights 
	#first number is either weight 1 (between input and hidden) or weight 2 (between hidden and output)
	#second number is the hidden node # and last is the weight of the input node w.r.t. the hidden node
	random.seed(9)

	w11 = random.random()
	w12 = random.random()
	w13 = random.random()
	w14 = random.random()
	weightArray = np.array([w11,w12,w13,w14])

	#vertical array 4x1
	w2 = random.random()	


	def __init__(self, entry):
		sleepTime = datetime.datetime.strptime(entry[0], '%Y-%m-%d %H:%M:%S')
		wakeTime = datetime.datetime.strptime(entry[1], '%Y-%m-%d %H:%M:%S')
		quality = entry[2]
		timeInBed = entry[3]

		#input
		sleepTime = sleepData.bedtimeRatio(sleepTime.time())
		wakeTime = sleepData.wakeUpTimeRatio(wakeTime.time())
		timeInBed = sleepData.timeInBedRatio(timeInBed)
		dayOfWeek = sleepData.dayOfWeekRatio(entry[0])
		#output
		self.quality = sleepData.qualityRatio(quality)

		#horizontal array of inputs 
		self.inputArray = np.array([sleepTime, wakeTime, timeInBed, dayOfWeek])
	
	@staticmethod 
	def sigmoid(x):
		return 1 / (1 + math.e**(-x))


	def getHiddenLayer(self):
		hiddenNode = np.dot(self.inputArray,sleepNeuralNet.weightArray)
		#apply sigmoid function to get value between 0 and 1
		hiddenNode = sleepNeuralNet.sigmoid(hiddenNode)
		print(hiddenNode)

		return hiddenNode

	def getOutput(self):
		self.hiddenLayerNode = self.getHiddenLayer()
		self.sum = self.hiddenLayerNode*sleepNeuralNet.w2
		result = sleepNeuralNet.sigmoid(self.sum)
		print("guess: %0.2f" % result)
		print("actual:", self.quality)
		return result

	#derivative of sigmoid, where the input x is actually sigmoid(x)
	@staticmethod
	def derSigmoid(x):
		return (1- x)*x

	def train(self):
		guess = self.getOutput()
		actual = self.quality
		

		margin = actual - guess

		#find the direction and amount the sum needs to change
		correctSum = (margin/(sleepNeuralNet.derSigmoid(guess))) + self.sum 
		#this is how much sum needs to change by 
		delta = correctSum-self.sum

		deltaNodes = delta/self.hiddenLayerNode
		#changes second class of weights
		sleepNeuralNet.w2 += deltaNodes

		#now we change the first class of weights 
		deltaHidden = (delta/sleepNeuralNet.w2)*sleepNeuralNet.derSigmoid(self.hiddenLayerNode)
		input4x1 = self.inputArray.reshape(4,1)
		deltaHidden = deltaHidden

		deltaClassOneWeights = deltaHidden/input4x1
		#adjust weights
		sleepNeuralNet.w11 += deltaClassOneWeights[0][0]
		sleepNeuralNet.w12 += deltaClassOneWeights[1][0]
		sleepNeuralNet.w13 += deltaClassOneWeights[2][0]
		sleepNeuralNet.w14 += deltaClassOneWeights[3][0]


def main():
	data = (sleepData("sleep.csv")).info
	for i in range(170):
		print(i)
		if not sleepData.isNap(data[i][3]):
			this = sleepNeuralNet(data[i])
			#these are cases that throw off the learning 
			if (this.quality < .6 or i == 62):
				continue
			this.train()

main()

