from datetime import timedelta

class Predictor(object):
    def __init__(self, users):
        self.users = users
    
    def predict(self, user):
        raise NotImplementedError()

class BasicPredictor(Predictor):
    def predict(self, user):
        users = self._find_matches(user)
        if users:
            rate  = filter(None, users.get_field("monthly_rate"))
            return Result(float(sum(rate)) / len(rate), float(len(rate)))

    def _filter_matches(self, users, user):
        raise NotImplementedError()

    def _find_matches(self, user):
        users = self.users.find_with_booking()
        users = users.find_with_monthly_rate()
        users = self._filter_matches(users, user)
        if user in users: users.remove(user)

        return users

class AllPredictor(BasicPredictor):
    def _find_matches(self, user):
        users = self.users.find_with_booking()
        if user in users: users.remove(user)

        return users

class RegDatePredictor(BasicPredictor):
    def _filter_matches(self, users, user):
        return users.find_by_reg_date(user.reg_date, timedelta(days=365*2))

class InsuranceGroupPredictor(BasicPredictor):
    def _filter_matches(self, users, user):
        return users.find_by_insurance_group(user.insurance_group, 3)

class TypePredictor(BasicPredictor):
    def _filter_matches(self, users, user):
        return users.find_by_car_type(user.type)

class EngineCCPredictor(BasicPredictor):
    def _filter_matches(self, users, user):
        return users.find_by_engine_cc(user.engine_cc)

class EngineCO2Predictor(BasicPredictor):
    def _filter_matches(self, users, user):
        return users.find_by_engine_co2(user.engine_co2)

class EngineBothPredictor(BasicPredictor):
    def _filter_matches(self, users, user):
        users = users.find_by_engine_cc(user.engine_cc)
        return users.find_by_engine_co2(user.engine_co2)

class RegDateInsPredictor(BasicPredictor):
    def _filter_matches(self, users, user):
        users = users.find_by_reg_date(user.reg_date, timedelta(days=365*2))
        return users.find_by_insurance_group(user.insurance_group, 3)

class Result(object):
    def __init__(self, price, matches):
        self.price = price
        self.matches = matches