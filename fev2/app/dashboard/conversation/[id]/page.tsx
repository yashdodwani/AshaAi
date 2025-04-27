"use client"

import { useState, useEffect } from "react"
import { useParams, useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { ArrowLeft } from "lucide-react"
import { useAuth } from "@/lib/auth"

interface Conversation {
  id: string
  messages: {
    role: "user" | "assistant"
    content: string
    timestamp: string
  }[]
  summary: string
  intent: string
}

export default function ConversationPage() {
  const params = useParams()
  const router = useRouter()
  const { user } = useAuth()
  const [conversation, setConversation] = useState<Conversation | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  const conversationId = params.id as string

  useEffect(() => {
    if (!user) return

    const fetchConversation = async () => {
      setLoading(true)
      try {
        // In a real app, you would fetch the conversation from your API
        // const response = await fetch(`/api/conversations/${user.id}/${conversationId}`);
        // const data = await response.json();

        // For demo purposes, we'll use mock data
        await new Promise((resolve) => setTimeout(resolve, 1000))

        // Mock conversation data
        setConversation({
          id: conversationId,
          summary: "Job search: software developer",
          intent: "DYNAMIC-JOB_LISTINGS",
          messages: [
            {
              role: "user",
              content: "I'm looking for software developer jobs",
              timestamp: "2025-04-26T14:30:00Z",
            },
            {
              role: "assistant",
              content:
                "I found 3 job opportunities that might interest you:\n\n" +
                "1. Senior Software Developer at TechInnovate (Remote)\n" +
                "   We are looking for an experienced software developer with expertise in Python and React.\n" +
                "   Salary range: $80,000 - $120,000\n" +
                "   Experience required: 3-5 years\n" +
                "   Women-friendly benefits: Flexible working hours, Parental leave, Mentorship program\n\n" +
                "2. Data Scientist at DataMinds (Bangalore, India)\n" +
                "   Join our diverse team of data scientists working on cutting-edge AI solutions.\n" +
                "   Salary range: $70,000 - $95,000\n" +
                "   Experience required: 2-4 years\n" +
                "   Women-friendly benefits: Remote work options, Professional development, Inclusive culture\n\n" +
                "Is there a specific job you'd like more information about?",
              timestamp: "2025-04-26T14:30:30Z",
            },
            {
              role: "user",
              content: "Tell me more about the Senior Software Developer role",
              timestamp: "2025-04-26T14:31:15Z",
            },
            {
              role: "assistant",
              content:
                "Here are more details about the Senior Software Developer role at TechInnovate:\n\n" +
                "Position: Senior Software Developer (Full-time, Remote)\n" +
                "Company: TechInnovate - A growing tech company focused on AI-powered solutions for healthcare\n\n" +
                "Key Responsibilities:\n" +
                "- Design and develop scalable software solutions\n" +
                "- Lead technical implementation of new features\n" +
                "- Collaborate with cross-functional teams\n" +
                "- Mentor junior developers\n" +
                "- Participate in code reviews and architectural decisions\n\n" +
                "Requirements:\n" +
                "- 3-5 years of experience in software development\n" +
                "- Strong proficiency in Python and React\n" +
                "- Experience with cloud platforms (AWS/Azure/GCP)\n" +
                "- Knowledge of database systems and API design\n" +
                "- Excellent problem-solving and communication skills\n\n" +
                "Women-friendly benefits:\n" +
                "- Flexible working hours with core collaboration hours\n" +
                "- Generous parental leave (16 weeks paid)\n" +
                "- Dedicated mentorship program for career advancement\n" +
                "- Professional development budget\n" +
                "- Mental health and wellness support\n\n" +
                "The application deadline is May 15, 2025. Would you like me to help you prepare an application for this position?",
              timestamp: "2025-04-26T14:32:00Z",
            },
          ],
        })
      } catch (error) {
        console.error("Error fetching conversation:", error)
        setError("Failed to load conversation")
      } finally {
        setLoading(false)
      }
    }

    fetchConversation()
  }, [user, conversationId])

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <p>Loading conversation...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-full">
        <p className="text-red-500">{error}</p>
        <Button variant="outline" className="mt-4" onClick={() => router.push("/dashboard")}>
          Back to Dashboard
        </Button>
      </div>
    )
  }

  if (!conversation) {
    return (
      <div className="flex flex-col items-center justify-center h-full">
        <p>Conversation not found</p>
        <Button variant="outline" className="mt-4" onClick={() => router.push("/dashboard")}>
          Back to Dashboard
        </Button>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full p-4 md:p-6">
      <div className="mb-4">
        <Button variant="outline" onClick={() => router.push("/dashboard")} className="mb-4">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Dashboard
        </Button>
        <h2 className="text-xl font-bold">{conversation.summary}</h2>
      </div>
      <Card className="flex-1 overflow-y-auto p-4">
        <div className="space-y-4">
          {conversation.messages.map((message, index) => (
            <div key={index} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
              <div
                className={`max-w-[80%] rounded-lg p-4 ${
                  message.role === "user" ? "bg-purple-600 text-white" : "bg-gray-100 text-gray-900"
                }`}
              >
                <div className="whitespace-pre-wrap">{message.content}</div>
                <div className={`text-xs mt-1 ${message.role === "user" ? "text-purple-200" : "text-gray-500"}`}>
                  {formatDate(message.timestamp)}
                </div>
              </div>
            </div>
          ))}
        </div>
      </Card>
      <div className="mt-4">
        <Button onClick={() => router.push("/dashboard")}>Continue Conversation</Button>
      </div>
    </div>
  )
}
