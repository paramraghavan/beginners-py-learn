# 03 - ML Model API Project

## Project Overview

Build an end-to-end machine learning system with model training, serving via API, monitoring, and retraining. This integrates data science, web development, and DevOps.

**Duration:** 3-4 weeks
**Difficulty:** Intermediate-Advanced
**Best For:** Data Scientists & ML Engineers
**Key Technologies:** scikit-learn, TensorFlow, FastAPI, Docker, AWS, MLflow

---

## Learning Objectives

By completing this project, you'll learn:
- Build ML pipelines with scikit-learn
- Evaluate and tune models
- Serialize and version models
- Create prediction APIs
- Monitor model performance
- Handle data drift
- Implement retraining strategies
- Deploy to production

---

## Project Scenario

**Problem:** Build a machine learning system that predicts customer churn for a telecom company.

**Business Requirements:**
- Predict which customers will churn in next 30 days
- Provide prediction confidence scores
- Make predictions via REST API
- Monitor model accuracy in production
- Retrain monthly with new data
- Explain predictions to business users

**Data:** Telecom customer dataset (20,000 records, 20 features)

---

## System Architecture

```
┌─────────────────────────────────────────┐
│      Raw Data (Customer Features)        │
└─────────────────────────────────────────┘
              │
┌─────────────────────────────────────────┐
│   Data Exploration & Preprocessing       │
│  • Missing values, outliers, scaling     │
│  • Feature engineering                   │
│  • Train/test split                      │
└─────────────────────────────────────────┘
              │
┌─────────────────────────────────────────┐
│      Model Training (scikit-learn)       │
│  • Baseline model                        │
│  • Hyperparameter tuning                 │
│  • Cross-validation                      │
│  • Model evaluation                      │
└─────────────────────────────────────────┘
              │
┌─────────────────────────────────────────┐
│    Model Registry (MLflow)               │
│  • Save model version                    │
│  • Store metrics & parameters            │
│  • Track experiments                     │
└─────────────────────────────────────────┘
              │
┌─────────────────────────────────────────┐
│    Prediction API (FastAPI)              │
│  • Load model                            │
│  • Input validation                      │
│  • Make predictions                      │
│  • Return confidence scores              │
└─────────────────────────────────────────┘
              │
┌─────────────────────────────────────────┐
│    Monitoring & Alerting                 │
│  • Track prediction distribution         │
│  • Detect data drift                     │
│  • Alert on performance degradation      │
│  • Schedule retraining                   │
└─────────────────────────────────────────┘
```

---

## Week-by-Week Implementation

### Week 1: Data Exploration & Model Development

**Goals:**
- Load and explore data
- Handle missing values and outliers
- Feature engineering
- Train baseline models
- Evaluate performance

**Deliverables:**
- EDA notebook
- Data preprocessing pipeline
- 3+ trained models (Logistic Regression, Random Forest, Gradient Boosting)
- Model evaluation report

**Key Code:**

