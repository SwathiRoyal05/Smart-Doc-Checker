# Smart Document Checker

A lightweight AI-assisted tool that analyzes multiple policy documents and automatically detects **contradicting rules** such as attendance requirements, submission deadlines, and notice periods.
The application helps organizations maintain **consistent policies across documents** and quickly identify mismatches.

Built using **Python, Streamlit, and rule-based text analysis**, the system provides instant feedback and generates downloadable reports for review.

---

## Features

* **Multi-document analysis** – Upload 2–3 documents (TXT or PDF) and analyze them together.
* **Automatic rule extraction** – Detects structured rules such as:

  * Attendance percentage
  * Submission deadlines
  * Notice periods
  * Team member limits
  * Presentation durations
* **Contradiction detection** – Flags conflicting rules across documents.
* **External policy monitoring** – Detects changes in external policy files and re-analyzes conflicts.
* **Report generation** – Download a summary report of detected contradictions and suggestions.
* **Fast execution** – Uses lightweight rule-based extraction instead of heavy ML models.

---

## Tech Stack

* **Python**
* **Streamlit** – Web interface
* **PyPDF2** – PDF text extraction
* **Regex (Regular Expressions)** – Rule extraction and comparison

---

## Project Structure

```
SmartDocChecker
│
├── app.py
│
├── datasets
│   ├── doc1.txt
│   ├── doc2.txt
│   └── doc3.txt
│
└── mock_external
    └── external_policy.txt
```

---

## Installation

Clone the repository and install dependencies.

```bash
git clone https://github.com/your-username/smart-document-checker.git
cd smart-document-checker
pip install streamlit PyPDF2
```

---

## Running the Application

Start the Streamlit server:

```bash
streamlit run app.py
```

---

## How It Works

1. **Upload Documents**
   Users upload 2–3 documents containing rules or policies.

2. **Text Extraction**

   * TXT files are read directly.
   * PDF files are processed using PyPDF2.

3. **Rule Detection**
   Regular expressions extract structured rules such as attendance percentages and deadlines.

4. **Conflict Detection**
   Extracted rules from each document are compared.
   If values differ, the system flags them as **contradictions**.

5. **External Policy Monitoring**
   The system checks an external policy file (`external_policy.txt`).
   If updated, it re-analyzes all documents with the new policy.

6. **Report Generation**
   A downloadable report summarizes contradictions and suggested fixes.

---

## Example Output

```
⚠️ Attendance conflict:
Doc 1: 75%
Doc 2: 65%
Doc 3: 80%
Doc 4: 70%

⚠️ Submission conflict:
Doc 1: 10 PM
Doc 2: 8 PM

⚠️ Notice conflict:
Doc 1: 2 weeks
Doc 3: 3 weeks
Doc 4: 2 weeks
```

Suggested Fix:

```
• Standardize attendance percentage across all documents
• Ensure submission deadlines are consistent
• Align notice period rules
```

---

## External Policy Updates

To simulate external updates:

1. Open:

```
mock_external/external_policy.txt
```

2. Modify rules such as attendance or deadlines.

3. Click **"Check External Policy"** in the application.

The system will detect the update and re-analyze documents.

---

## Use Cases

* **University policy verification**
* **HR compliance checks**
* **Legal document review**
* **Government regulation comparison**
* **Corporate guideline validation**

---

## Future Improvements

* Natural Language Processing (NLP) models for deeper semantic comparison
* Support for DOCX files
* Database-based document management
* Dashboard analytics for policy trends

---

## Author

**K Swathi Royal**

Project developed for **Denovate Hackathon - Microsoft Hyderabad**.
