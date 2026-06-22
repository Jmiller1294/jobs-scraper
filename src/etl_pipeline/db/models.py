from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship as Relationship

Base = declarative_base()

class JobPosting(Base):
  __tablename__ = 'job_postings'
  __table_args__ = {"schema": "jobs"}

  id = Column(Integer, primary_key=True)
  job_title = Column(String(100))
  summary = Relationship(
    "JobPostingSummary", 
    back_populates="job",
    uselist=False,              
    cascade="all, delete-orphan"
  )
  job_url = Column(String(255))
  company = Column(String(100))
  company_industry = Column(String(100))
  description = Column(Text)
  location = Column(String(100))  
  date_posted = Column(String(50))
  company_url = Column(String(255))
  job_type = Column(String(50))
  job_level = Column(String(50))
  emails = Column(Text)  # Store as JSON string
  

class JobPostingSummary(Base):
  __tablename__ = 'job_posting_summaries'
  __table_args__ = {"schema": "jobs"}

  id = Column(Integer, primary_key=True)
  job_id = Column(Integer, ForeignKey("jobs.job_postings.id"))
  job = Relationship("JobPosting", back_populates="summary")
  job_url = Column(String(255))
  ats_keywords = Column(Text)  # Store as JSON string
  score = Column(Integer)
  score_rationale = Column(Text)
  matched_keywords = Column(Text)  # Store as JSON string
  missing_keywords = Column(Text)  # Store as JSON string
  strengths = Column(Text)  # Store as JSON string
  weaknesses = Column(Text)  # Store as JSON string
  improvement_bullets = Column(Text)  # Store as JSON string
  resume_text = Column(Text)
  cover_letter = Column(Text)


