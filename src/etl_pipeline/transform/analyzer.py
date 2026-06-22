import re
import json
from openai import OpenAI
from config import CONFIG
from google import genai
import asyncio
import time


async def call_gemini_with_limits(manager, make_request, retries=5):
  for attempt in range(retries):
    key = await manager.get_key()

    try:
      return await make_request(api_key=key)

    except Exception as e:
      msg = str(e).lower()

      if any(x in msg for x in ["daily", "per day"]):
        await manager.mark_daily_limited(key)

      elif any(x in msg for x in ["rate", "429", "quota"]):
        await manager.mark_rate_limited(key)

      else:
        raise

      await asyncio.sleep(2 ** attempt)

  raise RuntimeError("All API keys failed after retries")


async def analyze_job(open_ai_client: OpenAI, gemini_manager, job: dict, resume_text: str, template_text: str) -> dict:
  """
  Run the full ATS pipeline for a single job posting.

  Returns a dict with:
    job_title, company, ats_keywords, score,
    matched_keywords, missing_keywords, improvement_bullets, cover_letter
  """
  job_title   = job.get("title", "Unknown Role")
  company     = job.get("company", "Unknown Company")
  location    = job.get("location", "")
  description = job.get("description", "")
  job_url     = job.get("job_url", "")

  print(f"\n{'═'*60}")
  print(f"  Analyzing: {job_title} @ {company}")
  print(f"{'═'*60}")

  # ── Step 1: Extract ATS keywords from job description ─────────────────
  print("  [1/3] Extracting ATS keywords...")

  combined_prompt = f"""
    You are a Targeted Resume scoring engine. Analyze the resume against the job description using the criteria below, then produce the output specified.

    Return ONLY valid JSON matching the schema exactly.

    Scoring factors:
    - hard skill match
    - years of experience
    - title alignment
    - quantified achievements

    Rules:
    - Extract at most 25 unique keywords.
    - Prioritize hard skills first.
    - Use concise phrases only.
    - Do not include explanations.
    - Do not include duplicate keywords.
    - missing_keywords must contain only keywords not present in matched_keywords.
    - strengths: max 5 items, concise.
    - weaknesses: max 5 items, concise.
    - No explanations outside the schema.

    Schema:
    {{
      "score": "integer",
      "top_keywords": ["string"],
      "matched_keywords": ["string"],
      "missing_keywords": ["string"],
      "strengths": ["string"],
      "weaknesses": ["string"]
    }}

    JOB DESCRIPTION:
    {description}

    RESUME:
    {resume_text}
  """

  raw_response = open_ai_client.responses.create(
    model=CONFIG["openai_model"],
    input=combined_prompt,
    reasoning={"effort":"minimal"},
    max_output_tokens=1200
  )

  print(raw_response)

  score_data = json.loads(raw_response.output_text)

  #keywords = extract_json(kw_response.choices[0].message.content)
  print(f"     Found {len(score_data.get('top_keywords', []))} top keywords")
 

  # ── Step 2: Score the resume ───────────────────────────────────────────
  print("  [2/3] Scoring resume...")
  score = score_data.get("score", 0)
  print(f"     ATS Score: {score}/100")

  bullets_and_cover_letter_data = {}
  if(score > CONFIG["cover_letter_threshold"]):
    # ── Step 3: Generate cover letter ──────────────────────────────
    print("  [3/3] Generating improvement bullets & cover letter...")

    bullets_and_cover_letter_prompt = f"""
      You are a expert resume and cover letter writer. Based on the following job description, resume, and ATS analysis, do two things: 
        
        Resume:
        {resume_text}
        
        Job Description:
        {description}
        
        ATS Analysis:
        {json.dumps(score_data, indent=2)}

        1. **Line-by-line rewrites**: For each missing keyword or skill, suggest a specific bullet point rewrite that incorporates that term while remaining truthful to the candidate's experience to increase the ATS score for this role. (only if score > {CONFIG['cover_letter_threshold']}):
            For example, "Managed a team" could become "Managed a team of 5 analysts to deliver monthly reports, improving decision-making speed by 20%." Only provide rewrites for bullets that have specific weaknesses — do not rewrite strong bullets that simply lack a keyword.
            Please provide no more than 5 bullet point rewrites, and only for the most important missing keywords (prioritize hard skills, then soft skills, then buzzwords).
        
        2. Draft a tailored cover letter using the template below.
          Replace {{{{ROLE}}}} with "{job_title}", {{{{COMPANY}}}} with "{company}",
          {{{{YOUR_NAME}}}} with "{CONFIG['your_name']}", and customize the body
          to highlight the matched keywords and address the missing ones.
        
          Cover Letter Template:
          {template_text}
        
          Return ONLY with a valid JSON object (no markdown, no extra text):
          {{
            "improvement_bullets": [
              "bullet point rewrite 1 here",
              "bullet point rewrite 2 here",
              "...up to 5 bullets"
            ],
            "cover_letter": "Full cover letter text here..."
          }}"""
  
    
    
    async def make_request(api_key: str):
      client = genai.Client(api_key=api_key)
      # Order of models to try
      models = CONFIG["gemini_models"]
    
      for model_id in models:
        try:
          # Your API call logic here
          return client.models.generate_content(
            model=model_id,
            contents=bullets_and_cover_letter_prompt
          )    
        except Exception as e:
          if "503" in str(e):
            print(f"Model {model_id} busy, trying next...")
            time.sleep(1) # Short pause before trying the next tier
            continue
          raise e # Raise other errors (like 400s) immediately

      

    response = await call_gemini_with_limits(
      gemini_manager,
      make_request
    )
    print(response)

    clean_text = re.sub(r"```json|```", "", response.text or "").strip()
    bullets_and_cover_letter_data = json.loads(clean_text)
    print(f"     Generated {len(bullets_and_cover_letter_data.get('improvement_bullets', []))} improvement bullets and cover letter.")
  else:
    print(f"  [3/3] ATS score below threshold ({CONFIG['cover_letter_threshold']}), skipping cover letter generation.")
  return {
    "job_title":            job_title,
    "company":              company,
    "location":             location,
    "job_url":              job_url,
    "ats_keywords":         score_data.get("top_keywords", []),
    "score":                score,
    "matched_keywords":     score_data.get("matched_keywords", []),
    "missing_keywords":     score_data.get("missing_keywords", []),
    "strengths":            score_data.get("strengths", []),
    "weaknesses":           score_data.get("weaknesses", []),
    "improvement_bullets":  bullets_and_cover_letter_data.get("improvement_bullets", []),
    "cover_letter":         bullets_and_cover_letter_data.get("cover_letter", "")
  }
   