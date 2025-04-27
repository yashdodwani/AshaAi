from fastapi import FastAPI, HTTPException, Depends, Body
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

# Import our services
from app.intent_manager import IntentManager

from app.services.chatbot import ChatBot
from app.services.job_listings_service import JobListingsService
from app.services.event_mentorship_service import EventsService, MentorshipService
from app.db.database import save_conversation, get_user_conversations

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Asha AI Chatbot",
    description="AI-powered virtual assistant for JobsForHer Foundation",
    version="1.0.0"
)

# Initialize services
intent_manager = IntentManager()
chatbot = ChatBot()
job_listings_service = JobListingsService()
events_service = EventsService()
mentorship_service = MentorshipService()


# Define request and response models
class ChatRequest(BaseModel):
    user_id: str
    query: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: Dict[str, Any]
    conversation_id: Optional[str] = None


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    """
    Main chat endpoint that processes user queries and returns appropriate responses
    """
    user_id = chat_request.user_id
    user_query = chat_request.query

    try:
        # Classify the intent of the user query
        routing_info = intent_manager.route_intent(user_query)

        # Route to appropriate service based on intent
        if routing_info["service"] == "job_listings":
            service_response = job_listings_service.get_job_listings(
                job_type=routing_info["parameters"].get("job_type", "general"),
                experience_level=routing_info["parameters"].get("experience_level", "all"),
                query=user_query
            )

            # Format the job listings for a chatbot response
            formatted_response = format_job_listings_response(service_response, user_id, user_query)
            response_data = formatted_response

        elif routing_info["service"] == "events":
            service_response = events_service.get_events(
                event_type=routing_info["parameters"].get("event_type", "all"),
                timeframe=routing_info["parameters"].get("timeframe", "upcoming")
            )

            # Format the events for a chatbot response
            formatted_response = format_events_response(service_response, user_id, user_query)
            response_data = formatted_response

        elif routing_info["service"] == "mentorship":
            service_response = mentorship_service.get_mentorship_programs(
                mentorship_type=routing_info["parameters"].get("mentorship_type", "general"),
                industry=routing_info["parameters"].get("industry", "all")
            )

            # Format the mentorship programs for a chatbot response
            formatted_response = format_mentorship_response(service_response, user_id, user_query)
            response_data = formatted_response

        else:  # Default to chatbot
            conversation_type = routing_info["parameters"].get("conversation_type", "NORMAL")
            sentiment = routing_info["parameters"].get("sentiment", "neutral")

            response_data = chatbot.generate_response(
                user_id=user_id,
                user_query=user_query,
                conversation_type=conversation_type,
                sentiment=sentiment
            )

        # Save the conversation to the database
        conversation_id = save_conversation(response_data)

        return {
            "response": response_data,
            "conversation_id": conversation_id
        }

    except Exception as e:
        # Log the error (in a production environment, use proper logging)
        print(f"Error processing chat request: {e}")

        # Return a friendly error response
        fallback_response = {
            "user_id": user_id,
            "user_query": user_query,
            "bot_reply": "I'm sorry, I encountered an issue processing your request. Please try again in a moment.",
            "query_summary": "Error processing query",
            "time": datetime.utcnow().isoformat(),
            "intent": "ERROR",
            "sentiment": "neutral"
        }

        return {
            "response": fallback_response,
            "conversation_id": None
        }


