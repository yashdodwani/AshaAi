import os
from dotenv import load_dotenv
from openai import OpenAI
import json

# Load environment variables
load_dotenv()

# Initialize OpenAI client with OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


class IntentManager:
    def __init__(self):
        self.model = "meta-llama/llama-4-maverick:free"

    def classify_intent(self, user_query):
        """
        Classify the user's intent using LLM to determine if it's a default or dynamic intent

        Args:
            user_query (str): The user's query

        Returns:
            dict: Contains intent classification and other metadata
        """
        prompt = f"""
        You are Asha, an AI assistant for JobsForHer Foundation that helps women with their careers.
        Classify the following user query into one of these categories:

        1. DEFAULT-GENDER_BIASED: If the query contains gender bias issues, concerns unique to women in workplace, or emotional content where the user needs motivation/inspiration.
        2. DEFAULT-NORMAL: General conversation, greeting, or simple questions about Asha or JobsForHer.
        3. DYNAMIC-JOB_LISTINGS: Any query about job opportunities, openings, vacancies, or career positions.
        4. DYNAMIC-EVENTS: Any query about events, workshops, webinars, or conferences.
        5. DYNAMIC-MENTORSHIP: Any query about mentoring, coaching, guidance, or professional development programs.

        Additionally, analyze the sentiment of the query (positive, negative, neutral, nervous, happy, etc.).

        User Query: "{user_query}"

        Format your response as a JSON with fields:
        - intent_type: (DEFAULT or DYNAMIC)
        - intent_category: (GENDER_BIASED, NORMAL, JOB_LISTINGS, EVENTS, or MENTORSHIP)
        - sentiment: (detected sentiment)
        - confidence: (value between 0 and 1)
        """

        try:
            completion = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://jobsforher.com",
                    "X-Title": "Asha AI Bot"
                },
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful intent classification assistant."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )

            # Parse the JSON response
            response_content = completion.choices[0].message.content
            intent_data = json.loads(response_content)

            return intent_data

        except Exception as e:
            print(f"Error classifying intent: {e}")
            # Fallback to default classification if API fails
            return {
                "intent_type": "DEFAULT",
                "intent_category": "NORMAL",
                "sentiment": "neutral",
                "confidence": 0.5
            }

    def route_intent(self, user_query):
        """
        Classify intent and return appropriate routing information

        Args:
            user_query (str): The user's query

        Returns:
            dict: Contains routing information including service to call
        """
        intent_data = self.classify_intent(user_query)

        routing_info = {
            "original_query": user_query,
            "intent_data": intent_data,
            "service": None,
            "parameters": {}
        }

        # Route based on intent classification
        if intent_data["intent_type"] == "DYNAMIC":
            if intent_data["intent_category"] == "JOB_LISTINGS":
                routing_info["service"] = "job_listings"
                # Extract potential job parameters (placeholders for now)
                routing_info["parameters"] = {
                    "job_type": "general",  # Will be refined by parameter extraction
                    "experience_level": "all"
                }

            elif intent_data["intent_category"] == "EVENTS":
                routing_info["service"] = "events"
                routing_info["parameters"] = {
                    "event_type": "all",
                    "timeframe": "upcoming"
                }

            elif intent_data["intent_category"] == "MENTORSHIP":
                routing_info["service"] = "mentorship"
                routing_info["parameters"] = {
                    "mentorship_type": "general",
                    "industry": "all"
                }
        else:  # DEFAULT type
            routing_info["service"] = "chatbot"
            routing_info["parameters"] = {
                "conversation_type": intent_data["intent_category"],
                "sentiment": intent_data["sentiment"]
            }

        return routing_info


# For testing
if __name__ == "__main__":
    intent_mgr = IntentManager()
    test_queries = [
        "I'm looking for software engineering jobs",
        "Are there any upcoming networking events?",
        "How can I find a mentor in the finance industry?",
        "I feel like I'm not taken seriously at meetings because I'm a woman",
        "Hi Asha, how are you today?"
    ]

    for query in test_queries:
        result = intent_mgr.route_intent(query)
        print(f"Query: {query}")
        print(f"Result: {result}\n")