import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from . import MessageDataSet


class BayesianFilter:

    def __init__(self):
        self.vectorizer = None
        self.classifier = None
        self.is_trained = False
        self.training_data_set = MessageDataSet.get_named_set('training')
        self.vectorizer = CountVectorizer()
        self.classifier = MultinomialNB()

    def train(self):

        x = self.training_data_set.data_frame.body
        y = self.training_data_set.data_frame.class_num

        x_train, x_test, y_train, y_test = train_test_split(x, y)

        counts = self.vectorizer.fit_transform(x_train.values)

        targets = y_train.values.astype('int')
        self.classifier.fit(counts, targets)
        self.is_trained = True

    def get_spam_probability(self, body: str):
        if not self.is_trained:
            print("WARN: The filter has not been trained yet!")
        example_count = self.vectorizer.transform([body])
        predictions = self.classifier.predict_proba(example_count)
        return predictions[0]

    def is_spam(self, body: str):
        probabilities = self.get_spam_probability(body)
        spam_class = np.where(probabilities == np.amax(probabilities))[0]
        return spam_class == 1
