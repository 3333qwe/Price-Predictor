import csv
from datetime import datetime, timedelta

class User(object):
    @classmethod
    def from_list(cls, value):
        user = User()

        return user

class UserCollection(list):
    pass

reader = csv.reader(open("anonwhipdata.csv"))

users  = UserCollection()

first  = True
for row in reader:
    if first:
        first = False
    else:
        users.append(User.from_list(value))

print users[0]
print users[1]
print users[0].distance(users[1])