from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from . import training_data_set


vectorizer = None
classifier = None
is_trained = False


def train():
    global vectorizer, classifier

    x = training_data_set.data_frame.body
    y = training_data_set.data_frame.class_num

    x_train, x_test, y_train, y_test = train_test_split(x, y)

    vectorizer = CountVectorizer()
    counts = vectorizer.fit_transform(x_train.values)

    classifier = MultinomialNB()
    targets = y_train.values.astype('int')
    classifier.fit(counts, targets)


def is_spam(body: str):
    example_count = vectorizer.transform([body])
    predictions = classifier.predict_proba(example_count)
    return predictions[0]