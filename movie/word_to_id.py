import numpy as np
import os.path

def get_ids(comment):
    dic_path = os.path.realpath("movie/imdb_dictionary_w2id.npy")
    word2id = np.load(dic_path)  #### new

    comment_token_ids = [word2id.item().get(token, -1) + 1 for token in comment]  # new

    return comment_token_ids
