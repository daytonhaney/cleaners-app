# Cleaners App v1.1.0 Release Files

## What's New in v1.5.0

### ✨ New Features
- **PDF Export**: Export daily transaction reports to professional PDF format
- **CLI PDF Options**: `--export-pdf` flag for both main and demo commands
- **Enhanced User Interface**: Prompt to save PDF after customer summaries
- **Professional Reports**: Include summary statistics and detailed customer transactions

### 🔧 Technical Improvements
- **ReportLab Integration**: Added professional PDF generation library
- **Rich PDF Layouts**: Professional formatting with company branding
- **Data Visualization**: Enhanced customer summary displays
- **Error Handling**: Robust PDF export error management

### 🐳 Container Updates
- **Docker Support**: Updated for PDF dependencies
- **Python 3.14**: Support for latest Python version
- **System Dependencies**: Added font rendering libraries for PDF generation

### 📦 Build Updates
- **Version**: 1.0.0 → 1.1.0
- **Dependencies**: Added `reportlab>=4.0.0`
- **Classifiers**: Added Office/Business and Utility categories
- **Scripts**: Added `cleaners-demo` CLI command

## 📋 Installation

### Option 1: Download Archive
```bash
# Download and extract
wget https://github.com/your-repo/cleaners-app/releases/download/v1.5.0/cleaners-app-v1.5.0.tar.gz
tar -xzf cleaners-app-v1.5.0.tar.gz
cd cleaners-app-v1.5.0

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### Option 2: Docker
```bash
docker build -t cleaners-app:v1.5.0 .
docker run -it -v $(pwd)/data:/app/data cleaners-app:v1.5.0
```

### Option 3: Production Executables
For immediate access to the production executables, visit [Dist](https://github.com/your-repo/cleaners-app/dist).

## ⚠️ System Requirements

- **Python**: 3.11+ (3.14 recommended)
- **Memory**: 512MB minimum
- **Storage**: 100MB 

## Documentation

- **User Manual**: Available via `--man` flag
- **Help System**: Comprehensive `--help` documentation
- **Demo Mode**: Interactive learning environment with `--generate-data`

