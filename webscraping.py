#!/usr/bin/env python3


import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score

import joblib

"""
Webscraping Fake News Detector
"""

def readFile(filename):
    data = []
    with open(filename, 'r') as file:
        lines = list(file.readlines())
        title = "default title"
        body = ""
        value = "REAL"
        for i in range(len(lines)):
            if i == 0:
                lines[i] = title
            if i in range(1, len(lines) - 1):
                body += lines[i]
            if i == len(lines) - 1:
                value = lines[i]
        data.append([title, body, value])
    return data


def predictValue(filenamepac, filenamevector, data):
    pac = joblib.load(filenamepac)
    tfidf_vectorizer = joblib.load(filenamevector)

    # data has to be form [[title, text, label], [title, text, label], etc.]
    testDataDF = pd.DataFrame(data, columns=['title', 'text', 'label'])

    tfidf_test = tfidf_vectorizer.transform(testDataDF["text"])
    value = pac.predict(tfidf_test)
    confidence = pac.decision_function(tfidf_test)


    return confidence, value




def constructPickles(filename):
    dataDF = pd.read_csv(filename)

    labels = dataDF.label

    # DataFlair - Split the dataset
    x_train, x_test, y_train, y_test = train_test_split(dataDF['text'], labels, test_size=0.2, random_state=7)

    # DataFlair - Initialize a TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)

    # DataFlair - Fit and transform train set, transform test set
    tfidf_train = tfidf_vectorizer.fit_transform(x_train)
    tfidf_test = tfidf_vectorizer.transform(x_test)

    # DataFlair - Initialize a PassiveAggressiveClassifier
    pac = PassiveAggressiveClassifier(max_iter=50)
    pac.fit(tfidf_train, y_train)

    # DataFlair - Predict on the test set and calculate accuracy
    pac = joblib.load("testPickle")
    tfidf_vectorizer = joblib.load("testPickleVector")

    tfidf_test = tfidf_vectorizer.transform(x_test)

    y_pred = pac.predict(tfidf_test)
    score = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {round(score * 100, 2)}%')

    joblib.dump(pac, "testPickle")
    joblib.dump(tfidf_vectorizer, "testPickleVector")




def main():

    # Example input: "webscraping.py testData.txt -useExisting testPickle.txt testPickleVector.txt"
    args = sys.argv[1:]

    data = readFile(args[0])

    testpickle = "testPickle"
    testpicklevector = "testPickleVector"

    if len(args) > 1 and args[1] == "-createPickles":
        constructPickles(args[2])

    if len(args) > 1 and args[1] == "-useExisting":
        testpickle = args[2]
        testpicklevector = args[3]

    confidence, value = predictValue(testpickle, testpicklevector, data)

    print(f'Confidence is: {confidence}')
    print(f'Expected value is: {value}')


if __name__ == '__main__':
    main()