```python
# data_preparation.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

class DataPreprocessor:
    """Prepare data for modeling"""

    def __init__(self):
        self.scaler = StandardScaler()
        self.encoders = {}

    def load_data(self, filepath: str) -> pd.DataFrame:
        """Load customer churn dataset"""
        df = pd.read_csv(filepath)
        print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
        return df

    def explore_data(self, df: pd.DataFrame):
        """EDA"""
        print("\n=== DATA OVERVIEW ===")
        print(df.head())
        print(f"\nShape: {df.shape}")
        print(f"\nData Types:\n{df.dtypes}")
        print(f"\nMissing Values:\n{df.isnull().sum()}")
        print(f"\nTarget Distribution:\n{df['churn'].value_counts()}")
        print(f"\nNumeric Stats:\n{df.describe()}")

    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle nulls"""
        # Check which columns have nulls
        null_cols = df.columns[df.isnull().any()]

        for col in null_cols:
            if df[col].dtype == 'float64':
                # Numeric: fill with median
                df[col].fillna(df[col].median(), inplace=True)
            else:
                # Categorical: fill with mode
                df[col].fillna(df[col].mode()[0], inplace=True)

        print(f"Handled missing values for: {null_cols.tolist()}")
        return df

    def encode_categorical(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """Encode categorical variables"""
        categorical_cols = df.select_dtypes(include=['object']).columns

        df_encoded = df.copy()

        for col in categorical_cols:
            if col == 'churn':  # Target variable
                encoder = LabelEncoder()
                df_encoded[col] = encoder.fit_transform(df[col])
                self.encoders[col] = encoder
            else:
                # Use one-hot encoding
                dummies = pd.get_dummies(df_encoded[col], prefix=col, drop_first=True)
                df_encoded = pd.concat([df_encoded, dummies], axis=1)
                df_encoded.drop(col, axis=1, inplace=True)

        print(f"Encoded {len(categorical_cols)} categorical columns")
        return df_encoded

    def scale_features(self, X_train: pd.DataFrame, X_test: pd.DataFrame, fit: bool = True):
        """Scale numeric features"""
        if fit:
            X_train_scaled = self.scaler.fit_transform(X_train)
        else:
            X_train_scaled = self.scaler.transform(X_train)

        X_test_scaled = self.scaler.transform(X_test)

        return X_train_scaled, X_test_scaled

    def prepare(self, filepath: str, test_size: float = 0.2):
        """Full preprocessing pipeline"""
        df = self.load_data(filepath)
        self.explore_data(df)
        df = self.handle_missing_values(df)
        df = self.encode_categorical(df)

        X = df.drop('churn', axis=1)
        y = df['churn']

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        X_train_scaled, X_test_scaled = self.scale_features(X_train, X_test)

        return X_train_scaled, X_test_scaled, y_train, y_test


# model_training.py
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
import mlflow
import mlflow.sklearn

class ModelTrainer:
    """Train and evaluate models"""

    @staticmethod
    def train_logistic_regression(X_train, y_train):
        """Baseline model"""
        model = LogisticRegression(max_iter=1000, random_state=42)
        model.fit(X_train, y_train)
        return model

    @staticmethod
    def train_random_forest(X_train, y_train):
        """Tree-based model"""
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        return model

    @staticmethod
    def train_gradient_boosting(X_train, y_train):
        """Gradient boosting"""
        model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        model.fit(X_train, y_train)
        return model

    @staticmethod
    def evaluate(model, X_test, y_test, model_name: str):
        """Evaluate model"""
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]

        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba),
        }

        print(f"\n=== {model_name} ===")
        for metric, value in metrics.items():
            print(f"{metric}: {value:.4f}")

        print(f"\nConfusion Matrix:\n{confusion_matrix(y_test, y_pred)}")
        print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")

        return metrics

    @staticmethod
    def log_to_mlflow(model, metrics: dict, params: dict, model_name: str):
        """Log to MLflow"""
        with mlflow.start_run(run_name=model_name):
            mlflow.log_params(params)
            mlflow.log_metrics(metrics)
            mlflow.sklearn.log_model(model, "model")

            print(f"Logged {model_name} to MLflow")


# Train multiple models
if __name__ == "__main__":
    # Prepare data
    preprocessor = DataPreprocessor()
    X_train, X_test, y_train, y_test = preprocessor.prepare("data/churn.csv")

    # Train models
    trainer = ModelTrainer()

    # Logistic Regression
    lr_model = trainer.train_logistic_regression(X_train, y_train)
    lr_metrics = trainer.evaluate(lr_model, X_test, y_test, "Logistic Regression")
    trainer.log_to_mlflow(lr_model, lr_metrics, {}, "logistic_regression")

    # Random Forest
    rf_model = trainer.train_random_forest(X_train, y_train)
    rf_metrics = trainer.evaluate(rf_model, X_test, y_test, "Random Forest")
    trainer.log_to_mlflow(rf_model, rf_metrics, {"n_estimators": 100}, "random_forest")

    # Gradient Boosting
    gb_model = trainer.train_gradient_boosting(X_train, y_train)
    gb_metrics = trainer.evaluate(gb_model, X_test, y_test, "Gradient Boosting")
    trainer.log_to_mlflow(gb_model, gb_metrics, {"n_estimators": 100}, "gradient_boosting")

    # Best model
    best_model = gb_model  # Based on F1 score
    print("\n✅ Best model selected: Gradient Boosting")
```

