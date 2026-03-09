# app.py - Smart Doc Checker Hackathon Project (Updated for Hugging Face)
# To run: pip install streamlit PyPDF2 transformers torch

import streamlit as st
from PyPDF2 import PdfReader
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import re

# -----------------------------
# Function to extract text from uploaded files
# -----------------------------
def extract_text_from_file(file):
    if file.type == "application/pdf":
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
        return text
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    else:
        st.error("Unsupported file type. Please upload PDF or TXT.")
        return ""

# -----------------------------
# Load models (cached after first run)
# -----------------------------
@st.cache_resource
def load_models():
    # BART-MNLI for contradiction detection
    nli_tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-mnli")
    nli_model = AutoModelForSequenceClassification.from_pretrained("facebook/bart-large-mnli")
    nli_pipe = pipeline(
        "text-classification",
        model=nli_model,
        tokenizer=nli_tokenizer,
        device=0 if torch.cuda.is_available() else -1,
        return_all_scores=True  # important to get scores for each label
    )

    # Simple text generation for suggestions (DistilGPT-2)
    suggestion_pipe = pipeline(
        "text-generation",
        model="distilgpt2",
        device=0 if torch.cuda.is_available() else -1
    )

    return nli_pipe, suggestion_pipe

# -----------------------------
# Extract simple rules from text
# -----------------------------
def extract_rules(text):
    rules = re.findall(
        r'(attendance|deadline|submit|notice|required):?\s*(\d+%|\d+ (PM|AM)|\d+ (week|month)s?|\d+ PM)',
        text, re.IGNORECASE
    )
    if not rules:
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if len(s.strip()) > 10][:5]
    return [f"{rule[0]}: {rule[1]}" for rule in rules]

# -----------------------------
# Detect contradictions
# -----------------------------
def find_contradictions(texts, threshold=0.6):
    nli_pipe, _ = load_models()
    all_rules = []
    for i, text in enumerate(texts):
        rules = extract_rules(text)
        all_rules.extend([(r, i) for r in rules])

    conflicts = []
    for j in range(len(all_rules)):
        for k in range(j+1, len(all_rules)):
            rule1, doc1 = all_rules[j]
            rule2, doc2 = all_rules[k]
            if doc1 != doc2:
                # Use NLI pipeline
                result = nli_pipe(f"{rule1} </s></s> {rule2}")
                # result is a list of dicts with 'label' and 'score'
                # Find label with max score
                max_label = result[0]
                if max_label['label'].lower() == "contradiction" and max_label['score'] > threshold:
                    conflicts.append(
                        f"Conflict between Doc {doc1+1} ('{rule1}') and Doc {doc2+1} ('{rule2}') "
                        f"(Confidence: {max_label['score']:.2f})"
                    )
    if not conflicts:
        return "No clear contradictions detected. Try docs with differing rules."
    return "\n".join(conflicts)

# -----------------------------
# Suggest fixes using text generation
# -----------------------------
#def suggest_fixes(conflicts):
#   _, suggestion_pipe = load_models()
#    prompt = f"Based on these document conflicts, suggest simple fixes:\n{conflicts}\nSuggestions:"
#    response = suggestion_pipe(prompt, max_length=150, num_return_sequences=1, temperature=0.7)
#    return response[0]['generated_text'].split("Suggestions:")[-1].strip()

# -----------------------------
# Suggest fixes based on detected conflicts (rule-based)
# -----------------------------
def suggest_fixes(conflicts):
    """
    Generate simple, actionable suggestions based on contradictions.
    This is rule-based and deterministic—no GPT hallucinations.
    """
    suggestions = []
    if not conflicts or "No clear contradictions" in conflicts:
        return "No suggestions needed. Documents are consistent."

    # Parse each conflict line
    for line in conflicts.split("\n"):
        # Check if the conflict mentions 'required'
        if "required" in line.lower():
            suggestions.append(
                "⚠️ Align the required percentages across all documents to avoid contradictions."
            )
        # Check if the conflict mentions 'deadline'
        elif "deadline" in line.lower():
            suggestions.append(
                "⚠️ Ensure deadlines are consistent across all documents."
            )
        # Check for 'submit', 'notice', or other keywords
        elif any(keyword in line.lower() for keyword in ["submit", "notice", "attendance"]):
            suggestions.append(
                "⚠️ Standardize submission rules and notices across documents."
            )
        else:
            # Fallback suggestion
            suggestions.append("⚠️ Review this conflict manually for clarity.")

    # Remove duplicates while preserving order
    seen = set()
    final_suggestions = []
    for s in suggestions:
        if s not in seen:
            final_suggestions.append(s)
            seen.add(s)

    return "\n".join(final_suggestions)


