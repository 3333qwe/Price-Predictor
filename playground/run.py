import numpredict, csv, test
from datetime import datetime

sizes = [200, 400, 600, 1000, 1500]
datas = [numpredict.wineset2(size) for size in sizes]
tests = [test.Tester(data) for data in datas]

rows  = []
start = datetime.now()
for i, size in enumerate(sizes):
    rows.append([])
    for key, algf in numpredict.algos:
        row = [size, key] + list(tests[i].crossvalidate(algf))
        rows[i].append(row)
        print (datetime.now() - start), algf, "% 3s % 10s % 20s % 20s % 20s % 20s" % tuple(row)

writer = csv.writer(open("data/all-data.csv", "w+"))
for i in range(len(rows[0])):
    for j in range(len(rows)):
        writer.writerow(rows[j][i])