# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 12:15:42 2016

@author: matthew.smith
"""

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import sklearn
import seaborn as sns

from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import Imputer
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from imblearn.under_sampling import RandomUnderSampler
from sklearn.decomposition import PCA
from sklearn import svm
from sklearn import tree
from sklearn.grid_search import GridSearchCV
from IPython.display import Image
from sklearn.grid_search import GridSearchCV
import datetime as dt


df=pd.read_csv('S:\CG ANALYTICS\Learning\Sustainers\FIFCampaignResponses.csv', encoding='latin-1', parse_dates=True)

#df=pd.read_csv('C:\\Users\\matthew.smith\\Desktop\\Learning\\Sustainers\\FIFCampaignResponses.csv', encoding='latin-1', parse_dates=True)

# Reorder columns so it is easier to exclude dates

df = df[['#ID', 'Lastgift', 'Maxgift', 'Totalgifts', 'Totalpayamount', 'Firstgift','Maxgiftdate', 'Firstgiftdate', 'Lastgiftdate', 'Mail?']]

# Find out if data has any NULL values

print(df.isnull().any(), '\n')

# Change First Gift Date and Last Gift Date to Ordinal 
df['Firstgiftdate']= (pd.to_datetime(df['Firstgiftdate'])).map(dt.datetime.toordinal)
df['Lastgiftdate'] = (pd.to_datetime(df['Lastgiftdate'])).map(dt.datetime.toordinal)

# Split between X and y

df_X = df[['Lastgift', 'Maxgift', 'Totalgifts', 'Totalpayamount', 'Firstgift','Firstgiftdate','Lastgiftdate']]

df_y = df[['Mail?']]

print(df_X.describe(), '\n')
print(df_y.describe(), '\n')

# Remove headers from dataset

original_headers_X = list(df_X.columns.values)

original_headers_y = list(df_y.columns.values)

print('Feature Headers: ', original_headers_X)
print('Target Header: ', original_headers_y, '\n')

# Convert data into NumPy Array

X_matrix = df_X.values

y_matrix = df_y.values

y = y_matrix.flatten()

print('Shape of original dataset:', df.shape, '\n')
print('Shape of features:', X_matrix.shape)
print('Shape of targets:', y.shape, '\n')
print('Total Number of Samples (rows): ', X_matrix.shape[0])
print('Total Number of Features (columns): ', X_matrix.shape[1], '\n')

#Run Imputer to fill in NULL values

imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
imp.fit(X_matrix)
X_imp = imp.fit_transform(X_matrix)

# Use Scaler

scaler = StandardScaler()
X = scaler.fit_transform(X_imp)

print('Shape of Imputed Features: ', X.shape)
print('Shape of Target: ', y.shape, '\n')

#Fixing imbalance of negative class with undersampling of positive class

sns.set()

almost_black = '#262626'
palette = sns.color_palette()

# Instanciate a PCA object for the sake of easy visualisation
pca = PCA(n_components=2)

# Fit and transform x to visualise inside a 2D feature space
X_vis = pca.fit_transform(X)

# Apply the random over-sampling
US = RandomUnderSampler()
usx,usy = US.fit_sample(X,y)
X_res_vis = pca.transform(usx)

# Two subplots, unpack the axes array immediately
f, (ax1, ax2) = plt.subplots(1, 2)

ax1.scatter(X_vis[y == 0, 0], X_vis[y == 0, 1], label="Class #0", alpha=0.5,
            edgecolor=almost_black, facecolor=palette[0], linewidth=0.15)
ax1.scatter(X_vis[y == 1, 0], X_vis[y == 1, 1], label="Class #1", alpha=0.5,
            edgecolor=almost_black, facecolor=palette[2], linewidth=0.15)
ax1.set_title('Original set')

ax2.scatter(X_res_vis[usy == 0, 0], X_res_vis[usy == 0, 1],
            label="Class #0", alpha=.5, edgecolor=almost_black,
            facecolor=palette[0], linewidth=0.15)
ax2.scatter(X_res_vis[usy == 1, 0], X_res_vis[usy == 1, 1],
            label="Class #1", alpha=.5, edgecolor=almost_black,
            facecolor=palette[2], linewidth=0.15)
ax2.set_title('Random over-sampling')

plt.show()

# Set Estimator for KNN

knn = KNeighborsClassifier(n_neighbors=30)

# Fit Estimator to the dataset

knn.fit(usx,usy)

# Predict using X_imp

y_pred_knn = knn.predict(usx)

# Cross-validation for KNN

knn_scores = cross_val_score(knn, usx, usy, cv=10, scoring='accuracy')

# Grid Search for KNN

k_range = list(range(1,31))
param_grid = dict(n_neighbors=k_range)
grid = GridSearchCV(knn, param_grid, cv=10, scoring='accuracy')
grid.fit(usx,usy)

grid_mean_scores = [result.mean_validation_score for result in grid.grid_scores_]

plt.plot(k_range, grid_mean_scores)
plt.xlabel('Value of K for KNN')
plt.ylabel('Cross-Validated Accuracy')
plt.show()

print('Grid Best Score: ', grid.best_score_)
print('Grid Best Parameter: ', grid.best_params_)
print('Grid Best Estimator: ', grid.best_estimator_)

# Cross-validation for Logistic Regression

logreg = LogisticRegression()
log_scores = cross_val_score(logreg, usx, usy, cv=10, scoring='accuracy')

# Cross-validation for SVM

svc = svm.SVC()
svc_scores = cross_val_score(svc, usx, usy, cv=10, scoring='accuracy')

k_range = list(range(1,100))
k_scores = []
for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, usx, usy, cv=10, scoring='accuracy')
    k_scores.append(scores.mean())

# Decision Tree

tree = tree.DecisionTreeClassifier()

tree_k_range = list(range(1,31))
tree_param_grid = dict(max_depth=tree_k_range)
tree_grid = GridSearchCV(tree, tree_param_grid, cv=10, scoring='accuracy')
tree_grid.fit(usx,usy)

tree_grid_mean_scores = [result.mean_validation_score for result in tree_grid.grid_scores_]

plt.plot(tree_k_range, tree_grid_mean_scores)
plt.xlabel('Value of Max Depth for Tree')
plt.ylabel('Cross-Validated Accuracy')
plt.show()

print('Grid Max Depth Best Score: ', tree_grid.best_score_)
print('Grid Max Depth Best Parameter: ', tree_grid.best_params_)
print('Grid Max Depth Best Estimator: ', tree_grid.best_estimator_)

# Plot of the value of K versus the Accuracy

plt.plot(k_range, k_scores)
plt.xlabel('Value of K for KNN')
plt.ylabel('Cross-Validated Accuracy')
plt.show()

print('Average accuracy score for KNN Cross-Validation: ', knn_scores.mean(), '\n')
print('Average accuracy score for Logistic Regression Cross-Validation: ', log_scores.mean(), '\n')
print('Average accuracy score for Support Vector Machine: ', svc_scores.mean())







