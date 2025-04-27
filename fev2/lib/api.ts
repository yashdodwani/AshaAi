// API utility functions for interacting with the backend

interface User {
  id: string
  email: string
  name?: string
}

interface ChatRequest {
  user_id: string
  query: string
  session_id?: string
}

interface ChatResponse {
  response: {
    user_id: string
    user_query: string
    bot_reply: string
    query_summary: string
    time: string
    intent: string
    sentiment: string
    job_data?: any
    event_data?: any
    mentorship_data?: any
  }
  conversation_id?: string
}

interface Conversation {
  id: string
  summary: string
  timestamp: string
  intent: string
}

// Base API URL - change this to your backend URL
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

// Authentication functions
export async function loginUser(email: string, password: string): Promise<User> {
  try {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || "Failed to login")
    }

    const data = await response.json()
    return data.user
  } catch (error) {
    console.error("Login error:", error)
    throw error
  }
}

export async function registerUser(name: string, email: string, password: string): Promise<User> {
  try {
    const response = await fetch(`${API_URL}/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, email, password }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || "Failed to register")
    }

    const data = await response.json()
    return data.user
  } catch (error) {
    console.error("Registration error:", error)
    throw error
  }
}

// Chat functions
export async function sendChatMessage(userId: string, query: string, sessionId?: string): Promise<ChatResponse> {
  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: userId,
        query,
        session_id: sessionId,
      } as ChatRequest),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || "Failed to send message")
    }

    return await response.json()
  } catch (error) {
    console.error("Chat error:", error)
    throw error
  }
}

// Get user conversations
export async function getUserConversations(userId: string): Promise<Conversation[]> {
  try {
    const response = await fetch(`${API_URL}/conversations/${userId}`)

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || "Failed to fetch conversations")
    }

    return await response.json()
  } catch (error) {
    console.error("Get conversations error:", error)
    throw error
  }
}

// Get performance metrics
export async function getUserPerformanceMetrics(userId: string): Promise<any> {
  try {
    const response = await fetch(`${API_URL}/performance/${userId}`)

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || "Failed to fetch performance metrics")
    }

    return await response.json()
  } catch (error) {
    console.error("Get performance metrics error:", error)
    throw error
  }
}
