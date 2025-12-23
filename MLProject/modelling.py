"""LinearSVC hyperparameter-tuned model with automatic MLflow logging.

This script trains a LinearSVC (SVM-based) model with hyperparameter tuning.
Logs parameters, metrics, model artifacts, and a confusion matrix to MLflow.
Designed to run as an MLflow Project for automated CI/CD pipelines.
"""
from pathlib import Path
from typing import Tuple
import os
import sys

import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold


def load_datasets(data_path: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Load train/test splits from the specified data directory.
    
    Args:
        data_path: Path to the dataset folder containing train_data.csv and test_data.csv
        
    Returns:
        Tuple of (X_train, X_test, y_train, y_test)
    """
    data_dir = Path(data_path)
    
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")
    
    train_csv = data_dir / "train_data.csv"
    test_csv = data_dir / "test_data.csv"
    
    if not train_csv.exists():
        raise FileNotFoundError(f"Training data not found: {train_csv}")
    if not test_csv.exists():
        raise FileNotFoundError(f"Test data not found: {test_csv}")
    
    train_df = pd.read_csv(train_csv)
    test_df = pd.read_csv(test_csv)

    feature_cols = [col for col in train_df.columns if col != "sentiment"]
    X_train = train_df[feature_cols]
    y_train = train_df["sentiment"]
    X_test = test_df[feature_cols]
    y_test = test_df["sentiment"]
    
    print(f"Loaded training data: {X_train.shape}")
    print(f"Loaded test data: {X_test.shape}")
    
    return X_train, X_test, y_train, y_test


def run(data_path: str = "sentiment_analysis_preprocessing", 
        experiment_name: str = "svc_tuning_production") -> None:
    """Run the model training pipeline.
    
    Args:
        data_path: Path to the dataset folder
        experiment_name: Name of the MLflow experiment
    """
    # Set experiment (MLflow will respect this when running via mlflow run)
    mlflow.set_experiment(experiment_name)
    
    # Load datasets
    X_train, X_test, y_train, y_test = load_datasets(data_path)

    # Define hyperparameter search space
    search_space = {
        "C": [0.001, 0.01, 0.1, 0.5, 1.0, 5.0],
        "class_weight": [None, "balanced"],
        "max_iter": [5000],
    }

    estimator = LinearSVC(random_state=42, dual=False)
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    grid = GridSearchCV(
        estimator,
        search_space,
        scoring="f1_macro",
        cv=cv,
        n_jobs=-1,
        refit=True,
        verbose=1,
    )

    print("Starting model training with hyperparameter tuning...")
    grid.fit(X_train, y_train)
    best_model = grid.best_estimator_

    # Log hyperparameters
    mlflow.log_params({f"best_{k}": v for k, v in grid.best_params_.items()})
    mlflow.log_param("n_features", X_train.shape[1])
    mlflow.log_param("model_type", "LinearSVC")
    mlflow.log_param("cv_splits", 3)
    
    # Log cross-validation score
    mlflow.log_metric("cv_best_f1_macro", grid.best_score_)

    # Evaluate on test set
    predictions = best_model.predict(X_test)
    test_acc = accuracy_score(y_test, predictions)
    test_f1 = f1_score(y_test, predictions, average="macro")
    test_precision = precision_score(y_test, predictions, average="macro")
    test_recall = recall_score(y_test, predictions, average="macro")
    
    # Log test metrics
    mlflow.log_metric("test_accuracy", test_acc)
    mlflow.log_metric("test_f1_macro", test_f1)
    mlflow.log_metric("test_precision_macro", test_precision)
    mlflow.log_metric("test_recall_macro", test_recall)

    # Log the trained model
    mlflow.sklearn.log_model(best_model, artifact_path="model")

    # Generate and log confusion matrix
    try:
        fig, ax = plt.subplots(figsize=(6, 5))
        ConfusionMatrixDisplay.from_predictions(
            y_test,
            predictions,
            ax=ax,
            cmap="Blues",
            colorbar=False,
        )
        ax.set_title("Confusion Matrix (Test) - LinearSVC")
        fig.tight_layout()
        mlflow.log_figure(fig, "confusion_matrix.png")
        plt.close(fig)
    except Exception as e:
        print(f"Warning: Could not generate confusion matrix: {e}")

    # Print summary
    print("TRAINING COMPLETE")
    print(f"Best parameters: {grid.best_params_}")
    print(f"Best CV F1 (macro): {grid.best_score_:.4f}")
    print(f"Test Accuracy: {test_acc:.4f}")
    print(f"Test F1 (macro): {test_f1:.4f}")
    print(f"Test Precision (macro): {test_precision:.4f}")
    print(f"Test Recall (macro): {test_recall:.4f}")


if __name__ == "__main__":
    # Parse arguments from command line or use defaults
    data_path = os.getenv("DATA_PATH", "sentiment_analysis_preprocessing")
    experiment_name = os.getenv("EXPERIMENT_NAME", "svc_tuning_production")
    
    run(data_path=data_path, experiment_name=experiment_name)
