import { useState } from 'react'
import { ChatContainer } from './components/Chat'
import { RequirementsContainer } from './components/Requirements'

type TabType = 'chat' | 'requirements'

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('chat')
  const [prompt, setPrompt] = useState('')
  const [messages, setMessages] = useState<{ role: 'user' | 'assistant', content: string }[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!prompt.trim() || isLoading) return

    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: prompt }])
    setIsLoading(true)
    setPrompt('')

    try {
      const response = await fetch(import.meta.env.VITE_API_URL + '/assistant', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream',
        },
        body: JSON.stringify({
          prompt,
          stream: true
        })
      })

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()

      if (!reader) throw new Error('No reader available')

      // Add initial assistant message with loading state
      setMessages(prev => [...prev, { role: 'assistant', content: 'Thinking...' }])

      let assistantResponse = ''
      let hasStartedReceiving = false

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')
        
        for (const line of lines) {
          if (line.startsWith('data:')) {
            try {
              const data = JSON.parse(line.slice(5))
              if (data.content) {
                hasStartedReceiving = true
                assistantResponse = data.content
                setMessages(prev => {
                  const newMessages = [...prev]
                  newMessages[newMessages.length - 1].content = assistantResponse
                  return newMessages
                })
              }
            } catch (e) {
              console.error('Error parsing SSE data:', e)
            }
          }
        }
      }

      // If we never received a response, show an error
      if (!hasStartedReceiving) {
        setMessages(prev => {
          const newMessages = [...prev]
          newMessages[newMessages.length - 1].content = 'Sorry, I encountered an error while processing your request.'
          return newMessages
        })
      }
    } catch (error) {
      console.error('Error:', error)
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, there was an error processing your request.' 
      }])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-dark-900 text-gray-100 font-mono">
      <div className="max-w-4xl mx-auto p-4">
        <header className="py-6 mb-8 border-b border-dark-800">
          <h1 className="text-2xl font-bold text-primary-400 mb-4">AWS Well-Architected Assistant</h1>
          <div className="flex space-x-4">
            <button
              onClick={() => setActiveTab('chat')}
              className={`px-4 py-2 rounded-lg transition-all ${
                activeTab === 'chat'
                  ? 'bg-primary-600 text-white'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Chat
            </button>
            <button
              onClick={() => setActiveTab('requirements')}
              className={`px-4 py-2 rounded-lg transition-all ${
                activeTab === 'requirements'
                  ? 'bg-primary-600 text-white'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Requirements
            </button>
          </div>
        </header>

        <main className="h-[calc(100vh-12rem)]">
          {activeTab === 'chat' ? (
            <ChatContainer
              messages={messages}
              prompt={prompt}
              isLoading={isLoading}
              onPromptChange={setPrompt}
              onSubmit={handleSubmit}
            />
          ) : (
            <RequirementsContainer />
          )}
        </main>
      </div>
    </div>
  )
}

export default App
