import { useRef, useEffect } from 'react'
import { ChatMessage } from './ChatMessage'
import { ChatInput } from './ChatInput'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

interface ChatContainerProps {
  messages: Message[]
  prompt: string
  isLoading: boolean
  onPromptChange: (value: string) => void
  onSubmit: (e: React.FormEvent) => void
}

export function ChatContainer({ messages, prompt, isLoading, onPromptChange, onSubmit }: ChatContainerProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  return (
    <div className="h-full flex flex-col">
      <div className="space-y-6 mb-8 flex-1 overflow-y-auto rounded-lg bg-dark-800 p-6">
        {messages.map((message, index) => (
          <ChatMessage key={index} {...message} />
        ))}
        <div ref={messagesEndRef} />
      </div>
      <ChatInput
        prompt={prompt}
        isLoading={isLoading}
        onPromptChange={onPromptChange}
        onSubmit={onSubmit}
      />
    </div>
  )
}
