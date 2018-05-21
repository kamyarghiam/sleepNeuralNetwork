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

	w111 = random.random()
	w112 = random.random()
	w113 = random.random()
	w114 = random.random()
	node1 = np.array([w111,w112,w113,w114])

	w121 = random.random()
	w122 = random.random()
	w123 = random.random()
	w124 = random.random()
	node2 = np.array([w121,w122,w123,w124])

	w131 = random.random()
	w132 = random.random()
	w133 = random.random()
	w134 = random.random()
	node3 = np.array([w131,w132,w133,w134])

	w141 = random.random()
	w142 = random.random()
	w143 = random.random()
	w144 = random.random()
	node4 = np.array([w141,w142,w143,w144])

	#hidden layer weights
	w21 = random.random()
	w22 = random.random()
	w23 = random.random()
	w24 = random.random()
	#vertical array 4x1
	hiddenLayerArray = np.array([w21,w22,w23,w24]).T	


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
		node1 = np.dot(self.inputArray,sleepNeuralNet.node1)
		node2 = np.dot(self.inputArray,sleepNeuralNet.node2)
		node3 = np.dot(self.inputArray,sleepNeuralNet.node3)
		node4 = np.dot(self.inputArray,sleepNeuralNet.node4)

		#apply sigmoid function to get value between 0 and 1
		node1 = sleepNeuralNet.sigmoid(node1)
		node2 = sleepNeuralNet.sigmoid(node2)
		node3 = sleepNeuralNet.sigmoid(node3)
		node4 = sleepNeuralNet.sigmoid(node4)

		return np.array([node1,node2,node3,node4])

	def getOutput(self):
		self.hiddenLayerNodes = self.getHiddenLayer()
		self.sum = np.dot(self.hiddenLayerNodes, sleepNeuralNet.hiddenLayerArray)
		result = sleepNeuralNet.sigmoid(self.sum)
		print("guess: %0.2f" % result)
		print("actual:", self.quality)
		return result

	#derivative of sigmoid, where the input x is actually sigmoid(x)
	@staticmethod
	def derSigmoid(x):
		return (1- x)*x

	@staticmethod
	def reformatWeights():
		sleepNeuralNet.hiddenLayerArray = np.array([sleepNeuralNet.w21,sleepNeuralNet.w22,sleepNeuralNet.w23,sleepNeuralNet.w24]).T
		sleepNeuralNet.node1 = np.array([sleepNeuralNet.w111,sleepNeuralNet.w112,sleepNeuralNet.w113,sleepNeuralNet.w114])
		sleepNeuralNet.node2 = np.array([sleepNeuralNet.w121,sleepNeuralNet.w122,sleepNeuralNet.w123,sleepNeuralNet.w124])
		sleepNeuralNet.node3 = np.array([sleepNeuralNet.w131,sleepNeuralNet.w132,sleepNeuralNet.w133,sleepNeuralNet.w134])
		sleepNeuralNet.node4 = np.array([sleepNeuralNet.w141,sleepNeuralNet.w142,sleepNeuralNet.w143,sleepNeuralNet.w144])

	def train(self):
		guess = self.getOutput()
		actual = self.quality
		

		margin = actual - guess

		#find the direction and amount the sum needs to change
		correctSum = (margin/(sleepNeuralNet.derSigmoid(guess))) + self.sum 
		#this is how much sum needs to change by 
		delta = correctSum-self.sum

		deltaNodes = delta/self.hiddenLayerNodes
		#changes second class of weights
		sleepNeuralNet.w21 += deltaNodes[0]
		sleepNeuralNet.w22 += deltaNodes[1]
		sleepNeuralNet.w23 += deltaNodes[2]
		sleepNeuralNet.w24 += deltaNodes[3]

		#now we change the first class of weights 
		deltaHidden = (delta/sleepNeuralNet.hiddenLayerArray.T)*sleepNeuralNet.derSigmoid(self.hiddenLayerNodes)
		#print(deltaHidden.T)
		input4x1 = self.inputArray.reshape(4,1)
		deltaHidden = deltaHidden.reshape(1,4)

		deltaClassOneWeights = deltaHidden/input4x1
		#adjust weights
		sleepNeuralNet.w111 += deltaClassOneWeights[0][0]
		sleepNeuralNet.w112 += deltaClassOneWeights[0][1]
		sleepNeuralNet.w113 += deltaClassOneWeights[0][2]
		sleepNeuralNet.w114 += deltaClassOneWeights[0][3]
		sleepNeuralNet.w122 += deltaClassOneWeights[1][0]
		sleepNeuralNet.w123 += deltaClassOneWeights[1][1]
		sleepNeuralNet.w124 += deltaClassOneWeights[1][2]
		sleepNeuralNet.w131 += deltaClassOneWeights[1][3]
		sleepNeuralNet.w132 += deltaClassOneWeights[2][0]
		sleepNeuralNet.w121 += deltaClassOneWeights[2][1]
		sleepNeuralNet.w133 += deltaClassOneWeights[2][2]
		sleepNeuralNet.w134 += deltaClassOneWeights[2][3]
		sleepNeuralNet.w141 += deltaClassOneWeights[3][0]
		sleepNeuralNet.w142 += deltaClassOneWeights[3][1]
		sleepNeuralNet.w143 += deltaClassOneWeights[3][2]
		sleepNeuralNet.w144 += deltaClassOneWeights[3][3]

		sleepNeuralNet.reformatWeights()
		print(sleepNeuralNet.node1, sleepNeuralNet.node2, sleepNeuralNet.node3, sleepNeuralNet.node4)

def main():
	data = (sleepData("sleep.csv")).info
	for i in range(100):
		this = sleepNeuralNet(data[i])
		this.train()
	

main()

