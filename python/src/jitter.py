from parse import parse_csv, base_path
import numpy as np
import matplotlib.pyplot as plt
import random
from datetime import datetime, timedelta
import os.path

img_path = os.path.join(base_path, "images")

class Jitter(object):
    def __init__(self, users):
        self.users = users

    def plot_nom_rate(self, field, func=None, filters=None):
        self.plot(NominalSeries(field, func), FloatSeries("monthly_rate"), filters=filters)

    def _title(self, name):
        return name.replace("_", " ").title().replace("Cc", "CC")

    def plot(self, x_series, y_series, filters=None):
        if filters is None:
            filters = []
        title = "%s against %s" % (self._title(x_series.name), self._title(y_series.name))
        if filters:
            title += " filtered by %s" % " and ".join(["%s is %s" % (self._title(f.name), f.args_str()) for f in filters])
        
        print "Plotting %s" % title

        fig = plt.figure(figsize=(18, 10))
        ax  = fig.add_subplot(111)

        fig.suptitle(title)

        users       = self.users.find_with_monthly_rate()
        for f in filters:
            users = getattr(users, "find_by_%s" % f.name)(*f.args, **f.kwargs)
        x_series.set_names(users)
        has_booking = users.find_with_booking()
        no_booking  = users.find_with_no_booking()

        x_data1 = x_series.values(has_booking)
        y_data1 = y_series.values(has_booking)
        ax.scatter(self.jitter(x_data1, 0.05), self.jitter(y_data1, 0.1), marker="+", color="blue")

        x_data2 = x_series.values(no_booking)
        y_data2 = y_series.values(no_booking)
        ax.scatter(self.jitter(x_data2, 0.05), self.jitter(y_data2, 0.1), marker="x", color="red")

        names    = dict(zip(x_series.names.values(), x_series.names.keys()))
        name_ids = sorted(x_series.names.values())
        plt.xticks(name_ids, [names[i] for i in name_ids])

        lookup = dict((v, []) for v in x_series.names.values())
        for i, v in enumerate(x_data1):
            lookup[v].append(y_data1[i])

        ax.scatter(*[np.array(v) for v in zip(*[(k, np.array(v).mean()) for k, v in lookup.items()])], marker="o", color="green")

        plt.xlabel(x_series.name)
        plt.ylabel(y_series.name)

        ax.grid(b=True)

        plt.savefig(os.path.join(img_path, "%s-%s%s" % (x_series.name, y_series.name, "f".join([f.name for f in filters]))))


    def jitter(self, array, jitter):
        return map(self._jitter(array, jitter), array)

    def _jitter(self, array, jitter):
        mean = array.mean() * jitter
        return lambda value: value + mean * random.random() - mean

class Series(object):
    def __init__(self, name):
        self.name = name
        self.func = lambda value: value

    def values(self, users):
        return np.array(map(self.func, users.get_field(self.name)))

class FloatSeries(Series):
    pass

class NominalSeries(Series):
    def __init__(self, name, func=None):
        super(NominalSeries, self).__init__(name)
        self.func   = func or fill_none
        self.names = None

    def set_names(self, users):
        data = super(NominalSeries, self).values(users)
        self.names = dict((value, i) for i, value in enumerate(sorted(list(set(data)))))

    def values(self, users):
        return np.array([self.names[value] for value in super(NominalSeries, self).values(users)])

def date_to_age(value):
    delta = datetime.now() - value
    if delta < timedelta(days=365):
        return "< 1 year"
    elif delta < timedelta(days=365*2):
        return "1 - 2 years"
    elif delta < timedelta(days=365*4):
        return "2 - 4 years"
    elif delta < timedelta(days=365*6):
        return "4 - 6 years"
    elif delta < timedelta(days=365*8):
        return "6 - 8 years"
    else:
        return "> 8 years"

def date_to_age_small(value):
    delta = datetime.now() - value
    if delta < timedelta(days=30):
        return "< 1 month"
    elif delta < timedelta(days=90*2 + 60):
        return "1-8 months"
    elif delta < timedelta(days=90*3):
        return "8-9 months"
    elif delta < timedelta(days=90*3 + 30):
        return "09-10 months"
    elif delta < timedelta(days=90*3 + 60):
        return "10-11 months"
    elif delta < timedelta(days=90*4):
        return "11-12 months"
    else:
        return ">12 months"


def fill_none(value):
    return value or "none"

def insurance_group(value):
    value = int(value)
    if value < 4:
        return "01 - 03"
    elif value < 8:
        return "04 - 07"
    elif value < 12:
        return "08 - 11"
    else:
        return "12+"

def int_slop(slop=5, bottom=0, top=900):
    def func(value):
        value = int(value)
        if value > top:
            return "%05s+" % top
        counter = bottom + slop
        while value > counter:
            counter += slop
        return "%05s - %s" % (counter - slop, counter)
    return func

class Filter(object):
    def __init__(self, name, args=None, kwargs=None):
        self.name   = name
        self.args   = [] if args is None else args
        self.kwargs = {} if kwargs is None else kwargs
    
    def args_str(self):
        out = ""
        if len(self.args) > 0:
            out += " is %s" % self.args[0]
            if len(self.args) > 1:
                out += " slop %s" % self.args[1]
        return out

def main():
    users  = parse_csv("anonwhipdata.csv")
    jitter = Jitter(users)

    jitter.plot_nom_rate("type")
    jitter.plot_nom_rate("insurance_group", insurance_group)
    jitter.plot_nom_rate("doors")
    jitter.plot_nom_rate("seats")
    jitter.plot_nom_rate("fuel", lambda value: value == "heavy oil" and "diesel" or value)
    jitter.plot_nom_rate("transmission", lambda value:  value and "automatic" in value and "automatic" or value or "None")
    jitter.plot_nom_rate("engine_cc", int_slop(slop=500, top=10000))
    jitter.plot_nom_rate("engine_co2", int_slop(slop=30))
    jitter.plot_nom_rate("has_photos")
    jitter.plot_nom_rate("reg_date", date_to_age)
    jitter.plot_nom_rate("join_date", date_to_age_small)
    jitter.plot_nom_rate("engine_cc", int_slop(slop=200, top=10000), filters=[Filter("car_type", ["car.hatchback"])])
    jitter.plot_nom_rate("engine_cc", int_slop(slop=200, top=10000), filters=[Filter("insurance_group", [10, 3])])

if __name__ == "__main__":
    main()