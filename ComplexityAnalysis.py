# Coded by KangKang Li
# for complexity Analysis

from src.complexity.UserCF import userCF_TestU2I
from src.complexity.ItemCF import itemCF_TestU2I
from src.LoadData import *

itemCutterS=[1,2,4,8,12,16,20,24,30,36,48,72,96,144,192][::-1]
userCutterS=[2,4,8,12,16,20,24,30,36,48,72,96,144,192][::-1]
# itemCutterS=[4]
# userCutterS=[4]
timeTrainS=[0]*len(itemCutterS)
timeTestS=[0]*len(itemCutterS)
itemCounterS=[0]*len(itemCutterS)
userCounterS=[0]*len(itemCutterS)
# sourceData=load_file('ratings.dat')
sourceData=load_file('ratings.csv')
print('file loaded')
result=[itemCounterS,userCounterS,timeTrainS,timeTestS]

cutter=1
counter=0

for itemCutter in itemCutterS:
	# print(itemCutter)

	# time1,time2=
	timeTrainS[counter],timeTestS[counter],itemCounterS[counter],userCounterS[counter]=userCF_TestU2I(sourceData,itemCutter,cutter)
	counter+=1
printArrayS(result)

counter=0
for userCutter in userCutterS:
	# print(userCutter)

	# time1,time2=
	timeTrainS[counter],timeTestS[counter],itemCounterS[counter],userCounterS[counter]=userCF_TestU2I(sourceData,cutter,userCutter)
	counter+=1
printArrayS(result)



counter=0
for itemCutter in itemCutterS:
	# time1,time2=
	# print(itemCutter)
	timeTrainS[counter],timeTestS[counter],itemCounterS[counter],userCounterS[counter]=itemCF_TestU2I(sourceData,itemCutter,cutter)
	counter+=1
printArrayS(result)

counter=0
for userCutter in userCutterS:
	# time1,time2=
	timeTrainS[counter],timeTestS[counter],itemCounterS[counter],userCounterS[counter]=itemCF_TestU2I(sourceData,cutter,userCutter)
	counter+=1
printArrayS(result)

