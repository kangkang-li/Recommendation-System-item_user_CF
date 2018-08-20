# Xuehai Wu
# different similiarity function analysis for ItemCF
# training data-set are seperated by 30%, 50%, 70% and 100%
# 3 different similiarity function are consider regular-mehtod, consine-based mehtod and IUF mehtod
# method choosing described in code

import time

# import random

import math
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
        user, movie, rating, timestamp =  line.split(',')
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

class ItemBasedCF():
    def __init__(self):
        self.n_sim_movie = 20
        self.n_rec_movie = 10

        self.trainSet = {}
        self.testSet = {}

        self.movie_sim_matrix = {}
        self.movie_popular = {}
        self.movie_count = 0

    def calc_movie_sim(self):
        for user, movies in self.trainSet.items():
            for movie in movies:
                if movie not in self.movie_popular:
                    self.movie_popular[movie] = 0
                #self.movie_popular[movie] += 1 # for regular mehtod and consine-based method
                self.movie_popular[movie] += 1/math.log(1+len(movies)*1.0) # for IUF method
        self.movie_count = len(self.movie_popular)
        print("Total movie number = %d" % self.movie_count)

        for user, movies in self.trainSet.items():
            for m1 in movies:
                for m2 in movies:
                    if m1 == m2:
                        continue
                    self.movie_sim_matrix.setdefault(m1, {})
                    self.movie_sim_matrix[m1].setdefault(m2, 0)
                    self.movie_sim_matrix[m1][m2] += 1/math.log(1+len(movies)*1.0)
        # print("Build co-rated users matrix success!")

        # print("Calculating movie similarity matrix ...")
        for m1, related_movies in self.movie_sim_matrix.items():
            for m2, count in related_movies.items():
                if self.movie_popular[m1] == 0 or self.movie_popular[m2] == 0:
                    self.movie_sim_matrix[m1][m2] = 0
                else:
                    self.movie_sim_matrix[m1][m2] = count / math.sqrt(self.movie_popular[m1] * self.movie_popular[m2]) # for IUF mehtod and consine-based method
                    #self.movie_sim_matrix[m1][m2] = count / float(self.movie_popular[m1]) # for regular method

        # print('Calculate movie similarity matrix success!')


    def recommend(self, user):
        M = self.n_sim_movie
        K = self.n_rec_movie
        rank = {}
        watched_movies = self.trainSet[user]

        for movie, rating in watched_movies.items():
            for related_movie, w in sorted(self.movie_sim_matrix[movie].items(), key=itemgetter(1), reverse=True)[:M]:
                if related_movie in watched_movies:
                    continue
                rank.setdefault(related_movie, 0)
                rank[related_movie] += w * float(rating)
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[:K]


    def evaluate(self):
        # print('Evaluating start ...')
        N = self.n_rec_movie
        hit = 0
        rec_count = 0
        test_count = 0
        all_rec_movies = set()

        for i, user in enumerate(self.trainSet):
            test_moives = self.testSet.get(user, {})
            rec_movies = self.recommend(user)
            for movie, w in rec_movies:
                if movie in test_moives:
                    hit += 1
                all_rec_movies.add(movie)
            rec_count += N
            test_count += len(test_moives)

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

        itemCF = ItemBasedCF()
        sourceData=load_file(rating_file)

        itemCF.trainSet, itemCF.testSet=get_dataset(sourceData,sizeSpliter=dataRatio)
    
        time0=time.clock()
        itemCF.calc_movie_sim()
        time1=time.clock()
        result.append(itemCF.evaluate())
        time2=time.clock()
        print('time1=',time1-time0)
        print('time2=',time2-time1)
        result.append([time1-time0,time2-time1])
allResult.append(result)

