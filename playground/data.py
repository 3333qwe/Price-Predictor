import csv, re, decimal
from datetime import datetime, timedelta

class User(object):
    @classmethod
    def from_list(cls, value):
        user = User()
        user.set_join_date(value[2])
        user.set_bookings(value[3])
        user.set_revenue(value[4])
        user.set_location(value[5])
        user.set_reg_date(value[6])
        user.set_manufacture_date(value[7])
        user.set_make(value[8])
        user.set_model(value[9])
        user.set_colour(value[10])
        user.set_type(value[12], value[11])
        user.set_seats(value[13])
        user.set_engine_cc(value[14])
        user.set_engine_co2(value[15])
        user.set_fuel(value[16])
        user.set_gearbox(value[17])
        user.set_insurance_group(value[18])
        user.set_rates(value[19], value[20], value[21], value[22])
        user.set_has_photo(value[23])
        user.set_avg_booking_length(value[24])
        user.set_avg_booking_value(value[25])
        user.set_age(value[26])

        return user
        
    def set_join_date(self, value):
        self.join_date = datetime.strptime(value, "%d/%m/%y")
    
    def set_bookings(self, value):
        self.bookings = int(value)
    
    def set_revenue(self, value):
        self.revenue = float(value)
    
    def set_location(self, value):
        # needs more work
        self.location = value
    
    def set_reg_date(self, value):
        self.reg_date = datetime.strptime(value, "%d/%m/%y")

    def set_manufacture_date(self, value):
        self.manufacture_date = datetime.strptime(value, "%d/%m/%y")
    
    def set_make(self, value):
        self.make = value
    
    def set_model(self, value):
        self.model = value
    
    def set_colour(self, value):
        self.colour = value.lower()
        
    def set_type(self, value, subvalue):
        vtype = value.lower()
        subvalue = subvalue.lower()
        match = re.search("(hatchback|mpv|estate|saloon|convertible|coupe)", subvalue)
        if match:
            vtype = "%s.%s" % (vtype, match.group(1))
        self.type = vtype
        match = re.search("(\d) door", subvalue)
        self.doors = match and match.group(1) or None
    
    def set_seats(self, value):
        match = re.search("(\d+)(?: seats?)", value.lower())
        if match:
            self.seats = int(match.group(1))
        else:
            if value == "five comfortably":
                self.seats = 5
            elif not value:
                self.seats = None
            else:
                self.seats = int(value)
    
    def set_engine_cc(self, value):
        try:
            self.engine_cc = int(value)
        except ValueError:
            match = re.search("(\d+(?:\.\d+)) litres?", value)
            if match:
                self.engine_cc = int(float(match.group(1)) * 1000)
            else:
                self.engine_cc = None
    
    def set_engine_co2(self, value):
        self.engine_co2 = int(value)
    
    def set_fuel(self, value):
        self.fuel = value.lower()
    
    def set_gearbox(self, value):
        if not value:
            self.gearbox = None
        else:
            value = value.lower()
            if value in ["automatic", "cvt", "manual"]:
                self.gearbox = value
            elif "tiptronic" in value:
                self.gearbox = "automatic.tiptronic"
            else:
                self.gearbox = "unknown"
    
    def set_insurance_group(self, value):
        self.insurance_group = int(value)
    
    def set_rates(self, hourly, daily, weekly, monthly):
        self.rates = map(lambda x: len(x) and float(x) or None, [hourly, daily, weekly, monthly])
    
    def set_has_photo(self, value):
        self.has_photo = {"no":0, "yes":1}[value.lower()]
    
    def set_avg_booking_length(self, value):
        match  = re.search("(?:(\d+) weeks?(?:\s+and\s+)?)?(?:(\d+) days?(?:\s+and\s+)?)?(?:(\d+) hours?)?", value)
        groups = match.groups()
        if reduce(lambda x, y: y != None and y or x, groups, None) != None:
            self.avg_booking_length = timedelta(weeks=int(groups[0] or 0), days=int(groups[1] or 0), hours=int(groups[2] or 0))
        else:
            self.avg_booking_length = None
    
    def set_avg_booking_value(self, value):
        self.avg_booking_value = float(value)
    
    def set_age(self, value):
        match = re.search("(\d+) years? old", value)
        if match:
            self.age = int(match.group(1))
        else:
            print value

    def distance(self, other):
        return 0

    def _distance_nominal(self, val1, val2):
        if val1 == val2:
            return 0
        else:
            return 1

    def distance_join_date(self, other):
        return (self.join_date - other.join_date).days

    def distance_bookings(self, other):
        return self.bookings - other.bookings

    def distance_revenue(self, other):
        return self.revenue - other.revenue

    def distance_location(self, other):
        return "UNKOWN"

    def distance_reg_date(self, other):
        return (self.reg_date - other.reg_date).days

    def distance_manufacture_date(self, other):
        return (self.manufacture_date - other.manufacture_date).days

    def distance_make(self, other):
        return self._distance_nominal(self.make, other.make)

    def distance_model(self, other):
        # If make matches then term based levenshtein?
        return self._distance_nominal(self.model, other.model)

    def distance_colour(self, other):
        return self._distance_nominal(self.colour, other.colour)

    def distance_doors(self, other):
        # TODO: is this really nominal?
        return self._distance_nominal(self.doors, other.doors)

    def distance_type(self, other):
        return self._distance_nominal(self.type, other.type)

    def distance_seats(self, other):
        # TODO: is this really nominal?
        return self._distance_nominal(self.doors, other.doors)

    def distance_engine_cc(self, other):
        return self.engine_cc - other.engine_cc

    def distance_engine_co2(self, other):
        return self.engine_co2 - other.engine_co2

    def distance_fuel(self, other):
        return self._distance_nominal(self.fuel, other.fuel)

    def distance_gearbox(self, other):
        return self._distance_nominal(self.gearbox, other.gearbox)

    def distance_insurance_group(self, other):
        return self.insurance_group - other.insurance_group

    def distance_rates(self, other):
        return [self.rates[i] - other.rates[i] for i in range(len(self.rates))]

    def distance_has_photo(self, other):
        return self._distance_nominal(self.has_photo, other.has_photo)

    def distance_avg_booking_length(self, other):
        return ((self.avg_booking_length or timedelta()) - (other.avg_booking_length or timedelta())).days

    def distance_avg_booking_value(self, other):
        return self.avg_booking_value - other.avg_booking_value

    def distance_age(self, other):
        return self.age - other.age

    def __str__(self):
        return "<User %s>" % ", ".join(["%s=%s" % (key, value) for key, value in self.__dict__.items()])

