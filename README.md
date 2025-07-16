# 🛠️ Bug Fixer - Hybrid Retriever System

This project implements a **hybrid retriever system** to identify similar bug reports and return root causes, fixes, and descriptions using both **TF-IDF** and **sentence embeddings**.

---

## 📁 Project Structure

```
├── Clean_Code.py                 # Preprocessing script to clean descriptions
├── data_ingest.py               # Ingests data, computes embeddings + TF-IDF, and stores in MongoDB
├── retriever.py                 # Hybrid retriever using TF-IDF + embeddings
├── query_issue.py               # Accepts a new issue and queries MongoDB for similar cases
├── embedding_model/             # Saved sentence transformer model
├── tfidf_vectorizer.pkl         # Saved TF-IDF model
├── ultra_refined_descriptions.xlsx # Raw input Excel file
├── .gitignore                   # Ignored files/folders (venv, models, Excel, etc.)
```

---

## 🔄 Workflow

1. **Preprocess Data**
   - Run `Clean_Code.py` to clean or refine the `"Detailed Description"` and save the cleaned Excel.

2. **Ingest Cleaned Data**
   - Run `data_ingest.py` to:
     - Read the Excel file
     - Generate sentence embeddings and TF-IDF vectors
     - Store everything in MongoDB (`hybrid_retriever.issues`)

3. **Query the System**
   - Use `query_issue.py` to input a new issue query.
   - The script retrieves the most similar historical issues based on semantic and keyword similarity.

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/mominarashad/Bug_fixer.git
cd Bug_fixer
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

(You can generate `requirements.txt` using `pip freeze > requirements.txt` after setup.)

---

## 🧪 Run the System

### Step 1: Clean Descriptions
```bash
python Clean_Code.py
```

### Step 2: Ingest Data to MongoDB
```bash
python data_ingest.py
```

### Step 3: Query Similar Issues
```bash
python query_issue.py
```

---

### Step 4:Run the FastApi Endpoint
```bash
uvicorn api:app --reload
```

---

## 💡 Sample Query Output

```bash
 Result 1 (Score: 0.8762)
 Summary: Crash on missing config
 Root Cause: Config loader fails when default is not set
 Fix: Add fallback in config parser
 Description: App crashes if VAR_ENV is undefined in staging
```

---

## 🗃️ MongoDB Details

- **Database**: `hybrid_retriever`
- **Collection**: `issues`
- Stores:
  - Original issue text
  - TF-IDF vector
  - Embedding vector

---

## 📌 .gitignore Highlights

This project ignores:
- `venv/`, `.pkl`, `.xlsx`, `embedding_model/`
- `__pycache__/`, temporary Excel files like `~$...`

---
