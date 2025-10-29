# GitHub Actions Workflow Fixes

## Issue Summary

The GitHub Actions ML Pipeline workflow was failing with two critical errors:

1. **LFS Pointer File Issue**: The model file (`model.pkl`) was being downloaded as a Git LFS pointer text file instead of the actual binary file
2. **Version Mismatch**: scikit-learn version mismatch between model training (1.3.0) and loading (1.6.1)

### Error Details

```
_pickle.UnpicklingError: invalid load key, '\x0b'.
```

This error occurs when trying to unpickle a text file (LFS pointer) instead of a binary pickle file.

## Root Causes

### 1. Git LFS Not Properly Initialized

**Problem**: The workflow was checking out code without properly pulling LFS objects.

**Original Code**:
```yaml
- name: Checkout code (without LFS)
  uses: actions/checkout@v4
  with:
    lfs: false  # This disabled LFS!
```

**Impact**: The `model.pkl` file remained as a 134-byte text pointer instead of the 2.1MB binary model.

### 2. Scikit-learn Version Drift

**Problem**: No version pinning in the workflow, causing GitHub Actions to install the latest scikit-learn (1.6.1) instead of the version used for training (1.3.0).

**Warning**:
```
InconsistentVersionWarning: Trying to unpickle estimator DecisionTreeClassifier 
from version 1.3.0 when using version 1.6.1
```

## Solutions Implemented

### Fix 1: Proper LFS Checkout

**Updated Workflow**:
```yaml
steps:
  - name: Checkout code with LFS
    uses: actions/checkout@v4
    with:
      lfs: true  # Enable LFS checkout
  
  - name: Pull all LFS files
    run: |
      git lfs install
      git lfs pull  # Pull all LFS objects
```

**Key Changes**:
- Set `lfs: true` in checkout action
- Explicitly run `git lfs pull` to ensure all LFS files are downloaded
- Removed the `--include` filter that was limiting which files were pulled

### Fix 2: Version Pinning

**Added Environment Variables**:
```yaml
env:
  PYTHON_VERSION: '3.9'
  SCIKIT_LEARN_VERSION: '1.3.0'  # Match training version
```

**Updated Installation**:
```yaml
- name: Install dependencies with version pinning
  run: |
    python -m pip install --upgrade pip
    pip install scikit-learn==${{ env.SCIKIT_LEARN_VERSION }}
    pip install numpy pandas joblib
```

### Fix 3: Enhanced Debugging

**Added Comprehensive Checks**:
```yaml
- name: Debug - Check model file
  run: |
    echo "=== File Info ==="
    ls -lh model/saved_models/model.pkl
    
    echo "=== File Type ==="
    file model/saved_models/model.pkl
    
    echo "=== First 100 bytes ==="
    head -c 100 model/saved_models/model.pkl | od -An -tx1
    
    echo "=== Check if it's LFS pointer ==="
    if head -n 1 model/saved_models/model.pkl | grep -q "version https://git-lfs"; then
      echo "ERROR: This is still an LFS pointer file!"
      exit 1
    fi
```

**Benefits**:
- Catches LFS issues before attempting to load the model
- Provides clear error messages
- Shows file size to verify it's the actual binary (2.1MB vs 134 bytes)

### Fix 4: Docker Image Updates

**Updated Dockerfile**:
```dockerfile
# Install dependencies with scikit-learn version pinned
RUN pip install --no-cache-dir scikit-learn==1.3.0 && \
    pip install --no-cache-dir -r requirements.txt
```

**Added Health Check**:
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/metrics')"
```

## Verification Steps

### 1. Verify LFS Files Locally

```bash
# Check if file is an LFS pointer
head -n 1 model/saved_models/model.pkl

# Should output binary data, NOT:
# version https://git-lfs.github.com/spec/v1

# Check file size
ls -lh model/saved_models/model.pkl
# Should be ~2.1M, not 134 bytes
```

### 2. Test Model Loading

```bash
python -c "
import pickle
import sklearn
print(f'scikit-learn: {sklearn.__version__}')
with open('model/saved_models/model.pkl', 'rb') as f:
    model = pickle.load(f)