---

### Week 2: Hyperparameter Tuning & Model Validation

**Goals:**
- Optimize best model
- Cross-validation strategy
- Feature importance analysis
- Final model selection

**Deliverables:**
- Tuned model with better metrics
- Cross-validation report
- Feature importance analysis
- Model ready for serving

**Key Code:**

```python
# hyperparameter_tuning.py
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np

class HyperparameterTuner:
    """Optimize model parameters"""

    @staticmethod
    def grid_search(X_train, y_train, X_test, y_test):
        """Grid search for best parameters"""
        param_grid = {
            'n_estimators': [100, 200],
            'learning_rate': [0.01, 0.1],
            'max_depth': [3, 5, 7],
            'min_samples_split': [5, 10],
        }

        base_model = GradientBoostingClassifier(random_state=42)
        grid_search = GridSearchCV(
            base_model,
            param_grid,
            cv=5,
            scoring='f1',
            n_jobs=-1,
            verbose=1
        )

        print("Running grid search...")
        grid_search.fit(X_train, y_train)

        print(f"\nBest parameters: {grid_search.best_params_}")
        print(f"Best CV F1 score: {grid_search.best_score_:.4f}")

        # Evaluate on test set
        y_pred = grid_search.best_estimator_.predict(X_test)
        test_f1 = f1_score(y_test, y_pred)
        print(f"Test F1 score: {test_f1:.4f}")

        return grid_search.best_estimator_

    @staticmethod
    def feature_importance(model, feature_names: list):
        """Analyze feature importance"""
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]

        print("\n=== Top 10 Important Features ===")
        for i in range(min(10, len(feature_names))):
            idx = indices[i]
            print(f"{i+1}. {feature_names[idx]}: {importances[idx]:.4f}")

        return dict(zip([feature_names[i] for i in indices[:10]], importances[indices[:10]]))

    @staticmethod
    def cross_validate(model, X, y, cv: int = 5):
        """Perform cross-validation"""
        from sklearn.model_selection import cross_val_score

        scores = cross_val_score(model, X, y, cv=cv, scoring='f1')
        print(f"\n=== Cross-Validation Results (k={cv}) ===")
        print(f"Scores: {scores}")
        print(f"Mean: {scores.mean():.4f} (+/- {scores.std():.4f})")
        return scores.mean()
```

---

### Week 3: API Development & Serving

**Goals:**
- Create prediction API
- Input validation
- Model versioning
- Confidence scores

**Deliverables:**
- FastAPI application with prediction endpoint
- API documentation
- Model loaded from MLflow
- Input validation

**Key Code:**

