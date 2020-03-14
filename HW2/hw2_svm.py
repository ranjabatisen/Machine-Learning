# -*- coding: utf-8 -*-
"""hw2_svm.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SDzRPOzBk6oNInVT9W2yGsdlfu2cZcaD
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from cvxopt import matrix
from cvxopt.solvers import qp,options

#Importing data from dataset
data = pd.read_csv('hw2data.csv', header = None).values

r,col = data.shape
#Storing 80% of data as non-test data
X = data[:int(0.8*r),0:2] 
y = data[:int(0.8*r),2].reshape(int(0.8*r),1)
#Storing 20% of data as test data
X_test = data[int(0.8*r):,0:2]
y_test = data[int(0.8*r):,2].reshape(int(0.2*r),1)

#Cross validation function
def cross_validation(k):
    length = X.shape[0]
    position = np.arange(length)
    #position = [0, 1, 2, ..... length]
    #randomly shuffling the position array
    np.random.shuffle(position)
    X_shuffled = dict()
    y_shuffled = dict()
    for i in range(k):
        start_index= i * int(length/k)
        end_index= (i+1) * int(length/k)
        #Saving each of the 10 folds
        X_shuffled[i] = X[position[start_index:end_index],:]
        y_shuffled[i] = y[position[start_index:end_index],:]
    return X_shuffled, y_shuffled

#Function that takes one fold as validation data and combines the other folds to form training data
def get_next_train_valid(X_shuffled, y_shuffled, itr, k):
    X_train = np.zeros((1,X_shuffled[itr].shape[1]))
    y_train = np.zeros((1,y_shuffled[itr].shape[1]))
    for i in range(k):
        if i == itr:
            X_valid = X_shuffled[itr]
            y_valid = y_shuffled[itr]
        else:
            X_train = np.concatenate((X_train, X_shuffled[i]), axis=0)
            y_train = np.concatenate((y_train, y_shuffled[i]), axis=0)
    X_train = np.delete(X_train, 0, axis=0)
    y_train = np.delete(y_train, 0, axis=0)
    return X_train, y_train, X_valid, y_valid

def svmfit(X1,y1,c):
  options['show_progress'] = False
  P = matrix(np.dot(y1*X1 , (y1*X1).T) * 1.)
  q = matrix(np.ones(X1.shape[0]) * -1)
  G = matrix(np.vstack((np.diag(np.ones(X1.shape[0]) * -1), np.identity(X1.shape[0]))))
  h = matrix(np.hstack((np.zeros(X1.shape[0]), np.ones(X1.shape[0]) * c)))
  A = matrix(y1.reshape(1, -1))
  b = matrix(0.0)
  alpha = np.array(qp(P, q, G, h, A, b)['x'])
  weight = (np.matmul((y1 * alpha).T, X1)).reshape(-1,1)
  return weight

# Predicting class
def predict(X1, model_weights):
    y_predict_class = np.matmul(X1, model_weights)
    for i in range(len(y_predict_class)):
        if y_predict_class[i]<0:
            y_predict_class[i]=-1
        else:
            y_predict_class[i]=1
    return y_predict_class

# Calculating error rate as no. of misclassified samples/ total no. of samples
def error_rate_calc(y, y_predict_class):
    misclassification = y_predict_class - y
    no_of_misclassified_samples = np.count_nonzero(misclassification)
    total_no_of_samples = len(misclassification)
    return no_of_misclassified_samples/total_no_of_samples

def k_fold_cv(k,c1):
  train_accuracy = list()
  cv_accuracy = list()
  test_accuracy = list()
  #Calling cross validation function
  X_shuffled, y_shuffled = cross_validation(k)
  for c in c1:
    training_acc = list()
    cv_acc = list()
    test_acc = list()
    for i in range(k):
      # Getting training and validation data
      X_train, y_train, X_cv, y_cv = get_next_train_valid(X_shuffled, y_shuffled, i, k)
      #Training model
      weight = svmfit(X_train,y_train,c)
      #Predicting labels using the model
      label_train = predict(X_train,weight)
      label_cv = predict(X_cv, weight)
      label_test = predict(X_test, weight)
      # Calculation accuracy rates
      training_acc.append(1 - error_rate_calc(y_train, label_train))
      cv_acc.append(1 - error_rate_calc(y_cv, label_cv))
      test_acc.append(1 - error_rate_calc(y_test, label_test))
    #Storing average accuracy rates as C varies
    train_accuracy.append(np.average(training_acc))
    cv_accuracy.append(np.average(cv_acc))
    test_accuracy.append(np.average(test_acc))
  return train_accuracy, cv_accuracy, test_accuracy


def main():
  #Number of folds in cv
  k=10
  c1 = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]
  train_accuracy, cv_accuracy, test_accuracy = k_fold_cv(k, c1)
  print("Training accuracy =")
  print(train_accuracy)
  print("Validation accuracy =")
  print(cv_accuracy) 
  print("Test accuracy =")
  print(test_accuracy)
  #Plot of accuracy rates
  plt.plot(train_accuracy, label = 'Training')
  plt.plot(cv_accuracy, label = 'Validation')
  plt.plot(test_accuracy, label = 'Test')          
  plt.xlabel("C")
  plt.ylabel("Accuracy")
  plt.xticks(np.arange(8), c1)
  plt.legend()
  plt.show()

if __name__== "__main__":
    main()