class UserCollection(list):
    pass

def main():
    reader = csv.reader(open("data/anonwhipdata.csv"))
    users  = UserCollection()
    first  = True
    for row in reader:
        if first:
            first = False
        else:
            users.append(User.from_list(row))

    print users[0]
    print users[1]
    print ""
    print "Distances from user0 to user1"
    for distance in [name for name in dir(users[0]) if name.startswith("distance_")]:
        print "% 30s %s" % (distance, getattr(users[0], distance)(users[1]))
    print ""
    print "Distances from user1 to user0"
    for distance in [name for name in dir(users[0]) if name.startswith("distance_")]:
        print "% 30s %s" % (distance, getattr(users[1], distance)(users[0]))


    writer = csv.writer(open("clean-data.csv", "w+"))
    fields = [
        'join_date', 'bookings', 'revenue', 'reg_date', 'manufacture_date', 'make',
        'model', 'colour', 'type', 'doors', 'seats', 'engine_cc', 'engine_co2', 'fuel',
        'gearbox', 'insurance_group', 'has_photo', 'avg_booking_length', 'avg_booking_value'
    ]
    writer.writerow(fields + ["hourly_rate", "daily_rate", "weekly_rate", "monthly_rate"])
    for user in users:
        values = [getattr(user, name) for name in fields]
        values = [isinstance(value, datetime) and value.strftime("%Y-%m-%d") or value for value in values]
        values = [isinstance(value, timedelta) and "%s days, %s hours, %s minutes" % (value.days, value.seconds / 60 / 60, value.seconds / 60 % 60) or value for value in values]
        writer.writerow(values + user.rates)

if __name__ == "__main__":
    main()