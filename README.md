**Overview**
Candidate Matcher is an AI-powered application that matches uploaded resumes with a given job description and generates similarity scores along with an AI-generated summary using Google Gemma 2B IT model from Hugging Face.

**The app provides:**
**Resume Parsing** – Extracts text from uploaded resumes.
**Embedding & Similarity Scoring** – Uses embeddings to compare resumes with job descriptions.
**AI Summary **–  Generates a short, human-readable summary of how well a candidate matches the role.
**Interactive UI **  – Built with Streamlit, featuring a horizontal navigation bar for Dashboard, Create Match, Results, and Settings.
Features
Multiple Resume Uploads

**Structured Job Description Input**
Similarity Score Table
Full AI Summary visible by default
Hugging Face LLM integration with secure token storage via st.secrets
No Sidebar – Clean, wide layout

** Tech Stack**
Frontend & UI: Streamlit
Backend Logic: Python
AI/ML: Google Gemma 2B IT via Hugging Face Transformers
Embedding & Similarity: Sentence Transformers
Deployment: Streamlit Cloud

The Hugging Face API token is stored securely in Streamlit Secrets.
In modules/summarizer.py:
import streamlit as st
import os

HF_TOKEN = st.secrets["HF_TOKEN"]
os.environ["HF_TOKEN"] = HF_TOKEN
Note: Do not hardcode tokens in the codebase.

**Installation & Local Run**
# Clone the repo
git clone https://github.com/jp2501/candidate-matcher.git
cd candidate-matcher
# Create virtual environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
# Install dependencies
pip install -r requirements.txt
# Run the app
streamlit run app.py

**Deployment**
Push the repository to GitHub.
Deploy on Streamlit Cloud.
Add HF_TOKEN in Streamlit Secrets.
Share your Streamlit public link.

**Assumptions**
Uploaded resumes are in PDF format.
Job description input is provided in plain text.
Hugging Face model (google/gemma-2b-it) is available and accessible with the given token.

**Known Issues**
On first load, st.session_state.settings is initialized in app.py to avoid missing key errors.
The AI summary feature requires a valid Hugging Face token.
