from jobspy import scrape_jobs
from config import CONFIG

mock_jobs = [
    {
        "title": "Data Analyst",
        "company": "Google",
        "location": "New York, NY",
        "job_url": "https://linkedin.com/jobs/view/1",
        "description": "Analyze large datasets using SQL and Python.",
        "salary": "$90,000 - $120,000",
        "date_posted": "2026-04-28"
    },
    {
        "title": "Senior Data Scientist",
        "company": "Meta",
        "location": "Remote",
        "job_url": "https://linkedin.com/jobs/view/2",
        "description": "Build machine learning models and deploy to production.",
        "salary": "$130,000 - $180,000",
        "date_posted": "2026-04-27"
    },
    {
        "title": "Machine Learning Engineer",
        "company": "Amazon",
        "location": "Seattle, WA",
        "job_url": "https://linkedin.com/jobs/view/3",
        "description": "Develop ML pipelines using AWS and Python.",
        "salary": "$140,000 - $190,000",
        "date_posted": "2026-04-26"
    },
    {
        "title": "Data Analyst",
        "company": "Startup Inc",
        "location": "Austin, TX",
        "job_url": "https://linkedin.com/jobs/view/4",
        "description": "Create dashboards and perform ad-hoc analysis.",
        "salary": "$80,000 - $100,000",
        "date_posted": "2026-04-25"
    }
]


async def getLinkedinJobs(search_term: str) -> list:
#   return [job for job in mock_jobs if search_term.lower() in job["title"].lower()]
  jobs = scrape_jobs(
    site_name=["linkedin", "indeed"], # "glassdoor", "bayt", "naukri", "bdjobs"
    search_term=search_term,
    location=CONFIG["location"],
    distance=CONFIG["distance"],  # miles
    results_wanted=CONFIG["results_wanted"],
    hours_old=CONFIG["hours_old"],
    country_indeed='USA',
    linkedin_fetch_description=True
    # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
  )

  print(f"Found {len(jobs)} jobs")
  print(jobs.head())
  return jobs.to_dict(orient="records")