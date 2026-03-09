#  Smart Doc Checker – AI-Powered Document Verification Tool

 **Live Application:** https://smartdocchecker.streamlit.app

## Overview

**Smart Doc Checker** is an AI-powered document analysis tool designed to automatically review and verify documents for **consistency, accuracy, and policy compliance**.

The system analyzes uploaded documents, detects **contradictions between rules**, and provides **clear suggestions to resolve inconsistencies**.

This project was developed as part of a **hackathon innovation challenge**, focusing on improving document validation using **Natural Language Processing (NLP)** and **machine learning techniques**.

The application provides a **user-friendly web interface using Streamlit**, allowing users to upload documents and receive instant analysis reports.

---

#  Problem Statement

Organizations often maintain multiple documents such as **policies, guidelines, and notices**.
Over time these documents may become inconsistent or contradictory.

Examples:

* Different documents defining **different deadlines**
* Conflicting **attendance requirements**
* Mismatched **submission rules**

Manually reviewing documents to detect such inconsistencies is **time-consuming and error-prone**.

---

#  Solution

Smart Doc Checker provides an **automated AI solution** that:

* Analyzes multiple documents simultaneously
* Detects logical contradictions between rules
* Generates clear suggestions to resolve conflicts
* Provides downloadable verification reports

The tool improves **document quality, policy consistency, and compliance management**.

---

#  Key Features

✔ **Automated document analysis**

✔ **Contradiction detection between documents**

✔ **AI-powered rule extraction**

✔ **Suggested corrections for inconsistencies**

✔ **Interactive Streamlit interface**

✔ **Downloadable analysis reports**

✔ **External policy monitoring for updates**

---

#  AI & NLP Techniques Used

The system integrates multiple AI components:

### Natural Language Inference (NLI)

Model used:

```
facebook/bart-large-mnli
```

Purpose:

* Detect contradictions between statements in different documents
* Evaluate whether rules conflict with each other

---

### Rule Extraction

Important rules such as:

* Attendance requirements
* Deadlines
* Submission rules
* Notices

are automatically extracted from document text using **pattern matching and NLP techniques**.

---

### Suggestion Engine

Once conflicts are detected, the system generates **actionable suggestions** to help users resolve inconsistencies.

Example:

```
Conflict detected:
Attendance requirement: 75%
Attendance requirement: 80%

Suggested Fix:
Align the required percentages across documents to avoid contradictions.
```

---

#  Technologies Used

### Programming

* **Python**

### Machine Learning / NLP

* **Hugging Face Transformers**
* **BART Large MNLI Model**
* **PyTorch**

### Data Processing

* **Pandas**
* **Regex**

### Document Processing

* **PyPDF2**

### Interface

* **Streamlit**

### Visualization

* **Matplotlib**

---

#  Project Structure

```
smart-doc-checker
│
├── app.py
├── README.md
│
├── mock_external
    └── external_policy.txt

```

| File               | Description                                      |
| ------------------ | ------------------------------------------------ |
| `app.py`           | Main Streamlit application                       |
| `mock_external/`   | External policy documents for monitoring updates |
| `README.md`        | Project documentation                            |

---

#  Installation

Clone the repository:

```bash
git clone https://github.com/K-Anusha-13/smart-doc-checker.git
cd smart-doc-checker
```

---

#  Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will launch in your browser.

---

#  Example Workflow

1. Upload **2–3 documents (PDF or TXT)**
2. The system extracts text and identifies important rules
3. AI model analyzes rules across documents
4. Contradictions are detected
5. Suggestions are generated to resolve conflicts
6. A **downloadable report** is generated

---

#  Example Output

Example conflict:

```
Conflict between Doc 1 (attendance: 75%)
and Doc 2 (attendance: 80%)
```

Suggested fix:

```
Align attendance requirements across documents to avoid policy conflicts.
```

---

#  Future Improvements

* Support **Word (.docx) documents**
* Real-time document monitoring
* Integration with **enterprise document management systems**
* Advanced grammar and compliance analysis
* Cloud deployment and API integration

---
##  Developed For

Hackathon Submission – Denovate(Miscrosoft Hyderabad)
---
