"""
LinkedIn ATS Resume Scanner
----------------------------
Takes job data from a LinkedIn scraper, scans the job description for keywords,
scores your resume against those keywords (0–100), suggests ATS-boosting bullet
points, and drafts a cover letter from your template.
 
Requirements:
    pip install anthropic pypdf python-docx requests
 
Usage:
    python ats_scanner.py
 
Configuration:
    Set your ANTHROPIC_API_KEY in the environment or in the CONFIG block below.
    Point RESUME_PATH and COVER_LETTER_TEMPLATE_PATH to your files.
    Provide job data via the LinkedIn scraper integration at the bottom.
"""