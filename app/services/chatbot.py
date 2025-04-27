import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize OpenAI client with OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


class ChatBot:
    def __init__(self):
        self.model = "meta-llama/llama-4-maverick:free"

    def generate_response(self, user_id, user_query, conversation_type, sentiment):
        """
        Generate a response to the user's query based on the conversation type and sentiment

        Args:
            user_id (str): User identifier
            user_query (str): The user's query
            conversation_type (str): GENDER_BIASED or NORMAL
            sentiment (str): Detected sentiment of the query

        Returns:
            dict: Response data including bot reply and metadata
        """
        system_prompt = self._get_system_prompt(conversation_type, sentiment)

        try:
            completion = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://jobsforher.com",
                    "X-Title": "Asha AI Bot"
                },
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ]
            )

            bot_reply = completion.choices[0].message.content

            # Prepare response data
            response_data = {
                "user_id": user_id,
                "user_query": user_query,
                "bot_reply": bot_reply,
                "query_summary": self._summarize_query(user_query),
                "time": datetime.utcnow().isoformat(),
                "intent": conversation_type,
                "sentiment": sentiment
            }

            return response_data

        except Exception as e:
            print(f"Error generating response: {e}")
            # Fallback response if API fails
            return {
                "user_id": user_id,
                "user_query": user_query,
                "bot_reply": "I apologize, but I'm having trouble connecting to my knowledge base right now. Could you please try again in a moment?",
                "query_summary": "Error processing query",
                "time": datetime.utcnow().isoformat(),
                "intent": conversation_type,
                "sentiment": sentiment
            }

    def _get_system_prompt(self, conversation_type, sentiment):
        """
        Get the appropriate system prompt based on conversation type and sentiment

        Args:
            conversation_type (str): GENDER_BIASED or NORMAL
            sentiment (str): Detected sentiment of the query

        Returns:
            str: System prompt for the LLM
        """
        if conversation_type == "GENDER_BIASED":
            return f"""
            You are Asha, an empathetic AI assistant for the JobsForHer Foundation that helps women with their careers.

            The user appears to be expressing concerns related to gender bias or challenges women face in the workplace.
            Their message has a {sentiment} sentiment.

            Your role is to:
            1. Validate their experience without generalizing about genders
            2. Provide factual, evidence-based responses that empower the user
            3. Suggest practical strategies or resources when appropriate
            4. Be supportive and motivational while remaining grounded in reality
            5. Never perpetuate stereotypes, even positive ones

            Keep your tone warm, supportive, and professional. Focus on facts and empowerment.
            """
        else:  # NORMAL conversation
            return f"""
            You are Asha, a friendly and professional AI assistant for the JobsForHer Foundation.

            The JobsForHer Foundation is dedicated to empowering women in their professional journeys
            by connecting them with career opportunities, mentorship, and skill development resources.

            Your role is to:
            1. Be helpful, informative, and engage in natural conversation
            2. Keep responses concise, gentle, and to the point
            3. Avoid using terms that could be insensitive or harmful
            4. Maintain a positive, supportive tone throughout the conversation

            Respond in a way that is warm and professional, focusing on being helpful.
            """

    def _summarize_query(self, user_query):
        """
        Generate a short summary of the user query for logging purposes

        Args:
            user_query (str): The user's query

        Returns:
            str: A short summary of the query
        """
        # For longer queries, we could use the LLM to summarize
        # For now, use a simple truncation method
        if len(user_query) <= 50:
            return user_query

        return user_query[:47] + "..."