from config import CONFIG
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]  
RESUME_LOOKUP = [ { "keywords": [kw.lower() for kw in r["keywords"]], "path": r["path"] } for r in CONFIG["resume_map"] ]
RESUME_CACHE: dict[str, bool] = {}


def get_resume_for_job(title: str) -> str:
  fallback_resume_path = BASE_DIR / CONFIG["resume_path"][0]
  title_lower = title.lower()

  for resume in RESUME_LOOKUP:
    if any(kw in title_lower for kw in resume["keywords"]):
      path = resume["path"]

      # Cache hit
      if path in RESUME_CACHE:
        return path if RESUME_CACHE[path] else fallback_resume_path

      # Validate file exists
      if Path(path).exists():
        RESUME_CACHE[path] = True
        return path
      else:
        print(f"⚠️ Resume not found: {path}")
        RESUME_CACHE[path] = False
        return fallback_resume_path

  print(f"⚠️ No resume matched for title: '{title}'")
  return fallback_resume_path 