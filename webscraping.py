#!/usr/bin/env python3

import random
import sys
import urllib3
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd
import itertools
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

import joblib

import csv

"""
Webscraping Fake News Detector
"""

def readFile(filename):
    data = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            index = line.find(',')
            index2 = line.find(',', index + 1)
            data.append([line[0:index], line[index + 1:index2], line[index2 + 1:]])
    return data


def predictValue():
    value = 1


    return value




def constructVectorMap(grid):
    return




def main():
    args = sys.argv[1:]

    # data = readFile(args[0])

    # dataDF = pd.DataFrame(data, columns=['text', 'label'])

    # dataDF = pd.read_csv('news.csv')

    # labels = dataDF.label

    # DataFlair - Split the dataset
    # x_train, x_test, y_train, y_test = train_test_split(dataDF['text'], labels, test_size=0.2, random_state=7)

    # DataFlair - Initialize a TfidfVectorizer
    # tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)

    # DataFlair - Fit and transform train set, transform test set
    # tfidf_train = tfidf_vectorizer.fit_transform(x_train)
    # tfidf_test = tfidf_vectorizer.transform(x_test)

    # joblib.dump(tfidf_vectorizer, "testPickleVector")

    # DataFlair - Initialize a PassiveAggressiveClassifier
    # pac = PassiveAggressiveClassifier(max_iter=50)
    # pac.fit(tfidf_train, y_train)
    # DataFlair - Predict on the test set and calculate accuracy

    # pac = joblib.load("testPickle")
    # tfidf_vectorizer = joblib.load("testPickleVector")

    # tfidf_test = tfidf_vectorizer.transform(x_test)


    # y_pred = pac.predict(tfidf_test)
    # score = accuracy_score(y_test, y_pred)
    # print(f'Accuracy: {round(score * 100, 2)}%')

    # TESTING VALUE:

    pac = joblib.load("testPickle")
    tfidf_vectorizer = joblib.load("testPickleVector")

    testData = readFile(args[0])
    # data has to be form [[title, text, label], [title, text, label], etc.]
    testDataDF = pd.DataFrame(testData, columns=['title', 'text', 'label'])

    tfidf_test = tfidf_vectorizer.transform(testDataDF["text"])
    prediction = pac.predict(tfidf_test)
    accuracy_score(["FAKE"], prediction)
    pac.decision_function(tfidf_test)



    # joblib.dump(pac, "testPickle")





if __name__ == '__main__':
    main()

