"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { LogOut, Menu } from "lucide-react"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { useMediaQuery } from "@/hooks/use-media-query"
import { useAuth } from "@/lib/auth"
import { getUserConversations } from "@/lib/api"

interface Conversation {
  id: string
  summary: string
  timestamp: string
  intent: string
}

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const { user, logout, loading } = useAuth()
  const isMobile = useMediaQuery("(max-width: 768px)")
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [loadingConversations, setLoadingConversations] = useState(false)

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login")
    }
  }, [user, loading, router])

  useEffect(() => {
    if (user) {
      fetchConversations()
    }
  }, [user])

  const fetchConversations = async () => {
    if (!user) return

    setLoadingConversations(true)
    try {
      const data = await getUserConversations(user.id)
      setConversations(data)
    } catch (error) {
      console.error("Failed to fetch conversations:", error)
      // Use placeholder data if API fails
      setConversations([
        {
          id: "conv1",
          summary: "Job search: software developer",
          timestamp: "2025-04-26T14:30:00Z",
          intent: "DYNAMIC-JOB_LISTINGS",
        },
        {
          id: "conv2",
          summary: "Mentorship programs",
          timestamp: "2025-04-25T10:15:00Z",
          intent: "DYNAMIC-MENTORSHIP",
        },
        {
          id: "conv3",
          summary: "Upcoming tech events",
          timestamp: "2025-04-23T16:45:00Z",
          intent: "DYNAMIC-EVENTS",
        },
      ])
    } finally {
      setLoadingConversations(false)
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    const today = new Date()

    if (date.toDateString() === today.toDateString()) {
      return `Today, ${date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}`
    }

    const yesterday = new Date(today)
    yesterday.setDate(yesterday.getDate() - 1)
    if (date.toDateString() === yesterday.toDateString()) {
      return `Yesterday, ${date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}`
    }

    return `${date.toLocaleDateString([], { month: "short", day: "numeric" })}, ${date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}`
  }

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>
  }

  if (!user) {
    return null
  }

  const Sidebar = () => (
    <div className="flex h-full flex-col bg-white border-r">
      <div className="p-4">
        <h2 className="text-xl font-bold text-purple-600">Asha AI</h2>
        <p className="text-sm text-gray-500 mt-1">Your career assistant</p>
      </div>
      <div className="flex-1 overflow-auto p-4">
        <div className="space-y-1">
          <h3 className="text-sm font-medium text-gray-500 mb-2">Recent Conversations</h3>
          {loadingConversations ? (
            <div className="text-sm text-gray-500">Loading conversations...</div>
          ) : conversations.length > 0 ? (
            conversations.map((conversation) => (
              <div
                key={conversation.id}
                className="rounded-md bg-gray-100 p-3 cursor-pointer hover:bg-gray-200"
                onClick={() => router.push(`/dashboard/conversation/${conversation.id}`)}
              >
                <p className="text-sm font-medium">{conversation.summary}</p>
                <p className="text-xs text-gray-500 truncate">{formatDate(conversation.timestamp)}</p>
              </div>
            ))
          ) : (
            <div className="text-sm text-gray-500">No conversations yet</div>
          )}
        </div>
      </div>
      <div className="p-4 border-t">
        <Button variant="outline" className="w-full justify-start" onClick={logout}>
          <LogOut className="mr-2 h-4 w-4" />
          Log out
        </Button>
      </div>
    </div>
  )

  return (
    <div className="flex h-screen bg-gray-50">
      {isMobile ? (
        <>
          <Sheet open={isSidebarOpen} onOpenChange={setIsSidebarOpen}>
            <SheetTrigger asChild>
              <Button variant="outline" size="icon" className="fixed top-4 left-4 z-40 md:hidden">
                <Menu className="h-4 w-4" />
              </Button>
            </SheetTrigger>
            <SheetContent side="left" className="p-0 w-72">
              <Sidebar />
            </SheetContent>
          </Sheet>
        </>
      ) : (
        <div className="hidden md:block md:w-72 h-full">
          <Sidebar />
        </div>
      )}
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-white border-b h-16 flex items-center px-4 md:px-6">
          <div className="md:hidden mr-2">
            <Button variant="outline" size="icon" onClick={() => setIsSidebarOpen(true)}>
              <Menu className="h-4 w-4" />
            </Button>
          </div>
          <div className="flex-1">
            <h1 className="text-lg font-semibold">Dashboard</h1>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-sm text-right">
              <p className="font-medium">{user.email}</p>
            </div>
          </div>
        </header>
        <main className="flex-1 overflow-auto">{children}</main>
      </div>
    </div>
  )
}
