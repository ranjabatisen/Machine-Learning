# -*- coding: utf-8 -*-
"""hw2_multi_logistic.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JtPDPCU7xilW0ESkmmgkZRKNt2WwqLeI
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

#Importing data from dataset
training_data = pd.read_csv('mnist_train.csv', header = None).values
test_data = pd.read_csv('mnist_test.csv', header = None).values

X_train = training_data[:,1:]
y_train = training_data[:,0].reshape(-1,1)

X_test = test_data[:,1:]
y_test = test_data[:,0].reshape(-1,1)

def create_mini_batch(X, y, batch_size, itr):
  X_mini = X[itr*batch_size:(itr+1)*batch_size,:]
  y_mini = y[itr*batch_size:(itr+1)*batch_size]
  return X_mini, y_mini

def softmax_calc(X,w):
  #softmax1 = np.ones((X.shape[0],w.shape[1]))
  H = np.dot(X,w)
  #To prevent overflow
  r,c = H.shape
  if r!=0:
    softmax1 = np.exp(H - np.max(H))
  softmax = softmax1 /np.array([np.sum(softmax1, axis=1)]).T
  return softmax

def gradient(X,y,w):
  grad = 0
  if X.shape[0] != 0:
    grad = (-1 / X.shape[0]) * np.dot(X.T,(y - softmax_calc(X,w)))
  return grad

def calc_loss(X, y, w):
  loss = 0
  if X.shape[0] != 0:
    loss = (-1 / X.shape[0]) * np.sum(y * np.log(softmax_calc(X,w)))
  return loss

def mnist_train(X_train, y_train, learning_rate):
  model_weights = np.random.rand(X_train.shape[1], 10)
  loss = list()
  model_weights *= 0.00001
  for itr in range(10000):
    X_mini, y_mini = create_mini_batch(X_train, y_train, 100, itr % int(X_train.shape[0]/100))
    # change labels in y mini to binary representation (For label 1, the representation will be 0100000000)
    y = np.zeros((len(y_mini), 10))
    for i in range(len(y_mini)):
      if math.isnan(y_mini[i]):
        a = 0
      elif int(y_mini[i]) <= 10:
        y[i,int(y_mini[i])] = 1
    y_mini = y
    model_weights = model_weights - (learning_rate * gradient(X_mini, y_mini, model_weights))
    #print(model_weights)
    if itr % 50 == 0:
      loss.append(calc_loss(X_mini, y_mini, model_weights)) 
  return model_weights, loss

def mnist_predict(w, X):
  return np.argmax(softmax_calc(X,w), axis=1)

def acc_rate_calc(y, y_predict_class):
    misclassification = y_predict_class - y
    no_of_misclassified_samples = np.count_nonzero(misclassification)
    total_no_of_samples = len(misclassification)
    error = no_of_misclassified_samples/total_no_of_samples
    return (1-error)

def main():
  learning_rate = 1e-6
  #To train the model
  weight, loss = mnist_train(X_train, y_train, learning_rate)
  #To predict the labels using the model
  label = mnist_predict(weight, X_test)
  accuracy = acc_rate_calc(y_test,label.reshape(-1,1))
  print("Accuracy for test data :" + str(accuracy))
  y_actu = pd.Series(y_test.flatten(), name='Actual')
  y_pred = pd.Series(label, name='Predicted')
  confusion_matrix = pd.crosstab(y_actu, y_pred)
  print(confusion_matrix)
  # Check convergence of loss function
  plt.plot(loss)
  plt.ylabel("Loss")
  plt.title("Loss Function")
  plt.show()

if __name__== "__main__":
    main()