```python
# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.sklearn
import numpy as np
import pandas as pd
from typing import List

app = FastAPI(title="Churn Prediction API")

# Load model
model_uri = "models:/gradient_boosting/production"
model = mlflow.sklearn.load_model(model_uri)

# Load preprocessor
from data_preparation import DataPreprocessor
preprocessor = DataPreprocessor()

# Request/Response models
class CustomerData(BaseModel):
    tenure: int
    monthly_charges: float
    total_charges: float
    contract: str  # Month-to-month, One year, Two year
    internet_service: str  # DSL, Fiber optic, No
    # ... more features

    class Config:
        json_schema_extra = {
            "example": {
                "tenure": 24,
                "monthly_charges": 65.5,
                "total_charges": 1570.0,
                "contract": "Month-to-month",
                "internet_service": "Fiber optic"
            }
        }

class PredictionResponse(BaseModel):
    churn_probability: float
    will_churn: bool
    confidence: float
    explanation: str

@app.post("/predict", response_model=PredictionResponse)
def predict(data: CustomerData):
    """Predict churn for a customer"""
    try:
        # Convert to dataframe
        customer_df = pd.DataFrame([data.dict()])

        # Preprocess
        customer_encoded = preprocessor.encode_categorical(customer_df, fit=False)
        customer_scaled = preprocessor.scaler.transform(customer_encoded)

        # Predict
        churn_prob = model.predict_proba(customer_scaled)[0, 1]
        will_churn = model.predict(customer_scaled)[0] == 1

        # Calculate confidence
        confidence = max(churn_prob, 1 - churn_prob)

        # Explanation
        if will_churn:
            explanation = f"Customer has {churn_prob:.1%} probability of churning"
        else:
            explanation = f"Customer has {1-churn_prob:.1%} probability of staying"

        return PredictionResponse(
            churn_probability=float(churn_prob),
            will_churn=bool(will_churn),
            confidence=float(confidence),
            explanation=explanation
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
def health():
    """Health check"""
    return {"status": "healthy"}

@app.get("/model/info")
def model_info():
    """Get model info"""
    return {
        "model": "Gradient Boosting Classifier",
        "version": "production",
        "features": 20,
        "accuracy": 0.85
    }

# Test
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Tests:**

```python
# test_api.py
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_predict():
    response = client.post("/predict", json={
        "tenure": 24,
        "monthly_charges": 65.5,
        "total_charges": 1570.0,
        "contract": "Month-to-month",
        "internet_service": "Fiber optic"
    })

    assert response.status_code == 200
    data = response.json()
    assert 0 <= data["churn_probability"] <= 1
    assert isinstance(data["will_churn"], bool)
    assert 0.5 <= data["confidence"] <= 1.0

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_invalid_input():
    response = client.post("/predict", json={
        "tenure": "invalid"
    })
    assert response.status_code == 422  # Validation error
```

---

### Week 4: Monitoring & Retraining

**Goals:**
- Monitor model performance
- Detect data drift
- Schedule retraining
- Document operations

**Deliverables:**
- Monitoring pipeline
- Drift detection
- Retraining script
- Operational dashboard

**Key Code:**

```python
# monitoring.py
import pandas as pd
import numpy as np
from datetime import datetime
from prometheus_client import Counter, Histogram, start_http_server

# Prometheus metrics
prediction_counter = Counter('predictions_total', 'Total predictions made')
churn_histogram = Histogram('churn_probability', 'Distribution of churn probabilities')
latency_histogram = Histogram('prediction_latency_seconds', 'API latency')

class ModelMonitor:
    """Monitor model in production"""

    def __init__(self):
        self.predictions = []

    def log_prediction(self, customer_id: str, prediction: float, actual: float = None):
        """Log prediction for monitoring"""
        self.predictions.append({
            'timestamp': datetime.now(),
            'customer_id': customer_id,
            'prediction': prediction,
            'actual': actual
        })

        # Update Prometheus metrics
        prediction_counter.inc()
        churn_histogram.observe(prediction)

    def detect_data_drift(self, current_data: pd.DataFrame,
                         baseline_data: pd.DataFrame, threshold: float = 0.05):
        """Detect data drift using Kolmogorov-Smirnov test"""
        from scipy.stats import ks_2samp

        drifted_features = []

        for col in current_data.select_dtypes(include=[np.number]).columns:
            statistic, p_value = ks_2samp(baseline_data[col], current_data[col])
            if p_value < threshold:
                drifted_features.append((col, p_value))

        if drifted_features:
            print("⚠️  Data drift detected:")
            for col, p_val in drifted_features:
                print(f"  {col}: p-value={p_val:.4f}")
            return True

        return False

    def calculate_performance_metrics(self) -> dict:
        """Calculate model performance on recent predictions"""
        df = pd.DataFrame(self.predictions)

        # Only use predictions with actual labels
        labeled = df[df['actual'].notna()]

        if len(labeled) == 0:
            return {}

        y_pred = (labeled['prediction'] > 0.5).astype(int)
        y_actual = labeled['actual']

        from sklearn.metrics import accuracy_score, f1_score

        return {
            'accuracy': accuracy_score(y_actual, y_pred),
            'f1': f1_score(y_actual, y_pred),
            'sample_count': len(labeled)
        }


