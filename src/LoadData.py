import random

def load_file(filename):
    a=[]
    with open(filename, 'r') as f:
        if filename[-3:]=='csv':
            f.readline()
            for line in f:
                # if i == 0:  # remove title line
                    # continue
                a.append(line.strip('\r\n').split(',')[:-1])
        # print('Load %s success!' % filename)
        elif filename[-3:]=='dat':
        # with open(filename, 'r') as f:
            for line in f:
                a.append(line.strip('\r\n').split('::')[:-1])
            # for i, line in enumerate(f):
    return a


# # 读文件，返回文件的每一行
# def load_file(filename):
#     with open(filename, 'r') as f:
#         for i, line in enumerate(f):
#             if i == 0:  # remove title line
#                 continue
#             yield line.strip('\r\n')
    # print('Load %s success!' % filename)


def get_dataset(sourceData, sizeSpliter=1,trainTestSpliter=0.75,userCutter=1,itemCutter=1):
    trainSet_len = 0
    testSet_len = 0
    trainSet={}
    testSet={}
    pivot1=1-trainTestSpliter
    pivot2=pivot1+(trainTestSpliter*sizeSpliter)
    for lineArray in sourceData:
        # lineArray=line.split(',')
        # print(lineArray)
        # user=int(int(lineArray[0])/userCutter)
        # movie=int(int(lineArray[1])/itemCutter)
        # rating=int(float(lineArray[2])*2)
        
        
        user=int(lineArray[0])
        movie=int(lineArray[1])
        rating=int(float(lineArray[2])*2)

        if user % userCutter or movie % itemCutter:
            continue
        # user, movie, rating, timestamp = []
        # print(user)
        # user=int(user/userCutter)
        # movie=int(movie/itemCutter)
        # user=int(user/itemCutter)

        rd=random.random()
        if  rd< pivot1:
            testSet.setdefault(user, {})
            testSet[user][movie] = rating
            testSet_len += 1

        elif rd<pivot2:
            trainSet.setdefault(user, {})
            trainSet[user][movie] = rating
            trainSet_len += 1
    # print('Split trainingSet and testSet success!')
    # print('TrainSet = %s' % trainSet_len)
    # print('TestSet = %s' % testSet_len)
    return trainSet,testSet,len(trainSet)

# def get_dataset(filename, sizeSpliter,movieCutter,userCutter,trainTestSpliter=0.75):
#     trainSet_len = 0
#     testSet_len = 0
#     trainSet={}
#     testSet={}
#     pivot1=sizeSpliter*trainTestSpliter
#     for line in load_file(filename):
#         user, movie, rating, timestamp = line.split(',')
#         rd=random.random()
#         if  rd< pivot1:
#             trainSet.setdefault(user, {})
#             trainSet[user][movie] = rating
#             trainSet_len += 1
#         elif rd<sizeSpliter:
#             testSet.setdefault(user, {})
#             testSet[user][movie] = rating
#             testSet_len += 1
#     # print('Split trainingSet and testSet success!')
#     # print('TrainSet = %s' % trainSet_len)
#     # print('TestSet = %s' % testSet_len)
#     return trainSet,testSet