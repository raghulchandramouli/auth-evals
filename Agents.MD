# AUTH-EVAL – Agents Specification

This document is used for agents to understand what's happening codebase

---

# 🎯 Purpose

AUTH-EVAL is a standardized evaluation framework for AI-Generated Image (AIGI) detection models.

The system is designed to:

* Evaluate multiple detection models
* Benchmark across multiple datasets
* Support robustness testing (JPEG, blur, resize, etc.)
* Produce reproducible CSV-based results
* Enable research-grade comparisons

---


# 🏗️ System Agents

Below is the mapping between directories and system agents.

| Directory     | Agent            | Responsibility                       |
| ------------- | ---------------- | ------------------------------------ |
| architecture/ | Model Agent      | Defines neural network architectures |
| artifacts/    | Checkpoint Agent | Stores trained model weights         |
| configs/      | Config Agent     | YAML configuration files for runs    |
| databunch/    | Dataset Agent    | Raw dataset storage                  |
| inferencers/  | Inference Agent  | Standardized model wrappers          |
| metrics/      | Metrics Agent    | Accuracy, F1, AUC, etc.              |
| transforms/   | Robustness Agent | Evaluation-time corruptions          |
| scripts/      | Utility Agent    | Metadata building & helpers          |
| results/      | Logging Agent    | CSV outputs                          |

---

# 🔹 1️⃣ Model Agent (architecture/)

Defines ONLY neural architectures.

### Rules:

* ❌ No dataset logic
* ❌ No metric computation
* ❌ No file writing
* ❌ No evaluation code

### Example:

```python
class Model(nn.Module):
    def forward(self, x):
        return logits
```

---

# 🔹 2️⃣ Inferencer Agent (inferencers/)

Wraps model architecture + checkpoint loading.

Every inferencer MUST implement:

```python
from PIL import Image

class BaseInferencer:
    def predict(self, image: Image.Image) -> dict:
        return {
            "real_prob": float,
            "fake_prob": float
        }
```

### Responsibilities:

* Load model weights
* Preprocess input image
* Run forward pass
* Return probabilities

### Constraints:

* Must not compute metrics
* Must not write CSV files
* Must not depend on specific dataset

---

# 🔹 3️⃣ Dataset Agent (databunch/ + scripts/)

Raw datasets are stored in `databunch/`.

All datasets must be converted into a unified metadata format before evaluation.

### Unified Metadata Format

All evaluation uses standardized CSV with columns:

```
image_path,label,generator,source,split,compression
```

Where:

* `label` → 0 = real, 1 = fake
* `generator` → sdxl, dalle3, midjourney, gan, etc.
* `source` → dataset name
* `split` → train / test
* `compression` → none / jpeg90 / resized256 etc.

Metadata building scripts live in:

```
scripts/build_metadata.py
```

---

# 🔹 4️⃣ Metrics Agent (metrics/)

Computes evaluation metrics.

### Required Metrics:

* Accuracy
* F1-score
* ROC-AUC

### Optional Metrics:

* Precision / Recall
* Confusion matrix
* ECE (Expected Calibration Error)
* Per-generator breakdown

Metrics must:

* Be dataset-agnostic
* Accept lists of predictions & labels
* Return dictionary

Example:

```python
def compute_metrics(y_true, y_pred, y_scores):
    return {
        "accuracy": float,
        "f1": float,
        "auc": float
    }
```

---

# 🔹 5️⃣ Robustness Agent (transforms/)

Applies evaluation-time corruptions.

Supported transforms:

* JPEG compression
* Gaussian blur
* Resize
* Noise injection

These transforms are applied during evaluation only.

Example modes:

```
clean
jpeg_90
resize_256
blur_1.0
```

---

# 🔹 6️⃣ Logging Agent (results/)

Stores benchmark outputs.

Structure:

```
results/
    opensource/
    inhouse/
```

Each evaluation appends a row to a CSV file:

```
model_name,dataset,accuracy,f1,auc,transform
```

---

# 🔹 7️⃣ Config Agent (configs/)

All runs must be config-driven.

Example YAML:

```yaml
model: model1
checkpoint: artifacts/model1/model1.pth
metadata_csv: metadata/master.csv
transform: clean
batch_size: 32
```

No hardcoded paths inside evaluation scripts.

---

# 🔁 Evaluation Flow

1. Load config
2. Load metadata CSV
3. Instantiate inferencer
4. Apply transform (if any)
5. Run predictions
6. Compute metrics
7. Save results to CSV

---

# 📊 Future Extensions

Planned additions:

* Cross-dataset generalization score
* Robustness leaderboard
* Per-generator performance table
* Failure case saving
* Calibration analysis
* Confidence histograms

---

# 🔐 Contribution Rules

When adding a new model:

1. Add architecture in `architecture/`
2. Add inferencer in `inferencers/`
3. Ensure predict() follows contract
4. Add config file

When adding a new dataset:

1. Place raw files in `databunch/`
2. Write metadata conversion script
3. Ensure CSV follows unified format

---

# 🧭 Final Philosophy

AIGI-EVAL is designed to be:

* Research-grade
* Modular
* Reproducible
* Extensible

If a feature breaks modularity, it should not be added.

---

**End of Agents Specification**
