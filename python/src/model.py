# -*- coding: utf8 -*-
from datetime import timedelta

class User(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def pretty_print(self):
        print "User %s (%s) joined %s" % (self.user_id, self.status, self.join_date)
        print "Bookings %s (£%s)" % (self.bookings, self.revenue)
        print "Insurance Group: %s" % (self.insurance_group)
    
    def __eq__(self, user):
        return self.user_id == user.user_id

class UserCollection(list):
    def _filter(self, cond):
        users = UserCollection()
        for user in self:
            if cond(user):
                users.append(user)
        return users

    def find_with_booking(self):
        return self._filter(lambda user: user.bookings)
    
    def find_with_no_booking(self):
        return self._filter(lambda user: not user.bookings)
    
    def find_with_monthly_rate(self):
        return self._filter(lambda user: user.monthly_rate != None)

    def find_by_reg_date(self, reg_date, delta):
        return self._filter(lambda user: abs(reg_date - user.reg_date) < delta)

    def find_by_insurance_group(self, insurance_group, delta):
        return self._filter(lambda user: abs(int(user.insurance_group) - int(insurance_group)) < delta)
    
    def find_by_car_type(self, car_type):
        return self._filter(lambda user: user.type == car_type)
    
    def find_by_engine_cc(self, engine_cc, slop=300):
        return self._filter(lambda user: abs(int(user.engine_cc) - int(engine_cc)) < slop)

    def find_by_engine_co2(self, engine_co2, slop=30):
        return self._filter(lambda user: abs(int(user.engine_co2) - int(engine_co2)) < slop)

    def get_field(self, name):
        return [getattr(user, name) for user in self]