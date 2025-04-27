import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()


class EventsService:
    def __init__(self):
        self.eventbrite_api_key = os.getenv("EVENTBRITE_API_KEY", "")
        self.meetup_api_key = os.getenv("MEETUP_API_KEY", "")

    def get_events(self, event_type="all", timeframe="upcoming"):
        """
        Get events based on parameters

        Args:
            event_type (str): Type of event (networking, workshop, webinar, etc.)
            timeframe (str): Time period for events (upcoming, this_week, this_month)

        Returns:
            dict: Events data and metadata
        """
        events = []

        # Call APIs to fetch events
        eventbrite_events = self._fetch_from_eventbrite(event_type, timeframe)
        meetup_events = self._fetch_from_meetup(event_type, timeframe)

        # Combine results
        events.extend(eventbrite_events)
        events.extend(meetup_events)

        # Add placeholder data for testing/development if no events found
        if not events:
            events = self._get_placeholder_events(event_type, timeframe)

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "timeframe": timeframe,
            "event_count": len(events),
            "events": events
        }

    def _fetch_from_eventbrite(self, event_type, timeframe):
        """
        Fetch events from Eventbrite API

        Args:
            event_type (str): Type of event
            timeframe (str): Time period for events

        Returns:
            list: Event listings
        """
        # In a real implementation, this would make actual API calls
        # For now, return an empty list as placeholder
        try:
            # Example API call (commented out since we're using placeholders)
            # headers = {"Authorization": f"Bearer {self.eventbrite_api_key}"}
            # response = requests.get("https://www.eventbriteapi.com/v3/events/search/", headers=headers)
            # if response.status_code == 200:
            #     return response.json().get("events", [])
            return []
        except Exception as e:
            print(f"Error fetching from Eventbrite API: {e}")
            return []

    def _fetch_from_meetup(self, event_type, timeframe):
        """
        Fetch events from Meetup API

        Args:
            event_type (str): Type of event
            timeframe (str): Time period for events

        Returns:
            list: Event listings
        """
        # In a real implementation, this would make actual API calls
        # For now, return an empty list as placeholder
        try:
            # Example API call (commented out since we're using placeholders)
            # params = {"key": self.meetup_api_key, "category": event_type}
            # response = requests.get("https://api.meetup.com/find/upcoming_events", params=params)
            # if response.status_code == 200:
            #     return response.json().get("events", [])
            return []
        except Exception as e:
            print(f"Error fetching from Meetup API: {e}")
            return []

    def _get_placeholder_events(self, event_type, timeframe):
        """
        Get placeholder event listings for development/testing

        Args:
            event_type (str): Type of event
            timeframe (str): Time period for events

        Returns:
            list: Placeholder event listings
        """
        # Generate dates based on timeframe
        today = datetime.now()
        next_week = today + timedelta(days=7)
        next_month = today + timedelta(days=30)

        # Create event type specific placeholder data
        event_type_lower = event_type.lower()

        if event_type_lower == "all" or "networking" in event_type_lower:
            return [
                {
                    "id": "evt1",
                    "title": "Women in Tech Networking Mixer",
                    "organizer": "JobsForHer Foundation",
                    "location": "Virtual",
                    "description": "Connect with other women in technology fields and build your professional network.",
                    "date": (today + timedelta(days=3)).strftime("%Y-%m-%d"),
                    "time": "18:00 - 20:00 IST",
                    "registration_url": "https://example.com/events/evt1",
                    "is_free": True,
                    "topics": ["Networking", "Technology", "Career Development"]
                },
                {
                    "id": "evt2",
                    "title": "Returning to Work After a Career Break",
                    "organizer": "WomenRestart",
                    "location": "Hyderabad, India",
                    "description": "In-person networking event focused on strategies for returning to the workforce after a career break.",
                    "date": (today + timedelta(days=10)).strftime("%Y-%m-%d"),
                    "time": "10:00 - 13:00 IST",
                    "registration_url": "https://example.com/events/evt2",
                    "is_free": False,
                    "fee": "₹500",
                    "topics": ["Career Breaks", "Networking", "Skill Development"]
                }
            ]
        elif "workshop" in event_type_lower or "webinar" in event_type_lower:
            return [
                {
                    "id": "evt3",
                    "title": "Resume Building Workshop for Women Professionals",
                    "organizer": "CareerAdvance",
                    "location": "Virtual",
                    "description": "Learn effective resume writing techniques tailored for women professionals returning to work or seeking advancement.",
                    "date": (today + timedelta(days=5)).strftime("%Y-%m-%d"),
                    "time": "14:00 - 16:00 IST",
                    "registration_url": "https://example.com/events/evt3",
                    "is_free": True,
                    "topics": ["Resume Building", "Career Development"]
                },
                {
                    "id": "evt4",
                    "title": "Leadership Skills Webinar Series",
                    "organizer": "Women Leaders Forum",
                    "location": "Virtual",
                    "description": "A three-part webinar series focusing on developing essential leadership skills for women in management positions.",
                    "date": (today + timedelta(days=7)).strftime("%Y-%m-%d"),
                    "time": "17:00 - 18:30 IST",
                    "registration_url": "https://example.com/events/evt4",
                    "is_free": False,
                    "fee": "₹1200 for full series",
                    "topics": ["Leadership", "Management", "Professional Development"]
                }
            ]
        else:
            return [
                {
                    "id": "evt5",
                    "title": "Women's Career Fair 2025",
                    "organizer": "JobsForHer Foundation",
                    "location": "Bangalore, India",
                    "description": "Annual career fair connecting women professionals with inclusive employers across industries.",
                    "date": (today + timedelta(days=20)).strftime("%Y-%m-%d"),
                    "time": "10:00 - 17:00 IST",
                    "registration_url": "https://example.com/events/evt5",
                    "is_free": True,
                    "topics": ["Job Fair", "Recruitment", "Career Opportunities"]
                }
            ]


