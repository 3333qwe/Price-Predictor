import csv

reader = csv.reader(open("anonwhipdata.csv"))
doors  = []
for row in reader:
    doors.append(row[11].lower())

print filter(lambda a: "hatchback" not in a and "mpv" not in a and "estate" not in a and "saloon" not in a and "convertible" not in a and "coupe" not in a, doors)