print(f'Model type: {type(model).__name__}')
"
```

Expected output:
```
scikit-learn: 1.3.0
Model type: RandomForestClassifier
```

### 3. Verify Docker Build

```bash
# Build image
docker build -t fraud-detector:test .

# Check scikit-learn version in container
docker run fraud-detector:test python -c "import sklearn; print(sklearn.__version__)"
# Should output: 1.3.0
```

## Best Practices Applied

### 1. Dependency Version Management

**Pin all critical dependencies**:
- Python version (3.9)
- scikit-learn version (1.3.0)
- All packages in requirements.txt

**Document version requirements**:
```python
# requirements.txt
scikit-learn==1.3.0
pandas==2.0.3
numpy==1.24.3
```

### 2. Git LFS Best Practices

**Always enable LFS in CI/CD**:
```yaml
uses: actions/checkout@v4
with:
  lfs: true
```

**Explicitly pull LFS objects**:
```bash
git lfs install
git lfs pull
```

**Verify LFS files before use**:
- Check file size
- Inspect file headers
- Validate binary format

### 3. CI/CD Debugging

**Add validation steps**:
- File existence checks
- Size verification
- Content inspection
- Version validation

**Clear error messages**:
- Descriptive step names
- Detailed output
- Exit with specific error codes

### 4. Docker Best Practices

**Separate dependency installation**:
- Install critical packages first
- Better caching
- Faster rebuilds

**Health checks**:
- Monitor container health
- Auto-restart on failure
- Integration testing

## Troubleshooting Guide

### Issue: "UnpicklingError: invalid load key"

**Cause**: Model file is an LFS pointer, not binary data

**Solution**:
```bash
git lfs install
git lfs pull
# Verify file size is >2MB
ls -lh model/saved_models/model.pkl
```

### Issue: "InconsistentVersionWarning"

**Cause**: scikit-learn version mismatch

**Solution**:
```bash
pip install scikit-learn==1.3.0
```

### Issue: Workflow fails on "Download trained model"

**Cause**: Artifact name mismatch

**Fix**: Ensure artifact names match:
```yaml
# Upload
name: fraud-detection-model

# Download
name: fraud-detection-model
```

## Testing the Fixes

### Local Testing

```bash
# 1. Clean checkout
git clone <repo-url>
cd <repo>

# 2. Install LFS and pull
git lfs install
git lfs pull

# 3. Create virtual environment with correct version
python3.9 -m venv venv
source venv/bin/activate
pip install scikit-learn==1.3.0
pip install -r requirements.txt

# 4. Test model loading
python model/model.py

# 5. Build and test Docker
docker build -t fraud-detector:test .
docker run -p 8000:8000 fraud-detector:test
```

### GitHub Actions Testing

1. **Push changes** to trigger workflow
2. **Monitor workflow** execution in Actions tab
3. **Check debug output** for file size verification
4. **Verify** all jobs complete successfully

## Migration Guide

If you're updating an existing project with similar issues:

### Step 1: Update Workflow File

Replace `.github/workflows/ml-pipeline.yml` with the corrected version that includes:
- LFS checkout enabled
- Version pinning
- Debugging steps

### Step 2: Update Dockerfile

Add scikit-learn version pinning:
```dockerfile
RUN pip install --no-cache-dir scikit-learn==1.3.0
```

### Step 3: Update Requirements

Pin all package versions in `requirements.txt`

### Step 4: Test Locally

Verify changes work locally before pushing

### Step 5: Deploy

Push changes and monitor the workflow execution

## Conclusion

The fixes ensure:

1. **Reliable LFS file handling** in CI/CD
2. **Version consistency** across environments  
3. **Proper error detection** and debugging
4. **Reproducible builds** in Docker
5. **Production-ready** deployment pipeline

## Additional Resources

- [Git LFS Documentation](https://git-lfs.github.com/)
- [GitHub Actions - actions/checkout](https://github.com/actions/checkout)
- [scikit-learn Model Persistence](https://scikit-learn.org/stable/model_persistence.html)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Last Updated**: October 29, 2025
**Author**: MLOps Team
**Version**: 2.0