class MentorshipService:
    def __init__(self):
        self.api_key = os.getenv("MENTORSHIP_API_KEY", "")

    def get_mentorship_programs(self, mentorship_type="general", industry="all"):
        """
        Get mentorship programs based on parameters

        Args:
            mentorship_type (str): Type of mentorship (one-on-one, group, etc.)
            industry (str): Industry focus (tech, finance, etc.)

        Returns:
            dict: Mentorship programs data and metadata
        """
        # In a real implementation, this would fetch from an API
        # For now, use placeholder data
        programs = self._get_placeholder_mentorship_programs(mentorship_type, industry)

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "mentorship_type": mentorship_type,
            "industry": industry,
            "program_count": len(programs),
            "programs": programs
        }

    def _get_placeholder_mentorship_programs(self, mentorship_type, industry):
        """
        Get placeholder mentorship program listings for development/testing

        Args:
            mentorship_type (str): Type of mentorship
            industry (str): Industry focus

        Returns:
            list: Placeholder mentorship program listings
        """
        industry_lower = industry.lower()

        if industry_lower == "all" or "tech" in industry_lower:
            return [
                {
                    "id": "ment1",
                    "title": "Women in Tech Mentorship Program",
                    "organization": "TechWomen Foundation",
                    "format": "One-on-one",
                    "description": "Connecting women in technology with experienced mentors to advance their careers.",
                    "duration": "6 months",
                    "application_deadline": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
                    "application_url": "https://example.com/mentorship/ment1",
                    "is_free": True,
                    "industries": ["Technology", "Software Development", "Data Science"]
                },
                {
                    "id": "ment2",
                    "title": "Tech Leadership Accelerator",
                    "organization": "WomenLead",
                    "format": "Group mentorship",
                    "description": "Group mentorship program designed to help women advance into technical leadership roles.",
                    "duration": "3 months",
                    "application_deadline": (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"),
                    "application_url": "https://example.com/mentorship/ment2",
                    "is_free": False,
                    "fee": "₹5000",
                    "industries": ["Technology", "Product Management", "Engineering Leadership"]
                }
            ]
        elif "finance" in industry_lower or "banking" in industry_lower:
            return [
                {
                    "id": "ment3",
                    "title": "Women in Finance Mentorship Circle",
                    "organization": "Finance Forward",
                    "format": "Group mentorship",
                    "description": "Monthly mentorship circles for women working in or aspiring to work in finance and banking.",
                    "duration": "Ongoing",
                    "application_deadline": "Rolling applications",
                    "application_url": "https://example.com/mentorship/ment3",
                    "is_free": True,
                    "industries": ["Finance", "Banking", "Investment"]
                }
            ]
        else:
            return [
                {
                    "id": "ment4",
                    "title": "Career Restart Mentorship Program",
                    "organization": "JobsForHer Foundation",
                    "format": "One-on-one",
                    "description": "Mentorship for women returning to the workforce after a career break.",
                    "duration": "4 months",
                    "application_deadline": (datetime.now() + timedelta(days=21)).strftime("%Y-%m-%d"),
                    "application_url": "https://example.com/mentorship/ment4",
                    "is_free": True,
                    "industries": ["All industries"]
                },
                {
                    "id": "ment5",
                    "title": "Executive Women's Mentorship Program",
                    "organization": "Women's Leadership Institute",
                    "format": "One-on-one + Group sessions",
                    "description": "High-level mentorship for women in senior management positions looking to advance to executive roles.",
                    "duration": "12 months",
                    "application_deadline": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                    "application_url": "https://example.com/mentorship/ment5",
                    "is_free": False,
                    "fee": "₹25,000",
                    "industries": ["All industries"]
                }
            ]