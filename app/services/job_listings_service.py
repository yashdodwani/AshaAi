import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()


class JobListingsService:
    def __init__(self):
        self.indeed_api_key = os.getenv("INDEED_API_KEY", "")
        self.github_jobs_api_url = "https://jobs.github.com/positions.json"

    def get_job_listings(self, job_type="general", experience_level="all", query=""):
        """
        Get job listings based on parameters

        Args:
            job_type (str): Type of job (tech, marketing, etc.)
            experience_level (str): Level of experience (entry, mid, senior)
            query (str): Original user query for context

        Returns:
            dict: Job listings data and metadata
        """
        job_listings = []

        # Determine which API to use based on job type
        if self._is_tech_job(job_type, query):
            # Use GitHub Jobs API for tech jobs
            job_listings = self._fetch_from_github_jobs(job_type, experience_level)
        else:
            # Use Indeed API for non-tech jobs
            job_listings = self._fetch_from_indeed(job_type, experience_level)

        # Add placeholder data for testing/development
        if not job_listings:
            job_listings = self._get_placeholder_jobs(job_type, experience_level)

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "job_type": job_type,
            "experience_level": experience_level,
            "job_count": len(job_listings),
            "listings": job_listings
        }

    def _is_tech_job(self, job_type, query):
        """
        Determine if the job query is tech-related

        Args:
            job_type (str): Type of job
            query (str): Original user query

        Returns:
            bool: True if tech job, False otherwise
        """
        tech_keywords = ["developer", "engineer", "software", "programming",
                         "tech", "IT", "data", "analyst", "science"]

        # Check job_type and query for tech keywords
        job_type_lower = job_type.lower()
        query_lower = query.lower()

        for keyword in tech_keywords:
            if keyword.lower() in job_type_lower or keyword.lower() in query_lower:
                return True

        return False

    def _fetch_from_github_jobs(self, job_type, experience_level):
        """
        Fetch jobs from GitHub Jobs API

        Args:
            job_type (str): Type of job
            experience_level (str): Level of experience

        Returns:
            list: Job listings
        """
        # In a real implementation, this would make actual API calls
        # For now, return an empty list as placeholder
        try:
            # Example API call (commented out since we're using placeholders)
            # response = requests.get(f"{self.github_jobs_api_url}?description={job_type}")
            # if response.status_code == 200:
            #     return response.json()
            return []
        except Exception as e:
            print(f"Error fetching from GitHub Jobs API: {e}")
            return []

    def _fetch_from_indeed(self, job_type, experience_level):
        """
        Fetch jobs from Indeed API

        Args:
            job_type (str): Type of job
            experience_level (str): Level of experience

        Returns:
            list: Job listings
        """
        # In a real implementation, this would make actual API calls
        # For now, return an empty list as placeholder
        try:
            # Example API call (commented out since we're using placeholders)
            # headers = {"Authorization": f"Bearer {self.indeed_api_key}"}
            # response = requests.get(f"https://api.indeed.com/v2/jobs?q={job_type}", headers=headers)
            # if response.status_code == 200:
            #     return response.json()
            return []
        except Exception as e:
            print(f"Error fetching from Indeed API: {e}")
            return []

    def _get_placeholder_jobs(self, job_type, experience_level):
        """
        Get placeholder job listings for development/testing

        Args:
            job_type (str): Type of job
            experience_level (str): Level of experience

        Returns:
            list: Placeholder job listings
        """
        # Create job type specific placeholder data
        job_type_lower = job_type.lower()

        if "tech" in job_type_lower or "software" in job_type_lower:
            return [
                {
                    "id": "tech1",
                    "title": "Senior Software Developer",
                    "company": "TechInnovate",
                    "location": "Remote",
                    "description": "We are looking for an experienced software developer with expertise in Python and React.",
                    "salary_range": "$80,000 - $120,000",
                    "posting_date": "2025-04-20",
                    "application_url": "https://example.com/jobs/tech1",
                    "experience_required": "3-5 years",
                    "women_friendly_benefits": ["Flexible working hours", "Parental leave", "Mentorship program"]
                },
                {
                    "id": "tech2",
                    "title": "Data Scientist",
                    "company": "DataMinds",
                    "location": "Bangalore, India",
                    "description": "Join our diverse team of data scientists working on cutting-edge AI solutions.",
                    "salary_range": "$70,000 - $95,000",
                    "posting_date": "2025-04-22",
                    "application_url": "https://example.com/jobs/tech2",
                    "experience_required": "2-4 years",
                    "women_friendly_benefits": ["Remote work options", "Professional development", "Inclusive culture"]
                }
            ]
        elif "marketing" in job_type_lower:
            return [
                {
                    "id": "mkt1",
                    "title": "Digital Marketing Manager",
                    "company": "BrandGrowth",
                    "location": "Mumbai, India",
                    "description": "Lead our digital marketing initiatives and campaigns for major clients.",
                    "salary_range": "$60,000 - $80,000",
                    "posting_date": "2025-04-21",
                    "application_url": "https://example.com/jobs/mkt1",
                    "experience_required": "3-6 years",
                    "women_friendly_benefits": ["Flexible schedules", "Childcare assistance",
                                                "Women's leadership program"]
                }
            ]
        else:
            return [
                {
                    "id": "gen1",
                    "title": "HR Manager",
                    "company": "PeopleFirst",
                    "location": "Delhi, India",
                    "description": "Oversee HR operations and implement employee growth programs.",
                    "salary_range": "$55,000 - $75,000",
                    "posting_date": "2025-04-19",
                    "application_url": "https://example.com/jobs/gen1",
                    "experience_required": "3-5 years",
                    "women_friendly_benefits": ["Flex time", "Return-to-work program", "Leadership development"]
                },
                {
                    "id": "gen2",
                    "title": "Project Coordinator",
                    "company": "GlobalSolutions",
                    "location": "Hybrid - Chennai, India",
                    "description": "Coordinate project activities and ensure timely delivery of project milestones.",
                    "salary_range": "$40,000 - $55,000",
                    "posting_date": "2025-04-23",
                    "application_url": "https://example.com/jobs/gen2",
                    "experience_required": "1-3 years",
                    "women_friendly_benefits": ["Part-time options", "Child wellness days", "Mentorship"]
                }
            ]