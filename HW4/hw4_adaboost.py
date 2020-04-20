# -*- coding: utf-8 -*-
"""hw4_adaboost.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1B63P7MxUgeD7jFqTNx_LfhlG9ZAOk4BV
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

#Importing data from dataset
training_data = pd.read_csv('cancer_train.csv').values
test_data = pd.read_csv('cancer_test.csv').values

X = training_data[:,0:-1]
y = training_data[:,-1].reshape(-1,1)

X_test = test_data[:,0:-1]
y_test = test_data[:,-1].reshape(-1,1)

def getWeights(y_predict, w):
  misclassification = (y_predict != y)
  error = np.mean( np.average(misclassification, weights=w, axis=0))
  coeff =  0.5 * np.log((1. - error) / error)
  result = np.dot(y.flatten(), y_predict)
  w = np.dot(w, np.exp(-coeff * result))
  w = w / np.sum(w)
  return w

def error_rate_calc(y, y_predict_class):
  y_predict_class = y_predict_class.reshape(-1,1)
  misclassification = y_predict_class - y
  no_of_misclassified_samples = np.count_nonzero(misclassification)
  total_no_of_samples = len(misclassification)
  return no_of_misclassified_samples/total_no_of_samples

def Adaboost(n_weaklearners):
  w = np.ones(y.shape[0]) / y.shape[0]
  train_err = list()
  test_err = list()
  for i in range(n_weaklearners):
    dtree = DecisionTreeClassifier(criterion='gini', max_depth=1)
    dtree.fit(X, y, sample_weight=w)
    y_predict_train = dtree.predict(X)
    w = getWeights(y_predict_train, w)
    y_predict_test = dtree.predict(X_test)
    train_err.append(error_rate_calc(y, y_predict_train))
    test_err.append(error_rate_calc(y_test, y_predict_test))
  return train_err, test_err

def main():
  n_weaklearners = [25, 50, 75, 100]
  for i in n_weaklearners:
    train_err, test_err = Adaboost(i)
    plt.plot(train_err, label = 'Training')
    plt.plot(test_err, label = 'Testing')
    plt.ylabel("Error rate")
    plt.xlabel("Number of weaklearners")
    plt.title("Error rate vs Number of weak learners = " + str(i))
    plt.legend()
    plt.show()

if __name__== "__main__":
    main()