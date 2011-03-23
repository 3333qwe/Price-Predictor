from random import random
import math

class Tester(object):
    def __init__(self, data):
        self.data = data
        self.create_test_sets()

    def create_test_sets(self, trials=100):
        self.tests  = []
        self.trials = trials
        for i in range(trials):
            self.tests.append(self._divide_data())

    def crossvalidate(self, algf):
        results = []
        for trainset, testset in self.tests:
            results.append(self._testalgorithm(algf, trainset, testset))

        mean = sum(results) / self.trials
        minv = min(results)
        maxv = max(results)
        var  = maxv - minv
        
        return mean, minv, maxv, var

    def _divide_data(self, test=0.05):
        trainset = []
        testset  = []
        for row in self.data:
            if random() < test:
                testset.append(row)
            else:
                trainset.append(row)

        return trainset, testset

    def _testalgorithm(self, algf, trainset, testset):
        error = 0.0
        for row in testset:
            guess  = algf(trainset, row['input'])
            error += (row['result'] - guess) ** 2
        return math.sqrt(error/len(testset))