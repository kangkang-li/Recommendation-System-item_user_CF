from src.UserCF import userCF_Test
from src.ItemCF import itemCF_Test
from src.LoadData import *

# print(int(3/2))
itemCutterS=[1,2,4,8,12,16,20,24]
userCutterS=[1,2,4,8,12,16,20,24]
# itemCutterS=[2,4]
# userCutterS=[2,4]
timeTrainS=[0]*len(itemCutterS)
timeTestS=[0]*len(itemCutterS)
itemCounterS=[0]*len(itemCutterS)
userCounterS=[0]*len(itemCutterS)
sourceData=load_file('ratings.dat')
counter=0

for itemCutter in itemCutterS:
	# time1,time2=
	timeTrainS[counter],timeTestS[counter],itemCounterS[counter],userCounterS[counter]=itemCF_Test(sourceData,itemCutter,1)
	counter+=1
print(timeTrainS)
print(timeTestS)
print(itemCounterS)
print(userCounterS)

counter=0
for userCutter in userCutterS:
	# time1,time2=
	timeTrainS[counter],timeTestS[counter],itemCounterS[counter],userCounterS[counter]=itemCF_Test(sourceData,1,userCutter)
	counter+=1
print(timeTrainS)
print(timeTestS)
print(itemCounterS)
print(userCounterS)


for itemCutter in itemCutterS:
	# time1,time2=
	timeTrainS[counter],timeTestS[counter],itemCounterS[counter],userCounterS[counter]=userCF_Test(sourceData,itemCutter,1)
	counter+=1
print(timeTrainS)
print(timeTestS)
print(itemCounterS)
print(userCounterS)

counter=0
for userCutter in userCutterS:
	# time1,time2=
	timeTrainS[counter],timeTestS[counter],itemCounterS[counter],userCounterS[counter]=userCF_Test(sourceData,1,userCutter)
	counter+=1
print(timeTrainS)
print(timeTestS)
print(itemCounterS)
print(userCounterS)

