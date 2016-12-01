# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 12:15:42 2016

@author: matthew.smith
"""

import numpy as np
import pandas as pd
import sklearn
import sklearn_pandas

from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import Imputer
from sklearn_pandas import DataFrameMapper
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split

#df=pd.read_csv('S:\CG ANALYTICS\Learning\Sustainers\FIFCampaignResponses.csv', encoding='latin-1', parse_dates=True)

df=pd.read_csv('C:\\Users\\matthew.smith\\Desktop\\Learning\\Sustainers\\FIFCampaignResponses.csv', encoding='latin-1', parse_dates=True)

#df['Firstgiftdate'].apply(lambda x: x.toordinal())

#df['Firstgiftdate'] = pd.to_datetime(df['Firstgiftdate'])

#df['Lastgiftdate'] = pd.to_datetime(df['Lastgiftdate'])

#df['Maxgiftdate'] = pd.to_datetime(df['Maxgiftdate'])

#df['Firstgiftdate_delta'] = (pd.to_datetime('today') - df['Firstgiftdate'] / np.timedelta64(1, 'D'))

#df['Lastgiftdate'] = (df['Lastgiftdate'] - df['Lastgiftdate'].min()) / np.timedelta64(1,'M')

#df['Maxgiftdate'] = (df['Maxgiftdate'] - df['Maxgiftdate'].min()) / np.timedelta64(1,'M')


# Reorder columns so it is easier to exclude dates

df = df[['#ID', 'Lastgift', 'Maxgift', 'Totalgifts', 'Totalpayamount', 'Firstgift','Maxgiftdate', 'Firstgiftdate', 'Lastgiftdate', 'Mail?']]

# Find out if data has any NULL values

print(df.isnull().any())

# Split between X and y

df_X = df[['Lastgift', 'Maxgift', 'Totalgifts', 'Totalpayamount', 'Firstgift']]

df_y = df[['Mail?']]

# Remove headers from dataset

original_headers_X = list(df_X.columns.values)

original_headers_y = list(df_y.columns.values)

print(original_headers_X)

print(original_headers_y)

# Convert data into NumPy Array

X = df_X.as_matrix()

y_matrix = df_y.as_matrix()

y = y_matrix.flatten()

print('Shape of original dataset:', df.shape)

print('Shape of features:', X.shape)

print('Shape of targets:', y.shape)

print('Total Number of Samples (rows)', X.shape[0])

print('Total Number of Features (columns)', X.shape[1])

#Run Imputer to fill in NULL values

imp = Imputer(missing_values='NaN', strategy='median', axis=0)

imp.fit(X)

X_imp = imp.fit_transform(X)

print(X_imp.shape)

print(y.shape)

# Set Estimator

knn_5 = KNeighborsClassifier(n_neighbors=5)

print(knn_5)

# Fit Estimator to the dataset

knn_5.fit(X_imp,y)

# Predict using X_imp

y_pred_knn5 = knn_5.predict(X_imp)

# Logistic Regression

logreg = LogisticRegression()

print(logreg)

logreg.fit(X_imp,y)

y_pred_logreg = logreg.predict(X_imp)

#Accuracy measures

print('Accuraccy of knn_5 =', metrics.accuracy_score(y, y_pred_knn5))

print('Accuraccy of logreg =', metrics.accuracy_score(y, y_pred_logreg))

#Train/Test Split

X_train, X_test, y_train, y_test = train_test_split(X_imp, y, test_size=0.4, random_state=4)

print('Shape of X - Train =', X_train.shape)

print('Shape of X - Test =', X_test.shape)







