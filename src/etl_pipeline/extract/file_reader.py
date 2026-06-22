import os
import json
import re
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[2]  



def clean_resume_text(text):
  text = text.lower()

  # Add space before parentheses
  text = re.sub(r'\(', ' (', text)

  # Remove parentheses but keep content
  text = re.sub(r'[()]', '', text)

  # Normalize commas and spacing
  text = re.sub(r'[,/]', ' ', text)

  # Normalize whitespace
  text = re.sub(r'\s+', ' ', text)
  print(f"  🧹 Cleaned resume text length: {len(text)} characters")
  return text.strip()

def read_file(path: str) -> str:
  p = BASE_DIR / path
  print(f"📄 Reading file: {p}")
  """Read text from .txt, .pdf, or .docx files."""
  text = os.path.splitext(p)[1].lower()

  if text == ".txt":
    with open(p, "r", encoding="utf-8") as f:
      return clean_resume_text(f.read())
  raise ValueError(f"Unsupported file type: {text}. Use .txt, .pdf, or .docx")


def extract_json(text: str) -> dict:
  """Extract the first JSON object found in a Chat GPT response."""
  match = re.search(r"\{.*\}", text, re.DOTALL)
  if not match:
    raise ValueError("No JSON object found in Chat GPT response.")
  return json.loads(match.group())

