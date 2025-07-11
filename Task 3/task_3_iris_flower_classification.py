# -*- coding: utf-8 -*-
"""TASK 3 IRIS FLOWER CLASSIFICATION.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19VcG8kNO4ca4YiGhmnU5ZYwVqFPYqNZZ

**1. Loading the dataset**
"""

import pandas as pd

# GitHub raw URL
url = 'https://raw.githubusercontent.com/abuthahir17/CODSOFT_INTERNSHIP/main/IRIS.csv'

# Read CSV file
data = pd.read_csv(url)

print("Dataset loaded successfully.")

"""**2. Data Inspection**

2.1. First 5 Rows
"""

print("First 5 rows of the dataset:")
print(data.head())

"""2.2. Dataset Information"""

print("Information about the dataset:")
print(data.info())

""" 2.3. Describing the Dataset"""

print("Descriptive statistics of the dataset:")
print(data.describe())

"""2.4. Checking Dataset Shape"""

print("Dataset Shape:", data.shape)

"""2.5. Checking Missing Values"""

print("Missing values in each column:")
print(data.isnull().sum())

# There is no missing value

"""2.6. Species Distribution

"""

print(data['species'].value_counts())

"""**3. Data Visualization**

3.1. Class Distribution Plot (Count Plot)
"""

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
sns.countplot(data=data, x='species' ,hue='species',  palette='Set2')
plt.title("Class Distribution")
plt.xlabel("Species")
plt.ylabel("Count")
plt.show()

"""3.2. Pairplot of Iris Features (Pairplot)"""

sns.pairplot(data, hue="species")
plt.suptitle("Iris Features by Species", y=1.02)
plt.show()

"""3.3. Feature Correlation Heatmap"""

plt.figure(figsize=(8, 6))
sns.heatmap(data.drop('species', axis=1).corr(), annot=True, cmap="YlGnBu")
plt.title("Feature Correlation Heatmap")
plt.show()

"""**4. Data Preprocessing**

4.1. Label Encoding
"""

# Encode the target variable
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
data['species_encoded'] = le.fit_transform(data['species'])

"""4.2. Feature and Target Separation

"""

# Split the data
X = data.drop(['species', 'species_encoded'], axis=1)
y = data['species_encoded']

"""4.3. Data Splitting

"""

# Split the data into training and testing sets (80% train, 20% test)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training set size: {X_train.shape[0]} samples")
print(f"Testing set size: {X_test.shape[0]} samples")

"""**5. Model Training**

5.1. Initialize the models
"""

# Model Training
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

# Logistic Regression
log_model = LogisticRegression(max_iter=200)
log_model.fit(X_train, y_train)

# Support Vector Machine
svm_model = SVC(kernel='linear')
svm_model.fit(X_train, y_train)

# Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

print("Model training complete.")

"""5.2. Feature Importance"""

importances = rf_model.feature_importances_
features = X.columns

plt.figure(figsize=(8, 5))
sns.barplot(x=importances, y=features)
plt.title("Feature Importance")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.show()

"""5.3. Model Prediction

"""

y_pred_log = log_model.predict(X_test)
y_pred_svm = svm_model.predict(X_test)
y_pred_rf = rf_model.predict(X_test)

"""**6. Model Evaluation and Saving**

6.1. Classification Reports
"""

from sklearn.metrics import classification_report, accuracy_score
#  Calculate the accuracy of the model.
print("Logistic Regression Report:")
print(classification_report(y_test, y_pred_log, target_names=le.classes_))
print(f"Accuracy: {accuracy_score(y_test, y_pred_log) * 100:.2f}%")

print("\n\nSVM Classification Report:")
print(classification_report(y_test, y_pred_svm, target_names=le.classes_))
print(f"Accuracy: {accuracy_score(y_test, y_pred_svm) * 100:.2f}%")

print("\n\nRandom Forest Classification Report:")
print(classification_report(y_test, y_pred_rf, target_names=le.classes_))
print(f"Accuracy: {accuracy_score(y_test, y_pred_rf) * 100:.2f}%")

"""6.2. Confusion Matrices

"""

from sklearn.metrics import ConfusionMatrixDisplay

print("Confusion Matrix for Logistic Regression:\n")

ConfusionMatrixDisplay.from_estimator(log_model, X_test, y_test, display_labels=le.classes_, cmap='Greens')
plt.title("Logistic Regression - Confusion Matrix")
plt.show()

print("\nConfusion Matrix for Support Vector Machine:\n")

ConfusionMatrixDisplay.from_estimator(svm_model, X_test, y_test, display_labels=le.classes_, cmap='Blues')
plt.title("SVM - Confusion Matrix")
plt.show()

print("\nConfusion Matrix for Random Forest:\n")

ConfusionMatrixDisplay.from_estimator(rf_model, X_test, y_test, display_labels=le.classes_, cmap='Oranges')
plt.title("Random Forest - Confusion Matrix")
plt.show()

"""6.3. Saving and Storing Models"""

import joblib
joblib.dump(log_model, "iris_logistic_model.pkl")
joblib.dump(svm_model, "iris_svm_model.pkl")
joblib.dump(rf_model, "iris_random_forest_model.pkl")
print("Models saved: 'iris_logistic_model.pkl' , 'iris_svm_model.pkl' and 'iris_random_forest_model.pkl' ")

"""**7. Model Performance Analysis**

7.1. Performance Metrics Table
"""

#Performance Comparison Table
from sklearn.metrics import precision_recall_fscore_support

def get_metrics(y_true, y_pred, model_name):
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='macro')
    accuracy = accuracy_score(y_true, y_pred)
    return {
        "Model": model_name,
        "Accuracy": round(accuracy * 100, 2),
        "Precision": round(precision * 100, 2),
        "Recall": round(recall * 100, 2),
        "F1-Score": round(f1 * 100, 2)
    }

results = [
    get_metrics(y_test, y_pred_log, "Logistic Regression"),
    get_metrics(y_test, y_pred_svm, "SVM"),
    get_metrics(y_test, y_pred_rf, "Random Forest")
]

comparison_df = pd.DataFrame(results)
print("\n📊 Model Performance Comparison:")
print(comparison_df)

"""7.2 Performance Comparison Bar Chart"""

comparison_df.set_index("Model")[["Accuracy", "Precision", "Recall", "F1-Score"]].plot(kind="bar", figsize=(10,6), colormap='Accent')
plt.title("Model Performance Comparison")
plt.ylabel("Score (%)")
plt.ylim(80, 105)
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

print("--- Iris Flower Classification Task Complete ---")