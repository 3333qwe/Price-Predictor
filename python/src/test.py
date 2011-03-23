from parse import parse_csv
from predict import RegDatePredictor, InsuranceGroupPredictor, RegDateInsPredictor, AllPredictor, TypePredictor, EngineCCPredictor, EngineCO2Predictor, EngineBothPredictor
import math

users      = parse_csv("anonwhipdata.csv")
predictors = [p(users) for p in [RegDatePredictor, InsuranceGroupPredictor, RegDateInsPredictor, AllPredictor, TypePredictor, EngineCCPredictor, EngineCO2Predictor, EngineBothPredictor]]
sqdiffs    = [0] * len(predictors)
matches    = [0] * len(predictors)
sqcounts   = [0] * len(predictors)

for user in users:
    if user.monthly_rate:
        for i, predictor in enumerate(predictors):
            result      = predictor.predict(user)
            if result:
                difference  = user.monthly_rate - result.price
                sqdiffs[i]  += difference ** 2
                sqcounts[i] += 1
                matches[i]  += result.matches

for i, predictor in enumerate(predictors):
    print "%- 25s %0.2f % 5s" % (predictor.__class__.__name__, math.sqrt(sqdiffs[i] / sqcounts[i]), matches[i] / sqcounts[i])
