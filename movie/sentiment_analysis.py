import os
from sklearn.externals import joblib
from django.core.cache import cache



def predict_sentiment(comment):
    model_cache_key = 'model_cache'
    model_rel_path = "movie/machine_learning_model/model_cache/model.pkl"
    model = cache.get(model_cache_key)

    if model is None:
        model_path = os.path.realpath(model_rel_path)
        model = joblib.load(model_path)
        #save in django memory cache
        cache.set(model_cache_key, model, None)


    pred = model.predict(comment)
    if pred >= 0.5:
        prediction = 1
    else:
        prediction = -1

    return prediction
