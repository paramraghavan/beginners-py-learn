# 📊 Data Scientist Career Path

## Overview

This is a comprehensive 16-week curriculum to become a job-ready Python data scientist. It progresses from Python fundamentals through data manipulation, statistical analysis, machine learning, and production deployment.

**Target Outcomes:**
- Analyze and visualize data effectively
- Build machine learning models from scratch
- Apply statistical methods to real datasets
- Deploy models to production
- Communicate findings to stakeholders
- Solve data science interview problems

**Time Commitment:** 40-50 hours/week for 16 weeks (best as intensive bootcamp or part-time over 6-8 months)

**Recommended Setup:**
- Python 3.9+
- Anaconda or miniconda
- Jupyter Notebook
- Git & GitHub account
- PostgreSQL (optional for data engineering)

---

## Week-by-Week Curriculum

### 🟢 Foundation Phase (Weeks 1-4)

#### Week 1: Python Basics & Environment Setup
**Learning Goals:**
- Install Python and set up data science environment
- Understand basic Python syntax
- Use Jupyter Notebook effectively
- Manage conda environments

**Resources:**
- [Python Study Guide - Chapter 1](../python-study-guide.md#chapter-1-setting-up-your-sandbox)
- [Python Study Guide - Chapter 2: Basics](../python-study-guide.md#chapter-2-python-fundamentals)
- [Quick Reference Cards - Python Syntax](../quick-reference-cards.md#1-python-syntax-essentials)

**Daily Practice (1-2 hours):**
- Day 1-2: Anaconda setup, conda environments, Jupyter basics
- Day 3-4: Python variables, data types, operations
- Day 5-6: String operations, formatting
- Day 7: Mini project - Data loader for CSV/JSON files

**Deliverable:** Jupyter notebook with data loading utilities

---

#### Week 2: Data Structures & NumPy Fundamentals
**Learning Goals:**
- Master Python data structures
- Understand NumPy arrays vs lists
- Learn NumPy operations and broadcasting
- Use NumPy for numerical computing

**Resources:**
- [Python Study Guide - Chapter 3: Data Structures](../python-study-guide.md#chapter-3-data-structures)
- [Quick Reference Cards - Data Structures](../quick-reference-cards.md#2-common-data-structures-operations)

**Daily Practice (2 hours):**
- Day 1-2: NumPy arrays, creation, indexing, slicing
- Day 3: Array operations, broadcasting rules
- Day 4: Linear algebra basics (dot product, matrices)
- Day 5: NumPy statistical functions
- Day 6-7: Mini project - Statistical analysis of sample dataset

**Deliverable:** Jupyter notebook with NumPy analysis

---

#### Week 3: Pandas & Data Manipulation
**Learning Goals:**
- Use pandas DataFrames for data analysis
- Clean and preprocess data
- Handle missing values
- Transform and reshape data

**Resources:**
- Data Scientist Cheatsheet (if available)
- Pandas documentation

**Daily Practice (2-3 hours):**
- Day 1: DataFrame creation, indexing, basic operations
- Day 2-3: Data cleaning (missing values, duplicates, outliers)
- Day 4: Groupby and aggregation operations
- Day 5: Merging and joining datasets
- Day 6-7: Mini project - Real dataset cleanup and analysis

**Deliverable:** Cleaned dataset with analysis notebook

---

#### Week 4: Exploratory Data Analysis (EDA)
**Learning Goals:**
- Perform comprehensive exploratory analysis
- Create effective visualizations
- Understand data distributions
- Identify patterns and relationships

**Resources:**
- [Quick Reference Cards - File I/O](../quick-reference-cards.md#6-file-io-patterns)

**Daily Practice (2-3 hours):**
- Day 1-2: Matplotlib and seaborn basics
- Day 3: Univariate analysis (histograms, distributions)
- Day 4: Bivariate analysis (scatter, correlation)
- Day 5: Multivariate visualization
- Day 6-7: Mini project - Complete EDA on Iris or titanic dataset

**Deliverable:** EDA report with visualizations (HTML or notebook)

**Week 1-4 Checkpoint:**
- [ ] Comfortable with NumPy and Pandas
- [ ] Can perform basic data cleaning
- [ ] Create publication-quality visualizations
- [ ] GitHub repo with 3-4 analysis notebooks

---

### 🟡 Intermediate Phase (Weeks 5-8)

#### Week 5: Statistical Analysis & Hypothesis Testing
**Learning Goals:**
- Understand probability distributions
- Perform hypothesis testing
- Calculate confidence intervals
- Use scipy for statistics

**Resources:**
- Statistics textbook or online course
- SciPy documentation

**Daily Practice (2-3 hours):**
- Day 1-2: Probability distributions (normal, binomial, Poisson)
- Day 3: Hypothesis testing (t-test, chi-square, ANOVA)
- Day 4: Confidence intervals and p-values
- Day 5: Effect sizes and statistical power
- Day 6-7: Mini project - Hypothesis testing on dataset

**Deliverable:** Statistical analysis report with conclusions

---

#### Week 6: Feature Engineering & Preprocessing
**Learning Goals:**
- Create meaningful features from raw data
- Handle categorical variables
- Scale and normalize data
- Select important features

**Resources:**
- [ML Workflow Guide - Feature Engineering](../ml-workflow-guide.md#feature-engineering)
- Scikit-learn documentation

**Daily Practice (2-3 hours):**
- Day 1-2: Encoding categorical variables (one-hot, label, target)
- Day 3: Scaling and normalization (standardization, min-max)
- Day 4: Creating polynomial and interaction features
- Day 5: Feature selection methods
- Day 6-7: Mini project - Feature engineering pipeline

**Deliverable:** Feature engineering notebook with sklearn Pipeline

---

#### Week 7: Machine Learning Fundamentals
**Learning Goals:**
- Understand supervised learning basics
- Implement regression and classification
- Evaluate model performance
- Understand overfitting and regularization

**Resources:**
- [ML Workflow Guide - Model Selection](../ml-workflow-guide.md#model-selection)
- [ML Workflow Guide - Training](../ml-workflow-guide.md#model-training)
- [ML Workflow Guide - Evaluation](../ml-workflow-guide.md#evaluation)
- Scikit-learn documentation

**Daily Practice (2-3 hours):**
- Day 1-2: Linear regression and logistic regression
- Day 3: Decision trees and random forests
- Day 4: Model evaluation (accuracy, precision, recall, F1)
- Day 5: Cross-validation and train/test split
- Day 6-7: Mini project - Multi-model comparison on classification dataset

**Deliverable:** ML models comparison notebook with evaluation metrics

---

#### Week 8: Advanced Algorithms & Ensemble Methods
**Learning Goals:**
- Implement advanced ML algorithms
- Use ensemble methods effectively
- Handle class imbalance
- Tune hyperparameters

**Resources:**
- [ML Workflow Guide - Hyperparameter Tuning](../ml-workflow-guide.md#hyperparameter-tuning)
- [ML Workflow Guide - Cross Validation](../ml-workflow-guide.md#cross-validation)
- Scikit-learn documentation

**Daily Practice (2-3 hours):**
- Day 1-2: Gradient boosting (XGBoost, LightGBM)
- Day 3: Stacking and voting classifiers
- Day 4: Handling imbalanced data (SMOTE, class weights)
- Day 5: Hyperparameter tuning (GridSearchCV, RandomizedSearchCV)
- Day 6-7: Mini project - Kaggle competition dataset or real dataset

**Deliverable:** Tuned ensemble model with validation results

**Week 5-8 Checkpoint:**
- [ ] Statistical analysis completed
- [ ] Feature engineering pipeline built
- [ ] Multiple ML models trained and compared
- [ ] Hyperparameter tuning applied
- [ ] 80%+ validation accuracy on test dataset

---

### 🔵 Deep Learning & Advanced Phase (Weeks 9-12)

#### Week 9: Deep Learning Basics with TensorFlow/Keras
**Learning Goals:**
- Build neural networks from scratch
- Understand layers, activation functions, loss functions
- Train deep learning models
- Use Keras for rapid prototyping

**Resources:**
- TensorFlow/Keras documentation
- Deep learning fundamentals resources

**Daily Practice (2-3 hours):**
- Day 1-2: Neural network architecture basics
- Day 3: Dense layers, activation functions, backpropagation
- Day 4: Loss functions and optimizers
- Day 5: Regularization (dropout, L1/L2)
- Day 6-7: Mini project - Image classification with MNIST or CIFAR-10

**Deliverable:** Neural network notebook with test accuracy

---

#### Week 10: Convolutional Neural Networks (CNN)
**Learning Goals:**
- Understand CNN architecture
- Use pre-trained models
- Apply transfer learning
- Work with image data

**Resources:**
- TensorFlow/Keras documentation
- Transfer learning guides

**Daily Practice (2-3 hours):**
- Day 1-2: Convolutional layers, pooling, filters
- Day 3: Popular architectures (ResNet, VGG)
- Day 4-5: Transfer learning with pre-trained models
- Day 6-7: Mini project - Image classification with transfer learning

**Deliverable:** CNN model with transfer learning applied

---

#### Week 11: Time Series & Recurrent Neural Networks
**Learning Goals:**
- Analyze time series data
- Understand RNNs, LSTMs, GRUs
- Forecast time series
- Handle sequential data

**Resources:**
- TensorFlow/Keras documentation
- Time series analysis resources

**Daily Practice (2-3 hours):**
- Day 1-2: Time series decomposition and analysis
- Day 2-3: ARIMA and exponential smoothing
- Day 4-5: LSTM and GRU layers for sequences
- Day 6-7: Mini project - Time series forecasting

**Deliverable:** LSTM-based forecasting model

---

#### Week 12: Machine Learning in Production
**Learning Goals:**
- Save and load models
- Create model serving APIs
- Monitor model performance
- Deploy models to cloud

**Resources:**
- [ML Workflow Guide - Model Serialization](../ml-workflow-guide.md#model-serialization)
- [ML Workflow Guide - Serving Models](../ml-workflow-guide.md#serving-models)
- [Web Development Guide - FastAPI Integration](../web-development-guide.md#database-integration)

**Daily Practice (2-3 hours):**
- Day 1-2: Model serialization (pickle, joblib, SavedModel)
- Day 3: Creating ML API with FastAPI
- Day 4: Model versioning and MLflow
- Day 5: Docker containerization of ML models
- Day 6-7: Mini project - Deploy ML model as REST API

**Deliverable:** ML model served via FastAPI API

**Week 9-12 Checkpoint:**
- [ ] CNN model trained and evaluated
- [ ] LSTM time series model built
- [ ] ML model deployed as API
- [ ] Can explain deep learning concepts
- [ ] GitHub shows 4-5 ML projects

---

### 🟣 Capstone & Optimization Phase (Weeks 13-16)

#### Week 13: Real-World Dataset Project Setup
**Learning Goals:**
- Choose realistic dataset
- Define clear success metrics
- Plan project timeline
- Set up data pipeline

**Resources:**
- Kaggle datasets or industry datasets
- [ML Workflow Guide - Project Structure](../ml-workflow-guide.md#ml-project-structure)

**Daily Practice (2-3 hours):**
- Day 1-2: Exploratory data analysis (2-3 hours)
- Day 3-4: Data cleaning and preprocessing
- Day 5: Feature engineering
- Day 6-7: Baseline model implementation

**Deliverable:** Clean dataset with EDA report and baseline model

---

#### Week 14: Advanced Model Development
**Learning Goals:**
- Optimize multiple models
- Implement ensemble techniques
- Perform error analysis
- Improve model generalization

**Daily Practice (2-3 hours):**
- Day 1-2: Test multiple algorithms
- Day 3-4: Hyperparameter optimization
- Day 5: Ensemble model building
- Day 6-7: Cross-validation and evaluation

**Deliverable:** Optimized ensemble model with validation score

---

#### Week 15: Deployment & Monitoring
**Learning Goals:**
- Deploy model to production
- Set up monitoring
- Implement retraining pipelines
- Create production documentation

**Resources:**
- [ML Workflow Guide - Serving Models](../ml-workflow-guide.md#serving-models)
- [ML Workflow Guide - Monitoring & Retraining](../ml-workflow-guide.md#monitoring--retraining)
- [Cloud & DevOps Guide](../cloud-devops-guide.md)

**Daily Practice (2-3 hours):**
- Day 1-2: Containerize ML model
- Day 3-4: Deploy model API
- Day 5: Set up monitoring and logging
- Day 6-7: Create deployment documentation

**Deliverable:** Deployed model with monitoring setup

---

#### Week 16: Interview Preparation & Capstone Refinement
**Learning Goals:**
- Solve data science interview problems
- Prepare to explain capstone project
- Practice system design for ML
- Refine capstone project for portfolio

**Resources:**
- [Interview Prep Supplement - System Design](../interview-prep-supplement.md#system-design-basics)
- [Interview Prep - Behavioral Interviews](../interview-prep-supplement.md#behavioral-interviews)

**Daily Practice (3-4 hours):**
- Day 1-2: Study 5-10 common interview problems
- Day 3: System design for ML systems
- Day 4: Behavioral interview prep
- Day 5-7: Refine capstone, create demo, prepare presentation

**Deliverable:** Capstone project ready for portfolio and interviews

**Week 13-16 Checkpoint:**
- [ ] Real-world ML project completed end-to-end
- [ ] Model deployed and monitored
- [ ] Portfolio-ready project documentation
- [ ] Can explain entire ML pipeline
- [ ] Interview ready

---

## Project Progression

### Phase 1: Foundation Projects (Weeks 1-4)
1. Data loading utilities
2. NumPy statistical analysis
3. Pandas data cleaning
4. EDA on public dataset

### Phase 2: ML Basics Projects (Weeks 5-8)
1. Statistical hypothesis testing analysis
2. Feature engineering pipeline
3. Multi-model comparison (regression vs classification)
4. Ensemble model with hyperparameter tuning

### Phase 3: Deep Learning Projects (Weeks 9-12)
1. Neural network on MNIST
2. CNN with transfer learning on image data
3. LSTM for time series forecasting
4. ML model deployed as FastAPI service

### Phase 4: Capstone Project (Weeks 13-16)
1. Real-world ML project end-to-end
   - Data exploration and cleaning
   - Feature engineering
   - Model selection and optimization
   - Evaluation and error analysis
   - Deployment and monitoring
   - Production documentation

---

## Dataset Recommendations

### Weeks 4, 8, 12 (Analysis Projects)
- Iris, Titanic, Boston Housing, Digits
- UCI Machine Learning Repository datasets
- Kaggle datasets (tabular, beginner-friendly)

### Week 12+ (Capstone)
Choose one of:
- **Classification:** Customer churn, fraud detection, credit approval
- **Regression:** House price prediction, stock price forecasting
- **Clustering:** Customer segmentation, anomaly detection
- **NLP:** Sentiment analysis, text classification
- **Time Series:** Stock prices, weather forecasting, traffic prediction

---

## Key Libraries & Tools

| Week | Library | Purpose |
|------|---------|---------|
| 1-4 | NumPy, Pandas | Data manipulation |
| 4 | Matplotlib, Seaborn | Visualization |
| 5 | SciPy, Statsmodels | Statistical analysis |
| 6 | Scikit-learn | Feature engineering |
| 7-8 | Scikit-learn | Traditional ML |
| 9-12 | TensorFlow, Keras | Deep learning |
| 12+ | FastAPI | Model serving |
| 12+ | Docker | Containerization |
| 13-16 | MLflow | Model management |

---

## Interview Problem Topics

**Target: Understand and explain 20+ ML concepts**

### Traditional ML (Weeks 7-8)
- Linear regression vs logistic regression
- Decision trees and random forests
- Cross-validation and overfitting
- Feature selection and scaling
- Imbalanced datasets and metrics

### Deep Learning (Weeks 9-12)
- Neural network architecture
- Gradient descent and backpropagation
- CNN vs RNN use cases
- Transfer learning benefits
- Regularization techniques

### ML Systems (Week 16)
- Serving ML models
- A/B testing for models
- Model versioning
- Data pipelines
- Monitoring and retraining

Reference: [Interview Prep Supplement](../interview-prep-supplement.md)

---

## Capstone Project Structure

### Project Components
```
capstone-project/
├── README.md                    # Project overview
├── data/                        # Raw and processed data
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── 01-eda.ipynb            # Exploratory analysis
│   ├── 02-preprocessing.ipynb   # Data cleaning
│   ├── 03-modeling.ipynb        # Model training
│   └── 04-evaluation.ipynb      # Results and analysis
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── model.py
│   ├── train.py
│   └── predict.py
├── api/
│   ├── main.py                  # FastAPI application
│   └── Dockerfile
├── tests/
│   └── test_model.py
├── requirements.txt
└── docker-compose.yml
```

### Deliverables
1. **EDA Report:** 10-15 visualizations, key findings
2. **Data Pipeline:** Automated cleaning and feature engineering
3. **Model:** Best performing model with validation metrics
4. **API:** FastAPI endpoint for predictions
5. **Documentation:** README, docstrings, comments
6. **Deployment:** Docker container, deployment instructions

---

## What You'll Be Able To Do

### By Week 4
- Load and explore datasets
- Clean and preprocess data
- Create publication-quality visualizations
- Summarize key insights

### By Week 8
- Feature engineering from raw data
- Train and evaluate multiple models
- Select best performing model
- Explain model performance

### By Week 12
- Build deep neural networks
- Use transfer learning for images
- Handle sequential data with RNNs
- Deploy ML models as APIs

### By Week 16
- Execute complete ML projects end-to-end
- Work with real-world datasets
- Deploy models to production
- Explain decisions to stakeholders
- Discuss ML systems design in interviews

---

## Study Habits for Data Science

1. **Work with real data** - Kaggle, UCI ML, industry datasets
2. **Iterate quickly** - Try multiple approaches
3. **Visualize everything** - Understand data patterns
4. **Document insights** - Clear notebooks with markdown
5. **Version control models** - Track experiments
6. **Publish results** - Share notebooks on GitHub

---

## Checkpoints & Milestones

| Week | Milestone | Deliverable |
|------|-----------|-------------|
| 4 | EDA Mastery | Complete analysis report |
| 8 | ML Fundamentals | Multi-model comparison |
| 12 | Deep Learning & Serving | API-served model |
| 16 | Job Ready | Portfolio capstone project |

---

## Next Steps After Completion

1. **Specialize:** NLP, Computer Vision, Reinforcement Learning
2. **Advanced ML:** XGBoost, ensemble techniques, Bayesian methods
3. **ML Ops:** Model monitoring, A/B testing, production pipelines
4. **Research:** Reading papers, implementing novel approaches
5. **Domain expertise:** Apply ML to specific industry/problem

---

## Additional Resources

- **Quick Refreshers:** [Quick Reference Cards](../quick-reference-cards.md)
- **Core Learning:** [Python Study Guide](../python-study-guide.md)
- **ML Deep Dive:** [ML Workflow Guide](../ml-workflow-guide.md)
- **Deployment:** [Cloud & DevOps Guide](../cloud-devops-guide.md)
- **Interview Prep:** [Interview Prep Supplement](../interview-prep-supplement.md)

---

**Status: Ready to Start!** 🚀

Choose your start date and commit to the full 16 weeks. This path takes you from beginner to job-ready data scientist.
