# src/job_pipeline/db/crud.py
from db.models import JobPosting, JobPostingSummary
from db.session import SessionLocal
from sqlalchemy.orm import Session

def save_job(job: dict, result: dict, db: Session):
  print(f"💾 Saving job: {job.get('title', '<Unknown Title>')} @ {job.get('company', '<Unknown Company>')}")

  created_session = False

  if db is None:
    db = SessionLocal()
    created_session = True

  try:
    new_job = JobPosting(
      job_title=job.get("title", "Unknown Title"),
      company=job.get("company", "Unknown Company"),
      job_url=job.get("job_url", "<Unknown URL>"),
      description=job.get("description", "<Unknown Description>"),
      location=job.get("location", "<Unknown Location>"),
      date_posted=job.get("date_posted", "<Unknown Date>"),
      company_url=job.get("company_url", "<Unknown Company URL>"),
      job_type=job.get("job_type", "<Unknown Job Type>"),
      job_level=job.get("job_level", "<Unknown Job Level>"),
      emails=job.get("emails", "<Unknown Emails>"),
      company_industry=job.get("company_industry", "<Unknown Industry>"),
      summary=JobPostingSummary(
        ats_keywords=result.get("ats_keywords", []),
        score=result.get("score", 0),
        score_rationale=result.get("score_rationale", ""),
        matched_keywords=result.get("matched_keywords", []),
        missing_keywords=result.get("missing_keywords", []),
        strengths=result.get("strengths", []),
        weaknesses=result.get("weaknesses", []),
        improvement_bullets=result.get("improvement_bullets", []),
        resume_text=result.get("resume_text", ""),
        cover_letter=result.get("cover_letter", "")
      )
    )
    db.add(new_job)
    db.commit()
  except Exception as e:
    print("ERROR:", e)
    db.rollback()

  finally:
    if created_session:
      db.close()

 