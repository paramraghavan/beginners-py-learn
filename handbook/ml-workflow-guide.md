# 🤖 ML Workflow Guide

> **End-to-End Machine Learning Development**
>
> Complete guide to building, training, evaluating, and deploying machine learning models in production.

---

## Table of Contents

1. [ML Fundamentals](#ml-fundamentals)
2. [Project Structure](#project-structure)
3. [Data Handling](#data-handling)
4. [Exploratory Data Analysis](#exploratory-data-analysis)
5. [Feature Engineering](#feature-engineering)
6. [Model Selection](#model-selection)
7. [Model Training](#model-training)
8. [Model Evaluation](#model-evaluation)
9. [Hyperparameter Tuning](#hyperparameter-tuning)
10. [Cross-Validation](#cross-validation)
11. [Model Serialization](#model-serialization)
12. [Model Serving](#model-serving)
13. [Monitoring & Retraining](#monitoring--retraining)
14. [Real-World Example](#real-world-example)

---

## ML Fundamentals

### Types of Learning

| Type | Definition | Examples |
|------|-----------|----------|
| **Supervised** | Learn from labeled data | Regression, Classification |
| **Unsupervised** | Find patterns in unlabeled data | Clustering, Dimensionality reduction |
| **Reinforcement** | Learn from rewards/penalties | Game AI, Robotics |
| **Semi-supervised** | Mix of labeled & unlabeled | Self-training, Co-training |

### ML Workflow

```
1. Define Problem
   ↓
2. Collect Data
   ↓
3. Explore Data (EDA)
   ↓
4. Prepare Data
   ├─ Handle missing values
   ├─ Handle outliers
   ├─ Scale features
   └─ Encode categorical variables
   ↓
5. Feature Engineering
   ├─ Create new features
   ├─ Select relevant features
   └─ Reduce dimensionality
   ↓
6. Model Selection
   ├─ Choose algorithm
   └─ Set initial hyperparameters
   ↓
7. Train Model
   ↓
8. Evaluate Model
   ├─ Test accuracy
   ├─ Cross-validation
   └─ Performance metrics
   ↓
9. Hyperparameter Tuning
   ↓
10. Final Evaluation
    ↓
11. Deploy Model
    ↓
12. Monitor Performance
    ↓
13. Retrain as Needed
```

---

## Project Structure

```
ml-project/
├── README.md
├── requirements.txt
├── setup.py
├── .env
├── .gitignore
│
├── data/
│   ├── raw/                    # Original data
│   ├── processed/              # Cleaned data
│   └── external/               # External data sources
│
├── notebooks/                  # Jupyter notebooks
│   ├── 01-eda.ipynb
│   ├── 02-feature-engineering.ipynb
│   └── 03-model-training.ipynb
│
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loader.py          # Load data
│   │   └── processor.py        # Clean/preprocess
│   ├── features/
│   │   ├── __init__.py
│   │   └── engineering.py      # Feature creation
│   ├── models/
│   │   ├── __init__.py
│   │   ├── train.py           # Training logic
│   │   └── evaluate.py        # Evaluation metrics
│   └── utils/
│       ├── __init__.py
│       └── helpers.py          # Utility functions
│
├── models/                     # Saved models
│   ├── model_v1.pkl
│   ├── scaler_v1.pkl
│   └── encoder_v1.pkl
│
├── tests/
│   ├── __init__.py
│   ├── test_data.py
│   ├── test_features.py
│   └── test_models.py
│
└── scripts/
    ├── train.py               # Training script
    ├── predict.py             # Prediction script
    └── evaluate.py            # Evaluation script
```

---

## Data Handling

### Load Data

```python
import pandas as pd
import numpy as np

# Load CSV
df = pd.read_csv('data/raw/data.csv')

# Load from database
from sqlalchemy import create_engine
engine = create_engine('postgresql://user:pass@localhost/db')
df = pd.read_sql('SELECT * FROM table', engine)

# Load from API
import requests
response = requests.get('https://api.example.com/data')
df = pd.DataFrame(response.json())

# Check data
print(df.shape)           # (1000, 20)
print(df.dtypes)          # Column types
print(df.head())          # First 5 rows
print(df.info())          # Null counts, types
print(df.describe())      # Summary statistics
```

### Handle Missing Values

```python
# Identify missing values
print(df.isnull().sum())
print(df.isnull().sum() / len(df) * 100)  # Percentage

# Drop rows with missing values
df_clean = df.dropna()  # Remove rows with any NaN
df_clean = df.dropna(subset=['age', 'salary'])  # Specific columns

# Fill missing values
df['age'].fillna(df['age'].median(), inplace=True)  # Median
df['category'].fillna('Unknown', inplace=True)      # Constant
df['price'].fillna(method='ffill', inplace=True)    # Forward fill

# More sophisticated imputation
from sklearn.impute import SimpleImputer, KNNImputer

imputer = SimpleImputer(strategy='mean')
df[['age', 'income']] = imputer.fit_transform(df[['age', 'income']])

# KNN imputation (uses k nearest neighbors)
knn_imputer = KNNImputer(n_neighbors=5)
df_imputed = knn_imputer.fit_transform(df)
```

### Handle Outliers

```python
# Identify outliers
Q1 = df['value'].quantile(0.25)
Q3 = df['value'].quantile(0.75)
IQR = Q3 - Q1
outliers = (df['value'] < Q1 - 1.5 * IQR) | (df['value'] > Q3 + 1.5 * IQR)

print(f"Outliers: {outliers.sum()}")

# Remove outliers
df_clean = df[~outliers]

# Cap outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df['value'] = df['value'].clip(lower_bound, upper_bound)

# Z-score method
from scipy import stats
z_scores = np.abs(stats.zscore(df[['value']]))
df_clean = df[z_scores < 3]  # Keep values with |z| < 3
```

### Scale Features

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# StandardScaler (mean=0, std=1)
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[['age', 'income']])

# MinMaxScaler (0 to 1 range)
scaler = MinMaxScaler()
df_scaled = scaler.fit_transform(df[['age', 'income']])

# Save scaler for later use
import pickle
pickle.dump(scaler, open('models/scaler.pkl', 'wb'))

# Load scaler
scaler = pickle.load(open('models/scaler.pkl', 'rb'))
new_data_scaled = scaler.transform(new_data)
```

### Encode Categorical Variables

```python
# One-hot encoding
df_encoded = pd.get_dummies(df, columns=['color', 'category'])

# Label encoding (for ordinal variables)
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['grade_encoded'] = le.fit_transform(df['grade'])  # A, B, C → 0, 1, 2

# Save encoder
pickle.dump(le, open('models/encoder.pkl', 'wb'))
```

---

## Exploratory Data Analysis

### Basic Statistics

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Summary statistics
df.describe()

# Correlation matrix
correlation = df.corr()
sns.heatmap(correlation, annot=True)
plt.show()

# Check class distribution
df['target'].value_counts()
df['target'].value_counts(normalize=True)
```

### Visualization

```python
# Distribution plots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Histogram
axes[0, 0].hist(df['age'], bins=30, edgecolor='black')
axes[0, 0].set_title('Age Distribution')

# Box plot
axes[0, 1].boxplot(df['income'])
axes[0, 1].set_title('Income Box Plot')

# Scatter plot
axes[1, 0].scatter(df['age'], df['income'])
axes[1, 0].set_title('Age vs Income')

# Bar plot
df['category'].value_counts().plot(kind='bar', ax=axes[1, 1])
axes[1, 1].set_title('Category Distribution')

plt.tight_layout()
plt.show()
```

---

## Feature Engineering

### Create New Features

```python
# Date features
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek

# Interaction features
df['age_income'] = df['age'] * df['income']
df['age_squared'] = df['age'] ** 2

# Binning/Bucketing
df['age_group'] = pd.cut(df['age'], bins=[0, 18, 35, 50, 100],
                         labels=['Child', 'Young', 'Middle', 'Senior'])

# Aggregation features
df['customer_purchases'] = df.groupby('customer_id')['purchase'].transform('count')
df['customer_avg_purchase'] = df.groupby('customer_id')['amount'].transform('mean')
```

### Feature Selection

```python
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif

# Select top 10 features
selector = SelectKBest(f_classif, k=10)
X_selected = selector.fit_transform(X, y)

# Feature importance from tree model
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()
rf.fit(X, y)
importances = rf.feature_importances_
feature_names = X.columns[np.argsort(importances)[-10:]]  # Top 10
```

---

## Model Selection

### Scikit-learn Models

```python
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

# Classification
models = {
    'Logistic Regression': LogisticRegression(),
    'Random Forest': RandomForestClassifier(n_estimators=100),
    'Gradient Boosting': GradientBoostingClassifier(),
    'SVM': SVC(),
    'KNN': KNeighborsClassifier()
}

# Regression
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(),
    'Gradient Boosting': GradientBoostingRegressor()
}
```

### Deep Learning with TensorFlow

```python
import tensorflow as tf
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')  # Binary classification
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

history = model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)
```

---

## Model Training

### Basic Training

```python
from sklearn.model_selection import train_test_split

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)
```

### Track Training

```python
from sklearn.metrics import accuracy_score

results = []
for n_estimators in [50, 100, 200, 300]:
    model = RandomForestClassifier(n_estimators=n_estimators)
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    results.append({
        'n_estimators': n_estimators,
        'train_accuracy': train_score,
        'test_accuracy': test_score
    })

results_df = pd.DataFrame(results)
print(results_df)
```

---

## Model Evaluation

### Classification Metrics

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)

# Basic metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Detailed report
print(classification_report(y_test, y_pred))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

# ROC-AUC
auc = roc_auc_score(y_test, y_pred_proba[:, 1])
fpr, tpr, _ = roc_curve(y_test, y_pred_proba[:, 1])

# Plot ROC curve
plt.plot(fpr, tpr, label=f'AUC = {auc:.3f}')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.show()
```

### Regression Metrics

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse:.4f}")
print(f"MAE: {mae:.4f}")
print(f"R²: {r2:.4f}")
```

---

## Hyperparameter Tuning

### Grid Search

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(
    RandomForestClassifier(),
    param_grid,
    cv=5,  # 5-fold cross-validation
    scoring='f1',
    n_jobs=-1  # Use all processors
)

grid_search.fit(X_train, y_train)
print(f"Best parameters: {grid_search.best_params_}")
print(f"Best score: {grid_search.best_score_:.4f}")

best_model = grid_search.best_estimator_
test_score = best_model.score(X_test, y_test)
```

### Random Search

```python
from sklearn.model_selection import RandomizedSearchCV
import scipy.stats as stats

param_dist = {
    'n_estimators': [50, 100, 200, 300],
    'max_depth': stats.randint(5, 50),
    'min_samples_split': stats.randint(2, 20),
    'min_samples_leaf': stats.randint(1, 10)
}

random_search = RandomizedSearchCV(
    RandomForestClassifier(),
    param_dist,
    n_iter=20,
    cv=5,
    n_jobs=-1
)

random_search.fit(X_train, y_train)
```

---

## Cross-Validation

### K-Fold Cross-Validation

```python
from sklearn.model_selection import cross_val_score, cross_validate

# Simple cross-validation
scores = cross_val_score(
    RandomForestClassifier(),
    X, y,
    cv=5,  # 5-fold
    scoring='accuracy'
)

print(f"Scores: {scores}")
print(f"Mean: {scores.mean():.4f} (+/- {scores.std():.4f})")

# Multiple metrics
metrics = cross_validate(
    RandomForestClassifier(),
    X, y,
    cv=5,
    scoring=['accuracy', 'precision', 'recall', 'f1']
)

print(metrics)
```

### Stratified K-Fold (for imbalanced data)

```python
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for train_idx, test_idx in skf.split(X, y):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(f"Fold score: {score:.4f}")
```

---

## Model Serialization

### Save Model

```python
import pickle
import joblib

# Pickle
pickle.dump(model, open('models/model.pkl', 'wb'))
model = pickle.load(open('models/model.pkl', 'rb'))

# Joblib (better for large models)
joblib.dump(model, 'models/model.joblib')
model = joblib.load('models/model.joblib')

# TensorFlow/Keras
model.save('models/model.h5')
model = keras.models.load_model('models/model.h5')
```

### Model Registry (MLflow)

```python
import mlflow
import mlflow.sklearn

with mlflow.start_run():
    # Log parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 10)

    # Train model
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    # Log metrics
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)

    # Log model
    mlflow.sklearn.log_model(model, "model")
```

---

## Model Serving

### FastAPI

```python
from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()

# Load model
model = joblib.load('models/model.joblib')
scaler = joblib.load('models/scaler.joblib')

class PredictRequest(BaseModel):
    age: int
    income: float
    experience: int

@app.post("/predict")
async def predict(request: PredictRequest):
    # Prepare data
    X = [[request.age, request.income, request.experience]]
    X_scaled = scaler.transform(X)

    # Make prediction
    prediction = model.predict(X_scaled)[0]
    probability = model.predict_proba(X_scaled)[0]

    return {
        "prediction": int(prediction),
        "confidence": float(probability[1])
    }
```

### Flask

```python
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)
model = joblib.load('models/model.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    X = [[data['age'], data['income'], data['experience']]]

    prediction = model.predict(X)[0]
    return jsonify({'prediction': int(prediction)})
```

---

## Monitoring & Retraining

### Track Model Performance

```python
import pandas as pd
from datetime import datetime

def log_prediction(features, prediction, actual=None):
    """Log predictions for monitoring"""
    record = {
        'timestamp': datetime.now(),
        'features': features,
        'prediction': prediction,
        'actual': actual
    }
    # Save to database or file
    df = pd.read_csv('logs/predictions.csv')
    df = df.append(record, ignore_index=True)
    df.to_csv('logs/predictions.csv', index=False)

def detect_drift(df_baseline, df_recent):
    """Detect data drift"""
    # Compare distributions
    from scipy.stats import ks_2samp

    for column in df_baseline.columns:
        statistic, p_value = ks_2samp(df_baseline[column], df_recent[column])
        if p_value < 0.05:
            print(f"Drift detected in {column}")
```

### Automated Retraining

```python
def should_retrain(metrics_history):
    """Check if model should be retrained"""
    # If accuracy drops below threshold
    if metrics_history[-1]['accuracy'] < 0.85:
        return True

    # If accuracy trending downward
    recent_accuracies = [m['accuracy'] for m in metrics_history[-5:]]
    if all(recent_accuracies[i] >= recent_accuracies[i+1] for i in range(4)):
        return True

    return False

def retrain_model():
    """Retrain model with new data"""
    # Load new data
    new_data = pd.read_csv('data/new_data.csv')

    # Combine with old data
    all_data = pd.concat([df_train, new_data])

    # Retrain
    X = all_data.drop('target', axis=1)
    y = all_data['target']

    model = RandomForestClassifier()
    model.fit(X, y)

    # Save new model
    joblib.dump(model, 'models/model_v2.joblib')
```

---

## Real-World Example

### Complete ML Pipeline

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1. Load data
df = pd.read_csv('data/raw/data.csv')

# 2. Data cleaning
df = df.dropna()
df['age'] = df['age'].clip(0, 100)

# 3. Feature engineering
df['age_group'] = pd.cut(df['age'], bins=[0, 18, 35, 50, 100])
df = pd.get_dummies(df, columns=['age_group'])

# 4. Split data
X = df.drop('target', axis=1)
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5. Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 6. Hyperparameter tuning
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20],
    'min_samples_split': [2, 5]
}

grid_search = GridSearchCV(
    RandomForestClassifier(),
    param_grid,
    cv=5
)

grid_search.fit(X_train_scaled, y_train)

# 7. Evaluate
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f}")
print(classification_report(y_test, y_pred))

# 8. Save model
joblib.dump(best_model, 'models/final_model.joblib')
joblib.dump(scaler, 'models/scaler.joblib')
```

---

## ML Best Practices

### Do's

✅ Start with baseline model
✅ Validate on holdout test set
✅ Use cross-validation
✅ Scale features appropriately
✅ Handle class imbalance
✅ Document experiments
✅ Save model versions
✅ Monitor in production

### Don'ts

❌ Test on training data
❌ Tune hyperparameters on test set
❌ Ignore class imbalance
❌ Forget to scale features
❌ Use inappropriate metrics
❌ Forget exploratory analysis
❌ Deploy without testing
❌ Stop monitoring after deployment

---

## Resources

- **Scikit-learn Documentation** - scikit-learn.org
- **TensorFlow/Keras** - tensorflow.org
- **Fast.ai** - fast.ai (practical deep learning)
- **Andrew Ng's ML Course** - Coursera
- **"Hands-On Machine Learning" Book** - Aurélien Géron

---

**Last Updated:** May 2026 | **Version:** 1.0

Related resources:
- [Database Operations Guide](database-operations-guide.md) - Data storage and retrieval
- [Cloud & DevOps Guide](cloud-devops-guide.md) - Model deployment and serving
- [Quick Reference Cards](quick-reference-cards.md) - Common ML commands
