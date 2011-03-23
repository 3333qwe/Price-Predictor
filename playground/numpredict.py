from random import random, randint
import math

def wineprice(rating, age):
    peak_age = rating - 50
    price    = rating / 2
    if age > peak_age:
        price *= 5-(age-peak_age)
    else:
        price *= 5*((age + 1) / peak_age)
    if price < 0:
        price = 0.0
    return price

def wineset1():
    rows = []
    for i in range(500):
        rating = random() * 40 + 60
        age    = random() * 50
        
        price  = wineprice(rating, age)
        price *= random() * 0.4 + 0.8
        
        rows.append({"input":(rating, age), "result":price})
    return rows

def wineprice2(rating, age, size):
    return wineprice(rating, age) * (size / 750) * (random() * 0.9 + 0.2)

def wineset2(size=500):
    rows = []
    for i in range(size):
        rating = random() * 40 + 60
        age    = random() * 50
        aisle  = float(randint(1, 20))
        size   = [375.0, 750.0, 1500.0, 3000.0][randint(0, 3)]
        price  = wineprice2(rating, age, size)
        rows.append({'input':(rating, age, aisle, size), 'result':price})
    return rows

def euclidean(v1, v2):
    d = 0.0
    for i in range(len(v1)):
        d += (v1[i] - v2[i]) ** 2
    return math.sqrt(d)

def getdistances(data, vec1):
    distancelist = []
    for i in range(len(data)):
        vec2 = data[i]['input']
        distancelist.append((euclidean(vec1, vec2), i))
    distancelist.sort()
    return distancelist

def knnestimate(data, vec1, k=5):
    dlist = getdistances(data, vec1)
    
    return sum([data[dist[1]]['result'] for dist in dlist[:k]]) / k

def inverseweight(dist, num=1.0, const=0.1):
    return num / (dist + const)

def gaussianweight(dist, sigma=10.0):
    return math.exp(-dist**2 / (2 * sigma**2))
    return (1/math.sqrt(2*math.pi*sigma)) * math.exp(-0.5 * (dist/sigma) ** 2)

def weightedknn(data, vec1, k=5, weightf=gaussianweight):
    dlist   = getdistances(data, vec1)[:k]
    
    avg = total = 0.0
    for dist, i in dlist:
        weight =  weightf(dist)
        avg    += weight * data[i]['result']
        total  += weight
    return avg / total

def dividedata(data, test=0.05):
    trainset = []
    testset  = []
    for row in data:
        if random() < test:
            testset.append(row)
        else:
            trainset.append(row)
    return trainset, testset

def testalgorithm(algf, trainset, testset):
    error = 0.0
    for row in testset:
        guess  = algf(trainset, row['input'])
        error += (row['result'] - guess) ** 2
    return error/len(testset)

def crossvalidate(algf, data, trials=100, test=0.05):
    error = 0.0
    for i in range(trials):
        trainset, testset = dividedata(data, test)
        error += testalgorithm(algf, trainset, testset)
    return error / trials

def crossinvestigate(algf, data, trials=100, test=0.05):
    results = []
    for i in range(trials):
        trainset, testset = dividedata(data, test)
        results.append(testalgorithm(algf, trainset, testset))

    mean = sum(results) / trials
    minv = min(results)
    maxv = max(results)
    var  = maxv - minv
    return mean, minv, maxv, var

def rescale(data, scale):
    l = range(len(scale))
    scaledata = []
    for row in data:
        scaled = [scale[i]*row['input'][i] for i in l]
        scaledata.append({'input':scaled, 'result':row['result']})
    return scaledata

def createcostfunction(algf, data):
    return lambda scale: crossvalidate(algf, rescale(data, scale), trials=10)

def createknnestimate(k):
    def func(data, vec1):
        return knnestimate(data, vec1, k=k)
    return func

def createweightedknn(k, sigma):
    def func(data, vec1):
        return weightedknn(data, vec1, k=k, weightf=lambda dist: gaussianweight(dist, sigma=sigma))
    return func

weightdomain = [(0,20)] * 4

algos = []
for i in [3, 5, 7, 9]:
    algos.append(("knne%s" % i, createknnestimate(i)))


for i in [3, 5, 7, 9]:
    for j in [4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0]:
        algos.append(("knnw%s|%s" % (i, j), createweightedknn(i, j)))