import os


CONFIG = {
  # Job role to search for and tailor the resume/cover letter to
  "search_terms": [
    "data analyst",
  ],
  "resume_map":[
    {"keywords": ["data analyst", "business intelligence", "data scientist", "analyst", "analytics", "intern", "specialist"], "path": "/Users/justin/Dev/jobs-scrapper/src/data/resumes/Data_Analyst_Resume.docx"},
    {"keywords": ["data engineer", "data architect", "solutions consultant", "software engineer"], "path": "/Users/justin/Dev/jobs-scrapper/src/data/resumes/Data_Engineer_Resume.docx"},
    {"keywords": ["analytics engineer"], "path": "/Users/justin/Dev/jobs-scrapper/src/data/resumes/Analytics_Engineer_Resume.docx"},
    {"keywords": ["executive assistant","executive administrative assistant", "administrative assistant", "administrative", "coordinator"], "path": "/Users/justin/Dev/jobs-scrapper/src/data/resumes/Executive_Administrative_Assistant_Resume.docx"}
  ],

  "location": "New York City Metropolitan Area",

  "results_wanted": 35,  # number of job listings to fetch and evaluate

  "hours_old": 1,  # only fetch jobs posted in the last X hours

  "distance": 30,  # miles

  # OpenAI API key (set OPENAI_API_KEY env var instead of hardcoding)
  "openai_api_key": os.getenv("OPENAI_API_KEY", "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"),

  "google_api_keys": [
    "AIzaSyAYCsuhlcHaCravRmmnFwsyNWjcyOkN8F8", 
    "AIzaSyD-53OT6apSDbi9oNctjgqA4lOV5OQB0oY",
    "AIzaSyCfBASzQ668v9Db1q7qmE0KdP6zAeT2fXM",
    "AIzaSyDyaUyOTspAbrgX0-iHiNtH7xefn5hVIa8",
    "AIzaSyCJHEDzHCk2KEI-0K-biuaLv26-sfSVR5U"
  ],

  # Path to your resume 
  "resume_path": ["data/resumes/Data_Analyst_Resume.docx","data/resumes/Data_Engineer_Resume.docx","data/resumes/Analytics_Engineer_Resume.docx"],

  # Path to your cover letter template (.txt or .docx)
  "cover_letter_template_path": "data/cover_letters/Cover_Letter_Template.docx",

  "cover_letter_text_path": "data/cover_letters/Cover_Letter_Body.txt",

  # Your name (used in cover letter)
  "your_name": "Justin Miller",

  # OpenAI model to use
  "openai_model": "gpt-5-mini",

  # gemini model to use
  "gemini_models": ["gemini-3.1-flash-lite", "gemini-2.5-flash-lite", "gemini-1.5-flash"],

  # Minimum ATS score to trigger cover letter generation (0–100)
  "cover_letter_threshold": 70,

  # Output folder for results
  "output_dir": "/results/ats_results",

  "output_resumes_dir": "results/resumes",

  "output_cover_letters_dir": "results/cover_letters",

  "email": {
    "sender":       "justin.alx.miller@gmail.com", # justin.alx.miller@gmail.com must be a valid email address (Gmail recommended for easy SMTP)
    "password":     "npfa lpkn qlnv sfxa", # app password for Gmail (not your main password)
    "recipient":    "justin.alx.miller@gmail.com", # can be same as sender or different
    "smtp_server":  "smtp.gmail.com", # Gmail SMTP server
    "smtp_port":    587, # Gmail SMTP port for TLS
    "min_score":    70,   # only include jobs at or above this score in digest
  }
}