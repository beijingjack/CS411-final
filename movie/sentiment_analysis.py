import numpy as np
#import nltk
import torch
from django.core.cache import cache
import os
from .BOW_model import BOW_model


# word2id = np.load('imdb_dictionary_w2id.npy')
def predict_sentiment(comment):
    model_cache_key = 'model_cache'
    model_rel_path = "movie/machine_learning_model/model_cache/BOW_model.pt"
    model = cache.get(model_cache_key)

    if model is None:
        model_path = os.path.realpath(model_rel_path)
        model = BOW_model(8000,500)
        model.cuda()
        model.load_state_dict(torch.load(model_path))
        #save in django memory cache
        cache.set(model_cache_key, model, None)


    # model.cuda()

    pred = model(comment)
    pred = pred.data.item()
    if pred > 0:
        prediction = 1
    else:
        prediction = -1

    return prediction
