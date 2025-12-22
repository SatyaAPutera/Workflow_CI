# MLflow CI/CD Workflow - Sentiment Analysis

Automated CI/CD pipeline for training and deploying sentiment analysis models using MLflow and GitHub Actions.

## 📁 Project Structure

```
Workflow_CI/
├── .github/
│   └── workflows/
│       └── ml-training.yml          # GitHub Actions workflow
├── MLProject/                         # MLflow project directory
│   ├── MLProject                     # MLflow project definition
│   ├── conda.yaml                    # Conda environment specification
│   ├── conda_requirements.txt        # pip requirements
│   ├── modelling.py                  # Training script
│   └── sentiment_analysis_preprocessing/
│       ├── train_data.csv            # Training dataset
│       └── test_data.csv             # Test dataset
└── README.md                          # This file
```

## 🚀 Quick Start

### Local Development

1. **Install MLflow**:
```bash
pip install mlflow==3.8.0
```

2. **Run the MLflow Project locally**:
```bash
cd MLProject
mlflow run . -P experiment_name="svc_tuning_local"
```

3. **View MLflow UI**:
```bash
mlflow ui
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

### GitHub Actions (Automated CI/CD)

The workflow automatically triggers on:
- **Push to main branch**: Automatically runs model training
- **Manual trigger**: Use `workflow_dispatch` to manually start training with custom parameters

#### To manually trigger:
1. Go to Actions tab → "MLflow Model Training Pipeline"
2. Click "Run workflow"
3. (Optional) Enter custom experiment name

## 📋 Configuration

### MLProject File

The `MLProject` file defines:
- **Entry points**: `main` command runs `modelling.py`
- **Parameters**:
  - `data_path`: Path to dataset folder (default: `sentiment_analysis_preprocessing`)
  - `experiment_name`: MLflow experiment name (default: `svc_tuning_production`)

### Conda Environment

Python 3.10 with essential ML libraries:
- **scikit-learn**: Machine learning algorithms
- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **matplotlib**: Visualization
- **mlflow**: Experiment tracking

## 🔄 Workflow Details

### GitHub Actions Pipeline

```
1. Checkout Code
2. Setup Python 3.10
3. Install Dependencies
4. Create MLflow Directory
5. Run MLflow Project
6. Upload Artifacts (mlruns/)
7. Create Training Summary
8. Validate Model Artifacts
```

### Model Training Process

1. **Data Loading**: Loads preprocessed train/test splits from CSV
2. **Model Training**: LinearSVC with hyperparameter tuning via GridSearchCV
3. **Evaluation**: Logs accuracy, F1-score, precision, recall metrics
4. **Artifacts**: Saves trained model and confusion matrix visualization

## 📊 Outputs

After training, the following artifacts are generated:

```
mlruns/
└── <experiment_id>/
    └── <run_id>/
        ├── artifacts/
        │   ├── model/                    # Trained model (sklearn format)
        │   └── confusion_matrix.png      # Visualization
        ├── metrics/
        │   ├── cv_best_f1_macro
        │   ├── test_accuracy
        │   ├── test_f1_macro
        │   ├── test_precision_macro
        │   └── test_recall_macro
        └── params/
            ├── best_C
            ├── best_class_weight
            └── model_type
```

## 📈 Metrics Tracked

- **cv_best_f1_macro**: Best F1 score during cross-validation
- **test_accuracy**: Accuracy on test set
- **test_f1_macro**: Macro-averaged F1 score on test set
- **test_precision_macro**: Macro-averaged precision
- **test_recall_macro**: Macro-averaged recall

## 🔧 Advanced Usage

### Custom Parameters

Run with custom parameters locally:
```bash
cd MLProject
mlflow run . -P data_path="custom_data_path" -P experiment_name="custom_experiment"
```

### Docker Execution

Build and run in Docker:
```bash
cd MLProject
mlflow run . --backend docker --env-manager=virtualenv
```

### Remote Tracking Server

Configure MLflow to use a remote tracking server:
```bash
export MLFLOW_TRACKING_URI=http://your-server:5000
mlflow run .
```

## 🌟 Features

✅ **Automated Training**: Triggers on every commit to main branch
✅ **MLflow Integration**: Full experiment tracking and artifact management
✅ **GitHub Artifacts**: Stores training artifacts for 30 days
✅ **Workflow Summary**: Auto-generated summary on each run
✅ **Error Validation**: Checks if model artifacts were created
✅ **Parametrized Runs**: Support for custom experiment names
✅ **Reproducible**: Conda environment ensures consistency

## 📝 Requirements

- Python 3.10
- Git and GitHub account
- 500MB+ disk space for artifacts
- ~2-5 minutes runtime per training (local)
- ~5-10 minutes on GitHub Actions (includes setup)

## 🚨 Troubleshooting

### Issue: Data files not found
**Solution**: Ensure CSV files are in `sentiment_analysis_preprocessing/` directory

### Issue: MLflow not found
**Solution**: Install with `pip install mlflow==3.8.0`

### Issue: Workflow fails on GitHub
**Solution**: Check artifact upload limits and workflow permissions

## 🔐 Best Practices

1. **Version Control**: Always commit `MLProject` file changes
2. **Backup Data**: Keep dataset backups separate from repository
3. **Monitor Artifacts**: Regularly download old artifacts before they expire
4. **Test Locally**: Run `mlflow run` locally before pushing
5. **Experiment Tracking**: Use meaningful experiment names

## 📚 Additional Resources

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [MLflow Projects](https://mlflow.org/docs/latest/projects.html)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [scikit-learn LinearSVC](https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html)

## 📄 License

This project is part of SMSML Kriteria 3 implementation.

## ✨ Author

Created as part of Sentiment Analysis ML Workflow CI/CD Implementation
