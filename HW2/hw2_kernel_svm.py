# -*- coding: utf-8 -*-
"""hw2_kernel_svm.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C3VrbDdbMv47K4XHl_B5lmGhTbQ_Xmn7
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

def rbf_svm_train(X1,y1,c,sigma):
  options['show_progress'] = False
  K = np.zeros((X1.shape[0], X1.shape[0]))
  for i in range(X1.shape[0]):
    for j in range(X1.shape[0]):
      K[i,j] = np.exp(-1 * np.square(np.linalg.norm(X1[i]-X1[j])) / (2 * np.square(sigma)))
  P = matrix(np.outer(y1,y1) * K)
  q = matrix(np.ones(X1.shape[0]) * -1)
  G = matrix(np.vstack((np.diag(np.ones(X1.shape[0]) * -1), np.identity(X1.shape[0]))))
  h = matrix(np.hstack((np.zeros(X1.shape[0]), np.ones(X1.shape[0]) * c)))
  A = matrix(y1.reshape(1, -1))
  b = matrix(0.0)
  alpha = np.array(qp(P, q, G, h, A, b)['x'])
  return alpha

# Predicting class
def predict(X_test, X1, y1, alpha, sigma):
    K = np.zeros((X_test.shape[0],X1.shape[0]))
    for i in range(X_test.shape[0]):
        for j in range(X1.shape[0]):
            K[i,j] = np.exp(-1 * np.square(np.linalg.norm(X_test[i]-X1[j])) / (2 * np.square(sigma)))
    y_predict_class = np.matmul(K, alpha * y1)
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
  test_err = list()
  cv_err = list()
  train_err = list()
  #Calling cross validation function
  X_shuffled, y_shuffled = cross_validation(k)
  for c in c1:
    sigma = c
    training_acc = list()
    cv_acc = list()
    test_acc = list()
    test_error = list()
    validation_error = list()
    training_error = list()
    for i in range(k):
      # Getting training and validation data
      X_train, y_train, X_cv, y_cv = get_next_train_valid(X_shuffled, y_shuffled, i, k)
      #Training model
      alpha = rbf_svm_train(X_train,y_train,c,sigma)
      #Predicting labels using the model
      label_cv = predict(X_cv, X_train, y_train, alpha, sigma)
      label_test = predict(X_test, X_train, y_train, alpha, sigma)
      # Calculation accuracy rates
      cv_acc.append(1 - error_rate_calc(y_cv, label_cv))
      test_acc.append(1 - error_rate_calc(y_test, label_test))
      # Storing error rates
      test_error.append(error_rate_calc(y_test, label_test))
      validation_error.append(error_rate_calc(y_cv, label_cv))
    
    if(c == 0.1):
      #Plotting error rates for each fold
      x = np.arange(k)
      width = 0.35
      fig, ax = plt.subplots()
      rects1 = ax.bar(x - width/2, test_error, width, label='Test error')
      rects2 = ax.bar(x + width/2, validation_error, width, label='Validation error')
      ax.set_title('Validation error and Test error for each fold for C = ' + str(c) + 'and sigma = ' + str(sigma))
      ax.legend()
      fig.tight_layout()
      plt.show()
    #Storing average accuracy rates as C and sigma vary
    cv_accuracy.append(np.average(cv_acc))
    test_accuracy.append(np.average(test_acc))
    #Storing average error rates as C and sigma vary
    cv_err.append(np.average(validation_error))
    test_err.append(np.average(test_error))
  print("Validation accuracy =")
  print(cv_accuracy) 
  print("Test accuracy =")
  print(test_accuracy)
  return cv_err, test_err


def main():
  #Number of folds in cv
  k=10
  c1 = [0.01, 0.1, 1]
  cv_error, test_error = k_fold_cv(k, c1)
  plt.plot(cv_error, label = 'Validation')
  plt.plot(test_error, label = 'Test')          
  plt.xlabel("C and sigma")
  plt.ylabel("Error rates")
  plt.xticks(np.arange(3), c1)
  plt.legend()
  plt.show()

if __name__== "__main__":
    main()