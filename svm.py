# -*- coding: utf-8 -*-
"""SVM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ShbnSqI1kWNfS8Ykl9YvtoCeLZVoQiRW

Support Vector Machines (SVM)

It is a supervised learning technique.

Works well for classifying higher dimensional data (lots of features) since it clusters data.

Uses kernel trick to represent data in higher dimensional spaces to find hyperplanes not apparent in lower dimensions
"""

# In practice, we use support vector classification (SVC) to classify data using SVM
# Different kernels can be used with SVC depending on the data set.

"""# Setup and Imports"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import metrics

from sklearn.svm import SVC

df = pd.read_csv('drive/MyDrive/Colab Notebook data/voice.csv')
df.head()

df.shape #(3168, 21)

"""# Prelim Analysis"""

# Can we reduce number of features ?
df.describe()

# Check for nulls
df.isnull().sum()

df.mode()

# Check for count of mode (variation in data)
df.apply(lambda row: row[row.isin(row.mode())].count())

# Check correlation between different fields
df.corr()

"""Looks like I can probably skip Centroid, Median and Q25 as they have high correl with the meanfreq

# Pre-processing
"""

X = df.iloc[:,:-1]
y = df.iloc[:,-1]

X.head()

allCols = df.columns
ignoreCols = ['median','Q25','centroid','label']
indepCols = list(set(allCols)-set(ignoreCols))

X = X[indepCols]
X.head()

type(y)

# I prefer keeping y as a dataframe instead of a series
y = pd.DataFrame(y)

# We need to encode male/female strings to numeric labels
enc = LabelEncoder()
y['encLabel'] = enc.fit_transform(y['label'])
y.head()

X_train, X_test,  y_train, y_test = train_test_split(X,y['encLabel'])

# Normalization

scale = StandardScaler()
X_train = pd.DataFrame(scale.fit_transform(X_train), columns = indepCols)
X_test = pd.DataFrame(scale.fit_transform(X_test), columns = indepCols)

print(X_train.shape) #(2376, 17)
X_train.head()

print(X_test.shape) #(792, 17)
X_test.head()

"""# Modeling

## Default parameters
"""

#from sklearn.svm import SVC

# Using default hyper-parameters
svc = SVC()
svc.fit(X_train, y_train)

pred_train = svc.predict(X_train) 
pred_test = svc.predict(X_test)

print('Training Accuracy:')
print(metrics.accuracy_score(y_train, pred_train))
print('Testing Accuracy:')
print(metrics.accuracy_score(y_test, pred_test))

"""## Polynomial kernel"""

svm = SVC(kernel = 'poly', degree = 3)
svm.fit(X_train, y_train)

pred_train = svm.predict(X_train) 
pred_test = svm.predict(X_test)

print('Training Accuracy:')
print(metrics.accuracy_score(y_train, pred_train))
print('Testing Accuracy:')
print(metrics.accuracy_score(y_test, pred_test))

# Polynomial kernel is doing worse thant he default (def is rbf)

"""## K-fold validation for rbf and polynomial kernels"""

from sklearn.model_selection import cross_val_score

# Again, rbf is the default kernel
svc = SVC()
scores = cross_val_score(svc, X,y['encLabel'], cv = 7, scoring = 'accuracy')
print(scores) # Scores for each iteration. Scores change suggesting split matters for the predictions
print(scores.mean()) # Mean accuracy for 7 fold cv

# For polynomial kernel
svc = SVC(kernel = 'poly', degree = 3, )
scores = cross_val_score(svc, X,y['encLabel'], cv = 7, scoring = 'accuracy')
print(scores.mean()) # Mean accuracy for 7 fold cv

"""## Parameter Search"""

# Let us check how chaning the parameters C, degree, co-eff and even the kernel change the accuracy
param_grid = {'C': list(range(1,10)),
              'degree': list(range(1,4)),
              'coef0': list(np.arange(0,3,0.5)),
              'kernel': ['rbf', 'poly']}

from sklearn.model_selection import GridSearchCV

clf = GridSearchCV(svc, param_grid)
clf.fit(X_train, y_train)

print(clf.best_params_)
print(clf.best_estimator_)

"""# Final model"""

# Using the best parameters from the parameter search

svc = SVC(C=7, kernel = 'poly', degree = 3, coef0 = 0.5)
scores = cross_val_score(svc, X,y['encLabel'], cv = 7, scoring = 'accuracy')
print(scores.mean())
svc.fit(X_train, y_train)

pred_test = svc.predict(X_test)
print(metrics.accuracy_score(y_test, pred_test))
# Accuracy improved from 0.9660 using def params to 0.9785..

from sklearn.metrics import precision_score, recall_score

print(precision_score(y_test, pred_test))
print(recall_score(y_test, pred_test))

