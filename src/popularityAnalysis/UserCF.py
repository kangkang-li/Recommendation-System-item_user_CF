# Xuehai Wu
# different similiarity function analysis for UserCF
# training data-set are seperated by 30%, 50%, 70% and 100%
# 3 different similiarity function are consider regular-mehtod, consine-based mehtod and IUF mehtod
# method choosing described in code

import math
import time
from operator import itemgetter
import random

def load_file(filename):
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if i == 0:  # remove title line
                continue
            yield line.strip('\r\n')
    # print('Load %s success!' % filename)


def get_dataset(sourceData, sizeSpliter=1,trainTestSpliter=0.75,userCutter=1):
    trainSet_len = 0
    testSet_len = 0
    trainSet={}
    testSet={}
    pivot1=1-trainTestSpliter
    pivot2=pivot1+(trainTestSpliter*sizeSpliter)
    for line in sourceData:
        user, movie, rating, timestamp = line.split(',')
        # user=int(user/userCutter)
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
    return trainSet,testSet
class UserBasedCF():
    def __init__(self):
        self.n_sim_user = 20
        self.n_rec_movie = 10

        self.trainSet = {}
        self.testSet = {}

        self.user_sim_matrix = {}
        self.movie_count = 0

        print('Similar user number = %d' % self.n_sim_user)
        print('Recommneded movie number = %d' % self.n_rec_movie)


    def calc_user_sim(self):
        # key = movieID, value = list of userIDs who have seen this movie
        print('Building movie-user table ...')
        movie_user = {}
        for user, movies in self.trainSet.items():
            for movie in movies:
                if movie not in movie_user:
                    movie_user[movie] = set()
                movie_user[movie].add(user)
        print('Build movie-user table success!')

        self.movie_count = len(movie_user)
        print('Total movie number = %d' % self.movie_count)

        print('Build user co-rated movies matrix ...')
        for movie, users in movie_user.items():
            for u in users:
                for v in users:
                    if u == v:
                        continue
                    self.user_sim_matrix.setdefault(u, {})
                    self.user_sim_matrix[u].setdefault(v, 0)
                    self.user_sim_matrix[u][v] += 1/math.log(1+len(users)*1.0) # for IUF method
                    #self.user_sim_matrix[u][v] += 1 # for regular mehtod and consine-based method
        print('Build user co-rated movies matrix success!')

        print('Calculating user similarity matrix ...')
        for u, related_users in self.user_sim_matrix.items():
            for v, count in related_users.items():
                self.user_sim_matrix[u][v] = count / math.sqrt(len(self.trainSet[u]) * len(self.trainSet[v])) # for IUF mehtod and consine-based method
                #self.user_sim_matrix[u][v] = count/float(len(self.trainSet[u])) # for regular method

        print('Calculate user similarity matrix success!')


    def recommend(self, user):
        K = self.n_sim_user
        N = self.n_rec_movie
        rank = {}
        watched_movies = self.trainSet[user]

        # v=similar user, wuv=similar factor
        for v, wuv in sorted(self.user_sim_matrix[user].items(), key=itemgetter(1), reverse=True)[0:K]:
            for movie in self.trainSet[v]:
                if movie in watched_movies:
                    continue
                rank.setdefault(movie, 0)
                rank[movie] += wuv
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]

    def evaluate(self):
        print("Evaluation start ...")
        N = self.n_rec_movie
        hit = 0
        rec_count = 0
        test_count = 0
        all_rec_movies = set()

        for i, user, in enumerate(self.trainSet):
            test_movies = self.testSet.get(user, {})
            rec_movies = self.recommend(user)
            for movie, w in rec_movies:
                if movie in test_movies:
                    hit += 1
                all_rec_movies.add(movie)
            rec_count += N
            test_count += len(test_movies)

        precision = hit / (1.0 * rec_count)
        recall = hit / (1.0 * test_count)
        coverage = len(all_rec_movies) / (1.0 * self.movie_count)
        print('precisioin=%.4f\trecall=%.4f\tcoverage=%.4f' % (precision, recall, coverage))
        return [precision, recall, coverage]


rating_file = 'E:\\OneDrive\\rutgers\\courses\\DATA STRUCT ALGS 01 Sp18\\project\\RecSys_573_code\\ratings.csv'

allResult=[]
result=[]
for dataRatio in [0.3,0.5,0.7,1.0]:
    for i in range(5):

        userCF = UserBasedCF()
        sourceData=load_file(rating_file)

        userCF.trainSet, userCF.testSet=get_dataset(sourceData,sizeSpliter=dataRatio)
    
        time0=time.clock()
        userCF.calc_user_sim()
        time1=time.clock()
        result.append(userCF.evaluate())
        time2=time.clock()
        print('time1=',time1-time0)
        print('time2=',time2-time1)
        result.append([time1-time0,time2-time1])
allResult.append(result)