# -----------------------------
# Fetch external policy file
# -----------------------------
def fetch_external_doc():
    try:
        with open("mock_external/external_policy.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "No external policy file found. Create 'mock_external/external_policy.txt'."

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("📑 Smart Doc Checker (Free Edition)")
st.info("🔥 Uses Hugging Face models—no OpenAI API keys required!")

# Session state
if "docs_analyzed" not in st.session_state:
    st.session_state.docs_analyzed = 0
if "reports_generated" not in st.session_state:
    st.session_state.reports_generated = 0
if "total_cost" not in st.session_state:
    st.session_state.total_cost = 0.0
if "external_content" not in st.session_state:
    st.session_state.external_content = ""

# Sidebar
st.sidebar.title("📊 Usage Stats")
st.sidebar.write(f"Documents Analyzed: {st.session_state.docs_analyzed}")
st.sidebar.write(f"Reports Generated: {st.session_state.reports_generated}")
st.sidebar.write(f"Total Cost (Mock): ${st.session_state.total_cost:.2f}")

# File uploader
uploaded_files = st.file_uploader(
    "Upload 2-3 documents (PDF/TXT)", accept_multiple_files=True, type=["pdf", "txt"]
)

if uploaded_files and 2 <= len(uploaded_files) <= 3:
    texts = [extract_text_from_file(file) for file in uploaded_files]
    st.session_state.docs_analyzed += len(uploaded_files)
    st.session_state.total_cost += len(uploaded_files) * 0.10

    if st.button("🔍 Analyze Documents"):
        with st.spinner("Analyzing contradictions..."):
            conflicts = find_contradictions(texts)
            st.subheader("⚠️ Flagged Contradictions")
            st.write(conflicts)

            suggestions = suggest_fixes(conflicts)
            st.subheader("✅ Suggested Clarifications")
            st.write(suggestions)

            report = f"Smart Doc Checker Report\n\nContradictions:\n{conflicts}\n\nSuggestions:\n{suggestions}"
            st.download_button("⬇️ Download Report", data=report, file_name="doc_checker_report.txt")
            st.session_state.reports_generated += 1
            st.session_state.total_cost += 0.50

# External updates
st.subheader("🌐 Monitor External Updates")
st.write("Place a text file at `mock_external/external_policy.txt`. Update it, then click below:")

if st.button("🔄 Check for External Updates"):
    with st.spinner("Checking for updates..."):
        current_external = fetch_external_doc()
        if current_external != st.session_state.external_content:
            st.write("🔔 Update detected! Re-analyzing with external policy...")
            st.session_state.external_content = current_external
            if 'texts' in locals() and uploaded_files:
                all_texts = texts + [current_external]
                conflicts = find_contradictions(all_texts)
                st.subheader("⚠️ Updated Contradictions (with External)")
                st.write(conflicts)

                suggestions = suggest_fixes(conflicts)
                st.subheader("✅ Updated Suggestions")
                st.write(suggestions)

                updated_report = f"Updated Report with External Policy\n\nContradictions:\n{conflicts}\n\nSuggestions:\n{suggestions}"
                st.download_button("⬇️ Download Updated Report", data=updated_report, file_name="updated_doc_checker_report.txt")
                st.session_state.reports_generated += 1
                st.session_state.total_cost += 0.50
            else:
                st.warning("Upload documents first to analyze with external policy.")
        else:
            st.write("No new updates detected.")
