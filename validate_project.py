#!/usr/bin/env python3
"""
Validation script for MLflow CI/CD project structure
Checks all required files and configurations
"""

import os
import sys
from pathlib import Path
import json

class ProjectValidator:
    def __init__(self, project_root="."):
        self.root = Path(project_root)
        self.errors = []
        self.warnings = []
        self.success = []
        
    def check_required_files(self):
        """Check if all required files exist"""
        print("\n📋 Checking Required Files...")
        
        required_files = {
            "MLProject/MLProject": "MLflow project manifest",
            "MLProject/conda.yaml": "Conda environment specification",
            "MLProject/modelling.py": "Model training script",
            "MLProject/conda_requirements.txt": "Python requirements",
            ".github/workflows/ml-training.yml": "Basic GitHub Actions workflow",
            ".github/workflows/ml-training-artifacts.yml": "Advanced workflow with artifacts",
            "Dockerfile": "Docker image definition",
            "docker-compose.yml": "Docker Compose configuration",
            ".gitignore": "Git ignore rules",
            "README.md": "Project documentation",
            "SETUP.md": "Setup guide",
        }
        
        for file_path, description in required_files.items():
            full_path = self.root / file_path
            if full_path.exists():
                size = full_path.stat().st_size
                self.success.append(f"✅ {file_path:<50} ({size:>6} bytes)")
            else:
                self.errors.append(f"❌ {file_path:<50} MISSING")
    
    def check_data_files(self):
        """Check if training data exists"""
        print("\n📊 Checking Data Files...")
        
        data_files = [
            "MLProject/sentiment_analysis_preprocessing/train_data.csv",
            "MLProject/sentiment_analysis_preprocessing/test_data.csv",
        ]
        
        for file_path in data_files:
            full_path = self.root / file_path
            if full_path.exists():
                size = full_path.stat().st_size / (1024 * 1024)  # Convert to MB
                self.success.append(f"✅ {file_path:<50} ({size:>6.2f} MB)")
            else:
                self.errors.append(f"❌ {file_path:<50} MISSING")
    
    def check_directory_structure(self):
        """Check required directory structure"""
        print("\n📁 Checking Directory Structure...")
        
        required_dirs = [
            "MLProject",
            "MLProject/sentiment_analysis_preprocessing",
            ".github",
            ".github/workflows",
        ]
        
        for dir_path in required_dirs:
            full_path = self.root / dir_path
            if full_path.is_dir():
                self.success.append(f"✅ {dir_path}/" )
            else:
                self.errors.append(f"❌ {dir_path}/ MISSING")
    
    def check_file_contents(self):
        """Check critical file contents"""
        print("\n📄 Checking File Contents...")
        
        # Check MLProject file has entry points
        mlproject_file = self.root / "MLProject/MLProject"
        if mlproject_file.exists():
            try:
                content = mlproject_file.read_text(encoding='utf-8', errors='ignore')
                if "entry_points" in content and "main" in content:
                    self.success.append("✅ MLProject file has entry_points")
                else:
                    self.warnings.append("⚠️  MLProject file missing entry_points")
            except:
                self.warnings.append("⚠️  Could not read MLProject file")
        
        # Check conda.yaml has dependencies
        conda_file = self.root / "MLProject/conda.yaml"
        if conda_file.exists():
            try:
                content = conda_file.read_text(encoding='utf-8', errors='ignore')
                if "dependencies" in content and "pip" in content:
                    self.success.append("✅ conda.yaml has proper dependencies")
                else:
                    self.warnings.append("⚠️  conda.yaml may be incomplete")
            except:
                self.warnings.append("⚠️  Could not read conda.yaml")
        
        # Check modelling.py has main script
        model_file = self.root / "MLProject/modelling.py"
        if model_file.exists():
            try:
                content = model_file.read_text(encoding='utf-8', errors='ignore')
                if "if __name__" in content and "mlflow" in content:
                    self.success.append("✅ modelling.py is properly structured")
                else:
                    self.warnings.append("⚠️  modelling.py may be incomplete")
            except:
                self.warnings.append("⚠️  Could not read modelling.py")
        
        # Check GitHub Actions workflows
        workflow_file = self.root / ".github/workflows/ml-training.yml"
        if workflow_file.exists():
            try:
                content = workflow_file.read_text(encoding='utf-8', errors='ignore')
                if "on:" in content and "jobs:" in content:
                    self.success.append("✅ ml-training.yml is valid GitHub Actions workflow")
                else:
                    self.warnings.append("⚠️  ml-training.yml may have issues")
            except:
                self.warnings.append("⚠️  Could not read ml-training.yml")
    
    def check_docker_files(self):
        """Check Docker-related files"""
        print("\n🐳 Checking Docker Configuration...")
        
        docker_file = self.root / "Dockerfile"
        if docker_file.exists():
            try:
                content = docker_file.read_text(encoding='utf-8', errors='ignore')
                if "FROM python:3.10" in content:
                    self.success.append("✅ Dockerfile uses Python 3.10")
                else:
                    self.warnings.append("⚠️  Dockerfile may have wrong Python version")
            except:
                self.warnings.append("⚠️  Could not read Dockerfile")
        
        compose_file = self.root / "docker-compose.yml"
        if compose_file.exists():
            try:
                content = compose_file.read_text(encoding='utf-8', errors='ignore')
                if "services:" in content:
                    self.success.append("✅ docker-compose.yml is properly structured")
                else:
                    self.warnings.append("⚠️  docker-compose.yml may have issues")
            except:
                self.warnings.append("⚠️  Could not read docker-compose.yml")
    
    def print_report(self):
        """Print validation report"""
        print("\n" + "="*70)
        print("VALIDATION REPORT - MLflow CI/CD Project Structure")
        print("="*70)
        
        if self.success:
            print("\n✅ PASSED CHECKS:")
            for msg in self.success:
                print(f"  {msg}")
        
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for msg in self.warnings:
                print(f"  {msg}")
        
        if self.errors:
            print("\n❌ FAILED CHECKS:")
            for msg in self.errors:
                print(f"  {msg}")
        
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"✅ Passed:  {len(self.success)}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        print(f"❌ Failed:  {len(self.errors)}")
        
        # Overall status
        if self.errors:
            print("\n❌ VALIDATION FAILED - Please fix errors above")
            return False
        elif self.warnings:
            print("\n⚠️  VALIDATION PASSED WITH WARNINGS")
            return True
        else:
            print("\n✅ VALIDATION PASSED - Project structure is complete!")
            return True
    
    def run_all_checks(self):
        """Run all validation checks"""
        print("🔍 Starting MLflow CI/CD Project Validation...")
        
        self.check_required_files()
        self.check_data_files()
        self.check_directory_structure()
        self.check_file_contents()
        self.check_docker_files()
        
        return self.print_report()

def main():
    validator = ProjectValidator()
    success = validator.run_all_checks()
    
    print("\n📚 Documentation Files:")
    print("  - README.md: Complete project documentation")
    print("  - SETUP.md: Installation and setup guide")
    print("  - Workflows: .github/workflows/ folder")
    
    print("\n🚀 Next Steps:")
    print("  1. Review README.md for project overview")
    print("  2. Check SETUP.md for detailed setup instructions")
    print("  3. Initialize git repository: git init")
    print("  4. Push to GitHub to enable CI/CD")
    print("  5. Monitor workflow runs in GitHub Actions")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
