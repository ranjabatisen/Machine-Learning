# -*- coding: utf-8 -*-
"""hw4_boosting_regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dnl2PO5BiSg9DwIhWvVnTYu_sBVMGPOM
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import test_score as ts

def blindboost(y, itr, learning_rate, N):
  minscore = ts.score(y)
  z = (itr + 1)/(itr + 2)
  for i in range(3000):
    y_random = np.random.uniform(50,size=(N, 1))
    yp = ((y_random * learning_rate) + y)*z
    score = ts.score(yp)
    if score < minscore and i > 100:
      break
    elif score < minscore:
      minscore = score
    if (i+1) % 50 == 0:
      learning_rate /= 2
  return yp, score

def main():
  learning_rate = 0.2
  N = 21283
  y = np.zeros((N, 1))
  listofscores = list()
  current_score = 3
  prev_score = 4
  itr = 0
  while prev_score - current_score > 0.000001:
    prev_score = current_score
    y, current_score = blindboost(y, itr, learning_rate, N)
    print(current_score)
    listofscores.append(current_score)
    itr = itr + 1
  # Plot of score vs no. of weak learners with blind boost
  plt.plot(listofscores)
  plt.xlabel("No. of weak learners")
  plt.ylabel("Scores")
  plt.title("Score vs No. of weak learners with blind boost")
  plt.show()
  

if __name__== "__main__":
    main()