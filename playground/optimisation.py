import time, random, math

people      = [('Hannah', 'BOS'), ('Leila', 'DAL'), ('Mum & Dad', 'CAK'), ('Rob', 'MIA'), ('Buddy', 'ORD'), ('Les', 'OMA')]
destination = 'LGA'

flights     = {}
for origin, dest, depart, arrive, price in [line.strip().split(',') for line in file('schedule.txt')]:
    flights.setdefault((origin, dest), []).append((depart, arrive, int(price)))

def getminutes(t):
    x = time.strptime(t, '%H:%M')
    return x[3] * 60 + x[4]

def printschedule(r):
    for d in range(0, len(r)/2):
        name   = people[d][0]
        origin = people[d][1]
        out    = flights[(origin, destination)][r[2*d]]
        ret    = flights[(origin, destination)][r[2*d+1]]
        print "%10s%10s %5s-%5s $%3s %5s-%5s $%3s" % (name, origin, out[0], out[1], out[2], ret[0], ret[1], ret[2])

def schedulecost(sol):
    totalprice    = 0
    latestarrival = 0
    earliestdep   = 24 * 60
    
    for d in range(len(sol)/2):
        origin   = people[d][1]
        outbound = flights[(origin, destination)][int(sol[2*d])]
        returnf  = flights[(origin, destination)][int(sol[2*d+1])]
        
        totalprice += outbound[2] + returnf[2]
        
        if latestarrival < getminutes(outbound[1]): latestarrival = getminutes(outbound[1])
        if earliestdep   > getminutes(returnf[0]):  earliestdep   = getminutes(returnf[0])
    
    totalwait = 0
    for d in range(len(sol) / 2):
        origin   = people[d][1]
        outbound = flights[(origin, destination)][int(sol[2*d])]
        returnf  = flights[(origin, destination)][int(sol[2*d+1])]
        
        totalwait += latestarrival - getminutes(outbound[1])
        totalwait += getminutes(returnf[0]) - earliestdep
    
    if latestarrival < earliestdep: totalprice += 5
    return totalprice + totalwait

def randomoptimise(domain, costf):
    best  = 999999999
    bestr = None
    for i in range(1000):
        r    = [random.randint(d[0], d[1]) for d in domain]
        cost = costf(r)
        if cost < best:
            best  = cost
            bestr = r
    return bestr

def hillclimb(domain, costf):
    sol = [random.randint(d[0], d[1]) for d in domain]
    
    while True:
        neighbors = []
        for j in range(len(domain)):
            if sol[j] > domain[j][0]:
                neighbors.append(sol[0:j] + [sol[j]-1] + sol[j+1:])
            if sol[j] < domain[j][1]:
                neighbors.append(sol[0:j] + [sol[j]+1] + sol[j+1:])
        current = costf(sol)
        best    = current
        for j in range(len(neighbors)):
            cost = costf(neighbors[j])
            if cost < best:
                best = cost
                sol  = neighbors[j]
        if best == current:
            break

    return sol

def annealingoptimise(domain, costf, T=1000.0, cool=0.95, step=1):
    vec = [float(random.randint(domain[i][0], domain[i][1])) for i in range(len(domain))]
    while T > 0.1:
        i    = random.randint(0, len(domain) - 1)
        dir  = step * (-1)**int(round(random.random()))
        vecb = vec[:]
        vecb[i] += dir
        if   vecb[i] < domain[i][0]: vecb[i] = domain[i][0]
        elif vecb[i] > domain[i][1]: vecb[i] = domain[i][1]

        ea = costf(vec)
        eb = costf(vecb)

        if eb < ea:
            vec = vecb
        else:
            p = pow(math.e, -(eb-ea)/T)
            if random.random() < p:
                vec = vecb

        T *= cool
    return vec

def geneticoptimise(domain, costf, popsize=50, step=1, mutprob=0.2, elite=0.2, maxiter=50):
    def mutate(vec):
        i = random.randint(0, len(domain)-1)
        if random.random() < 0.5 and vec[i] > domain[i][0]:
            return vec[0:i] + [vec[i] - step] + vec[i+1:]
        elif vec[i] < domain[i][1]:
            return vec[0:i] + [vec[i] + step] + vec[i+1:]
        else:
            return vec

    def crossover(r1, r2):
        i = random.randint(1, len(domain) - 2)
        return r1[0:i] + r2[i:]

    pop      = [[random.randint(d[0], d[1]) for d in domain] for _ in range(popsize)]
    topelete = int(elite * popsize)

    minscore = 99999999999
    for i in range(maxiter):
        print pop
        scores = [(costf(v), v) for v in pop]
        print "cost done"
        scores.sort()

        ranked = [v for _, v in scores]
        pop    = ranked[:topelete]

        while len(pop) < popsize:
            if random.random() < mutprob:
                new = mutate(ranked[random.randint(0, topelete)])
            else:
                new = crossover(
                        ranked[random.randint(0, topelete)],
                        ranked[random.randint(0, topelete)]
                    )
            if new not in pop:
                pop.append(new)
        print i, scores[0][1], scores[0][0]
        if scores[0][0] < minscore:
            minscore = scores[0][0]
    print "minscore: %s" % minscore
    return scores[0][1]

if __name__ == "__main__":
    domain = [(0.0,9.0)]*(len(optimisation.people)*2)
