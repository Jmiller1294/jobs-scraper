import os
import re
import json
from pathlib import Path


def save_results(result: dict, output_dir: Path):
  """Save analysis results to text and JSON files."""

  # Sanitize filename
  safe_name = re.sub(r"[^\w\-]", "_", f"{result['company']}_{result['job_title']}")[:60]

  # ── Human-readable report ─────────────────────────────────────────────
  report_path = os.path.join(output_dir, f"{safe_name}_report.txt")
  score = result["score"]
  bar   = "█" * (score // 5) + "░" * (20 - score // 5)

  with open(report_path, "w", encoding="utf-8") as f:
    f.write(f"ATS ANALYSIS REPORT\n{'='*60}\n")
    f.write(f"Role:     {result['job_title']}\n")
    f.write(f"Company:  {result['company']}\n")
    f.write(f"Location: {result['location']}\n")
    if result["job_url"]:
        f.write(f"URL:      {result['job_url']}\n")
    f.write(f"\n{'─'*60}\n")
    f.write(f"ATS SCORE: {score}/100\n")
    f.write(f"[{bar}] {score}%\n\n")

    f.write(f"{'─'*60}\n✅ MATCHED KEYWORDS ({len(result['matched_keywords'])})\n")
    for kw in result["matched_keywords"]:
        f.write(f"  • {kw}\n")

    f.write(f"\n{'─'*60}\n❌ MISSING KEYWORDS ({len(result['missing_keywords'])})\n")
    for kw in result["missing_keywords"]:
      f.write(f"  • {kw}\n")

    f.write(f"\n{'─'*60}\n💪 RESUME STRENGTHS\n")
    for s in result["strengths"]:
      f.write(f"  • {s}\n")

    f.write(f"\n{'─'*60}\n⚠️  RESUME GAPS\n")
    for w in result["weaknesses"]:
      f.write(f"  • {w}\n")

    f.write(f"\n{'─'*60}\n🚀 SUGGESTED RESUME BULLETS (add these to boost your score)\n")
    for b in result["improvement_bullets"]:
      f.write(f"  {b}\n")

    f.write(f"\n{'─'*60}\n📄 COVER LETTER\n{'─'*60}\n")
    f.write(result["cover_letter"])

  # ── Raw JSON ──────────────────────────────────────────────────────────
  json_path = os.path.join(output_dir, f"{safe_name}_data.json")
  with open(json_path, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

  # ── Cover letter as standalone file ───────────────────────────────────
  cl_path = os.path.join(output_dir, f"{safe_name}_cover_letter.txt")
  with open(cl_path, "w", encoding="utf-8") as f:
    f.write(result["cover_letter"])

  print(f"     Saved → {report_path}")


  return report_path
 
 
def print_summary(results: list):
  """Print a ranked summary table of all analyzed jobs."""
  print(f"\n{'═'*60}")
  print("  RESULTS SUMMARY (ranked by ATS score)")
  print(f"{'═'*60}")
  print(f"  {'Score':>5}  {'Company':<20}  {'Role'}")
  print(f"  {'─'*5}  {'─'*20}  {'─'*30}")

  for r in sorted(results, key=lambda x: x.get("score") or 0, reverse=True):
      score = r.get("score") or 0
      company_raw = r.get("company")
      job_title_raw = r.get("job_title")
      company = (company_raw if isinstance(company_raw, str) else "Unknown")[:20]
      job_title = (job_title_raw if isinstance(job_title_raw, str) else "Untitled")[:35]
      flag = "🟢" if score >= 80 else "🟡" if score >= 70 else "🔴"
      print(f"  {flag} {score:>3}/100  {company:<20}  {job_title}")
      
  print(f"{'═'*60}\n")