# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 2020

This code file implements the machine learning models from the below links for the disc golf data

The process comes from: https://machinelearningmastery.com/machine-learning-in-python-step-by-step/

@author: samta
"""

# Import libraries
import sys
import scipy
import numpy as np
import matplotlib as mat
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.preprocessing import OneHotEncoder
import seaborn as sns
from sklearn import metrics
# Read in model_data
dataset = pd.read_csv(r"C:\Users\samta\Documents\Python Scripts\disc_golf\data\model_data.csv")





# Review Summary Data on model_data -----------------------------------

# Shape
print(dataset.shape)

# Head
print(dataset.head(20))

# Decriptions
print(dataset.describe())

# Class descriptions
print(dataset.groupby('player_name').size())


# box and whisker plots
dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
mat.pyplot.show()

#histograms
dataset.hist()
mat.pyplot.show()

# scatter plot matrix

pd.plotting.scatter_matrix(dataset)
mat.pyplot.show()


# Add string version of pdga_number, subset to data used in model

dataset['str_pdga_number'] = dataset['pdga_number'].astype(str)
dataset['top_5'] = np.where(dataset['place']<=5,1,0)
print(dataset.describe())

model_input = dataset[['str_pdga_number','standard_event_name','rating','top_5']]


#Split Categorical Factor into dummy columns
dum_df = pd.get_dummies(model_input, columns=["standard_event_name"], prefix=["event_is"] )
dum_df_2 = pd.get_dummies(dum_df, columns=["str_pdga_number"], prefix=["pdganum_is"] )
# Create a Validation Dataset ------------------------------------------
# 80% of the data to be used as training data
# 20% to be held back as validation data

cols = dum_df_2.columns.tolist()
temp = [cols[1]]+[cols[0]]+cols[2:115]

input_w_dummies = dum_df_2[temp]

array = input_w_dummies.values
X = array[:,1:]
y = array[:,0]
X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=1)




# Evaluate 6 Different Models to See Which is Best
# Logistic Regression (LR)
# Linear Discriminant Analysis (LDA)
# K-Nearest Neighbors (KNN).
# Classification and Regression Trees (CART).
# Gaussian Naive Bayes (NB).
# Support Vector Machines (SVM).

# 'accuracy' = # correctly predicted instances divided by total number of instances in dataset

models = []
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))
# evaluate each model in turn
results = []
names = []
for name, model in models:
	kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
	cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
	results.append(cv_results)
	names.append(name)
	print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))

# Compare Algorithms
mat.pyplot.boxplot(results, labels=names)
mat.pyplot.title('Algorithm Comparison')
mat.pyplot.show()


# Make Predictions
# model = SVC(gamma='auto')

model = LogisticRegression()
model.fit(X_train, Y_train)
predictions = model.predict(X_validation)



# Evaluate predictions
print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))




#Make a Nice Confusion matrix
mat.pyplot.figure(figsize=(2,2))

cm = confusion_matrix(Y_validation, predictions)
score = accuracy_score(Y_validation, predictions)

sns.heatmap(cm, annot=True, fmt=".3f", linewidths=.5, square = True, cmap = 'Blues_r');
mat.pyplot.ylabel('Actual label');
mat.pyplot.xlabel('Predicted label');
all_sample_title = 'Accuracy Score: {0}'.format(score)
mat.pyplot.title(all_sample_title, size = 15); 









