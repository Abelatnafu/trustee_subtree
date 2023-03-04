"""
ClassificationTrustee
=====================

Simple example on how to use the ClassificationTrustee class to extract
a decision tree from a RandomForestClassifier from scikit-learn.
"""
# importing required libraries
# importing Scikit-learn library and datasets package
import graphviz
import numpy as np
from sklearn import tree
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from subtree import get_subtree
from trustee.utils.tree import get_dt_dict
from trustee import ClassificationTrustee
from trustee.utils import tree as tee
from trustee.utils import plot

# Loading the iris plants dataset (classification)
cancer = datasets.load_breast_cancer()
X, y = datasets.load_breast_cancer(return_X_y=True)

# Spliting arrays or matrices into random train and test subsets
# i.e. 70 % training dataset and 30 % test datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

# creating a RF classifier
clf = RandomForestClassifier(n_estimators=100)
# Training the model on the training dataset
# fit function is used to train the model using the training sets as parameters
clf.fit(X_train, y_train)
# performing predictions on the test dataset
y_pred = clf.predict(X_test)

# Evaluate model accuracy
# print("Model classification report:")
# print(classification_report(y_test, y_pred))

# Initialize Trustee and fit for classification models
trustee = ClassificationTrustee(expert=clf)
trustee.fit(X_train, y_train, num_iter=50, num_stability_iter=10, samples_size=0.3, verbose=True)

# Get the best explanation from Trustee
dt, pruned_dt, agreement, reward = trustee.explain()
# print(f"Model explanation training (agreement, fidelity): ({agreement}, {reward})")
# print(f"Model Explanation size: {dt.tree_.node_count}")
# print(f"Top-k Prunned Model explanation size: {pruned_dt.tree_.node_count}")

# Use explanations to make predictions
dt_y_pred = dt.predict(X_test)
pruned_dt_y_pred = pruned_dt.predict(X_test)

# Evaluate accuracy and fidelity of explanations
# print("Model explanation global fidelity report:")
# print(classification_report(y_pred, dt_y_pred))
# print("Top-k Model explanation global fidelity report:")
# print(classification_report(y_pred, pruned_dt_y_pred))
#
# print("Model explanation score report:")
# print(classification_report(y_test, dt_y_pred))
# print("Top-k Model explanation score report:")
# print(classification_report(y_test, pruned_dt_y_pred))


# Output decision tree to pdf
dot_data = tree.export_graphviz(
    dt,
    class_names=cancer.target_names,
    feature_names=cancer.feature_names,
    filled=True,
    rounded=True,
    special_characters=True,
)

# print("---------------------------")
# print(iris.target_names)
# print("----------------------------")
# print("---------------------------")
# print(tee.get_dt_dict(dt)["nodes"])
# print("----------------------------")
graph = graphviz.Source(dot_data)
graph.render("dt_explanation")

# Output pruned decision tree to pdf
dot_data = tree.export_graphviz(
    pruned_dt,
    class_names=cancer.target_names,
    feature_names=cancer.feature_names,
    filled=True,
    rounded=True,
    special_characters=True,
)
# print(dot_data)
graph = graphviz.Source(dot_data)
graph.render("pruned_dt_explation")


get_subtree(dt,0,cancer.target_names, cancer.feature_names )