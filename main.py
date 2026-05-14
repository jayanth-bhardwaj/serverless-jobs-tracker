import requests
from supabase import create_client

# --- CONFIGURATION ---
SUPABASE_URL = "https://byzdcvclssmtmtjojtrv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ5emRjdmNsc3NtdG10am9qdHJ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg3NTc1MDIsImV4cCI6MjA5NDMzMzUwMn0.i1pXqZXuNoDS_dcJr-lWcFZft2B6X_R-HiJzD70xcVA"
SERP_API_KEY = "083ea46784294cd633fe079a337a425c22aaa2378784e3d6fa9a53f6df01dc27" # Get this from serpapi.com

class JobSystem:
    def __init__(self):
        self.db = create_client(SUPABASE_URL, SUPABASE_KEY)

    def fetch_live_jobs(self, query="QA Engineer"):
        print(f"Searching for {query} jobs...")
        url = "https://serpapi.com/search.json"
        params = {
            "engine": "google_jobs",
            "q": query,
            "api_key": SERP_API_KEY
        }
        
        response = requests.get(url, params=params)
        return response.json().get("jobs_results", [])

    def save_to_cloud(self, jobs):
        for job in jobs[:5]:  # Let's just save the top 5 for now
            data = {
                "title": job.get("title"),
                "company": job.get("company_name"),
                "location": job.get("location"),
                "link": job.get("related_links", [{}])[0].get("link", "No link")
            }
            self.db.table("job listings").insert(data).execute()
        print(f"Successfully saved {len(jobs[:5])} live jobs to Supabase!")

# --- EXECUTION ---
if __name__ == "__main__":
    system = JobSystem()
    
    # 1. Get real data from the web
    live_jobs = system.fetch_live_jobs("Python Developer India")
    
    # 2. Send it to your Supabase project
    if live_jobs:
        system.save_to_cloud(live_jobs)
    else:
        print("No jobs found. Check your API Key!")