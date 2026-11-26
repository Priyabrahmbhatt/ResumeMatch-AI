# ResumeMatch AI

An AI-powered resume analysis application that compares a PDF resume with a job description to identify matching skills, missing skills, and semantic similarity.

Built with Python, Streamlit, and Sentence Transformers.

## Features

- Upload and analyze PDF resumes
- Extract technical skills from resumes and job descriptions
- Identify matching and missing skills
- Calculate skill coverage
- Measure semantic similarity using sentence embeddings
- Download a personalized analysis report
- Interactive Streamlit interface

## Tech Stack

- Python
- Streamlit
- PyMuPDF
- Sentence Transformers
- scikit-learn
- pytest

## How It Works

1. Upload a PDF resume.
2. Paste a job description.
3. The application extracts text from the PDF.
4. A rule-based skill extractor identifies relevant skills.
5. The application compares the detected skills.
6. A pretrained Sentence Transformer model calculates semantic similarity.
7. Results are displayed in an interactive dashboard.

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ResumeMatch-AI.git
cd ResumeMatch-AI
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python -m streamlit run app.py
```

## Testing

Run the automated tests:

```bash
python -m pytest tests/ -v
```

## Limitations

- Skill extraction relies on a predefined dictionary and matching rules.
- Semantic similarity is not a prediction of hiring success.
- PDF text extraction works best with text-based PDFs.
- The application may miss relevant skills or produce incorrect matches.

## Privacy

The application is designed to process uploaded resumes for analysis without intentionally saving them to a database or sending them to the developer.

Hosting infrastructure may still process uploaded data.

## Future Improvements

- Support additional resume formats
- Improve skill extraction using NLP
- Add more comprehensive evaluation datasets
- Generate PDF reports
- Expand resume feedback capabilities

## Disclaimer

ResumeMatch AI is an educational portfolio project. Its results should not be interpreted as hiring recommendations or guarantees.