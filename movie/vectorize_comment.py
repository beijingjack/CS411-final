from sklearn.externals import joblib
import os.path
import re


def preprocess_comments(reviews):
    REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])")
    REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
    reviews = [REPLACE_NO_SPACE.sub("", line.lower()) for line in reviews]
    reviews = [REPLACE_WITH_SPACE.sub(" ", line) for line in reviews]

    return reviews

def get_vector(raw_comment):
    comment = [raw_comment]
    # clean comment
    comment_clean = preprocess_comments(comment)
    # vectorize comment
    dic_path = os.path.realpath("movie/vectorize.pkl")
    cv = joblib.load(dic_path)
    comment_vec = cv.transform(comment_clean)

    return comment_vec
