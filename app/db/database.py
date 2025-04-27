import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid
from dotenv import load_dotenv
import motor.motor_asyncio
from pymongo import MongoClient
from bson.objectid import ObjectId

# Load environment variables
load_dotenv()

# MongoDB connection - supports both sync and async options
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "asha_chatbot")


# For synchronous operations
def get_db_client():
    """Get MongoDB client for synchronous operations"""
    try:
        client = MongoClient(MONGODB_URI)
        return client[DB_NAME]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        # Fallback to file-based storage if MongoDB connection fails
        return None


# For asynchronous operations
async def get_async_db_client():
    """Get MongoDB client for asynchronous operations"""
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
        return client[DB_NAME]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        # Fallback to file-based storage if MongoDB connection fails
        return None


# File-based storage fallback (for development or if MongoDB is unavailable)
DATA_DIR = os.getenv("DATA_DIR", "data")
os.makedirs(DATA_DIR, exist_ok=True)


def save_conversation(conversation_data: Dict[str, Any]) -> str:
    """
    Save conversation to the database

    Args:
        conversation_data (dict): Conversation data to save

    Returns:
        str: ID of the saved conversation
    """
    try:
        # Try to save to MongoDB first
        db = get_db_client()
        if db:
            # Add timestamp if not present
            if "timestamp" not in conversation_data:
                conversation_data["timestamp"] = datetime.utcnow()

            # Insert conversation data
            result = db.conversations.insert_one(conversation_data)
            return str(result.inserted_id)

        # Fallback to file storage if MongoDB is unavailable
        raise Exception("MongoDB unavailable, using file storage")

    except Exception as e:
        print(f"MongoDB error: {e}. Using file storage fallback.")

        # Generate a unique ID for the conversation
        conversation_id = str(uuid.uuid4())

        # Add ID to conversation data
        conversation_data["_id"] = conversation_id

        # Create user directory if it doesn't exist
        user_id = conversation_data.get("user_id", "unknown")
        user_dir = os.path.join(DATA_DIR, user_id)
        os.makedirs(user_dir, exist_ok=True)

        # Save conversation to file
        file_path = os.path.join(user_dir, f"{conversation_id}.json")
        with open(file_path, "w") as f:
            json.dump(conversation_data, f, default=str)

        return conversation_id


def get_user_conversations(user_id: str) -> List[Dict[str, Any]]:
    """
    Get all conversations for a specific user

    Args:
        user_id (str): User ID

    Returns:
        list: List of conversation data dictionaries
    """
    try:
        # Try to get from MongoDB first
        db = get_db_client()
        if db:
            conversations = list(db.conversations.find({"user_id": user_id}))
            # Convert ObjectId to string for JSON serialization
            for conv in conversations:
                if "_id" in conv and isinstance(conv["_id"], ObjectId):
                    conv["_id"] = str(conv["_id"])
            return conversations

        # Fallback to file storage if MongoDB is unavailable
        raise Exception("MongoDB unavailable, using file storage")

    except Exception as e:
        print(f"MongoDB error: {e}. Using file storage fallback.")

        # Get conversations from file storage
        user_dir = os.path.join(DATA_DIR, user_id)
        if not os.path.exists(user_dir):
            return []

        conversations = []
        for filename in os.listdir(user_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(user_dir, filename)
                try:
                    with open(file_path, "r") as f:
                        conversation = json.load(f)
                        conversations.append(conversation)
                except Exception as file_error:
                    print(f"Error reading file {file_path}: {file_error}")

        return conversations


def get_conversation_by_id(conversation_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a specific conversation by ID

    Args:
        conversation_id (str): Conversation ID

    Returns:
        dict or None: Conversation data if found, None otherwise
    """
    try:
        # Try to get from MongoDB first
        db = get_db_client()
        if db:
            # Try with ObjectId first (MongoDB's native ID format)
            try:
                object_id = ObjectId(conversation_id)
                conversation = db.conversations.find_one({"_id": object_id})
                if conversation:
                    conversation["_id"] = str(conversation["_id"])
                    return conversation
            except:
                # If conversion to ObjectId fails, try with string ID
                conversation = db.conversations.find_one({"_id": conversation_id})
                return conversation

        # Fallback to file storage if MongoDB is unavailable
        raise Exception("MongoDB unavailable, using file storage")

    except Exception as e:
        print(f"MongoDB error: {e}. Using file storage fallback.")

        # Search for the conversation in file storage
        for user_dir in os.listdir(DATA_DIR):
            user_path = os.path.join(DATA_DIR, user_dir)
            if os.path.isdir(user_path):
                file_path = os.path.join(user_path, f"{conversation_id}.json")
                if os.path.exists(file_path):
                    try:
                        with open(file_path, "r") as f:
                            return json.load(f)
                    except Exception as file_error:
                        print(f"Error reading file {file_path}: {file_error}")

        return None


def save_performance_metrics(user_id: str, metrics: Dict[str, Any]) -> str:
    """
    Save performance metrics for a user

    Args:
        user_id (str): User ID
        metrics (dict): Performance metrics data

    Returns:
        str: ID of the saved metrics record
    """
    try:
        # Try to save to MongoDB first
        db = get_db_client()
        if db:
            # Add timestamp and user_id
            metrics["user_id"] = user_id
            metrics["timestamp"] = datetime.utcnow()

            # Insert metrics data
            result = db.performance_metrics.insert_one(metrics)
            return str(result.inserted_id)

        # Fallback to file storage if MongoDB is unavailable
        raise Exception("MongoDB unavailable, using file storage")

    except Exception as e:
        print(f"MongoDB error: {e}. Using file storage fallback.")

        # Generate a unique ID for the metrics record
        metrics_id = str(uuid.uuid4())

        # Add ID and timestamp to metrics data
        metrics["_id"] = metrics_id
        metrics["user_id"] = user_id
        metrics["timestamp"] = datetime.utcnow().isoformat()

        # Create metrics directory if it doesn't exist
        metrics_dir = os.path.join(DATA_DIR, "metrics")
        os.makedirs(metrics_dir, exist_ok=True)

        # Save metrics to file
        file_path = os.path.join(metrics_dir, f"{user_id}_{metrics_id}.json")
        with open(file_path, "w") as f:
            json.dump(metrics, f, default=str)

        return metrics_id


def get_user_performance_metrics(user_id: str) -> List[Dict[str, Any]]:
    """
    Get all performance metrics for a specific user

    Args:
        user_id (str): User ID

    Returns:
        list: List of performance metrics dictionaries
    """
    try:
        # Try to get from MongoDB first
        db = get_db_client()
        if db:
            metrics = list(db.performance_metrics.find({"user_id": user_id}))
            # Convert ObjectId to string for JSON serialization
            for metric in metrics:
                if "_id" in metric and isinstance(metric["_id"], ObjectId):
                    metric["_id"] = str(metric["_id"])
            return metrics

        # Fallback to file storage if MongoDB is unavailable
        raise Exception("MongoDB unavailable, using file storage")

    except Exception as e:
        print(f"MongoDB error: {e}. Using file storage fallback.")

        # Get metrics from file storage
        metrics_dir = os.path.join(DATA_DIR, "metrics")
        if not os.path.exists(metrics_dir):
            return []

        metrics = []
        for filename in os.listdir(metrics_dir):
            if filename.startswith(f"{user_id}_") and filename.endswith(".json"):
                file_path = os.path.join(metrics_dir, filename)
                try:
                    with open(file_path, "r") as f:
                        metric = json.load(f)
                        metrics.append(metric)
                except Exception as file_error:
                    print(f"Error reading file {file_path}: {file_error}")

        return metrics