class RetrainingOrchestrator:
    """Schedule and manage retraining"""

    @staticmethod
    def should_retrain(model_age_days: int, accuracy_drop: float,
                      min_samples: int = 1000) -> bool:
        """Decide whether to retrain"""
        if model_age_days > 30:  # Monthly retraining
            return True

        if accuracy_drop > 0.05:  # 5% drop in accuracy
            return True

        return False

    @staticmethod
    def retrain_pipeline(X_train, y_train, X_test, y_test):
        """Run full retraining pipeline"""
        print("🔄 Starting model retraining...")

        # Train new model
        trainer = ModelTrainer()
        new_model = trainer.train_gradient_boosting(X_train, y_train)
        new_metrics = trainer.evaluate(new_model, X_test, y_test, "Retrained Model")

        # Compare with production model
        print("\n📊 Model comparison:")
        print("New model F1 score:", new_metrics['f1'])

        # Promote if better
        if new_metrics['f1'] > 0.82:  # Production baseline
            print("✅ New model is better, promoting to production")
            mlflow.sklearn.log_model(new_model, "model")
            return new_model
        else:
            print("❌ New model is not better, keeping current")
            return None
```

---

## Project Completion Checklist

### Model Development
- [ ] EDA completed
- [ ] Data preprocessed
- [ ] 3+ models trained
- [ ] Hyperparameters tuned
- [ ] Cross-validation passing
- [ ] F1 score > 0.80

### API & Serving
- [ ] FastAPI application created
- [ ] Prediction endpoint working
- [ ] Input validation implemented
- [ ] API documentation complete
- [ ] Tests passing (80%+ coverage)

### Monitoring
- [ ] Prometheus metrics setup
- [ ] Data drift detection
- [ ] Performance monitoring
- [ ] Alert thresholds defined

### Deployment
- [ ] Dockerfile created
- [ ] docker-compose.yml working
- [ ] GitHub Actions CI/CD
- [ ] Deployed and running

### Documentation
- [ ] Model card created
- [ ] API documentation
- [ ] Retraining runbook
- [ ] Monitoring dashboard

---

## Interview Questions

1. **How would you detect model drift in production?**
   - Monitor prediction distribution
   - Track actual vs predicted labels
   - Statistical tests (KS test)
   - Set alert thresholds

2. **How do you handle imbalanced classes?**
   - Class weights
   - SMOTE oversampling
   - Different evaluation metrics (F1, ROC-AUC)
   - Cost-sensitive learning

3. **What's the difference between data drift and model drift?**
   - Data drift: input distribution changes
   - Model drift: model performance decreases
   - Both should trigger retraining

4. **How would you explain predictions to stakeholders?**
   - Feature importance
   - SHAP values
   - Confidence scores
   - Similar historical examples

5. **How do you version and rollback models?**
   - MLflow model registry
   - Semantic versioning
   - Staging/production environments
   - A/B testing for rollout

---

## Resources

- [ML Workflow Guide](../ml-workflow-guide.md) - Complete ML workflow
- [Web Development Guide](../web-development-guide.md) - FastAPI details
- [Cloud & DevOps Guide](../cloud-devops-guide.md) - Docker and monitoring

---

## Time Estimate

- **Week 1:** 15-18 hours (Data prep, multiple models)
- **Week 2:** 12-15 hours (Tuning, validation)
- **Week 3:** 12-15 hours (API, tests)
- **Week 4:** 10-12 hours (Monitoring, documentation)

**Total: 49-60 hours**

---

## Next Steps

After completing:
1. Build frontend UI for predictions
2. Implement batch prediction API
3. Add explanation models (SHAP)
4. Advanced monitoring (Evidently AI)
5. Multi-model serving (multiple versions)
6. AutoML experimentation

**This is a production ML system!** Portfolio-ready and interview-impressive.