@app.get("/performance/{user_id}")
async def get_performance_metrics(user_id: str):
    """
    Get performance metrics for a specific user
    """
    try:
        # Retrieve user conversations
        conversations = get_user_conversations(user_id)

        # Calculate performance metrics
        metrics = calculate_performance_metrics(conversations)

        return {
            "user_id": user_id,
            "metrics": metrics
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving performance metrics: {str(e)}")


def calculate_performance_metrics(conversations):
    """
    Calculate performance metrics based on user conversations
    This is a placeholder implementation
    """
    # In a real implementation, this would analyze conversations and extract metrics
    # For now, return placeholder metrics

    # Count conversations by intent
    intent_counts = {}
    for conv in conversations:
        intent = conv.get("intent", "UNKNOWN")
        intent_counts[intent] = intent_counts.get(intent, 0) + 1

    # Calculate basic engagement metrics
    total_conversations = len(conversations)
    avg_query_length = sum(len(conv.get("user_query", "")) for conv in conversations) / max(1, total_conversations)

    # Placeholder for sentiment analysis
    sentiment_distribution = {
        "positive": 0.4,
        "neutral": 0.5,
        "negative": 0.1
    }

    return {
        "conversation_count": total_conversations,
        "intent_distribution": intent_counts,
        "average_query_length": avg_query_length,
        "sentiment_distribution": sentiment_distribution,
        "analysis": "User engagement is steady with a focus on job-related queries."
    }


def format_job_listings_response(job_data, user_id, user_query):
    """
    Format job listings data into a conversational response
    """
    listings = job_data.get("listings", [])
    job_count = len(listings)

    if job_count == 0:
        bot_reply = "I couldn't find any job listings matching your criteria at the moment. Would you like to try a different search or explore other career resources?"
    else:
        # Create a conversational summary of the job listings
        bot_reply = f"I found {job_count} job opportunities that might interest you:\n\n"

        for i, job in enumerate(listings[:3], 1):  # Limit to first 3 jobs for readability
            bot_reply += f"{i}. {job['title']} at {job['company']} ({job['location']})\n"
            bot_reply += f"   {job['description']}\n"
            bot_reply += f"   Salary range: {job['salary_range']}\n"
            bot_reply += f"   Experience required: {job['experience_required']}\n"

            # Highlight women-friendly benefits
            if job.get('women_friendly_benefits'):
                benefits = ', '.join(job['women_friendly_benefits'])
                bot_reply += f"   Women-friendly benefits: {benefits}\n"

            bot_reply += f"   Apply here: {job['application_url']}\n\n"

        if job_count > 3:
            bot_reply += f"...and {job_count - 3} more. Would you like me to show you more job listings or refine your search?"

        bot_reply += "\n\nIs there a specific job you'd like more information about?"

    return {
        "user_id": user_id,
        "user_query": user_query,
        "bot_reply": bot_reply,
        "query_summary": f"Job search: {job_data.get('job_type', 'general')}",
        "time": datetime.utcnow().isoformat(),
        "intent": "DYNAMIC-JOB_LISTINGS",
        "sentiment": "neutral",
        "job_data": job_data  # Include the full job data for reference
    }


def format_events_response(event_data, user_id, user_query):
    """
    Format events data into a conversational response
    """
    events = event_data.get("events", [])
    event_count = len(events)

    if event_count == 0:
        bot_reply = "I couldn't find any events matching your criteria at the moment. Would you like to try a different search or explore other resources?"
    else:
        # Create a conversational summary of the events
        bot_reply = f"I found {event_count} upcoming events that might interest you:\n\n"

        for i, event in enumerate(events[:3], 1):  # Limit to first 3 events for readability
            bot_reply += f"{i}. {event['title']} by {event['organizer']}\n"
            bot_reply += f"   {event['description']}\n"
            bot_reply += f"   Date: {event['date']} at {event['time']}\n"
            bot_reply += f"   Location: {event['location']}\n"

            # Add pricing information
            if event.get('is_free', False):
                bot_reply += f"   Free event\n"
            elif event.get('fee'):
                bot_reply += f"   Fee: {event['fee']}\n"

            # Add topics
            if event.get('topics'):
                topics = ', '.join(event['topics'])
                bot_reply += f"   Topics: {topics}\n"

            bot_reply += f"   Register here: {event['registration_url']}\n\n"

        if event_count > 3:
            bot_reply += f"...and {event_count - 3} more. Would you like me to show you more events or refine your search?"

    return {
        "user_id": user_id,
        "user_query": user_query,
        "bot_reply": bot_reply,
        "query_summary": f"Event search: {event_data.get('event_type', 'all')}",
        "time": datetime.utcnow().isoformat(),
        "intent": "DYNAMIC-EVENTS",
        "sentiment": "neutral",
        "event_data": event_data  # Include the full event data for reference
    }


def format_mentorship_response(mentorship_data, user_id, user_query):
    """
    Format mentorship program data into a conversational response
    """
    programs = mentorship_data.get("programs", [])
    program_count = len(programs)

    if program_count == 0:
        bot_reply = "I couldn't find any mentorship programs matching your criteria at the moment. Would you like to try a different search or explore other career development resources?"
    else:
        # Create a conversational summary of the mentorship programs
        bot_reply = f"I found {program_count} mentorship programs that might interest you:\n\n"

        for i, program in enumerate(programs[:3], 1):  # Limit to first 3 programs for readability
            bot_reply += f"{i}. {program['title']} by {program['organization']}\n"
            bot_reply += f"   {program['description']}\n"
            bot_reply += f"   Format: {program['format']}\n"
            bot_reply += f"   Duration: {program['duration']}\n"
            bot_reply += f"   Application deadline: {program['application_deadline']}\n"

            # Add pricing information
            if program.get('is_free', False):
                bot_reply += f"   Free program\n"
            elif program.get('fee'):
                bot_reply += f"   Fee: {program['fee']}\n"

            # Add industries
            if program.get('industries'):
                industries = ', '.join(program['industries'])
                bot_reply += f"   Industries: {industries}\n"

            bot_reply += f"   Apply here: {program['application_url']}\n\n"

        if program_count > 3:
            bot_reply += f"...and {program_count - 3} more. Would you like me to show you more mentorship programs or refine your search?"

        bot_reply += "\n\nMentorship can be a powerful catalyst for career growth. Is there a specific program that interests you?"

    return {
        "user_id": user_id,
        "user_query": user_query,
        "bot_reply": bot_reply,
        "query_summary": f"Mentorship search: {mentorship_data.get('mentorship_type', 'general')}",
        "time": datetime.utcnow().isoformat(),
        "intent": "DYNAMIC-MENTORSHIP",
        "sentiment": "neutral",
        "mentorship_data": mentorship_data  # Include the full mentorship data for reference
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)