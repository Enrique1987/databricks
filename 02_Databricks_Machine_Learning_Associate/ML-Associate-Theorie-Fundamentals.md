# Databricks Certified Machine Leaning Associate.

## Databricks


- [ ] [Data Preparation for Machine Learning](#data-preparation-for-machine-learning)
	- [ ] [Introduction to Data Preparation for Machine Learning](#introduction-to-data-preparation-for-machine-learning)
	- [ ] [Managing and Exploring Data](#managing-and-exploring-data)
	- [ ] [Data Preparation and Feature Engineering](#data-preparation-and-feature-engineering)
	- [ ] [Feature Store](#feature-store)


- [ ] [Machine Learning Model Development](#machine-learning-model-development)

- [ ] [Machine Learning Model Deployment](#machine-learning-model-deployment)

- [ ] [Machine Learning Module Operations](#machine-learning-module-operations)

- [ ] [Course Summary and Next Steps](#course-summary-and-next-steps)



## Udemy 
## Objetives

- Create Data Processing pipelines with Spark.  
- Build a tune machine learning models with Spark ML.  
- Track, Version, and deploy machine learning models with MLflow.  
- Perform distributed hyperparameter tuning with Hyperopt.  
- Scale the inference of single-node models with Spark.  

## Introduction

### Spark Review

#### Spark Structure Data
![Description of Image](img/01_Spark_Structure_Data.PNG)


### Delta Lake Review  

- Open-source Storage Layer.
- ACID Transactions.  
- Time Travel.  
- Schema enforcement and evolution.(validation schema + allow schema evolotuion over time.).  
- Parquet fromat.  
- Compatible with Apache Spark API.  

### Machine Learning Engineer

- What is machine learning ? Learn patterns and relationships in your data without explicitly programming them.  


#### Machine Learning Workflow

- 1. Define Business Use Case.  
- 2. Define Success, Constraints and infrastructure.  
- 3. Data Collation.  
- 4. Feature Engineering.  
- 5. Modeling.  
- 6. Deployment.  

(Loop)

#### Importance of Data Visualization

![importance of Visualization](img/02_Importance_Visualization.PNG)



## AutoML
AutoML, or Automated Machine Learning, is a process that automates the end-to-end tasks of applying machine learning to real-world problems.
It simplifies the model selection, preprocessing, feature engineering, and hyperparameter tuning steps, making machine learning more accessible and efficient, particularly for non-experts.

## Feature Store

A Feature Store is a centralized repository for storing, managing, and serving pre-processed features for machine learning models. 
It ensures consistency in feature calculations, reduces redundancy, and facilitates easier and more efficient access to features for training and inference across various ML models.

## MLflow

MLflow is an open-source platform for managing the end-to-end machine learning lifecycle, encompassing experiment tracking,
reproducible runs, and model packaging. It simplifies the process of tracking experiments, packaging code into reproducible runs,
 and sharing or deploying models across diverse platforms.
 
`MLflow components` MLflow Tracking for experiment logging, MLflow Projects for packaging ML code, MLflow Models for model packaging and sharingm and MLflow Registry for model versioning.

`What is MLflow used for` Used for managin the n-2-n ml lifecycle including experiment tracking, model development, deployment and lifecycle management.

`MLflow Tracking`: API for logging parameters, code version, metrics etc... Has a UI for reviewing and comparing runs and their results.

`MLflow Models`: Model packaging format and suit of tools that let you easyily deploy a trained model.

`MLflow Model Registry`: A Centralized model store, set of APIs, and UI focused on the appoval quality assurance.

`MLflow Projects`: A standard format for packaging reusable data science code.

`MLflow Recipes`: Predefined templates for developing high-quality models for a variety of common task, including classification and regression.

`MLflow used for`: USed to manage the ML lifecycle from initial model development through deployment and beyond tho sunsetting.


## EDA and Feature Engineering


### EDA should include:

- Display the first few rows of the dataset.  
- Determine the dimensions.  
- Summary of a DataFrame.  
- Number of non-null values in each column.  
- Retrieve the column names.  
- Examine the data types of each column.  
- Compute the pairwise correlation of columns.    
- Remove duplicate rows.  
- Summary statistics of numerical columns.  
- Check for missing values.  
- Visualize the Data.  
	- Correlation matrix and Heatmap.  
	- Scatter plot of two numercial variables.  
- Pandas profiling.  

### Feature Engineering

- Missing value inputation.  
	- Replace with mean in numerical
	- Replace with mode in objects
- Outlier removal  
	- IQR(Interquartile Range) Method  
	- Z-Score Method  
- Feature Creation.  
    When we need to add a new feature for analysis purpose
- Feature Scaling.
    Its the process of transformation numerical features in a dataset to a common scale. Its a crucial stept in data pre-procesing, help to bring the features to similar range of magnitude.
	Its important for:
		- Gradient-based optimization algorithms, such as gradient descent, converge faster when features are on a similar scale.  
		- Features with larger scales can dominate the learning process, leading to biased results.  
		- Many machine learning algorithms, such as K-nearest neighbors (KNN) and support vector machines (SVM), rely on calculating distances between data points.  
		- Some algorithms assumes that data is on a similar sclae.  
		```python
		from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        df[numerical_features] = scaler.fit_transform(df[numerical_features])
		```
- One-hot-encoding(Feature Encoding). 
    non numerical variables need to be numbericals `df = pd.get_dummies(data=df, drop_first=True)`
 
- Feature Selection.  
     Identify and select a subset of relevant features from the available set of features in a dataset.
	 1) Improve performance.  
	 2) Faster model training.  
	 3) Enhanced interpretability.  
	 4) Reduced dimensionality.  
- Feature Transformation (if needed).  
    The process of applying mathematical or statistical transformations to the existing features in a dataset to make
	them more suitable for a machine learning algorithm or to reveal underlying patterns in the data.
- Dimensionality Reduction (if needed).  
    ```python
	from sklearn.decomposition import PCA

    # Create the PCA model
    pca = PCA(n_components=2)

   # Fit the PCA model to X
   pca.fit(X)

   # Transform X to the new feature space
   X_reduced = pca.transform(X)

   # Print the shape of X_reduced
print(X_reduced.shape)


### Hyperopt
Hyperopt is a Python library used for optimizing machine learning model parameters and hyperparameters. It aims to find the best combination of parameters, 
from a predefined space, that results in the most accurate or efficient model for a given task. Hyperopt stands out for its use of Bayesian optimization techniques,
among others, to guide the search process, making it more efficient than simple grid search or random search methods.

