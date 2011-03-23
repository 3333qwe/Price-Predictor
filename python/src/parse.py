import csv
import re
import os.path
from model import User, UserCollection
from datetime import datetime, timedelta

base_path = os.path.split(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])[0]

def parse_csv(filename):
    path   = os.path.join(base_path, "data", filename)
    reader = csv.reader(open(path))
    
    first = True
    users = UserCollection()
    for row in reader:
        if first:
            first = False
            continue
        fields = {}
        fields['user_id']          = row[0]
        fields['status']           = row[1]
        fields['join_date']        = datetime.strptime(row[2], "%d/%m/%y")
        fields['bookings']         = int(row[3])
        fields['revenue']          = float(row[4])
        fields['location']         = row[5].lower()
        fields['reg_date']         = datetime.strptime(row[6], "%d/%m/%y")
        fields['manufacture_date'] = datetime.strptime(row[7], "%d/%m/%y")
        fields['make']             = row[8]
        fields['model']            = row[9]
        fields['colour']           = row[10]
        fields['type'], fields['doors']  = _parse_type(row[11], row[12])
        fields['seats']            = _parse_seats(row[13])
        fields['engine_cc']        = _parse_engine_cc(row[14])
        fields['engine_co2']       = _parse_engine_co2(row[15])
        fields['fuel']             = _parse_fuel(row[16])
        fields['transmission']     = _parse_transmission(row[17])
        fields['insurance_group']  = row[18]
        fields['hourly_rate']      = _parse_rate(row[19])
        fields['daily_rate']       = _parse_rate(row[20])
        fields['weekly_rate']      = _parse_rate(row[21])
        fields['monthly_rate']     = _parse_rate(row[22])
        fields['has_photos']       = row[23].lower() == "yes"

        users.append(User(**fields))

    return users

def _parse_type(v1, v2):
    v1 = v1.lower()
    v2 = v2.lower()
    match   = re.search("(hatchback|mpv|estate|saloon|convertible|coupe)", v1)
    cartype = v2
    if match:
        cartype = "%s.%s" % (cartype, match.group(1))
    match = re.search("(\d) door", v1)
    doors = match and match.group(1) or None

    return cartype, doors

def _parse_seats(value):
    match = re.search("(\d+)(?: seats?)", value.lower())
    if match:
        return int(match.group(1))
    else:
        if value == "five comfortably":
            return 5
        elif not value:
            return None
        else:
            return int(value)

def _parse_engine_cc(value):
    try:
        return int(value)
    except ValueError:
        match = re.search("(\d+(?:\.\d+)) litres?", value)
        if match:
            return int(float(match.group(1)) * 1000)
        else:
            return None

def _parse_engine_co2(value):
    return int(value)

def _parse_fuel(value):
    value = value.lower()
    return value in ["heavy-oil"] and "diesel" or value

def _parse_transmission(value):
    if not value:
        return None
    else:
        value = value.lower()
        if value in ["automatic", "cvt", "manual"]:
            return value
        elif "tiptronic" in value:
            return "automatic.tiptronic"
        else:
            return "unknown"

def _parse_rate(value):
    return value and int(value) or None